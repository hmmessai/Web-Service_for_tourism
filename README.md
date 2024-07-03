# Web-Service for tourism, Oriented with Cities

This project is done to get a wider knowlwdge on Python's Flask framework. The idea behind it is to simply serve a service where it displays tourist sites in specific cities, It also allows users to add cities and tourist sites into the database which can make the database rich in information and can be reached where the author couldn't reach.

## Installation

### Dependencies

To be able to use this app we will need to have python version 3.6 or above with the following packages installed

- Flask - Framework for the API and serving the whole project
- SqlAlchemy - For the database ORM

To install all this using the python package manager(pip) we will follow the following steps:-

- First make sure you have pip installed before you start
- Then install all the dependencies with the following command

  `pip install -r requirements.txt`

### Execution

Executing this app will be done with the following code.

- Browse to the main directory of the repository and run the following code on the first terminal

  `flask --app api run`

## Viewing

After running the server with `flask --app api run` you should be able to access the website on http://localhost:5000.

Go to this URL and enjoy browsing through the website. Please make sure that the port 5000 is available and not taken by another process.

## Environmental variables

| VARIABLE    | VALUES                                           | Meaning                                                     |
| ----------- | ------------------------------------------------ | ----------------------------------------------------------- |
| DB_STORAGE  | db or other                                      | db - use a database storage, any other - use a file storage |
| DB_HOST     | localhost by default or your server name         | The database hosts ip address                               |
| DB_USER     | root by default or the user name of db           | The user you log in as to access the database               |
| DB_PASSWORD | password by default( password of the user )      | The password of the user you want to log in as              |
| DB_DATABASE | tourism_service by default or the name of the db | The name of the database you want to store the data in      |

When you use database storage make sure you have set the correct information of the database in your .env file following the format from the .env.example file or set the above environment variables correctly. And also create the database you specified in the .env file as DB_DATABASE

## Improvment that are being worked on

- Authentication system to filter who can add information to the database
- Better CSS to make it look more appealing

## Authors

| Name               | email                     | github                            |
| ------------------ | ------------------------- | --------------------------------- |
| Birhan Kassaye     | birhanyalew2019@gmail.com | https://github.com/birhan-kassaye |
| Messai Hailemariam | messai.h.m@gmail.com      | https://github.com/hmmessai       |
