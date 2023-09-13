from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8501",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

eye_blink_count = 0

@app.get("/api/increment-eye-count")
async def increment_eye_count():
    global eye_blink_count
    eye_blink_count += 1
    return {"message": "Eye blink count incremented", "count": eye_blink_count}

@app.get("/api/eye-count")
async def get_eye_count():
    return {"count": eye_blink_count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
