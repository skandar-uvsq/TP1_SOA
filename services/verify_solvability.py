from .property_evaluation import evaluate_property
from .information_extraction import extract_infos
import random


def get_monthly_income_from_bank_account(user):
    return random.randint(2000, 3000)


def get_credit_from_bank_account(user):
    return random.randint(50, 1000)


def is_solvable(name: str, monthly_cost_of_the_property: float):
    income = get_monthly_income_from_bank_account(user=name)
    credit = get_credit_from_bank_account(user=name)
    is_solvable = income - monthly_cost_of_the_property > 400 and credit > 150
    print(f"Is solvable ===> {is_solvable}")
    return is_solvable


# for i in range(1, 6):
#     with open(file=f"TP1_SOAP/sample_data/{i}.txt", encoding="utf-8") as f:
#         text = f.read()
#         data = extract_infos(text=text)

#     estimated_value = evaluate_property(
#         address=data["property_details"]["address"],
#         region=data["property_details"]["region"],
#         area_sqm=data["property_details"]["surface"],
#         condition=data["property_details"]["description"][-1].split(" ")[0],
#     )

#     print(
#         is_solvable(
#             name=data["personal_information"]["name"],
#             monthly_cost_of_the_property=estimated_value,
#         )
#     )
