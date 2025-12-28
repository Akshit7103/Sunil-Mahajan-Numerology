# Sunil Mahajan Numerology Tool

A beautiful, interactive, and modular web application for calculating numerology numbers based on date of birth. Now featuring PDF export and improved code organization!

## Features

### Core Calculations
- **Driver Number**: Sum of digits in birth date
- **Conductor Number**: Sum of all digits in birth date (reduced to single digit)
- **Kua Number**: Gender-specific calculation based on birth year
- **Loshu Grid**: Traditional 3x3 numerology grid display with visual count indicators

### Advanced Features
- **Number Compatibility**: Detailed planetary compatibility for Driver and Conductor numbers
- **Lucky/Bad/Neutral Numbers**: Comprehensive number analysis
- **Three-Part Remedies System**:
  - Part 1: Based on missing numbers in Loshu Grid
  - Part 2: Yantra-based remedies with specific conditions
  - Part 3: Planet-based remedies (tabular format)
- **Luck Factor Analysis**: Next 6 years prediction based on Personal Year calculation
- **PDF Export**: Download complete numerology report as PDF

### UI/UX Features
- Beautiful gradient UI with smooth animations
- Fully responsive design
- Fixed gender button selection (now works on initial selection)
- Clean, organized results layout

## Project Structure

```
Sunil-Mahajan-Numerology/
├── main.py                 # FastAPI application (routes only)
├── calculations.py         # Core numerology calculations
├── data.py                 # Compatibility and remedies data
├── remedies.py             # Remedies calculation logic
├── index.html              # Main HTML (clean, no inline CSS/JS)
├── static/
│   ├── styles.css         # All application styles
│   └── script.js          # All application logic + PDF export
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
├── render.yaml            # Render deployment settings
└── .gitignore             # Git ignore rules
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Sunil-Mahajan-Numerology
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development

1. Start the FastAPI server:
```bash
python main.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

### Production Deployment

The application is configured for deployment on Render:
- Automatic deployment via `render.yaml`
- Uses Procfile for process management

## How to Use

1. Enter your full name
2. Select your date of birth
3. Choose your gender (Male/Female) - buttons now highlight on selection!
4. Click "Calculate My Numbers"
5. View your personalized numerology results
6. Click "Export PDF" to download your complete report

## Calculation Logic

### Driver Number
Sum of digits in the birth date (day only).
- Example: Born on 07 → 0+7 = 7

### Conductor Number
Sum of all digits in the complete birth date, reduced to a single digit.
- Example: 07/01/2003 → 7+1+2+0+0+3 = 13 → 1+3 = 4

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
Each cell shows:
- The base number
- Count badge (×N) if number appears multiple times
- Visual highlighting for present/missing numbers

### Luck Factor
Calculated using Personal Year (PY) and Driver Number (D) combination for the next 6 years.

## Technology Stack

### Backend
- **FastAPI** (Python) - Modern, fast web framework
- **Pydantic V2** - Data validation with field validators
- **Uvicorn** - ASGI server

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **Vanilla JavaScript** - No framework dependencies
- **jsPDF** - Client-side PDF generation
- **jsPDF-AutoTable** - Table generation in PDFs

## Code Improvements

### Refactored & Modularized
- **Separated concerns**: Business logic, data, and presentation layers
- **Clean main.py**: Only routes and API endpoints
- **Dedicated modules**: calculations.py, data.py, remedies.py
- **External assets**: CSS and JS in separate files

### Better Code Quality
- Type hints throughout
- Pydantic V2 validators
- Comprehensive error handling
- Input validation (name, gender, date validation)
- Clean, readable code structure

### Enhanced Features
- Working PDF export functionality
- Fixed gender button selection issue
- Better user feedback
- Removed unused buttons (Copy JSON, New Reading)

## API Endpoints

### GET /
Returns the main HTML interface

### POST /calculate
Calculate numerology values

**Request Body**:
```json
{
  "name": "John Doe",
  "date_of_birth": "2003-01-07",
  "gender": "male"
}
```

**Response**:
```json
{
  "success": true,
  "name": "John Doe",
  "driver": 7,
  "conductor": 4,
  "kua": 6,
  "loshu_grid": [...],
  "missing_numbers": [...],
  "present_numbers": [...],
  "driver_compatibility": {...},
  "conductor_compatibility": {...},
  "lucky_numbers": [...],
  "bad_numbers": [...],
  "neutral_numbers": [...],
  "remedies_part1": [...],
  "remedies_part2": [...],
  "remedies_part3": [...],
  "luck_factors": [...]
}
```

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (responsive design)

## Future Enhancements

Potential improvements:
- User authentication and history
- Database integration for storing calculations
- More detailed interpretations
- Name numerology calculations
- Compatibility checker between two people
- Multi-language support
- Dark mode toggle

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Based on traditional numerology principles
- Sunil Mahajan's numerology methodology
- Modern web technologies for beautiful UI/UX
