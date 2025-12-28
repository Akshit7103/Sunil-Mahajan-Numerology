"""
Core numerology calculation functions
"""
from typing import Tuple, List, Dict, Any


def sum_digits_to_single(num: int) -> int:
    """Reduce a number to a single digit by repeatedly summing its digits"""
    while num > 9:
        num = sum(int(digit) for digit in str(num))
    return num


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


def calculate_personal_year(day: int, month: int, target_year: int) -> int:
    """Calculate personal year for a specific target year"""
    total = day + month + sum(int(digit) for digit in str(target_year))
    return sum_digits_to_single(total)


def create_personalized_loshu_grid(
    day: int, month: int, year: int, driver: int, conductor: int, kua: int
) -> Tuple[List[List[Dict[str, Any]]], List[int], List[int]]:
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


def calculate_lucky_bad_neutral_numbers(
    driver_compatibility: Dict[str, Any],
    conductor_compatibility: Dict[str, Any]
) -> Tuple[List[int], List[int], List[int]]:
    """Calculate lucky, bad, and neutral numbers based on compatibility"""
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

    return sorted(list(lucky_numbers)), sorted(list(bad_numbers)), sorted(list(neutral_numbers))
