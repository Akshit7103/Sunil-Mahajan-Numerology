from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI()

# Planet compatibility data with exact annotations from source
COMPATIBILITY = {
    1: {  # Sun (Surya)
        "planet": "Sun (Surya)",
        "friends_raw": "9, 2, 5(A), 3, 6, 1(B)",
        "friends": [9, 2, 5, 3, 6, 1],
        "non_friends_raw": "8 - Saturn being illegitimate child of SUN",
        "non_friends": [8],
        "neutral_raw": "4, 7",
        "neutral": [4, 7]
    },
    2: {  # Moon (Chandr)
        "planet": "Moon (Chandr)",
        "friends_raw": "1, 5, 3(A), 2(B)",
        "friends": [1, 5, 3, 2],
        "non_friends_raw": "8, 4, 9",
        "non_friends": [8, 4, 9],
        "neutral_raw": "7, 6",
        "neutral": [7, 6]
    },
    3: {  # Jupiter (Guru)
        "planet": "Jupiter (Guru)",
        "friends_raw": "1, 5, 3, 2, 7* (from knowledge perspective)",
        "friends": [1, 5, 3, 2, 7],
        "non_friends_raw": "6",
        "non_friends": [6],
        "neutral_raw": "4, 8, 9, 7* (from monetary success perspective)",
        "neutral": [4, 8, 9]
    },
    4: {  # Uranus (Rahu)
        "planet": "Uranus (Rahu)",
        "friends_raw": "7, 1, 5, 6, 4*, 8*",
        "friends": [7, 1, 5, 6, 4, 8],
        "non_friends_raw": "4*, 8*, 9, 2",
        "non_friends": [4, 8, 9, 2],
        "neutral_raw": "3",
        "neutral": [3]
    },
    5: {  # Mercury (Budh)
        "planet": "Mercury (Budh)",
        "friends_raw": "1, 2, 6(A), 3, 5(B)",
        "friends": [1, 2, 6, 3, 5],
        "non_friends_raw": "--------",
        "non_friends": [],
        "neutral_raw": "8, 7, 4, 9",
        "neutral": [8, 7, 4, 9]
    },
    6: {  # Venus (Shukar)
        "planet": "Venus (Shukar)",
        "friends_raw": "1, 7, 5, 6",
        "friends": [1, 7, 5, 6],
        "non_friends_raw": "3",
        "non_friends": [3],
        "neutral_raw": "8, 9, 2, 4",
        "neutral": [8, 9, 2, 4]
    },
    7: {  # Neptune (Ketu)
        "planet": "Neptune (Ketu)",
        "friends_raw": "4, 6, 1, 3, 5",
        "friends": [4, 6, 1, 3, 5],
        "non_friends_raw": "--------",
        "non_friends": [],
        "neutral_raw": "8, 9, 2, 7",
        "neutral": [8, 9, 2, 7]
    },
    8: {  # Saturn (Shani)
        "planet": "Saturn (Shani)",
        "friends_raw": "5, 3, 6, 7, 4*, 8*",
        "friends": [5, 3, 6, 7, 4, 8],
        "non_friends_raw": "1, 4*, 8*, 2",
        "non_friends": [1, 4, 8, 2],
        "neutral_raw": "9",
        "neutral": [9]
    },
    9: {  # Mars (Mangal)
        "planet": "Mars (Mangal)",
        "friends_raw": "1, 5, 3",
        "friends": [1, 5, 3],
        "non_friends_raw": "4, 2",
        "non_friends": [4, 2],
        "neutral_raw": "9, 7, 6, 8",
        "neutral": [9, 7, 6, 8]
    }
}

# Luck Factor Database - Personal Year (PY) x Driver (D)
LUCK_FACTOR = {
    1: {1: "100%", 2: "90-100%", 3: "90%", 4: "80-90%", 5: "100%", 6: "90%", 7: "70-80%", 8: "(-)?", 9: "100%"},
    2: {1: "50-60%", 2: "40%", 3: "30-40%", 4: "20%", 5: "50%", 6: "30%", 7: "20-30%", 8: "(-)?", 9: "20%"},
    3: {1: "50-60%", 2: "30-40%", 3: "50-40%", 4: "30%", 5: "30-40%", 6: "(-)", 7: "20-30%", 8: "20-30%", 9: "30-20%"},
    4: {1: "90-100%", 2: "80%/30%", 3: "70%", 4: "100%", 5: "90-100%", 6: "80-90%", 7: "100%", 8: "100%", 9: "50%"},
    5: {1: "100%", 2: "100%", 3: "90-100%", 4: "80%", 5: "100%", 6: "90-100%", 7: "80%", 8: "80-90%", 9: "80-90%"},
    6: {1: "90-100%", 2: "70-80%", 3: "(-)?", 4: "80% (above)", 5: "100%", 6: "100%", 7: "100%", 8: "70-80%", 9: "60-70%"},
    7: {1: "40-50%", 2: "30%", 3: "30-40%", 4: "40-50%", 5: "30-40%", 6: "50%", 7: "20%", 8: "20-30%", 9: "20-30%"},
    8: {1: "(-)?", 2: "(-)?", 3: "70-80%", 4: "100%", 5: "80-90%", 6: "80-90%", 7: "70%", 8: "100%", 9: "80%"},
    9: {1: "50%", 2: "30%", 3: "40-50%", 4: "30%", 5: "50%", 6: "10-20%", 7: "30-40%", 8: "50%", 9: "60-70%"}
}

# Remedies Part 3 - Planet-based remedies
REMEDIES_PART3 = {
    1: {  # Sun
        "planet": "Sun",
        "remedies": ["Offer water to the Sun"]
    },
    2: {  # Moon
        "planet": "Moon",
        "remedies": [
            "Appease Lord Shiva",
            "Offer water",
            "Offer milk",
            "Offer milk + water",
            "Offer Panchamrit"
        ]
    },
    3: {  # Jupiter
        "planet": "Jupiter",
        "remedies": ["Apply saffron tilak on your forehead"]
    },
    4: {  # Rahu
        "planet": "Rahu",
        "remedies": ["Give milk + bread to dog / crow"]
    },
    5: {  # Mercury
        "planet": "Mercury",
        "remedies": [
            "Free the parrot from cage on Wednesday",
            "Use more and more green colour"
        ]
    },
    6: {  # Venus
        "planet": "Venus",
        "remedies": [
            "Give white things on Friday",
            "Donate to a disabled person or beggar"
        ]
    },
    7: {  # Ketu
        "planet": "Ketu",
        "remedies": ["Same remedy as Rahu (Give milk + bread to dog / crow)"]
    },
    8: {  # Saturn
        "planet": "Saturn",
        "remedies": [
            "Offer sarson (mustard) oil",
            "Offer black cloth",
            "Light black oil deepak",
            "Read Shani Chalisa",
            "Give coins to the sweeper",
            "Do shoe service in Gurudwara / temple"
        ]
    },
    9: {  # Mars
        "planet": "Mars",
        "remedies": ["Remedy not mentioned"]
    }
}

class NumerologyInput(BaseModel):
    name: str
    date_of_birth: str
    gender: str

def sum_digits_to_single(num: int) -> int:
    """Reduce a number to a single digit by repeatedly summing its digits"""
    while num > 9:
        num = sum(int(digit) for digit in str(num))
    return num

def calculate_personal_year(day: int, month: int, target_year: int) -> int:
    """Calculate personal year for a specific target year"""
    total = day + month + sum(int(digit) for digit in str(target_year))
    return sum_digits_to_single(total)

def calculate_driver(day: int) -> int:
    """Calculate driver number from birth date"""
    return sum_digits_to_single(day)

def calculate_conductor(day: int, month: int, year: int) -> int:
    """Calculate conductor number from full date of birth"""
    total = sum(int(digit) for digit in str(day) + str(month) + str(year))
    return sum_digits_to_single(total)

def calculate_kua(year: int, gender: str) -> int:
    """Calculate kua number based on birth year and gender"""
    year_sum = sum(int(digit) for digit in str(year))
    year_digit = sum_digits_to_single(year_sum)

    if gender.lower() == "male":
        kua = 11 - year_digit
        # Handle special cases for Kua
        if kua > 9:
            kua = sum_digits_to_single(kua)
        return kua
    else:  # female
        kua = 4 + year_digit
        if kua > 9:
            kua = sum_digits_to_single(kua)
        return kua

def create_personalized_loshu_grid(day: int, month: int, year: int, driver: int, conductor: int, kua: int):
    """Create personalized Loshu grid based on date of birth and calculated numbers"""
    # Standard Loshu Grid template
    standard_grid = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]

    # Count occurrences of each digit (1-9)
    digit_count = {i: 0 for i in range(1, 10)}

    # Track if day is single digit (01-09) to limit its count to 1
    single_digit_day = None
    if day < 10:
        single_digit_day = day

    # For day: if 10-31, count each digit separately; if 01-09, count as single digit
    if day >= 10:
        for digit in str(day):
            if digit != '0':
                digit_count[int(digit)] += 1
    else:
        digit_count[day] += 1

    # Add digits from month
    for digit in str(month):
        if digit != '0':
            digit_count[int(digit)] += 1

    # Add digits from year
    for digit in str(year):
        if digit != '0':
            digit_count[int(digit)] += 1

    # Add driver, conductor, and kua numbers
    digit_count[driver] += 1
    digit_count[conductor] += 1
    digit_count[kua] += 1

    # If day is 01-09, cap that digit's count to 1
    if single_digit_day is not None:
        digit_count[single_digit_day] = 1

    # Create personalized grid
    personalized_grid = []
    missing_numbers = []
    present_numbers = []

    for row in standard_grid:
        new_row = []
        for cell in row:
            count = digit_count[cell]
            if count > 0:
                # Number appears - show it with repetition
                repeated_value = str(cell) * count
                new_row.append({
                    "value": repeated_value,
                    "present": True,
                    "count": count
                })
                if cell not in present_numbers:
                    present_numbers.append(cell)
            else:
                # Number is missing
                new_row.append({
                    "value": cell,
                    "present": False,
                    "count": 0
                })
                missing_numbers.append(cell)
        personalized_grid.append(new_row)

    return personalized_grid, sorted(missing_numbers), sorted(present_numbers)

@app.post("/calculate")
async def calculate_numerology(data: NumerologyInput):
    """Calculate all numerology values"""
    try:
        # Parse the date
        date_obj = datetime.strptime(data.date_of_birth, "%Y-%m-%d")
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year

        # Calculate values
        driver = calculate_driver(day)
        conductor = calculate_conductor(day, month, year)
        kua = calculate_kua(year, data.gender)

        # Create personalized Loshu Grid
        loshu_grid, missing_numbers, present_numbers = create_personalized_loshu_grid(
            day, month, year, driver, conductor, kua
        )

        # Get compatibility data
        driver_compatibility = COMPATIBILITY.get(driver, {})
        conductor_compatibility = COMPATIBILITY.get(conductor, {})

        # Calculate Lucky, Bad, and Neutral numbers
        driver_friends = set(driver_compatibility.get('friends', []))
        driver_non_friends = set(driver_compatibility.get('non_friends', []))
        driver_neutral = set(driver_compatibility.get('neutral', []))

        conductor_friends = set(conductor_compatibility.get('friends', []))
        conductor_non_friends = set(conductor_compatibility.get('non_friends', []))
        conductor_neutral = set(conductor_compatibility.get('neutral', []))

        # Bad numbers: union of all non-friends (priority)
        bad_numbers = driver_non_friends | conductor_non_friends

        # Lucky numbers: union of all friends, minus bad numbers
        lucky_numbers = (driver_friends | conductor_friends) - bad_numbers

        # Neutral numbers: everything else (1-9) not in lucky or bad
        all_numbers = set(range(1, 10))
        neutral_numbers = all_numbers - lucky_numbers - bad_numbers

        # Calculate Remedies Part 1 based on missing numbers
        remedies_part1 = []
        missing_set = set(missing_numbers)

        # If 4 OR 3 is missing
        if 4 in missing_set or 3 in missing_set:
            remedies_part1.append({
                "condition": "4 or 3 is missing",
                "remedy": "Wear Rudraksha Panchmukhi / Tulsi Mala / Wood Bracelet"
            })

        # If 2 OR 5 OR 8 is missing
        if 2 in missing_set or 5 in missing_set or 8 in missing_set:
            remedies_part1.append({
                "condition": "2 or 5 or 8 is missing",
                "remedy": "Wear Crystal Bracelet or Mala"
            })

        # If both 6 AND 7 are missing
        if 6 in missing_set and 7 in missing_set:
            remedies_part1.append({
                "condition": "6 and 7 both are missing",
                "remedy": "Wear Metal Strap Silver and Golden Colour Watch"
            })
        else:
            # If only 6 is missing
            if 6 in missing_set:
                remedies_part1.append({
                    "condition": "6 is missing",
                    "remedy": "Wear Metal Strap Golden Colour Watch"
                })
            # If only 7 is missing
            if 7 in missing_set:
                remedies_part1.append({
                    "condition": "7 is missing",
                    "remedy": "Wear Metal Strap Silver and Golden Colour Watch"
                })

        # If 1 is missing
        if 1 in missing_set:
            note = ""
            if driver == 8 or conductor == 8:
                note = " (Note: Driver or Conductor is 8, so drink less water)"
            else:
                note = " (Drink as much water as possible)"
            remedies_part1.append({
                "condition": "1 is missing",
                "remedy": f"Offer water to the Sun{note}"
            })

        # If 9 is missing
        if 9 in missing_set:
            remedies_part1.append({
                "condition": "9 is missing",
                "remedy": "Wear Red Coloured Thread"
            })

        # Calculate Remedies Part 2 - Yantra-based remedies with specific conditions
        remedies_part2 = []
        present_set = set(present_numbers)

        # 1. Surya Budha Yantra
        if 5 in missing_set and 6 in present_set and driver != 8 and conductor != 8:
            remedies_part2.append({
                "remedy": "Wear Surya Budha Yantra",
                "condition": "5 is missing and 6 is present, but driver or conductor should not be 8"
            })

        # 2. Budha Payra
        if 5 in missing_set and 6 in missing_set and driver != 3 and conductor != 3:
            remedies_part2.append({
                "remedy": "Wear Budha Payra",
                "condition": "5 and 6 are missing, but driver or conductor should not be 3"
            })

        # 3. Surya Payra
        if 6 in missing_set and 5 in present_set and driver not in [3, 8] and conductor not in [3, 8]:
            remedies_part2.append({
                "remedy": "Wear Surya Payra",
                "condition": "6 is missing and 5 is present, but driver or conductor should not be 8 or 3 (Pyra will not only take care of missing number 6 but also missing other numbers too)"
            })

        # 4. Pyra Yantra
        if 6 in missing_set and 5 in present_set and (driver == 8 or conductor == 8) and driver != 3 and conductor != 3:
            remedies_part2.append({
                "remedy": "Wear Pyra Yantra",
                "condition": "6 is missing and 5 is present, driver or conductor is 8, but driver or conductor should not be 3"
            })

        # 5. Budha Yantra
        if ((driver == 3 and conductor == 8) or (driver == 8 and conductor == 3)) and 5 in missing_set:
            remedies_part2.append({
                "remedy": "Wear Budha Yantra",
                "condition": "Driver-Conductor is 3-8 or 8-3, and 5 is missing"
            })

        # 6. Surya Yantra
        if ((driver == 3 and conductor == 6) or (driver == 6 and conductor == 3)) and 5 in present_set:
            remedies_part2.append({
                "remedy": "Wear Surya Yantra",
                "condition": "Driver-Conductor is 3-6 or 6-3, and 5 is present"
            })

        # 7. Saraswati Yantra
        if driver != 6 and conductor != 6:
            remedies_part2.append({
                "remedy": "Saraswati Yantra for the education of children",
                "condition": "Driver or conductor should not be 6"
            })

        # 8. Gayatri Yantra (always applicable for health)
        remedies_part2.append({
            "remedy": "Wear Gayatri Yantra for health issues only",
            "condition": "For health issues only"
        })

        # Calculate Remedies Part 3 - Planet-based remedies for missing numbers
        remedies_part3 = []
        for num in sorted(missing_numbers):
            if num in REMEDIES_PART3:
                remedy_data = REMEDIES_PART3[num]
                remedies_part3.append({
                    "number": num,
                    "planet": remedy_data["planet"],
                    "remedies": remedy_data["remedies"]
                })

        # Calculate Luck Factor for next 5 years
        from datetime import datetime as dt
        current_year = dt.now().year
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
            "driver_compatibility": driver_compatibility,
            "conductor_compatibility": conductor_compatibility,
            "lucky_numbers": sorted(list(lucky_numbers)),
            "bad_numbers": sorted(list(bad_numbers)),
            "neutral_numbers": sorted(list(neutral_numbers)),
            "remedies_part1": remedies_part1,
            "remedies_part2": remedies_part2,
            "remedies_part3": remedies_part3,
            "luck_factors": luck_factors
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
