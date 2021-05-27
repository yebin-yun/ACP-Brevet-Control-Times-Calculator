# UOCIS322 - Project 7 #
Adding authentication and user interface to brevet time calculator service

## What is in this repository

You have a minimal implementation of password- and token-based authentication modules in `DockerAuth` directory, and login forms in `DockerLogin`, using which you can create authenticated REST API-based services (as demonstrated in class), as well as a front end. 

## IMPORTANT NOTES

**MAKE SURE TO USE THE SOLUTION `acp_times.py` from Canvas for this project!**

**MAKE SURE TO KEEP YOUR FILES in `brevets`! REMOVE `DockerRestAPI` after you're done!**

## Getting started 

You will reuse *your* code from Project 6.

Recall: you created the following three parts: 

* You designed RESTful services to expose what is stored in MongoDB, and created the following:

** "http://<host:port>/listAll" should return all open and close times in the database

** "http://<host:port>/listOpenOnly" should return open times only

** "http://<host:port>/listCloseOnly" should return close times only

* You also designed two different representations: one in csv and one in json. For the above, JSON should be your default representation. 

** "http://<host:port>/listAll/csv" should return all open and close times in CSV format

** "http://<host:port>/listOpenOnly/csv" should return open times only in CSV format

** "http://<host:port>/listCloseOnly/csv" should return close times only in CSV format

** "http://<host:port>/listAll/json" should return all open and close times in JSON format

** "http://<host:port>/listOpenOnly/json" should return open times only in JSON format

** "http://<host:port>/listCloseOnly/json" should return close times only in JSON format

* You also added a query parameter to get top "k" open and close times. For examples, see below.

** "http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format 

** "http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format

* You'll also designed consumer programs (e.g., in jQuery) to expose the services.

### Functionality you will add

In this project, you will add the following functionalities:

#### Part 1: Authenticating the services 

- POST **/register**

Registers a new user. On success a status code 201 is returned. The body of the response contains a JSON object with the newly added user. On failure status code 400 (bad request) is returned. Note: The password is hashed before it is stored in the database. Once hashed, the original password is discarded. Your database should have three fields: id (unique index), username and password for storing the credentials.

- GET **/token**

Returns a token. This request must be authenticated using a HTTP Basic Authentication (see `DockerAuth/password.py` and `DockerAuth/testToken.py`). On success a JSON object is returned with a field `token` set to the authentication token for the user and a field `duration` set to the (approximate) number of seconds the token is valid. On failure status code 401 (unauthorized) is returned.

- GET **/RESOURCE-YOU-CREATED-IN-PROJECT-6**

Return a protected <resource>, which is basically what you created in project 6. This request must be authenticated using token-based authentication only (see `DockerAuth/testToken.py`). HTTP password-based (basic) authentication is not allowed. On success a JSON object with data for the authenticated user is returned. On failure status code 401 (unauthorized) is returned.

#### Part 2: User interface

The goal of this part of the project is to create frontend/UI for Brevet app using Flask-WTF and Flask-Login introduced in lectures. You frontend/UI should use the authentication that you created above. In addition to creating UI for basic authentication and token generation, you will add three additional functionalities in your UI: a) registration, b) login, c) remember me, d) logout.

#### Summary
You will still maintain your `brevetsapp` service, and `mongodb` service that you've had since project 5, that will remain UNCHANGED.

## Tasks

You'll turn in your credentials.ini using which we will get the following:

* The working application with two parts.

* Dockerfile

* docker-compose.yml

## Grading Rubric

* If your code works as expected: 100 points. This includes:
    * Basic APIs work as expected in part 1.
    * Decent user interface in part 2 including the three functionalities in the UI.

* For each non-working API in part 1, 15 points will be docked off. Part 1 carries 45 points.

* For the UI and the three functionalies, decent UI carries 15 points. Each functionality carries 10 points. In short, part 2 carries 45 points.

* If none of them work, you'll get 10 points assuming
    * `README` is updated with your name and email ID.
    * `credentials.ini` is submitted with the correct URL of your repo.
    * `docker-compose.yml` works/builds without any errors.

* If the `docker-compose.yml` doesn't build or if `credentials.ini` is missing, 0 will be assigned.
