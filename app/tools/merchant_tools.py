def get_merchant_risk(merchant_id: str):

    merchant_data = {

        "M101": {
            "merchant_id": "M101",
            "risk_score": 0.10,
            "risk_level": "LOW"
        },

        "M102": {
            "merchant_id": "M102",
            "risk_score": 0.15,
            "risk_level": "LOW"
        },

        "M103": {
            "merchant_id": "M103",
            "risk_score": 0.20,
            "risk_level": "LOW"
        },

        "M501": {
            "merchant_id": "M501",
            "risk_score": 0.90,
            "risk_level": "HIGH"
        }
    }

    return merchant_data.get(
        merchant_id,
        {
            "merchant_id": merchant_id,
            "risk_score": 0.50,
            "risk_level": "MEDIUM"
        }
    )