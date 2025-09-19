# file: config.py

# Default model name
MODEL = "test-model"

# Fallback guardrail function
def guardrail_input_function(user_input: str) -> bool:
    return bool(user_input and user_input.strip())

# Hotel data
HOTELS = {
    "Hotel Sannata": {
        "total_rooms": 200,
        "reserved_rooms": 20,
        "owner": "Mr. Ratan Lal"
    },
    "Hotel Paradise": {
        "total_rooms": 150,
        "reserved_rooms": 10,
        "owner": "Ms. Anita Sharma"
    },
    "Hotel BlueSky": {
        "total_rooms": 120,
        "reserved_rooms": 15,
        "owner": "Mr. John Doe"
    },
}
