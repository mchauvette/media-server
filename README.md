# media-server
A Flask backend web-UI for accessing pictures on a server.

## Setup
First, create a virtual environment and activate it:

`$ virtualenv env`
`$ source env/bin/activate`

Next, install dependencies:

`$ pip3 install -r requirements.txt`

Then, create an empty databse:

`$ python3`

`>>> from project import db, create_app`

`>>> db.create_all(app=create_app())`

`>>> exit()`

Lastly, modify the project/__init__.py file to specify the UPLOAD_FOLDER

## Running the server

To run the server simply run the app.py with python:

`$ python3 app.py`

Then, open the url "localhost:5000" in your web browser
