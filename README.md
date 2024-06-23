# Bookstore Application

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Documantation](#documentation)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [WebSocket Notifications](#websocket-notifications)
- [Design Decisions](#design-decisions)
- [AI Algorithms Used](#ai-algorithms-used)

## Introduction

An asynchronous communication system for an online bookstore using Python, Flask, Flask-restful. Additionally, OpenAI API was implemented to improve the functionality of the system. Other tools used in this project are: Docker, RabbitMQ, and WebSockets. It includes services for user management, order processing, and real-time notifications for order status changes using WebSockets.

## Features

- User authentication and authorization
- Order creation and management
- Inventory management
- Real-time notifications for order status changes
- Book uploads
- Book summary generation by OpenAI
- Microservice architecture
- RabbitMQ for inter-service communication
- WebSocket support with Flask-SocketIO

## Architecture

The application is divided into several parts:

1. **User Service**: Handles user authentication and profile management.
2. **Book Service**: Handles book upload, management, and summarization.
3. **Order Service**: Manages order creation, updates, and notifications with websockets.
4. **Inventory Service**: Keeps track of stock levels and updates inventory based on orders.

Inter-service communication between order and inventory is facilitated using RabbitMQ.

## Tech Stack

- **Flask**: Python web framework.
- **Flask-restful**: For building the RESTful API.
- **Flask-SocketIO**: For real-time WebSocket communications.
- **SQLAlchemy**: ORM for database interactions.
- **RabbitMQ**: Message broker for inter-service communication.
- **Firebase**: Python wrapper for Firebase for file storage.
- **PostgreSQL**: Database for local development.
- **Docker**: Containerization of services.
- **Error Logging**: Python's `logging` package for handling error logs.

## Documentation

Get the postman documentation for a detailed description on how to make use of the API. You can find it [here](https://documenter.getpostman.com/view/25448393/2sA3XVALMT)

## Setup and Installation

### Prerequisites

- Python 3.8+
- Docker
- RabbitMQ
- Firebase account (for file storage)

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/joboy-dev/Online-Bookstore-API.git
    cd Online-Bookstore-API
    ```

2. **Set up virtual environment**:

    ```sh
    python -m venv venv
    cd venv/Scripts/activate  # On mac, use `source venv/bin/activate`
    ```

3. **Install dependencies and set PYTHONPATH**:

    ```sh
    pip install -r requirements.txt
    set PYTHONPATH=. # on mac do export PYTHONPATH=.
    ```

4. **Setup database**

    Create a postgres database in PgAdmin4 ans set the `DATABASE_URL` in `.env` file to:
    ```sh
    DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/database_name"
    ```

5. **Run database migrations**:

    ```sh
    flask db mihrate -m "Run migrations"
    flask db upgrade
    ```

6. **Firebase connection**
    - Go go firebase console [here](https://console.firebase.google.com/) and sign up if you do not have an account.
    - Then, create a project.
    - In Project overview, click on add app amd select `web` icon.
    - Put in the app nickname and click on `Register app` and you'll be taken to the Project settings
    - Go to `Service accounts` tab.
    - Click on `Generate new private key` and a json file will download.
    - Rename the downloaded file to `serviceAccount.json` and put the file in the root directory of this project.
    - Create a file in the root directory of this project named `firebase_config.py`.
    - On the firebase console, navigate to the `General` tab, scroll down and you'll see a `firebaseDonfig` variable. Copy and paste it in the file just created.
    - Put it in this format:
        ```python
        firebase_config = {
            'apiKey': "apiKey",
            'authDomain': "authDomain",
            'projectId': "projectId",
            'storageBucket': "storageBucket",
            'messagingSenderId': "messagingSenderId",
            'appId': "appId",
            'measurementId': "measurementId",
            'serviceAccount': 'serviceAccount.json',
            'databaseURL': 'databaseURL'
        }
        ```
        All the values will be provided except for `serviceAccount` and `databaseURL`.
        Service account will be the path to the `serviceAccount.json` file.
    - To get the databaseURL, go to the sidebar in the firebase console for your project and click on `Build` and select `Realtime Database`.
    - Create the database and the URL will be provided for you. Copy and paste the URL in `databaseURL`.


7. **Start RabbitMQ**:

    ```sh
    docker pull rabbitmq
    docker run -d -p 5672:5672 -p 15672:15672 rabbitmq
    ```

## Running the Application

1. **Start the Flask application**:

    ```sh
    py app.py  # or flask run
    ```

    Or use Docker Compose to start all services:

    ```sh
    docker-compose up
    ```

## WebSocket Notifications

Real-time notifications are sent to clients when the order status changes. The WebSocket server runs on the same port as the Flask application.

### Client Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Notifications</title>
    <script src="https://cdn.socket.io/4.0.0/socket.io.min.js"></script>
</head>
<body>
    <h1>Order Notifications</h1>
    <ul id="notifications"></ul>

    <script>
        const socket = io('http://localhost:5001');

        socket.on('connect', () => {
            console.log('Connected to WebSocket server');
        });

        socket.on('order_status_change', (data) => {
            const notificationList = document.getElementById('notifications');
            const notificationItem = document.createElement('li');
            // You can filter the data coming in by checking if data.user_id is the same as the user_id stored in the localStorage or something.
            // For example, you might store the user_id in localStorage after login
            // const loggedInUserId = localStorage.getItem('user_id');
            // if (data.user_id !== loggedInUserId) return;

            notificationItem.textContent = `Order ID: ${data.order_id}, Status: ${data.status}`;
            notificationList.appendChild(notificationItem);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from WebSocket server');
        });
    </script>
</body>
</html> 
```

## Design Decisions

1. **Microservice Architecture**: The application is divided into multiple services to ensure modularity, scalability, and ease of maintenance.
2. **Asynchronous Communication**: RabbitMQ is used to facilitate communication between services, ensuring that they are loosely coupled and can scale independently.
3. **Real-time Notifications**: WebSocket is used to push real-time updates to the clients, providing instant feedback on order status changes.
4. **AI Integration**: OpenAI API is used to generate summaries for books, enhancing the user experience with intelligent features.
5. **Dockerization**: The application is containerized using Docker, allowing for consistent development and deployment environments.
6. **Security**: User authentication and role-based access control ensure that resources are protected and only accessible to authorized users.

## AI Algorithms Used

1. **OpenAI GPT-3.5**: Used for generating book summaries. This model is called via the OpenAI API, which enhances the application's functionality by providing intelligent text generation capabilities.


## Future implementations
1. The search functionality has been implmented. So in the future, AI will be added for book recommendation to users based on their searches and purchases.
2. Payment APIs like Paystack will be integrated for the seamless purchase of book items
