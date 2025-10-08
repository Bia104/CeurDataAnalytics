# CeurDataAnalytics

This project is part of the "Technology for Big Data Management" course. 
It aimed to develop a method to analyze the website of [CEUR-WS website](https://ceur-ws.org/).

Our objective was to extract data from the website, store it in a database, and make a graph out of it
so that there can be queries and analysis made on the data to display commonly searched information in a timely manner.

---

## Prerequisites

Before running the script, ensure you have the following installed:
- Python 3.8 or higher
- MongoDB (e.g. MongoDB Atlas)
- Memgraph (for graph database)
- Required Python packages (listed in `requirements.txt`)

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Bia104/CeurDataAnalytics.git
    cd CeurDataAnalytics

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```


## Configuration

Create a `.env` file in the `web-scraper` directory and add the following environment variables:

```env
BASE_URL = "https://ceur-ws.org/"
MONGO_URI = "mongodb://localhost:27017/" # Replace with the actual URI
DB_NAME = "ceur_ws"
```

Create the MongoDB database with the name `ceur_ws` (or the name you specified in the `.env` file).

## Running the Script

To run the script, execute the following command:

```sh
python main.py
```

Logs can be analyzed and found in `scraping.log`.
This will populate the MongoDB database with the scraped data.

Subsequently, you can run the two Jupyter notebooks:
- `etl/clear_dataset.ipynb`: Cleans the dataset and prepares it for graph construction.
- `etl/create_nodes.ipynb`: Constructs the graph in Memgraph from the cleaned dataset.

## Components

To develop this project, we used and upgraded an already existing [web scraper]() 
that was made in Python.

The other unique additions are the following:

1. **Parser**  
    Along with the web scraper, a parser was developed to extract structured data from the PDF's content.
    This parser extracts information such as the title, authors, keywords, references and abstract of each paper.

2. **Graph Construction**  
    A **Memgraph** graph database is constructed from the MongoDB data to enable complex queries and analysis.

    This enables queries such as:
```cypher
MATCH (a:Author)-[:WROTE]->(p:Paper)-[:IN_VOLUME]->(v:Volume)
RETURN a.name, p.title, v.title;
