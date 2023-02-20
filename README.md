                                The aim of the project

The project manages an employee table and their departments through various processes.

project components:
-main.py:
This file contains instructions that enable the user to select the tasks they wish to manage in the database. To begin, the user is required to enter their username and password to verify their authority to perform the operations.
After verifying the user's authority, the program will prompt the user to initialize the databases. If the user selects yes, a confirmation message will appear to indicate that the databases have been initialized. If the databases already exist, a message will appear to notify the user. Otherwise, the data will be imported from the Excel file and exported to the database.

-api.py
On this page, variables for the select, update, and delete commands are managed and then sent to the database.py file. These variables can be received through main.py or via HTTP requests using the GET, PUT, POST, and DELETE methods with FastAPI.

-database.py
On this page, the database is initialized if it does not already exist, data is imported from an Excel file and exported to the database, and all queries are executed based on the variables sent from the API page

-classes.py
This code contains all of the necessary classes that can be used to implement the program.

-users.db
Before starting the program, this file must be present.

-emp.db
At the start of the program, this file is not present. When the user enters the program, the program is asked to initialize the database. If the user approves, then the program creates this file.




Instructions:

To use this program we should install some libraries 
-pip install pydantic
then import from pydantic import BaseModel in classes.py
-pip install fastapi
from fastapi import FastAPI
-pip install uvicorn
to run the app using http requests we use
uvicorn api:app –reload
-pip install pandas
I use this library to read an Excel file into a DataFrame object and then export the data to a database.
