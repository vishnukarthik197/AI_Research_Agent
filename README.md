# 🔍 AI Research Agent

An AI-powered research application that searches the web, collects relevant information, and generates structured research reports using Generative AI.

## 🚀 Project Overview

AI Research Agent automates the process of researching a topic and generating a structured report.

Users enter a research topic through a Streamlit interface. The application searches the web, extracts relevant webpage content, uses Google's Gemini API to generate a research summary, evaluates the report structure, and stores research history in SQLite.

## ✨ Features

- Web search for user-provided topics
- Webpage content extraction using BeautifulSoup
- AI-powered report generation using Gemini
- Structured report evaluation
- Research history stored in SQLite
- Interactive Streamlit frontend
- REST API built with FastAPI
- API documentation through Swagger UI
- Docker containerization
- Docker Compose for running frontend and backend together

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Generative AI | Google Gemini API |
| Web Search | DDGS |
| Web Scraping | Requests, BeautifulSoup |
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| API Testing | Pytest |
| Containerization | Docker, Docker Compose |

## 🏗️ System Architecture

```text
             User
              |
              v
       Streamlit Frontend
              |
              v
        FastAPI Backend
              |
              v
       Research Engine
              |
       +------+------+
       |             |
       v             v
   Web Search    Web Scraping
       |             |
       +------+------+
              |
              v
        Gemini API
              |
              v
       Report Generation
              |
              v
       Report Evaluator
              |
         +----+----+
         |         |
         v         v
      SQLite    User Interface
```

## 📁 Project Structure

```text
ResearchAI_pilot/
│
├── app/
│   ├── agents/
│   │   └── evaluator.py
│   ├── api/
│   │   └── routes.py
│   └── app.py
│
├── database/
│   └── db.py
│
├── reports/
│
├── tests/
│   └── test_api.py
│
├── config/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ResearchAI_pilot
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never commit your actual API key to GitHub.

### 5. Start the FastAPI backend

```bash
python -m uvicorn app.api.routes:app --reload
```

Backend: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 6. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app/app.py
```

Frontend: http://localhost:8501

## 🐳 Run Using Docker

Make sure Docker Desktop is running.

```bash
docker compose up --build -d
```

Open the application:

- Frontend: http://localhost:8501
- Backend API: http://localhost:8000/docs

Check running containers:

```bash
docker compose ps
```

Stop containers:

```bash
docker compose down
```

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend welcome endpoint |
| POST | `/research` | Generate a research report |
| GET | `/history` | Retrieve previous research reports |

Interactive API documentation is available at `/docs`.

## 🧪 Testing

Run the API tests using:

```bash
pytest -v
```

## 📊 Report Evaluation

The evaluator checks for the presence of seven report sections:

1. Executive Summary
2. Introduction
3. Key Findings
4. Detailed Explanation
5. Source Analysis
6. Limitations
7. Conclusion

The structure score is calculated as:

`(Completed Sections / Total Required Sections) × 100`

This measures report structure, not factual accuracy.

## 🎯 Learning Objectives

This project demonstrates practical experience with:

- Python application development
- Generative AI API integration
- Web search and content extraction
- REST API development
- Database integration
- Frontend and backend communication
- API testing
- Docker-based application deployment

## 👨‍💻 Author

**Daburu Vishnu Karthikeya**

AI Engineer | Generative AI | Python | FastAPI | Agentic AI

---

*This project is developed as a hands-on learning and portfolio project.*