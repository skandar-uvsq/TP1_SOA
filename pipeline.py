import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from TP1_SOAP.services.verify_solvability import is_solvable
from TP1_SOAP.services.information_extraction import extract_infos
from TP1_SOAP.services.property_evaluation import evaluate_property
from suds.client import Client


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"New file uploaded: {event.src_path}")
            self.perform_action(event.src_path)

    def perform_action(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            # data = extract_infos(text=content)
            # estimated_value = evaluate_property(
            #     address=data["property_details"]["address"],
            #     region=data["property_details"]["region"],
            #     area_sqm=data["property_details"]["surface"],
            #     condition=data["property_details"]["description"][-1].split(" ")[0],
            # )
            # print(
            #     is_solvable(
            #         name=data["personal_information"]["name"],
            #         monthly_cost_of_the_property=estimated_value,
            #     )
            # )
            dataExtractionService_client = Client(
                "http://localhost:8000/DataExtractionService?wsdl"
            )
            result = dataExtractionService_client.service.extract_data(content)

            data = str(result)
            propertyEvaluationService_client = Client(
                "http://localhost:8000/PropertyEvaluationService?wsdl"
            )
            estimated_value = float(
                propertyEvaluationService_client.service.evaluate_property(data)
            )

            solvencyCheckService_client = Client(
                "http://localhost:8000/SolvencyCheckService?wsdl"
            )
            result = solvencyCheckService_client.service.check_solvency(
                data, estimated_value
            )

            decisionService_client = Client(
                "http://localhost:8000/DecisionService?wsdl"
            )
            result = decisionService_client.service.make_decision(result)
            print(result)


def start_watching(path):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    folder_to_watch = "TP1_SOAP/demands"
    start_watching(folder_to_watch)
