import csv
import json
import logging
import os

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    EmployeeID = req.params.get("EmployeeID")
    if not EmployeeID:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            EmployeeID = req_body.get("EmployeeID")

    if EmployeeID:
        folderpath = os.path.join(os.getcwd(), "output")
        filepath = os.path.join(folderpath, "EmployeeData.csv")
        try:
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    reader = csv.reader(file)
                    response_data = []
                    for row in reader:
                        if (int(EmployeeID) == 0) or (row[0] == EmployeeID):
                            response_data.append(
                                {
                                    "EmployeeID": row[0],
                                    "Name": row[1],
                                    "DOB": row[2],
                                    "Position": row[3],
                                }
                            )
                    if not response_data:
                        return func.HttpResponse(
                            f"The Employee ID {EmployeeID}, does not exist",
                            status_code=404,
                        )
                    else:
                        return func.HttpResponse(
                            json.dumps(response_data, indent=2),
                            mimetype="application/json",
                            status_code=200,
                        )
            else:
                return func.HttpResponse(
                    "The employee records file is not found.",
                    status_code=404,
                )

        except Exception as e:
            return func.HttpResponse(
                f"An error occured while processing the request. {str(e)}",
                status_code=400,
            )

    else:
        return func.HttpResponse(
            "Welcome. Enter an EmployeeID to display the Details.",
            status_code=200,
        )
