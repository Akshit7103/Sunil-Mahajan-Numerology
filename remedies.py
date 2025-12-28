"""
Remedies calculation logic for numerology
"""
from typing import List, Dict, Any, Set
from data import REMEDIES_PART3


def calculate_remedies_part1(
    missing_numbers: List[int],
    driver: int,
    conductor: int
) -> List[Dict[str, str]]:
    """Calculate remedies based on missing numbers in Loshu Grid"""
    remedies = []
    missing_set = set(missing_numbers)

    # If 4 OR 3 is missing
    if 4 in missing_set or 3 in missing_set:
        remedies.append({
            "condition": "4 or 3 is missing",
            "remedy": "Wear Rudraksha Panchmukhi / Tulsi Mala / Wood Bracelet"
        })

    # If 2 OR 5 OR 8 is missing
    if 2 in missing_set or 5 in missing_set or 8 in missing_set:
        remedies.append({
            "condition": "2 or 5 or 8 is missing",
            "remedy": "Wear Crystal Bracelet or Mala"
        })

    # If both 6 AND 7 are missing
    if 6 in missing_set and 7 in missing_set:
        remedies.append({
            "condition": "6 and 7 both are missing",
            "remedy": "Wear Metal Strap Silver and Golden Colour Watch"
        })
    else:
        # If only 6 is missing
        if 6 in missing_set:
            remedies.append({
                "condition": "6 is missing",
                "remedy": "Wear Metal Strap Golden Colour Watch"
            })
        # If only 7 is missing
        if 7 in missing_set:
            remedies.append({
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
        remedies.append({
            "condition": "1 is missing",
            "remedy": f"Offer water to the Sun{note}"
        })

    # If 9 is missing
    if 9 in missing_set:
        remedies.append({
            "condition": "9 is missing",
            "remedy": "Wear Red Coloured Thread"
        })

    return remedies


def calculate_remedies_part2(
    missing_numbers: List[int],
    present_numbers: List[int],
    driver: int,
    conductor: int
) -> List[Dict[str, str]]:
    """Calculate Yantra-based remedies with specific conditions"""
    remedies = []
    missing_set = set(missing_numbers)
    present_set = set(present_numbers)

    # 1. Surya Budha Yantra
    if 5 in missing_set and 6 in present_set and driver != 8 and conductor != 8:
        remedies.append({
            "remedy": "Wear Surya Budha Yantra",
            "condition": "5 is missing and 6 is present, but driver or conductor should not be 8"
        })

    # 2. Budha Payra
    if 5 in missing_set and 6 in missing_set and driver != 3 and conductor != 3:
        remedies.append({
            "remedy": "Wear Budha Payra",
            "condition": "5 and 6 are missing, but driver or conductor should not be 3"
        })

    # 3. Surya Payra
    if 6 in missing_set and 5 in present_set and driver not in [3, 8] and conductor not in [3, 8]:
        remedies.append({
            "remedy": "Wear Surya Payra",
            "condition": "6 is missing and 5 is present, but driver or conductor should not be 8 or 3 (Pyra will not only take care of missing number 6 but also missing other numbers too)"
        })

    # 4. Pyra Yantra
    if 6 in missing_set and 5 in present_set and (driver == 8 or conductor == 8) and driver != 3 and conductor != 3:
        remedies.append({
            "remedy": "Wear Pyra Yantra",
            "condition": "6 is missing and 5 is present, driver or conductor is 8, but driver or conductor should not be 3"
        })

    # 5. Budha Yantra
    if ((driver == 3 and conductor == 8) or (driver == 8 and conductor == 3)) and 5 in missing_set:
        remedies.append({
            "remedy": "Wear Budha Yantra",
            "condition": "Driver-Conductor is 3-8 or 8-3, and 5 is missing"
        })

    # 6. Surya Yantra
    if ((driver == 3 and conductor == 6) or (driver == 6 and conductor == 3)) and 5 in present_set:
        remedies.append({
            "remedy": "Wear Surya Yantra",
            "condition": "Driver-Conductor is 3-6 or 6-3, and 5 is present"
        })

    # 7. Saraswati Yantra
    if driver != 6 and conductor != 6:
        remedies.append({
            "remedy": "Saraswati Yantra for the education of children",
            "condition": "Driver or conductor should not be 6"
        })

    # 8. Gayatri Yantra (always applicable for health)
    remedies.append({
        "remedy": "Wear Gayatri Yantra for health issues only",
        "condition": "For health issues only"
    })

    return remedies


def calculate_remedies_part3(missing_numbers: List[int]) -> List[Dict[str, Any]]:
    """Calculate planet-based remedies for missing numbers"""
    remedies = []
    for num in sorted(missing_numbers):
        if num in REMEDIES_PART3:
            remedy_data = REMEDIES_PART3[num]
            remedies.append({
                "number": num,
                "planet": remedy_data["planet"],
                "remedies": remedy_data["remedies"]
            })
    return remedies
