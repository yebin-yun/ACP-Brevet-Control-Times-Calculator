# ACP Brevet Control Times Calculator #
> **Author: Ellie Yun, yyun.ellie@gmail.com**

Brevet time calculator with AJAX, MongoDB, and a RESTful API with authentication and user interface.

## Getting started

- Go to the ```brevets``` directory in the repository. 

- Build the flask app images and run the container using
           
      docker compose up

## Design 

This web application is composed with three services, and each service is implemented in a separate directory.

### brevets

![brevets](https://user-images.githubusercontent.com/87594239/127569871-99621a4e-6132-452e-959b-4e7a41e375c3.png)

In the ACP calculator web page, there are following functionalities:

- There are two buttons `Submit` and `Display` in the ACP calculator page.

- Upon clicking the `Submit` button, the filled-in control times will be inserted into a MongoDB database.

- Upon clicking the `Display` button, the entries from the database will be displayed in a new page.

- It handles some error cases appropriately. For example, `Submit` should return an error if no control times are input. One can imagine many such cases: you'll come up with as many cases as possible.

#### How to test it?

In the web browser, search the following url:

    http://<host>:<port>/

`Note: Change the values for host and port according to your machine.
 (check docker-compose.yml file for more details - port is set to 7127, which is editable.)`

### api

This is a Restful service that includes the following functionalities:

- POST **/register**
    - Registers a new user by storing the following three fields in the database:
        1. id (unique index)
        2. username (2-25 characters)
        3. password (8-25 characters)

    - On success, a status code 201 is returned. The body of the response 
    contains a JSON object with the newly added user. 
    
    - On failure, status code 400 (bad request) is returned. 
     
    `Note: The password is hashed before it is stored in the database. Once hashed, the original password is discarded.` 

- GET **/token**

    - Returns a token and an id. This request is authenticated using a HTTP Basic Authentication. 
    
    - On success a JSON object is returned with the following three fields:
        1. `token` set to the authentication token for the user
        2. `duration` set to the (approximate) number of seconds the token is valid
        3. `id` set to the id stored in the database for the user
     
    - On failure status code 401 (unauthorized) is returned.

- GET **/list...**
    - The following functionalities will be performed after the user gets authenticated:
        - Three basic APIs that exposes what is stored in MongoDB.three basic APIs:
            - "http://<host:port>/listAll" should return all open and close times in the database
            - "http://<host:port>/listOpenOnly" should return open times only
            - "http://<host:port>/listCloseOnly" should return close times only
        
        - Two different representations: one in csv and one in json. For the above, JSON is the default representation for the above three basic APIs. 
            - "http://<host:port>/listAll/csv" should return all open and close times in CSV format
            - "http://<host:port>/listOpenOnly/csv" should return open times only in CSV format
            - "http://<host:port>/listCloseOnly/csv" should return close times only in CSV format
        
            - "http://<host:port>/listAll/json" should return all open and close times in JSON format
            - "http://<host:port>/listOpenOnly/json" should return open times only in JSON format
            - "http://<host:port>/listCloseOnly/json" should return close times only in JSON format
        
        - A query parameter getting top "k" open and close times. For examples, see below.
        
            - "http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format 
            - "http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format
            - "http://<host:port>/listCloseOnly/csv?top=6" should return top 5 close times only (in ascending order) in CSV format
            - "http://<host:port>/listCloseOnly/json?top=4" should return top 4 close times only (in ascending order) in JSON format
        
        `Note: Change the values for host and port according to your machine 
        (check docker-compose.yml file for more detials - port is set to 7227, which is editable.), and use the web browser to check the results.`

### website 

![website_before_login](https://user-images.githubusercontent.com/87594239/127569902-9de6b5b0-ac5d-4602-90c9-994c5acfe125.png)

This is a consumer program to use the services that the user expose. The services are described above in the api.

![website_service](https://user-images.githubusercontent.com/87594239/127569920-66e9fd58-e1dd-46bf-b6ee-a6a91dfc04d8.png)

This is a frontend/UI for Brevet app using Flask-WTF and Flask-Login. 
The frontend/UI should use the authentication, which is created on api. 
In addition to creating UI for basic authentication and token generation, the following three additional functionalities 
will be added in the UI: 
1. registration

    ![website_register](https://user-images.githubusercontent.com/87594239/127569948-b4e7b4a8-f1ba-4bcc-ae80-469323154946.png)

2. sign in & remember me (possible after registration.)

    ![website_sign_in](https://user-images.githubusercontent.com/87594239/127569960-21228e5b-b9e6-410f-9a2a-355bd260377d.png)

3. logout (possible after signing in.)

    ![website_after_login](https://user-images.githubusercontent.com/87594239/127569989-aa9f772f-9fc9-41a7-987b-ec7b923c8507.png)

#### How to test it?

In the web browser, search the following url:

    http://<host>:<port>/
    
Then, explore the tabs on the page!

`Note: Change the values for host and port according to your machine (check docker-compose.yml file for more details - port is set to 7327, which is editable.)`

## Credits

Michal Young, Ram Durairajan, Steven Walton, Joe Istas, Ali Hassani.
