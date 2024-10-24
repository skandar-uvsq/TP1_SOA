from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from TP1_SOAP.services.verify_solvability import is_solvable
from TP1_SOAP.services.information_extraction import extract_infos
from TP1_SOAP.services.property_evaluation import evaluate_property
import json


class DataExtractionService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def extract_data(ctx, text):
        data = extract_infos(text)
        return json.dumps(data)


class SolvencyCheckService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def check_solvency(ctx, data, estimated_value):
        data = json.loads(data)
        solvable_client = is_solvable(
            name=data["personal_information"]["name"],
            monthly_cost_of_the_property=float(estimated_value),
        )
        return json.dumps(solvable_client)


class PropertyEvaluationService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def evaluate_property(ctx, data):
        data = json.loads(data)
        estimated_value = evaluate_property(
            address=data["property_details"]["address"],
            region=data["property_details"]["region"],
            area_sqm=data["property_details"]["surface"],
            condition=data["property_details"]["description"][-1].split(" ")[0],
        )
        return json.dumps(estimated_value)


class DecisionService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def make_decision(ctx, client_solvable):
        decision = ""
        print(client_solvable, client_solvable == "true")
        if client_solvable == "true":
            decision = "Final decision : Yes, client is solvable."
        else:
            decision = "Final decision : No, client is not solvable."
        return json.dumps(decision)


# Application configuration
application = Application(
    [
        DataExtractionService,
        SolvencyCheckService,
        PropertyEvaluationService,
        DecisionService,
    ],
    tns="tn.edu.uvsq.data_extraction",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":

    server = make_server("0.0.0.0", 8000, wsgi_app)
    print("Data extraction service is running on port 8000...")
    server.serve_forever()
