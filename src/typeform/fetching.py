"""Functions related to the gathering of data from online forms"""
import os
import json
import pandas as pd
from typing import Iterable
from typeform import Typeform


def fetch_typeform(login_filename: str = "login.json",
                   fields_filename="fields.json") -> pd.DataFrame:
    """
    Fetches answers
    Arguments:
        login_filename: filename of the file with login information
        fields_filename: filename of the field containing the expected fields
    """
    expected_fields = read_field_ids(fields_filename)
    login = load_login(login_filename)
    responses = Typeform(login["token"]).responses
    query_result: dict = responses.list(login["form_id"], pageSize=1000)

    answers = extract_answers(query_result, expected_fields)
    return answers


def read_field_ids(filename: str):
    """Reads the file (filename) and returns it as a dictionary"""
    path = os.path.dirname(os.path.realpath(__file__)) + "/" + filename
    with open(path, "r") as json_file:
        question_ids = json.load(json_file)
    return question_ids


def load_login(filename: str) -> dict:
    """Reads typeform credentials from filename and returns them as dict"""
    path = os.path.dirname(os.path.realpath(__file__)) + "/" + filename
    with open(path, "r") as f:
        login = json.load(f)
    return login


def extract_answers(query_response: dict, fields: list):
    """
    Extracts the answers from a Typeform formatted dict (single solved form)
    Arguments:
        query_response (dict): Typeform's dict containing all responses
        fields (list): list containing all the fields (questions) in the form
    Returns:
        dict containing the (formatted) answers to the form, in the shape of
        {field_a: [answer_a, answer_b, ...],
         field_b: [answer_a, answer_b, ...],...}.
        If no answer was found at some point, then its answer is None, which
        means that every list has the same length.
    """
    final_answers = {f: [] for f in fields}
    for answer_set in query_response["items"]:
        remaining_fields = set(fields)

        for question in answer_set["answers"]:
            field = question["field"]["ref"]
            answer = format_answer(question)
            final_answers[field].append(answer)
            remaining_fields.discard(field)
        for field in remaining_fields:
            final_answers[field].append(None)

    return final_answers


FORMAT_GUIDE = {
    "text": lambda x: x,
    "boolean": lambda x: x,
    "number": lambda x: float(x),
    "choice": lambda x: x["label"],
    "choices": lambda x: x["labels"]
}


def format_answer(question):
    """
    Extracts the answer from a question and formats it. Accordingly
    to the FORMAT_GUIDE.
    """
    answer_type = question["type"]
    answer = question[answer_type]

    return FORMAT_GUIDE[answer_type](answer)


if __name__ == "__main__":
    print(fetch_typeform())
