import csv
import datetime
import logging
import os
import random

import azure.functions as func


def create_file(filepath, utc_timestamp):
    with open(filepath, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Base_Salary", "Time", "Change", "Percentage"])
        writer.writerow([random.randint(1000, 5000), utc_timestamp, "-", "-"])

    return None


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = (
        datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    )

    if mytimer.past_due:
        logging.info("The timer is past due!")

    folderpath = os.path.join(os.getcwd(), "salary")
    filepath = os.path.join(folderpath, "salary.txt")
    try:
        if os.path.exists(folderpath):
            if os.path.exists(filepath):
                with open(filepath, "r") as file:
                    reader = csv.reader(file)
                    last_row = []
                    for row in reader:
                        last_row = row
                    print("Base salary is", last_row[0])
                    updated_salary = round((float(last_row[0]) * 1.025), 2)

                with open(filepath, "a") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [updated_salary, utc_timestamp, "Increment", "+2.5%"]
                    )
                    logging.info("SalaryIncrement function ran at %s", utc_timestamp)
                    logging.info(f"Updated Salary is {updated_salary}")
            else:
                create_file(filepath, utc_timestamp)

        else:
            os.makedirs(folderpath)
            create_file(filepath, utc_timestamp)

    except Exception as e:
        logging.info(
            f"An error occured while processing the request. {str(e)}",
        )
