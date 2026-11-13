
import streamlit as st
import requests
import os
# Page configuration
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔍",
    layout="wide"
)

# Application heading
st.title("🔍 AI Research Agent")
st.write(
    "Research any topic and generate an AI-powered research report."
)

# User input
topic = st.text_input(
    "Enter your research topic",
    placeholder="Example: Generative AI"
)

# Generate research
if st.button("Generate Research"):

    if topic.strip():

        with st.spinner("Researching your topic... Please wait."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/research",
                    json={"topic": topic},
                    timeout=300
                )

                response.raise_for_status()

                result = response.json()

                st.success("Research completed!")

                # Display Research Report
                st.subheader("📄 Research Report")

                report = result["result"]["report"]

                st.markdown(report)

                # Research Quality Evaluation
                evaluation = result["result"]["evaluation"]

                st.subheader("📊 Research Quality Evaluation")

                # Display structure score
                st.metric(
                    "Report Structure Score",
                    f"{evaluation['structure_score']}%"
                )

                # Display evaluation metrics
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Word Count",
                        evaluation["word_count"]
                    )

                with col2:
                    st.metric(
                        "Total Sources",
                        evaluation["total_sources"]
                    )

                with col3:
                    st.metric(
                        "All Sections Present",
                        "Yes" if evaluation["all_sections_present"] else "No"
                    )

                # Missing sections
                if evaluation["missing_sections"]:

                    st.warning(
                        "Missing sections: "
                        + ", ".join(evaluation["missing_sections"])
                    )

                else:
                    st.success(
                        "All required report sections are present!"
                    )

                # Display Research Sources
                st.subheader("🔗 Research Sources")

                for source in result["result"]["sources"]:

                    st.markdown(
                        f"- [{source['title']}]({source['url']})"
                    )

                # Download Research Report
                st.download_button(
                    label="⬇️ Download Research Report",
                    data=report,
                    file_name="research_report.md",
                    mime="text/markdown"
                )

            except requests.RequestException as error:

                st.error(
                    f"API connection error: {error}"
                )

            except (KeyError, TypeError) as error:

                st.error(
                    f"Unexpected API response format: {error}"
                )

    else:
        st.warning("Please enter a research topic.")

# Research History Section

st.divider()

st.subheader("📚 Previous Research History")

if st.button("View Research History"):

    try:
        history_response = requests.get(
            "http://127.0.0.1:8000/history",
            timeout=30
        )

        history_response.raise_for_status()

        history_data = history_response.json()

        st.write(
            f"Total saved reports: {history_data['total_records']}"
        )

        if history_data["history"]:

            for record in history_data["history"]:

                with st.expander(
                    f"{record['topic']} - {record['created_at']}"
                ):

                    st.write(
                        f"Sources: {record['total_sources']}"
                    )

                    st.write(
                        f"Structure Score: {record['structure_score']}%"
                    )

                    st.markdown(record["report"])

        else:
            st.info("No previous research reports found.")

    except requests.RequestException as error:

        st.error(f"Could not load research history: {error}")
