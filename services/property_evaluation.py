# Simulated Data
# TODO: put it in a json file
market_prices = {
    "region_1": 2500,  # Price per square meter
    "region_2": 3200,
    "region_3": 2800,
}

property_conditions = {
    "good": 1.0,  # No deduction
    "average": 0.9,  # 10% deduction
    "poor": 0.8,  # 20% deduction
}

legal_compliance = {
    "compliant": 1.0,
    "non_compliant": 0.5,  # Property not fully compliant has a lower value
}


# Main function to estimate the property value
def evaluate_property(region, area_sqm, condition, is_compliant):
    # Step 1: Get market price for the region
    if region not in market_prices:
        print("Region not found.")
        return None

    price_per_sqm = market_prices[region]

    # Step 2: Adjust based on the condition of the property
    if condition not in property_conditions:
        print("Condition not valid.")
        return None

    condition_multiplier = property_conditions[condition]

    # Step 3: Adjust based on legal compliance
    compliance_multiplier = (
        legal_compliance["compliant"]
        if is_compliant
        else legal_compliance["non_compliant"]
    )

    # Step 4: Calculate the final estimated value
    estimated_value = (
        area_sqm * price_per_sqm * condition_multiplier * compliance_multiplier
    )

    return estimated_value


# Example usage
region = "region_2"  # Chosen region
area_sqm = 100  # Property area in square meters
condition = "average"  # Property condition
is_compliant = True  # Compliance status

estimated_value = evaluate_property(region, area_sqm, condition, is_compliant)

if estimated_value:
    print(f"Estimated property value: {estimated_value} EUR")
