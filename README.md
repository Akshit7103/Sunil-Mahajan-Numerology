# Sunil Mahajan Numerology Tool

A beautiful and interactive web application for calculating numerology numbers based on date of birth.

## Features

- **Driver Number**: Sum of digits in birth date
- **Conductor Number**: Sum of all digits in birth date (reduced to single digit)
- **Kua Number**: Gender-specific calculation based on birth year
- **Loshu Grid**: Traditional 3x3 numerology grid display
- Beautiful gradient UI with smooth animations
- Fully responsive design

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## How to Use

1. Enter your full name
2. Select your date of birth
3. Choose your gender (Male/Female)
4. Click "Calculate My Numbers"
5. View your personalized numerology results including:
   - Driver Number
   - Conductor Number
   - Kua Number
   - Loshu Grid

## Calculation Logic

### Driver Number
Sum of digits in the birth date (day only).
Example: Born on 07 → 0+7 = 7

### Conductor Number
Sum of all digits in the complete birth date, reduced to a single digit.
Example: 07/01/2003 → 7+1+2+0+0+3 = 13 → 1+3 = 4

### Kua Number
- **Male**: 11 - (sum of birth year digits)
  - Example: 2003 → 11-(2+0+0+3) = 11-5 = 6
- **Female**: 4 + (sum of birth year digits)
  - Example: 2003 → 4+(2+0+0+3) = 4+5 = 9

### Loshu Grid
Traditional 3x3 magic square:
```
4 9 2
3 5 7
8 1 6
```

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with gradients and animations
- **Server**: Uvicorn ASGI server
