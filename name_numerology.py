"""
Name numerology calculations and validation rules
"""
from typing import List, Dict, Any, Tuple, Set
from data import ALPHABET_VALUES, COMPATIBILITY
from calculations import sum_digits_to_single


def calculate_name_value(name: str) -> int:
    """Calculate the numerology value of a name"""
    total = 0
    for char in name.upper():
        if char in ALPHABET_VALUES:
            total += ALPHABET_VALUES[char]
    return sum_digits_to_single(total)


def get_name_breakdown(name: str) -> Dict[str, Any]:
    """Get detailed breakdown of name calculation"""
    breakdown = []
    total = 0

    for char in name.upper():
        if char in ALPHABET_VALUES:
            value = ALPHABET_VALUES[char]
            breakdown.append({"letter": char, "value": value})
            total += value
        elif char == ' ':
            breakdown.append({"letter": ' ', "value": '-'})

    return {
        "breakdown": breakdown,
        "raw_total": total,
        "final_value": sum_digits_to_single(total)
    }


def validate_name_numerology(
    full_name: str,
    driver: int,
    conductor: int,
    bad_numbers: List[int],
    present_numbers: List[int],
    missing_numbers: List[int]
) -> Dict[str, Any]:
    """
    Validate name against numerology rules and return followed/contradicted rules
    """
    # Split name into first name and full name
    name_parts = full_name.strip().split()
    first_name = name_parts[0] if name_parts else ""

    # Calculate values
    first_name_value = calculate_name_value(first_name)
    full_name_value = calculate_name_value(full_name)

    # Get detailed breakdowns
    first_name_breakdown = get_name_breakdown(first_name)
    full_name_breakdown = get_name_breakdown(full_name)

    followed_rules = []
    contradicted_rules = []

    missing_set = set(missing_numbers)
    present_set = set(present_numbers)

    # Rule 3: Full name total should NEVER be 4 or 8
    if full_name_value not in [4, 8]:
        followed_rules.append({
            "rule": "Rule 3",
            "description": f"Full name total ({full_name_value}) is not 4 or 8 ✓",
            "status": "good"
        })
    else:
        contradicted_rules.append({
            "rule": "Rule 3",
            "description": f"Full name total is {full_name_value} (should NOT be 4 or 8)",
            "status": "bad",
            "severity": "high"
        })

    # Rule 4: First name total should NEVER be 4 or 8
    if first_name_value not in [4, 8]:
        followed_rules.append({
            "rule": "Rule 4",
            "description": f"First name total ({first_name_value}) is not 4 or 8 ✓",
            "status": "good"
        })
    else:
        contradicted_rules.append({
            "rule": "Rule 4",
            "description": f"First name total is {first_name_value} (should NOT be 4 or 8)",
            "status": "bad",
            "severity": "high"
        })

    # Rule 5: First name should NOT be anti (bad number) to driver number
    driver_non_friends = COMPATIBILITY.get(driver, {}).get('non_friends', [])
    if first_name_value not in driver_non_friends:
        followed_rules.append({
            "rule": "Rule 5",
            "description": f"First name total ({first_name_value}) is not anti to driver {driver} ✓",
            "status": "good"
        })
    else:
        contradicted_rules.append({
            "rule": "Rule 5",
            "description": f"First name total ({first_name_value}) is anti to driver {driver}",
            "status": "bad",
            "severity": "high"
        })

    # Rule 6: Name spelling should match/be comfortable with driver/conductor
    # This is a general compatibility check
    if full_name_value == driver or full_name_value == conductor:
        followed_rules.append({
            "rule": "Rule 6",
            "description": f"Full name total ({full_name_value}) matches driver or conductor ✓",
            "status": "good"
        })
    elif full_name_value not in bad_numbers:
        followed_rules.append({
            "rule": "Rule 6",
            "description": f"Full name total ({full_name_value}) is compatible with your numbers ✓",
            "status": "good"
        })
    else:
        contradicted_rules.append({
            "rule": "Rule 6",
            "description": f"Full name total ({full_name_value}) is not comfortable with driver/conductor",
            "status": "warning",
            "severity": "medium"
        })

    # Rule 7: Name should total to 1 IF both 5 and 6 are present in Loshu Grid AND driver/conductor is NOT 8
    if 5 in present_set and 6 in present_set and driver != 8 and conductor != 8:
        if full_name_value == 1:
            followed_rules.append({
                "rule": "Rule 7",
                "description": f"Name totals to 1 (both 5 & 6 present, D/C not 8) ✓",
                "status": "excellent"
            })
        else:
            contradicted_rules.append({
                "rule": "Rule 7",
                "description": f"Name should total to 1 (both 5 & 6 present, D/C not 8), but it's {full_name_value}",
                "status": "suggestion",
                "severity": "low"
            })

    # Rule 8: Name should total to 5 IF 5 is missing AND it completes 2-5-8 or 4-5-6 line
    if 5 in missing_set:
        # Check if adding 5 would complete lines
        line_258_incomplete = (2 in present_set and 8 in present_set)
        line_456_incomplete = (4 in present_set and 6 in present_set)

        if line_258_incomplete or line_456_incomplete:
            if full_name_value == 5:
                followed_rules.append({
                    "rule": "Rule 8",
                    "description": f"Name totals to 5 (completes line: {'2-5-8' if line_258_incomplete else '4-5-6'}) ✓",
                    "status": "excellent"
                })
            else:
                contradicted_rules.append({
                    "rule": "Rule 8",
                    "description": f"Name should total to 5 to complete line ({'2-5-8' if line_258_incomplete else '4-5-6'}), but it's {full_name_value}",
                    "status": "suggestion",
                    "severity": "medium"
                })

    # Rule 9: Name should total to 6 IF 6 is missing AND driver/conductor is NOT 3
    if 6 in missing_set and driver != 3 and conductor != 3:
        if full_name_value == 6:
            followed_rules.append({
                "rule": "Rule 9",
                "description": f"Name totals to 6 (6 missing, D/C not 3) ✓",
                "status": "excellent"
            })
        else:
            contradicted_rules.append({
                "rule": "Rule 9",
                "description": f"Name should total to 6 (6 is missing, D/C not 3), but it's {full_name_value}",
                "status": "suggestion",
                "severity": "medium"
            })

    # Rule 10: Name should total to 3 IF 3 is missing AND driver/conductor is NOT 6
    if 3 in missing_set and driver != 6 and conductor != 6:
        if full_name_value == 3:
            followed_rules.append({
                "rule": "Rule 10",
                "description": f"Name totals to 3 (3 missing, D/C not 6) ✓",
                "status": "excellent"
            })
        else:
            contradicted_rules.append({
                "rule": "Rule 10",
                "description": f"Name should total to 3 (3 is missing, D/C not 6), but it's {full_name_value}",
                "status": "suggestion",
                "severity": "medium"
            })

    return {
        "first_name": first_name,
        "first_name_value": first_name_value,
        "first_name_breakdown": first_name_breakdown,
        "full_name": full_name,
        "full_name_value": full_name_value,
        "full_name_breakdown": full_name_breakdown,
        "followed_rules": followed_rules,
        "contradicted_rules": contradicted_rules,
        "overall_status": "good" if len(contradicted_rules) == 0 else "needs_improvement"
    }


def suggest_name_corrections(
    current_name: str,
    target_value: int,
    driver: int,
    conductor: int,
    bad_numbers: List[int]
) -> List[Dict[str, Any]]:
    """
    Suggest possible name corrections to achieve target value
    This is a helper function for future enhancements
    """
    suggestions = []

    # This can be expanded to provide intelligent name suggestions
    # For now, we'll provide general guidance

    if target_value == 1:
        suggestions.append({
            "target": 1,
            "reason": "Recommended when both 5 and 6 are present",
            "guidance": "Add or modify letters to reach total of 1"
        })

    return suggestions
