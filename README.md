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
- **Logging**: Python's logging framework for handling error logs.

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

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
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

6. **Start RabbitMQ**:

    ```sh
    docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
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
