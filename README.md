# Order and Inventory Management Microservice Application

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [WebSocket Notifications](#websocket-notifications)

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

The application is divided into several services:

1. **User Service**: Handles user authentication and profile management.
2. **Book Service**: Handles book upload, management, and summarization.
3. **Order Service**: Manages order creation, updates, and notifications.
4. **Inventory Service**: Keeps track of stock levels and updates inventory based on orders.
5. **Notification Service**: Sends real-time notifications to users when order statuses change.

Inter-service communication is facilitated using RabbitMQ.

## Tech Stack

- **Flask**: Web framework for building the RESTful API.
- **Flask-SocketIO**: For real-time WebSocket communications.
- **SQLAlchemy**: ORM for database interactions.
- **RabbitMQ**: Message broker for inter-service communication.
- **Firebase**: Python wrapper for Firebase for file storage.
- **PostgreSQL**: Database for local development.
- **Docker**: Containerization of services.

## Setup and Installation

### Prerequisites

- Python 3.8+
- Docker
- RabbitMQ
- Firebase account (for file storage)

### Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/your-username/Online-Bookstore-API.git
    cd Online-Bookstore-API
    ```

2. **Set up virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```sh
    pip install -r requirements.txt
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
        const socket = io('http://localhost:5002');

        socket.on('connect', () => {
            console.log('Connected to WebSocket server');
        });

        socket.on('order_status_change', (data) => {
            const notificationList = document.getElementById('notifications');
            const notificationItem = document.createElement('li');
            notificationItem.textContent = `Order ID: ${data.order_id}, Status: ${data.status}`;
            notificationList.appendChild(notificationItem);
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from WebSocket server');
        });
    </script>
</body>
</html> 
