"""
FastAPI application for Numerology Calculator
Refactored and modularized for better code organization
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator
from datetime import datetime
import os

# Import modularized components
from calculations import (
    calculate_driver,
    calculate_conductor,
    calculate_kua,
    calculate_personal_year,
    create_personalized_loshu_grid,
    calculate_lucky_bad_neutral_numbers
)
from data import COMPATIBILITY, LUCK_FACTOR
from remedies import (
    calculate_remedies_part1,
    calculate_remedies_part2,
    calculate_remedies_part3
)
from name_numerology import validate_name_numerology
from loshu_lines import analyze_loshu_lines

app = FastAPI(title="Numerology Calculator API")

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


class NumerologyInput(BaseModel):
    """Input model for numerology calculation"""
    name: str
    date_of_birth: str
    gender: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v.strip()

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v.lower() not in ['male', 'female']:
            raise ValueError('Gender must be either male or female')
        return v.lower()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)


@app.post("/calculate")
async def calculate_numerology(data: NumerologyInput):
    """
    Calculate all numerology values including:
    - Driver, Conductor, Kua numbers
    - Personalized Loshu Grid
    - Compatibility data
    - Lucky/Bad/Neutral numbers
    - Remedies (3 parts)
    - Luck factors for next 6 years
    """
    try:
        # Parse the date
        date_obj = datetime.strptime(data.date_of_birth, "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year

        # Validate date is not in the future
        if date_obj > datetime.now():
            return {
                "success": False,
                "error": "Date of birth cannot be in the future"
            }

        # Calculate core numerology values
        driver = calculate_driver(day)
        conductor = calculate_conductor(day, month, year)
        kua = calculate_kua(year, data.gender)

        # Create personalized Loshu Grid
        loshu_grid, missing_numbers, present_numbers = create_personalized_loshu_grid(
            day, month, year, driver, conductor, kua
        )

        # Analyze Loshu Grid lines (horizontal, vertical, diagonal)
        loshu_lines = analyze_loshu_lines(present_numbers)

        # Get compatibility data
        driver_compatibility = COMPATIBILITY.get(driver, {})
        conductor_compatibility = COMPATIBILITY.get(conductor, {})

        # Calculate Lucky, Bad, and Neutral numbers
        lucky_numbers, bad_numbers, neutral_numbers = calculate_lucky_bad_neutral_numbers(
            driver_compatibility, conductor_compatibility
        )

        # Calculate all three parts of remedies
        remedies_part1 = calculate_remedies_part1(missing_numbers, driver, conductor)
        remedies_part2 = calculate_remedies_part2(missing_numbers, present_numbers, driver, conductor)
        remedies_part3 = calculate_remedies_part3(missing_numbers)

        # Calculate Luck Factor for next 6 years
        current_year = datetime.now().year
        luck_factors = []

        for i in range(6):  # Current year + next 5 years
            target_year = current_year + i
            personal_year = calculate_personal_year(day, month, target_year)
            luck_percentage = LUCK_FACTOR.get(personal_year, {}).get(driver, "N/A")

            luck_factors.append({
                "year": target_year,
                "date": f"{day:02d}/{month:02d}/{target_year}",
                "personal_year": personal_year,
                "driver": driver,
                "combination": f"{personal_year},{driver}",
                "luck_factor": luck_percentage
            })

        # Calculate Name Numerology Analysis
        name_analysis = validate_name_numerology(
            full_name=data.name,
            driver=driver,
            conductor=conductor,
            bad_numbers=bad_numbers,
            present_numbers=present_numbers,
            missing_numbers=missing_numbers
        )

        # Return comprehensive numerology data
        return {
            "success": True,
            "name": data.name,
            "date_of_birth": data.date_of_birth,
            "gender": data.gender,
            "driver": driver,
            "conductor": conductor,
            "kua": kua,
            "loshu_grid": loshu_grid,
            "missing_numbers": missing_numbers,
            "present_numbers": present_numbers,
            "loshu_lines": loshu_lines,
            "driver_compatibility": driver_compatibility,
            "conductor_compatibility": conductor_compatibility,
            "lucky_numbers": lucky_numbers,
            "bad_numbers": bad_numbers,
            "neutral_numbers": neutral_numbers,
            "remedies_part1": remedies_part1,
            "remedies_part2": remedies_part2,
            "remedies_part3": remedies_part3,
            "luck_factors": luck_factors,
            "name_analysis": name_analysis
        }
    except ValueError as ve:
        return {
            "success": False,
            "error": str(ve)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
