# AryaBota
An app to teach Python coding, that gradually allows students to transition from using commands similar to natural language, to more Pythonic constructs.   
The experience is gamified through a visual component called AryaBota (AB) - a bot in a grid that navigates its way around obstacles.
This tool is still under development.

## Set-Up:
### Virtual Environment for Server
1. Create the virtual environment called `venv` by running `virtualenv venv`, it should create a directory called `venv` at the root-level
1. On Linux-based OS, run `source venv/bin/activate`; on Windows, run `.\env\Scripts\activate`
2. To deactivate, run `deactivate`
### Dependencies for Server
1. Python3: install the required PyPi packages by running the following in `app/flask-app`  
 `python3 -m pip install -r requirements.txt`
### Running the Server
1. Start the server in development mode by running the following in `app/flask-app`  
`FLASK_ENV=development flask run`

## Development
Note: After you set this up, make sure you have the front-end React app up and running. Visit [aryabota-ui](https://github.com/ab-apps/aryabota-ui) to learn more about this.

## How To
Visit the documentation [here](https://aryabota-docs.notion.site/AryaBota-316098bf36fc4cef9aeb8ef884a8c2d3).