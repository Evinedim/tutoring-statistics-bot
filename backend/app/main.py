from fastapi import FastAPI

from backend.app.routers import students, tutors


app = FastAPI()

app.include_router(students.router)

@app.get("/")
async def health():
    return {"status": "ok"}