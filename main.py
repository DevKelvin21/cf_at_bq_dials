import os
import functions_framework
from flask import jsonify, Request
from google.cloud import bigquery
from datetime import datetime
from typing import Any

client = bigquery.Client()

DISPOSITION_MAP = {
    "DROP": "No Answer", "ADC": "No Answer", "PDROP": "Outbound Pre-Routing",
    "A": "Answering Machine", "AA": "Answering Machine Auto", "AB": "Busy Auto",
    "B": "Busy", "CALLBK": "Call Back", "CBL": "Call Back Later", 
    "DC": "Disconnected Number", "DNC": "Do Not Call", "Follow": "Follow Up", 
    "N": "No Answer", "NAU": "No Answer", "NA": "No Answer Autodial", 
    "NI": "Not Interested", "NPRSN": "In Person Appointment", "Nurtre": "Nurture", 
    "PHNAPT": "Phone Appointment", "WN": "Wrong Number"
}

ENV_VAR_MSG = "Specified environment variable is not set."

TABLE_ID = os.getenv("BIGQUERY_TABLE_ID", ENV_VAR_MSG)

def transform_field(field: str, default: str = "") -> str:
    return default if "--A--" in field and "--B--" in field else field

def validate_timestamp(timestamp: str) -> str:
    """Validate and parse timestamp."""
    try:
        # Try to parse the timestamp in ISO 8601 format
        parsed_time = datetime.fromisoformat(timestamp)
        return parsed_time.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError("Invalid timestamp format. Expected ISO 8601 string.")

@functions_framework.http
def post_to_bigquery_with_timestamp(request: Request) -> Any:
    """
    Handles HTTP POST requests to insert data into a BigQuery table with an optional timestamp.
    Args:
        request (Request): The HTTP request object containing query parameters and JSON body.
    Returns:
        Any: A JSON response indicating the success or failure of the data insertion.
    Query Parameters:
        firstName (str): The first name of the individual.
        lastName (str): The last name of the individual.
        listDescription (str): Description of the list.
        dialedNumber (str): The phone number that was dialed.
        disposition (str): The disposition of the call.
        talkTime (str): The talk time of the call.
        termReason (str): The termination reason of the call.
        callNote (str): Notes related to the call.
        email (str): The email address of the individual.
        listID (str): The ID of the list.
        leadID (str, optional): The ID of the lead. Defaults to '0' if not provided.
        subscriberID (str): The ID of the subscriber.
        leadType (str): The type of the lead.
        source (str): The source of the lead.
    JSON Body:
        timestamp (str, optional): The timestamp of the event in a valid format. If not provided, the current date and time will be used.
    Raises:
        ValueError: If the provided timestamp is in an invalid format.
        Exception: For any other exceptions that occur during processing.
    Returns:
        JSON response:
            - 200: If the data is successfully inserted into BigQuery.
            - 400: If there are errors during data insertion or invalid timestamp format.
            - 500: For any other exceptions encountered during processing.
    """
    try:
        params = request.args
        firstName = params.get('firstName')
        lastName = params.get('lastName')
        listDescription = params.get('listDescription')
        dialedNumber = params.get('dialedNumber')
        disposition = params.get('disposition')
        talkTime = params.get('talkTime')
        termReason = params.get('termReason')
        callNote = params.get('callNote')
        email = params.get('email')
        listID = params.get('listID')
        leadID = params.get('leadID', '0')
        subscriberID = params.get('subscriberID')
        leadType = params.get('leadType')
        source = params.get('source')

        request_data = request.get_json(silent=True) or {}
        timestamp = request_data.get('timestamp')

        if timestamp:
            date = validate_timestamp(timestamp)
        else:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not leadID:
            leadID = '0'

        callNotesFormatted = transform_field(callNote)
        dispositionFormatted = DISPOSITION_MAP.get(disposition, disposition)
        talkTimeFormatted = transform_field(talkTime, "0")
        termReasonFormatted = transform_field(termReason)
        subscriberIDFormatted = transform_field(subscriberID)
        listDescriptionFormatted = transform_field(listDescription)

        row_to_insert = [{
            "Date": date,
            "FirstName": firstName,
            "LastName": lastName,
            "CallNotesFormatted": callNotesFormatted,
            "Phone": dialedNumber,
            "Email": email,
            "ListID": listID,
            "Disposition": dispositionFormatted,
            "LeadID": leadID,
            "TalkTimeFormatted": talkTimeFormatted,
            "TermReasonFormatted": termReasonFormatted,
            "SubscriberIDFormatted": subscriberIDFormatted,
            "ListDescriptionFormatted": listDescriptionFormatted,
            "LeadType": leadType,
            "Source": source,
        }]

        errors = client.insert_rows_json(TABLE_ID, row_to_insert)
        
        if errors:
            return jsonify({"errors": errors}), 400

        return jsonify({"status": "success", "message": "Data inserted into BigQuery successfully"}), 200

    except ValueError as ve:
        # Handle invalid timestamp format
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Catch and return any exceptions
        return jsonify({"error": str(e)}), 500
