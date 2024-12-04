# Sample Web Scraper

## Overview
A Simple Web scraper built using FastAPI. It scrapes product data from a specified website and stores it in a Redis cache along with JSON dump of the data. The application includes middleware for authentication and is structured to allow easy extension and modification.

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Clone the Repository
First, clone the repository to your local machine:


### 2. Create a Virtual Environment
It's recommended to create a virtual environment to manage dependencies:

# For macOS/Linux
```
# For macOS/Linux
python3 -m venv venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment using the following command:

```bash
# For macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies
Once the virtual environment is activated, install the required dependencies:

```bash
pip install -r requirements.txt
```

### 5. Create a `.env` File
Create a `.env` file in the root directory of the project to store your environment variables. This file should include the following variables:

```plaintext
STATIC_TOKEN=<your_static_token what ever you want>
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
SCRAPER_RETRIES=3
SCRAPER_RETRIES_TIME=10
```

- Replace `<your_static_token>` with a secure token for authentication.
- Adjust the Redis configuration as necessary for your setup.

### 6. Run the Application
You can run the FastAPI application using Uvicorn. Make sure your Redis server is running, then execute the following command:

```bash
uvicorn app.main:app --reload
```

### 7. Access the API
Once the application is running, you can access the API at 
```
http://127.0.0.1:8000/api/scrape
```
or you can do postman request to the same endpoint with `x-auth-token` header as `STATIC_TOKEN`