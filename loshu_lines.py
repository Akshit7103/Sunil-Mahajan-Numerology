"""
Loshu Grid line analysis - detect complete lines and planes
"""
from typing import List, Dict, Any


# Loshu Grid Lines with their meanings
LOSHU_LINES = {
    # Diagonal Lines
    "456": {
        "numbers": [4, 5, 6],
        "name": "Super Success Line (Raj Yoga)",
        "type": "diagonal",
        "description": "Indicates exceptional success and royal fortune"
    },
    "258": {
        "numbers": [2, 5, 8],
        "name": "Success Line (Golden Line)",
        "type": "diagonal",
        "description": "Brings success and prosperity"
    },

    # Vertical Planes
    "438": {
        "numbers": [4, 3, 8],
        "name": "Thought Plane",
        "type": "vertical",
        "description": "Mental clarity and intellectual abilities"
    },
    "951": {
        "numbers": [9, 5, 1],
        "name": "Will Plane (Symbol of Success)",
        "type": "vertical",
        "description": "Strong willpower and determination"
    },
    "276": {
        "numbers": [2, 7, 6],
        "name": "Action Plane",
        "type": "vertical",
        "description": "Ability to take action and execute plans"
    },

    # Horizontal Planes
    "492": {
        "numbers": [4, 9, 2],
        "name": "Mental Plane",
        "type": "horizontal",
        "description": "Intellectual and analytical thinking"
    },
    "357": {
        "numbers": [3, 5, 7],
        "name": "Emotional Plane",
        "type": "horizontal",
        "description": "Emotional balance and intuition"
    },
    "816": {
        "numbers": [8, 1, 6],
        "name": "Practical Plane",
        "type": "horizontal",
        "description": "Practical skills and material success"
    }
}


def analyze_loshu_lines(present_numbers: List[int]) -> Dict[str, Any]:
    """
    Analyze which lines/planes are complete in the Loshu Grid

    Args:
        present_numbers: List of numbers present in the grid

    Returns:
        Dictionary containing complete lines categorized by type
    """
    present_set = set(present_numbers)
    complete_lines = {
        "diagonal": [],
        "vertical": [],
        "horizontal": [],
        "all": []
    }

    for line_key, line_info in LOSHU_LINES.items():
        required_numbers = set(line_info["numbers"])

        # Check if all numbers in the line are present
        if required_numbers.issubset(present_set):
            line_data = {
                "numbers": line_info["numbers"],
                "name": line_info["name"],
                "description": line_info["description"],
                "type": line_info["type"]
            }

            # Add to type-specific category
            complete_lines[line_info["type"]].append(line_data)

            # Add to all lines
            complete_lines["all"].append(line_data)

    return complete_lines


def get_line_summary(present_numbers: List[int]) -> str:
    """
    Get a text summary of complete lines

    Args:
        present_numbers: List of numbers present in the grid

    Returns:
        Summary string describing complete lines
    """
    lines = analyze_loshu_lines(present_numbers)

    if not lines["all"]:
        return "No complete lines found in your Loshu Grid"

    summary_parts = []

    # Special lines (diagonal)
    if lines["diagonal"]:
        diagonal_names = [line["name"] for line in lines["diagonal"]]
        summary_parts.append(f"✨ Special Lines: {', '.join(diagonal_names)}")

    # Vertical planes
    if lines["vertical"]:
        vertical_names = [line["name"] for line in lines["vertical"]]
        summary_parts.append(f"📊 Vertical Planes: {', '.join(vertical_names)}")

    # Horizontal planes
    if lines["horizontal"]:
        horizontal_names = [line["name"] for line in lines["horizontal"]]
        summary_parts.append(f"📈 Horizontal Planes: {', '.join(horizontal_names)}")

    return "\n".join(summary_parts)


def get_missing_lines(present_numbers: List[int]) -> List[Dict[str, Any]]:
    """
    Get lines that are incomplete (missing numbers)

    Args:
        present_numbers: List of numbers present in the grid

    Returns:
        List of incomplete lines with missing numbers
    """
    present_set = set(present_numbers)
    missing_lines = []

    for line_key, line_info in LOSHU_LINES.items():
        required_numbers = set(line_info["numbers"])

        # Check if line is incomplete
        if not required_numbers.issubset(present_set):
            missing_nums = required_numbers - present_set

            if len(missing_nums) > 0:  # Only if some numbers are missing
                missing_lines.append({
                    "numbers": line_info["numbers"],
                    "name": line_info["name"],
                    "description": line_info["description"],
                    "type": line_info["type"],
                    "missing": sorted(list(missing_nums)),
                    "present": sorted(list(required_numbers & present_set))
                })

    return missing_lines
