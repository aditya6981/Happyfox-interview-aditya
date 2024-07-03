import os
import json

from datetime import datetime

from db_models.email import Session, Email

CURRENT_BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def load_rules(path):
    with open(path, "r") as file:
        return json.load(file)


def process_email(email, actions, session=None):
    """
        Function to apply the actions mentioned in rules.json
        on the email records saved in db and commit
    """
    if not session:
        session = Session()

    for action in actions:
        if action["action_type"] == "read_status":
            email.read_status = action["value"]
        elif action["action_type"] == "mailbox":
            email.mailbox = action["value"]
    session.commit()


def apply_predicate(email, condition):
    """
        Function to validate if a email record satisfies the condition
        given in rules.json
    """
    field_value = getattr(email, condition["field"])
    predicate = condition["predicate"]
    conditional_value = condition["value"]

    # String Validations
    if isinstance(field_value, str):
        field_value = field_value.lower()
        conditional_value = conditional_value.lower()
   
        if predicate == "contains":
            return conditional_value in field_value
        elif predicate == "does_not_contain":
            return conditional_value not in field_value
        elif predicate == "equals":
            return conditional_value == field_value
        elif predicate == "does_not_equal":
            return conditional_value != field_value

    # Date Validations
    if isinstance(field_value, datetime):

        conditional_value = int(conditional_value)
        current_date = datetime.now()

        if predicate == "greater_than_days":
            return (current_date - field_value).days > conditional_value

        elif predicate == "less_than_days":
            return (current_date - field_value).days <= conditional_value

        elif predicate == "greater_than_months":
            return (current_date - field_value).days > conditional_value * 30

        elif predicate == "less_than_months":
            return (current_date - field_value).days <= conditional_value * 30


def evaluate_conditions(email, conditions, overall_predicate):
    """
        Function to to chack if an email if ready for applying actions
        based on condition validations and predicate validation as per
        the rules defined in rules.json
    """
    if overall_predicate == "all":
        return all(apply_predicate(email, condition) for condition in conditions)
    elif overall_predicate == "any":
        return any(apply_predicate(email, condition) for condition in conditions)
    return False


def apply_rules():
    """
        Function to apply to rules defined in rules.json on the
        email records saved in DB
    """
    session = Session()

    rules_path = os.path.join(CURRENT_BASE_PATH, "rules.json")
    rules = load_rules(rules_path)

    emails = session.query(Email).all()

    # Iterating each email record in db and applying actions if valid
    for email in emails:
        for rule in rules:
            if evaluate_conditions(email,
                                   rule["conditions"],
                                   rule["predicate"]):
                process_email(email, rule["actions"])

    print("Total Emails Processed : ", len(emails))


if __name__ == "__main__":
    apply_rules()
    print("Rules are applied to the DB records successfully!")
