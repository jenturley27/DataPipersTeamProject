from surveymonkey.client import Client
import os
import json
import pandas as pd


def fetch_monkey(login_filename: str = "login.json",
                 fields_filename: str = "form_config.json") -> pd.DataFrame:
    """
    Fetches answers
    Arguments:
        login_filename: filename of the file with login information
        fields_filename: filename of the field containing the expected fields
    """
    login = load_login(login_filename)
    config = load_config(fields_filename)

    client = Client(
        client_id=login["client_id"],
        client_secret=login["client_secret"],
        redirect_uri=login["redirect_uri"],
        access_token=login["access_token"])

    all_responses = client.get_survey_response_bulk(login["form_id"])

    answers = extract_answers(all_responses, config)
    return answers


def load_login(filename: str) -> dict:
    """Reads surveymonkey credentials from filename and returns them as dict"""
    path = os.path.dirname(os.path.realpath(__file__)) + "/" + filename
    with open(path, "r") as f:
        login = json.load(f)
    return login


def load_config(filename: str) -> dict:
    """
    Loads the config file at filename and returns a tuple containing its two
    dictionaries.
    """
    path = os.path.dirname(os.path.realpath(__file__)) + "/" + filename
    with open(path, "r") as f:
        config = json.load(f)
    return config


def extract_answers(query_response: dict, config: dict) -> dict:
    """
    Extracts the answers from a Survey Monkey single form
    Arguments:
        query_response (dict): Survey monkey's dict containing all responses
        id_to_field (dict): Connects question ids to corresponding fields
    Returns:
        dict containing the (formatted) answers to the form, in the shape of
        {field_a: [answer_a, answer_b, ...],
         field_b: [answer_a, answer_b, ...],...}.
        If no answer was found at some point, then its answer is None, which
        means that every list has the same length.
    """
    final_answers = {f: [] for f in config["id_to_field"].values()}

    for filled_form in query_response["data"]:
        remaining_fields = set(config["id_to_field"].values())

        question_set = filled_form["pages"][0]["questions"]

        for question in question_set:
            field = config["id_to_field"][question["id"]]
            answer = format_answer(
                question["answers"], field, config["id_to_choice"])
            final_answers[field].append(answer)
            remaining_fields.discard(field)

        for field in remaining_fields:
            final_answers[field].append(None)

    return final_answers


def format_answer(answer: dict, field: str, id_to_choice: dict):
    """
    Extracts the answer from a question and formats it. Accordingly
    to the FORMAT_GUIDE and its field.
    """
    FORMAT_GUIDE = {
        "default": lambda x: int(x[0]["text"]),
        "actions_taken_self": lambda x: [id_to_choice[choice_dict["choice_id"]] for choice_dict in answer]
    }
    formater = FORMAT_GUIDE.get(field, FORMAT_GUIDE["default"])
    return formater(answer)
