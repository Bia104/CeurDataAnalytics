# LLM Vector Search Application
This is a simple Flask-based search application where users can input a search term. The application vectorizes the input and uses it to query MongoDB Vector Search. The results are processed using the Gemini Model to generate LLM output. The frontend is styled with Bootstrap and the backend provides an API endpoint that handles the LLM Vector Search logic. The app can be deployed on Google Cloud Run.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [URL endpoints](#url-endpoints)
6. [Deplyoment](#deployment)

## Requirements
- Python 3.8+
- Google Cloud CLI (if you want to deploy the application to Google Cloud)
- Required Python packages (listed in `requirements.txt`)

## Installation

Clone the repository:
```sh
git clone https://github.com/AronOehrli/TBDM-CEUR-WS.git
cd search-app
```

Create a virtual environment:

```sh
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install the dependencies:

```sh
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the `search-app` directory and add the following environment variables:

```env
GOOGLE_API_KEY = "12345679" # Replace with the actual API Key
DATABASE_URL = "mongodb://localhost:27017/" # Replace with the actual URI
DB_NAME = "ceur_ws"
```

## Running the Application

Start the application:

```sh
python main.py
```

Open your browser:

```sh
Go to `http://127.0.0.1:8080/.`
```

## URL Endpoints

### GET /
- **Description:** Renders the search page.
- **Response:** HTML page with the search form.

### GET /search
- **Description:** Handles the search query and LLM vector search logic.
- **Query Parameters:**
  - q (string): The search query.
- **Response:** JSON object with a single result.

```json
{
  "result": "Result for query 'What is the CERIA framework?': The CERIA framework is a framework for proactively identifying supply chain risks. It       analyzes causal relationships between events that lead to supply chain risks. The CERIA framework is discussed in the document \"Empowering Supply Chains Resilience: LLMs-Powered BN for Proactive Supply Chain Risk Identification.pdf\".  ('filename': 'Empowering Supply Chains Resilience: LLMs-Powered BN for Proactive Supply Chain Risk Identification.pdf', 'page_number': 3) \n"
}
```

## Deployment

It is possible to deploy the application in multiple ways. Google Cloud offers its Cloud Run service, which provides a straightforward deployment method. You can follow the tutorial [here](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service) to learn how to deploy a Python application to Google Cloud Run.

If everything is set up as described in the documentation, you can simply run the following command to deploy the application:

```sh
gcloud run deploy
```

Follow the URL provided by the command to access your deployed application, for example: `https://search-app-22z5qauyca-uc.a.run.app/`.