# Wannabe-Serres-Hackathon-2019
## Development Team: Wannabe Programmers

The purpose of this project is the analysis of apache log files in order to detect web attacks, like SQL Injection, XSS and FLI.

The project is written in python. Before we begin, we first analysed the logs provided and we created an SQL Insert query, in order to add the data to an sql database. That way we can easier retrieve the data and make complicated quiries.

The database is automatically created when the project runs, so you don't need to worry about that.

## Required python modules.
* requests
* datetime
* numpy
* sklearn
* mysql.connector
* pycountry
* matplotlib
* urllib

Modules that were used to create the database script:
* apache_log_parser

Inside the folder python_code you can find two folders, our code inside the folder codes and the daily apache logs with the data insert query inside the folder daily-logs.

Inside the folder codes, you can find the `config.py.example` file. To run the project, you need to rename the file to `config.py`. After that, you can start editing your config file by adding your mySQL credentials.
