"""
Numerology data constants including planet compatibility, luck factors, and remedies
"""

# Alphabet to Number Mapping for Name Numerology
ALPHABET_VALUES = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

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
    4: {1: "90-100%", 2: "20-30%", 3: "70%", 4: "100%", 5: "90-100%", 6: "80-90%", 7: "100%", 8: "100%", 9: "50%"},
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
