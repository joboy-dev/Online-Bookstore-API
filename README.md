# Online Bookstore API
An asynchronous communication system for an online bookstore using Python, Flask, Flask-restful. Additionally, OpenAI API was implemented to improve the functionality of the system. Other tools used in this project are: Docker, RabbitMQ, and WebSockets.

### RabbitMQ Setup
* Run this command in the terminsal: `docker run -d -p 5672:5672 -p 15672:15672 rabbitmq:3-management`
* After this, you should be able to connect to `http://locahost:15672` and see the RabbitMQ management console. Use the username and password `guest` to login.

See full tutorial setup (here)[https://dhruvadave5297.medium.com/demo-application-for-background-processing-with-rabbitmq-python-flask-c3402bdcf7f0]