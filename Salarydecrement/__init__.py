import csv
import datetime
import logging
import os

import azure.functions as func


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

                    updated_salary = round((float(last_row[0]) * 0.99), 2)

                with open(filepath, "a") as file:
                    writer = csv.writer(file)
                    writer.writerow([updated_salary, utc_timestamp, "Decrement", "-1%"])

                    logging.info("SalaryDecrement function ran at %s", utc_timestamp)
                    logging.info(f"Updated Salary is {updated_salary}")
            else:
                logging.info("The Salary records file is not found.")

        else:
            logging.info("The Salary records folder is not found.")

    except Exception as e:
        logging.info(f"An error occured while processing the request. {str(e)}")
