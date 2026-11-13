import json
import requests
import os
from app.agents.evaluator import evaluate_report
from dotenv import load_dotenv
from google import genai
from database.db import create_table, save_research
create_table()

from bs4 import BeautifulSoup
from ddgs import DDGS

load_dotenv()

def fetch_page_content(url):

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for unwanted in soup(["script", "style", "nav", "footer", "header"]):
            unwanted.decompose()

        page_text = soup.get_text(separator=" ", strip=True)

        return page_text[:5000]

    except requests.RequestException as error:
        print(f"Could not read website: {error}")
        return ""
def generate_research_summary(research_data):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Gemini API key not found in .env file")

    client = genai.Client(api_key=api_key)

    source_text = ""

    for source in research_data["sources"]:

        source_text += f"""
        Title: {source['title']}
        URL: {source['url']}
        Description: {source['description']}
        Content: {source['page_content'][:4000]}
        """

    prompt = f"""
You are a professional AI research assistant.

Research topic: {research_data['topic']}

Your task is to prepare a detailed, well-organized research report
using only the information collected from the provided sources.

Follow this report structure:

# Research Report: {research_data['topic']}

## 1. Executive Summary
Give a short overview of the research topic.

## 2. Introduction
Explain the topic and its background.

## 3. Key Findings
Present the most important findings from the sources.

## 4. Detailed Explanation
Explain the important concepts in simple language.

## 5. Source Analysis
Mention the relevant source titles and URLs.
Explain which information each source supports.

## 6. Limitations
Mention missing information, conflicting claims,
or limitations in the collected sources.

## 7. Conclusion
Summarize the important points.

Important instructions:
- Use clear and professional language.
- Do not invent facts or statistics.
- Use only the collected source information.
- Include source URLs wherever relevant.
- Clearly mention when information is uncertain.
- Avoid repeating the same information.

Collected research information:

{source_text}
"""


    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print(f"Gemini API error: {e}")
        return "AI summary could not be generated. Please try again later."
def research_topic(topic):

    if not topic or not topic.strip():
        raise ValueError("Topic cannot be empty.")

    print(f"\nSearching the internet for: {topic}\n")

    results = DDGS().text(topic, max_results=15)

    clean_results = []

    seen_urls = set()

    for result in results:

        title = result.get("title", "").strip()
        url = result.get("href", "").strip()
        description = result.get("body", "").strip()

        if title and url and description:

            url_key = url.rstrip("/")

            if url_key in seen_urls:
                continue

            seen_urls.add(url_key)

            print(f"\nReading website: {title}")

            page_content = fetch_page_content(url)

            clean_result = {
                "title": title,
                "url": url,
                "description": description,
                "page_content": page_content
            }

        clean_results.append(clean_result)

    research_data = {
        "topic": topic,
        "total_sources": len(clean_results),
        "sources": clean_results
    }

    with open("reports/research_results.json", "w", encoding="utf-8") as file:
        json.dump(research_data, file, indent=4, ensure_ascii=False)

    print("\nResearch results saved successfully!")
    print(f"Total sources: {len(clean_results)}")

    print("\nGenerating AI research summary...")

    summary = generate_research_summary(research_data)

    with open("reports/research_summary.md", "w", encoding="utf-8") as file:
        file.write(summary)

    print("\nAI research summary generated successfully!")

    evaluation = evaluate_report(summary, research_data["sources"])
    save_research(
    topic,
    summary,
    len(research_data["sources"]),
    evaluation["structure_score"]
    )

    print("\n--- Research Quality Evaluation ---")
    print(f"Report generated: {evaluation['report_generated']}")
    print(f"Word count: {evaluation['word_count']}")
    print(f"Total sources: {evaluation['total_sources']}")
    print(f"All sections present: {evaluation['all_sections_present']}")
    print(f"Missing sections: {evaluation['missing_sections']}")

    if evaluation["report_generated"] and evaluation["all_sections_present"]:
        print("\n--- Research Report Quality Assessment ---")
        print(f"Report generated: {evaluation['report_generated']}")
        print(f"Word count: {evaluation['word_count']}")
        print(f"Total sources: {evaluation['total_sources']}")
        print(f"All sections present: {evaluation['all_sections_present']}")
        print(f"Missing sections: {evaluation['missing_sections']}")

    print("\n--- Research Report Evaluation Summary ---")
    print(f"Report generated: {evaluation['report_generated']}")
    print(f"Word count: {evaluation['word_count']}")
    print(f"Total sources: {evaluation['total_sources']}")
    print(f"All sections present: {evaluation['all_sections_present']}")
    print(f"Missing sections: {evaluation['missing_sections']}")

    return {
        "topic": topic,
        "total_sources": len(research_data["sources"]),
        "sources": [
        {
            "title": source["title"],
            "url": source["url"]
        }
        for source in research_data["sources"]
    ],
    "report": summary
}

if __name__ == "__main__":
    research_topic(input("Enter a topic to research: "))
