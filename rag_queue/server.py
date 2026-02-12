from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queues.worker import process_query

app = FastAPI()

app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/chat")
def chat(
    query: str =Query(..., description="The query to search the RAG database")
):
    job = queue.enqueue(process_query, query) # This will enqueue the query to the Redis queue and return the job id
    return {"status": "Queued", "job_id": job.id}

@app.get("/job-status")
def get_result(job_id: str = Query(..., description="The job id to get the result")):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    return {"result": result}

