# HappyFox Backend Assignment


# Prerequsites
    - Python 3.x

# Installation

    1. Clone the repository:

        ```
        git clone https://github.com/aditya6981/Happyfox-interview-aditya.git
        cd Happyfox-interview-aditya
        ```

    2. Create a virtual environment:

        ```
        python3 -m venv env
        source env/bin/activate
        ```

    3. Install the required packages

        ```
        pip install -r requirements.txt
        ```




# Project Structure

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



    - Gmail api enabled google cloud project with OAuth Credentials JSON
            Steps: 
                1. Go to the [Google Cloud Console](https://console.cloud.google.com/welcome?project=kubernetes-278505).
                2. Create a new project or select an existing one.
                3. Navigate to the "API & Services" dashboard.
                4. Click on "Enable APIs and Services" and enable the Gmail API.
                6. Click on "Create Credentials" and select "OAuth client ID".
                7. Configure the consent screen if prompted.
                8. Select "Desktop app" and create the credentials.
                6. Download the json file and place it in the path google_apis/credentials.json .

# Installation

    - Open Terminal

    - Clone the repository
        1. git clone https://github.com/aditya6981/Happyfox-interview-aditya.git
        2. cd Happyfox-interview-aditya

    - Activate env
        1. RUN : python3 -m venv env
        2. RUN : source env/bin/activate

    - Install Required Packages
        1. pip install requirements.txt

    - Google Authentication
        1. Download and save OAuth credentials in google_apis folder
        2. RUN : python google_apis

    
