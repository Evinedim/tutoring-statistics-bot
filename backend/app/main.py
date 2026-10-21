from fastapi import FastAPI

from backend.app.routers import students, tutors, lessons


app = FastAPI()

app.include_router(students.router)
app.include_router(tutors.router)
app.include_router(lessons.router)

@app.get("/")
async def health():
    return {"status": "ok"}