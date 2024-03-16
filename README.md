
# Dietician App

Application supporting the work of a dietitian. The program's task is to gather patient data 
as well as results of body weight and BMI (Body Mass Index) measurements taken at successive 
time points. <br>

![Home page of the app](App%20screens%2Fscreen1.png)


## Table of Contents
* [Installation](#installation)
* [Technologies and libraries](#technologies-and-libraries)
* [Functionalities](#functionalities)
* [Setup](#setup)
* [Run the application from the terminal:](#run-the-application-from-the-terminal)
* [Project Status](#project-status)
* [Project Authors](#project-authors-)

## Installation

1. Cloning the Repository: `git clone repository-adress`
2. Setting Up Dependencies `pip install -r requirements.txt`

## Technologies and libraries
Python 3.11.7  <br>
PyQt 6.6.1 <br>
matplotlib <br>

## Functionalities
For the selected patient, the application provides the capability to present both of these parameters in textual form 
as a table, as well as calculate basic statistics (minimum, maximum, and average values). 
The information is stored in a relational SQLite database. <br>

- Add a new patient <br>

![Screen of the page 'Add a new pacient'](App%20screens%2Fscreen2.png)
- Add a new measurement (weight) <br>

![Screen of the page Add a new measurement](App%20screens%2Fscreen3.png)
- Display sequentially recorded weights and BMI for a given patient <br>

![Screen of the page Statistics](App%20screens%2Fscreen4.png)
## Setup
Supported platforms: Windows x64, Linux x86_64 and macOS 11+  <br>
Python programming language and an appropriate compiler for the language are required on the computer.<br><br> 
Ensure that the required libraries are installed. To do this, open a terminal in the project folder 
and type`pip install matplotlib` and `pip install PyQt6`. <br><br>
Download the entire "Dietitian_app" folder, then run the `main.py` file. <br>


## Run the application from the terminal:

- Open the system terminal (`cmd` for Windows).
- Navigate to the directory where your project is saved by typing: 
`cd path\to\file`
If the project is on a different drive, use the following command instead:
`cd /d path\to\project\folder`
- Then, type either `python main.py` or `python3 main.py` depending on which Python version is installed on your 
computer. <br> 
This will execute the `main.py` file and launch the application. <br>

## Project Status:
The project is completed

## Project Authors 
**Julia Rozmarynowska**
- Database preparation
- Writing functions to handle the database.
- Implementing data input and display functionalities in the application, integrating with the GUI layer.
- Documentation section
<br>

**Julia Walczyna**
- Designing the GUI layer of the application.
- Connecting the GUI layer with the data handling functions.
- README.md file.
- Documentation section.