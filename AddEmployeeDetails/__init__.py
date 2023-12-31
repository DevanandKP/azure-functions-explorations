import csv
import json
import logging
import os

import azure.functions as func


def check_duplicates(filepath, EmployeeID):
    with open(filepath, "r") as file:
        writer = csv.reader(file)
        for row in writer:
            if (row[0]) == EmployeeID:
                return True
    return False


def add_entry(filepath, EmployeeID, Name, DOB, Position):
    with open(filepath, "a") as file:
        writer = csv.writer(file)
        if check_duplicates(filepath, EmployeeID):
            response_data = {
                "ERROR": f"EMPLOYEE ID {EmployeeID} ALREADY EXISTS. ENTER A NEW ID"
            }
        else:
            writer.writerow([EmployeeID, Name, DOB, Position])
            response_data = {
                "EmployeeID": EmployeeID,
                "Name": Name,
                "DOB": DOB,
                "Position": Position,
            }
    return response_data


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    EmployeeID = req.params.get("EmployeeID")
    Name = req.params.get("Name")
    DOB = req.params.get("DOB")
    Position = req.params.get("Position")

    if not (EmployeeID or Name or DOB or Position):
        return func.HttpResponse(
            "Welcome. Pass the parameters EmployeeID, Name, DOB and Position to add the employee detail.",
            status_code=200,
        )
    else:
        folderpath = os.path.join(os.getcwd(), "output")
        filepath = os.path.join(folderpath, "EmployeeData.csv")
        try:
            if os.path.exists(folderpath):
                response_data = add_entry(filepath, EmployeeID, Name, DOB, Position)
                return func.HttpResponse(
                    json.dumps(response_data),
                    mimetype="application/json",
                    status_code=201,
                )

            else:
                os.makedirs(folderpath)
                with open(filepath, "w") as file:
                    writer = csv.writer(file)
                    writer.writerow(["EmployeeID", "Name", "DOB", "Position"])

                response_data = add_entry(filepath, EmployeeID, Name, DOB, Position)
                return func.HttpResponse(
                    json.dumps(response_data),
                    mimetype="application/json",
                    status_code=201,
                )

        except Exception as e:
            return func.HttpResponse(
                f"An error occured while processing the request. {str(e)}",
                status_code=400,
            )
