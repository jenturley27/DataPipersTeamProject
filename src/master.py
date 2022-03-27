"""
Script containing the MasterData class and related functions
"""
import pandas as pd
from src.typeform.fetching import fetch_typeform
from src.survey_monkey.fetching import fetch_monkey


class MasterData:
    """
    Class designed to combine the results from the different survey platforms,
    providing the ability to update and return them separately. 
    """

    def __init__(self, config: dict = None):
        """
        Initializes the MasterData instance by fetching the data from the
        different sources.

        The config dictionary is supposed to contain the filenames used by
        fetch_typeform and fetch_monkey, stored at the keys "typeform_login",
        "typeform_config", "monkey_login" and "monkey_config". 
        """
        self.config = config
        self.typeform_data = None
        self.monkey_data = None
        self.update_all()

    def update_typeform(self) -> None:
        """Updates the data corresponding to the Typeform surveys"""
        if not self.config:
            self.typeform_data = fetch_typeform()
            return

        login = self.config["typeform_login"]
        config = self.config["typeform_config"]
        self.typeform_data = fetch_typeform(login, config)

    def update_monkey(self) -> None:
        """Updates the data corresponding to the Survey Monkey surveys"""
        if not self.config:
            self.monkey_data = fetch_monkey()
            return

        login = self.config["monkey_login"]
        config = self.config["monkey_config"]
        self.monkey_data = fetch_monkey(login, config)

    def update_all(self) -> None:
        """Updates the data from every form"""
        self.update_typeform()
        self.update_monkey()

    def get_typeform_data(self) -> pd.DataFrame:
        """Returns the data corresponding to Typeform as a panads DF"""
        return pd.DataFrame.from_dict(self.typeform_data)

    def get_monkey_data(self) -> pd.DataFrame:
        """Returns the data corresponding to Survey Monkey as a panads DF"""
        return pd.DataFrame.from_dict(self.monkey_data)

    def get_master_data(self) -> pd.DataFrame:
        """Retuns the combined results from all the sources"""
        d1 = label_all(self.typeform_data, "typeform", "source")
        d2 = label_all(self.monkey_data, "monkey", "source")
        merged = {k: d1[k] + d2[k] for k in d1.keys()}
        return pd.DataFrame.from_dict(merged)


def label_all(d: dict, label: str, field: str) -> dict:
    """
    Takes a dictionary <d> with the following structure
        string1: [object1, object2, object3, ..., objectN]
        string2: [...]
        ...
    Then includes a new entry of name <field> containing a list of N <label>
    strings. I.e. the return dict is
        string1: [object1, object2, object3, ..., objectN]
        string2: [...]
        ...
        <field>: [<label>, <label>, ..., <label>]
    """
    d_copy = d.copy()
    random_key = iter(d_copy).__next__()
    entry_count = len(d_copy[random_key])
    d_copy[field] = [label] * entry_count
    return d_copy
