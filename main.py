from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import calendar
import holidays
import uuid
import hashlib

from starlette.responses import RedirectResponse

app = FastAPI(
    title="FastAPI Starter",
    description="A simple FastAPI application with automatic Swagger documentation",
    version="1.0.0"
)

class InputRequest(BaseModel):
    string: str

class DateRequest(BaseModel):
    date: str

@app.get("/")
async def root():
    """
    This endpoint will redirect to the Swagger documentation.
    """
    return RedirectResponse(url="/docs", status_code=301)

@app.post("/reverse")
async def reverse_request(request: InputRequest):
    """
    This endpoint will reverse the request string.
    """
    return {"reversed_string": reverse_string(request.string)}

def reverse_string(string: str) -> str:
    return string[::-1]

@app.post("/day_of_week")
async def day_of_week_request(request: DateRequest):
    """
    This endpoint will provide the day of the week given a date.
    """
    return {"day_of_week": get_day_of_week_by_date(request.date)}

def get_date_object(date: str) -> datetime:
    year, month, day = map(int, date.split("-"))
    return datetime(year, month, day)

def get_day_of_week_by_date(date: str) -> str:
    date_obj = get_date_object(date)
    return calendar.day_name[date_obj.weekday()]

@app.post("/holiday")
async def holiday_request(request: DateRequest):
    """
    This endpoint given a date will provide whether it is a US holiday and it.
    """
    return {"holiday": get_holiday_by_date(request.date)}

def get_holiday_by_date(date: str) -> str:
    us_holidays = holidays.country_holidays('US')
    date_obj = get_date_object(date)
    if date_obj in us_holidays:
        return us_holidays.get(date_obj)
    else:
        return "No holiday"

@app.get("/uuid")
async def uuid_request():
    """
    This endpoint will provide a universally unique identifier.
    """
    return {"uuid": str(uuid.uuid4())}

@app.post("/hash")
async def hash_request(request: InputRequest):
    """
    This endpoint will provide the hash of a given string.
    """
    return {"hash": generate_sha256_from_string(request.string)}

def generate_sha256_from_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
