from suds.client import Client


dataExtractionService_client = Client(
    "http://localhost:8000/DataExtractionService?wsdl"
)
result = dataExtractionService_client.service.extract_data(
    "John Doe is looking to purchase a charming two-story house with a garden, located at 123 Rue de la Liberte, 75001 Paris, France, Apt N° 1401. This lovely property, with a surface area of 150m², is situated in a peaceful residential neighborhood and is in good condition. John is seeking a loan of 200000$ to finance this purchase. He can be contacted via email at john.doe@email.com or by phone at +33 123 456 789."
)

data = str(result)
propertyEvaluationService_client = Client(
    "http://localhost:8000/PropertyEvaluationService?wsdl"
)
estimated_value = float(
    propertyEvaluationService_client.service.evaluate_property(data)
)

solvencyCheckService_client = Client("http://localhost:8000/SolvencyCheckService?wsdl")
result = solvencyCheckService_client.service.check_solvency(data, estimated_value)

decisionService_client = Client("http://localhost:8000/DecisionService?wsdl")
result = decisionService_client.service.make_decision(result)


print(result)
