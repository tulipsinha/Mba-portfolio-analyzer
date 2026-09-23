from scoring import score_profile_against_all_colleges
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

# Serve everything inside the "static" folder at the /static URL path
app.mount("/static", StaticFiles(directory="static"), name="static")


# This defines the exact shape of data we expect the form to send.
# FastAPI uses this to automatically validate incoming data.
class Academics(BaseModel):
    class_10_percent: float
    class_12_percent: float
    graduation_percent: float
    graduation_stream: str

class EntranceExam(BaseModel):
    exam_name: str
    percentile: float

class WorkExperience(BaseModel):
    years: float
    domain: str

class Profile(BaseModel):
    specialization_interest: str
    academics: Academics
    entrance_exam: EntranceExam
    work_experience: WorkExperience


@app.get("/")
def serve_form():
    return FileResponse("static/index.html")


@app.post("/submit-profile")
def submit_profile(profile: Profile):
    # Convert the Pydantic model to a plain dictionary so our
    # scoring functions (which expect plain dicts) can read it.
    profile_dict = profile.model_dump()
    scores = score_profile_against_all_colleges(profile_dict)
    return {"status": "scored", "results": scores}