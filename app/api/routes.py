

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database.db import get_all_research

from main import research_topic

app = FastAPI(
    title="AI Research Agent",
    description="An API for researching topics and generating AI reports",
    version="1.0.0"
)

class ResearchRequest(BaseModel):
    topic: str

@app.get("/")
def home():
    return {
        "message": "AI Research Agent API is running!"
    }

@app.post("/research")
def research(request: ResearchRequest):

    try:
        result = research_topic(request.topic)

        return {
            "message": "Research completed successfully!",
            "topic": request.topic,
            "result": result
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@app.get("/history")
def get_research_history():

    records = get_all_research()

    history = []

    for record in records:
        history.append({
            "id": record[0],
            "topic": record[1],
            "report": record[2],
            "total_sources": record[3],
            "structure_score": record[4],
            "created_at": record[5]
        })

    return {
        "total_records": len(history),
        "history": history
    }
