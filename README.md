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

## Results

By Running the main.py you can get the following results.

### General
* Total traffic: **86402**
* Total 5XX requests: **4729**
* Total unique ips: **20**

### Data Mining:
* Percentage of attack requests: **31.88**%
* SQL Injection Requests: **5534**
* XSS Requests: **18722**
* LFI Requests: **3289**
* Most Attacked Websites:
  * '/': **5568**
  * '/index.php/': **4476**
  * '/login.php/': **3360**
  * '/api/v1/login/': **2347**
  * '/api/v1/register/': **1646**
* Country with attack requests is **China** with **9490** requests.
* Which time of day were the mest attack requests noticed? ¯\\_(ツ)_/¯

### Visualisation
* Server Requests per hour <img src="https://raw.githubusercontent.com/cmoutafidis/Wannabe-Serres-Hackathon-2019/master/python_code/diagrams/RequestsPerHour_BarGraph.png">
* Server Requests per country <img src="https://raw.githubusercontent.com/cmoutafidis/Wannabe-Serres-Hackathon-2019/master/python_code/diagrams/RequestsPerCountry_PieChart.png">
* [World graph of attack requests per hour per country](https://bit.ly/2Js7Q4H)

### Bonus
Most harmful IP was 62.109.16.162 with:
* **7453** Safe Requests
* **721** SQL Injection requests
* **2380** XSS requests
* **471** Local File Injection requests
