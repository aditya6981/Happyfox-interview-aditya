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
    ├── rules.json
    └── README.md
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
* Download the json file and place it in the path google_apis/credentials.json .
* run
    ```bash
    python google_apis/gmail_authentication.py
    ```
  This will open the browser and prompt to authenticate the request
  once authenticated google_apis/token.pickle will be created holding the token required for authentication 
       
# Usage

1. **Fetch and Save Emails**
    - This script will fetch the emails from gmail and save the emails in DB.
     DB schema is defined in `db_models/email.py`
        RUN :
        ```bash
        python src/fetch_emails.py
        ```

2. **Process Emails**
This script will process and update the email records in DB as per
the rules defined in `src/rules.json`.
these rules can be modified as per user preferences.

   RUN :
    ```bash
    python src/process_emails.py
    ```

# Rules Configuration


    

   
    
