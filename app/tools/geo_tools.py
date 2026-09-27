def get_location_info(location: str):
    location_data = {
        "Chennai": {
            "country": "India",
            "city": "Chennai",
            "risk_region": "LOW"
        },

        "Mumbai": {
            "country": "India",
            "city": "Mumbai",
            "risk_region": "LOW"
        },

        "New York": {
            "country": "USA",
            "city": "New York",
            "risk_region": "MEDIUM"
        },

        "London": {
            "country": "UK",
            "city": "London",
            "risk_region": "MEDIUM"
        }
    }

    return location_data.get(
        location,
        {
            "country": "Unknown",
            "city": location,
            "risk_region": "UNKNOWN"
        }
    )