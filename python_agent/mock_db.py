# mock_db.py

# 1. REAL LOOKING DOCTORS (Mapped by Specialty)
SPECIALIST_REGISTRY = {
    "cardiology": [
        {"name": "Dr. Emily Chen", "npi": "1457389201", "hospital": "Mercy General", "rating": 4.9},
        {"name": "Dr. Marcus Thorne", "npi": "1892039485", "hospital": "Sutter Health", "rating": 4.2}
    ],
    "dermatology": [
        {"name": "Dr. Sarah Lee", "npi": "1239048572", "hospital": "Skin Health Inst", "rating": 4.8},
        {"name": "Dr. Kevin Patel", "npi": "1928374650", "hospital": "Valley Derm", "rating": 4.5}
    ],
    "orthopedics": [
        {"name": "Dr. Brock Stone", "npi": "1122334455", "hospital": "Joint Center", "rating": 4.7}
    ]
}

# 2. INSURANCE RULES (The "Logic" for the demo)
INSURANCE_PLANS = {
    "Blue Cross": {
        "covered_specialties": ["cardiology", "dermatology"], 
        "copay": "$25.00"
    },
    "Kaiser": {
        "covered_specialties": ["general_practice"], # Kaiser is strict!
        "copay": "$15.00"
    },
    "Medi-Cal": {
        "covered_specialties": ["cardiology", "orthopedics"],
        "copay": "$0.00"
    }
}