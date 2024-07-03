### HappyFox Backend Assignment


## Prerequsites
    - Python 3.x
    - git

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/aditya6981/Happyfox-interview-aditya.git
    cd Happyfox-interview-aditya
    export PYTHONPATH=$(pwd)
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install the required packages**

    ```bash
    pip install -r requirements.txt
    ```


## Project Structure 

```bash
HAPPYFOX-INTERVIEW-ADITYA/
    │
    ├── src/
    │   ├── fetch_emails.py
    │   ├── save_email.py
    │   ├── process_emails.py
    │   ├── __init.py__
    │  
    ├── db_models/
    │   ├── email.py
    │   ├── email_test.py
    │   ├── __init.py__
    │
    │
    ├── google_apis/
    │   ├── credentials.json
    │   ├── gmail_authentication.py
    │   ├── token.pickle
    │   ├── __init.py__
    │
    ├── src/
    │   ├── fetch_emails.py
    │   ├── save_email.py
    │   ├── process_emails.py
    │   ├── rules.json       
    │   ├── __init.py__
    │
    ├── tests/
    │   ├── test_fetch_emails.py
    │   ├── test_process_emails.py
    │   ├── test_save_emails.py
    │
    ├── readme.md
    ├── requirements.txt
```

# Setup
**Enable Gmail API and Create OAuth Credentials**
* Go to the [Google Cloud Console](https://console.cloud.google.com/welcome?project=kubernetes-278505).
* Create a new project or select an existing one.
* Navigate to the "API & Services" dashboard.
* Click on "Enable APIs and Services" and enable the Gmail API.
* Click on "Create Credentials" and select "OAuth client ID".
* Configure the consent screen if prompted.
* Select "Desktop app" and create the credentials.
* Download the json file and place it in the path `google_apis/credentials.json` .
* run
    ```bash
    python google_apis/gmail_authentication.py
    ```
  This will open the browser and prompt to authenticate the request
  once authenticated google_apis/token.pickle will be created holding the token required for authentication 
       
# Usage

1. **Fetch and Save Emails**

    ```bash
    python src/fetch_emails.py
    ```   
    * This script will fetch the emails from gmail and save the emails in DB.
     DB schema is defined in `db_models/email.py`



3. **Process Emails**
    ```bash
    python src/process_emails.py
    ```
    - This script will process and update the email records in DB as per
    the rules defined in `src/rules.json`.
    these rules can be modified as per user preferences.




# Rules Configuration

- Example Rules JSON
`src/rules.json`  
```json
[
    {
        "name: : "Rule 1",
        "description" : "Sample Rule",
        "predicate": "all",
        "conditions": [
            {"field": "subject", "predicate": "contains", "value": "interview"},
            {"field": "sender", "predicate": "contains", "value": "adik170698@gmail.com"},
            {"field": "received_date", "predicate": "less_than_days", "value": "2"}
        ],
        "action": [
            {"action_type": "read_status", "value": "read"},
            {"action_type": "mailbox", "value": "inbox"}
        ]
    },
    {
        "name: : "Rule 2",
        "description" : "Sample Rule",
        "predicate": "any",
        "conditions": [
            {"field": "subject", "predicate": "contains", "value": "newsletter"},
            {"field": "sender", "predicate": "contains", "value": "marketing@example.com"},
            {"field": "received_date", "predicate": "greater_than_days", "value": "30"}
        ],
        "action": [
            {"action_type": "read_status", "value": "unread"},
            {"action_type": "mailbox", "value": "archive"}
        ]
    }
]
```
  

Each rule has the following structure:

- **predicate**: Defines how conditions are evaluated.
  - **Possible Values**:
    - `all`: All conditions must be met.
    - `any`: Any of the conditions must be met.
- **conditions**: A list of conditions that must be evaluated.
- **action**: A list of actions to be taken if the conditions are met.
- **name**: Name of the Rule.
- **description**: A Description for the defined Rule.

### Conditions

Each condition has the following keys:

- **field**: The field of the email to be evaluated.
  - **Possible Values**:
    - `subject`: The subject of the email.
    - `sender`: The sender's email address.
    - `recipient`: The recipient's email address.
    - `received_date`: The date the email was received.
    - `body`: The body content of the email.
- **predicate**: The condition to be applied to the field.
  - **Possible Values**:
    - `contains`: Checks if the field contains a specific value.
    - `equals`: Checks if the field is exactly equal to a specific value.
    - `does_not_contain`: Checks if the field does not contain a specific value. 
    - `does_not_equal`: Checks if the field is not equal to a specific value.
    - `less_than_days`: Checks if the date is less than a specific number of days ago.
    - `greater_than_days`: Checks if the date is greater than a specific number of days ago.
    - `less_than_months`: Checks if the date is less than a specific number of months ago.
    - `greater_than_months`: Checks if the date is greater than a specific number of months ago.
- **value**: The value to be compared against the field.

### Actions

Each action has the following keys:

- **action_type**: The type of action to be performed.
  - **Possible Values**:
    - `read_status`: Updates the read status of the email.
    - `mailbox`: Moves the email to a specific mailbox.
- **value**: The value associated with the action.
  - **Possible Values**:
    - For `read_status`:
      - `read`: Marks the email as read.
      - `unread`: Marks the email as unread.
    - For `mailbox`:
      - `inbox`: Moves the email to the inbox.
      - `spam`: Moves the email to the spam folder.
      - `trash`: Moves the email to the trash.
      - `important`: Moves the email to the important folder.

# TEST CASES
```bash
pytest tests/
```

Total Test Cases : 5

1. **Save Emails**
   * Asserts if email records are getting saved in DB successfully
   * `file_name` : src/test_save_emails.py
   * `module` : test_save_emails

2. **Fetch Emails**
   * Asserts if email records are fetched using gmail api and saved in DB successfully
   * `file_name` : src/test_fetch_emails.py
   * `module` : test_email_fetch
  
3. **Apply Predicates**
   * Asserts if predicates are applied as expected for the sample email and rules defined in the code. 
   * `file_name` : src/test_process_emails.py
   * `module` : test_apply_predicate
  
4. **Apply Conditions**
   * Asserts if email records are filtered and actions are taken as expected for the sample email and rules defined in the code. 
   * `file_name` : src/test_process_emails.py
   * `module` : test_apply_rules
     
5. **Process Emails**
   * Asserts if email records are uodated in DB as expected for the sample email records and rules defined in the code. 
   * `file_name` : src/test_process_emails.py
   * `module` : test_process_action

    

   
    
