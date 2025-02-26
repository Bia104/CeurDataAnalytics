# Tableau BI for ceur_ws
You can either: 
1. [Open pre-build ceur_ws dashboard in Tableau Desktop](#1-open-pre-build-ceur_ws-dashboard-in-tableau-desktop)
2. [Run your own Tableau queries on the ceur_ws data](#2-run-your-own-tableau-queries-on-the-ceur_ws-data)

## 1 Open pre-build ceur_ws dashboard in Tableau Desktop

### 1. Clone repository 
- Clone this repository "https://github.com/AronOehrli/TBDM-CEUR-WS.git"

### 2. Launch Tableau Desktop
- Open the Tableau Desktop application on your computer, if not alread running.

### 3. Open the Workbook File

#### Option 1: From the Start Page
1. On the Tableau start page, click on `Open` under the `Connect` pane.
2. Navigate to the location where you cloned the repository.
3. Select the `.twb` file and click `Open`. (`ceur_ws_bi_dashboard_tableau.twb`)

#### Option 2: Using the File Menu
1. Go to `File` in the top menu.
2. Select `Open...`.
3. Navigate to the location where you cloned the repository.
4. Select the `.twb` file and click `Open`. (`ceur_ws_bi_dashboard_tableau.twb`)

### 4. Extract Data if Needed (optional)
- If you are opening a `.twbx` file that contains extracted data, Tableau will prompt you to extract the data (.hyper file). Follow the prompts to extract the data to a local location if needed.
- The .hyper files are located in `/tableau-bi/prep_data_collections`

By following these steps, you can open and start working with our Tableau workbook.

---

## 2 Run your own Tableau queries on the ceur_ws data

### Prerequisites
1. **Tableau Desktop**: Ensure you have Tableau Desktop installed on your machine.
   - You can download Tableau Desktop from the [Tableau Desktop](https://www.tableau.com/products/desktop).

2. **Tableau Prep Builder (optional)**: Ensure you have Tableau Prep Builder installed on your machine.
   - You can download Tableau Desktop from the [Tableau Prep Builder: Dowload](https://www.tableau.com/products/prep/download).
   - The Tableau Prep Builder is only required if you want to structure, transform and clean the ceur_ws data before using in Tableau Desktop. This is needed to represent nested data (arrays) in Tableau visualizations and to extract certain data like paper pages or publication details such as the publication city.
   
2. **MongoDB Atlas Account**: You need an active MongoDB Atlas account and a running cluster.
   - Sign up for a MongoDB Atlas account [here](https://www.mongodb.com/cloud/atlas).
   - A cluster with the collections of ceur_ws is already existing. Contact the contributors of this repository for access.

3. **MongoDB Atlas Cluster Access**:
   - Make sure you have the correct permissions to access the MongoDB Atlas cluster. Ask the contributors for access and password
   - Ensure your IP address is whitelisted in MongoDB Atlas to allow connections from your machine.

4. **Java Runtime Environment (JRE)**: The MongoDB JDBC driver requires Java.
   - Ensure you have JRE 8 or later installed. You can download it from [Oracle's website](https://www.oracle.com/java/technologies/javase-downloads.html) or use OpenJDK.

5. **Network Configuration**: Ensure that your network allows outbound connections to MongoDB Atlas (typically port 27017), usually, VPNs do not work.


### Installation - MongoDB Atlas Tableau Connector

#### Step 1: Download MongoDB JDBC Driver
1. **Download the driver from**: [MongoDB JDBC 2.1.2](https://repo1.maven.org/maven2/org/mongodb/mongodb-jdbc/2.1.2/) (all.jar file)
2. **Save the driver in the following folder (create the folder if it doesn't exist)**:
   - **Windows**: `C:\Program Files\Tableau\Drivers`
   - **macOS**: `~/Library/Tableau/Drivers`

#### Step 2: Download Custom Tableau Connector (TACO file)
1. **Download the TACO file from one of the following links**: [MongoDB JDBC TACO 1.2.0](https://translators-connectors-releases.s3.amazonaws.com/mongo-tableau-connector/mongodb-jdbc-1.2.0.taco)
2. **Save the TACO file in the following folder (create the folder if it doesn't exist)**:
   - **Windows**: `C:\Program Files\Tableau\Connectors`
   - **macOS**: `~/Library/Tableau/Connectors`

#### Step 3: Establish a New Server Connection in Tableau Desktop
1. **Open Tableau Desktop**
2. **Go to** `Connect` and choose `Server`
3. **Select** `MongoDB Atlas by MongoDB` (this driver has been installed in step 1 & 2)
4. **Provide the credentials of your server as requested**:
   - **URL**: `mongodb://atlas-sql-6627b8c2756cdc360b8fef3e-rpb1k.a.query.mongodb.net/ceur_ws?ssl=true&authSource=admin`
   - **DB**: `ceur_ws`
   - **Username**: `admin`
   - **Password**: `on request`

5. **Alternatively, search for the connection details**:
   - **Go to our MongoDB**: [MongoDB Atlas](https://cloud.mongodb.com/v2/6627b85d3306e4391ba7a287#/overview)
   - **Under** `Connect`, choose `Atlas SQL`
   - **Select** `Tableau Connector` and the correct Collection `ceur_ws`

6. **Check connection**
   - **Now you should see the collections/tables of the ceur_ws database in your Tableau data source section** 
   - **On the top right corner select** `Extract` from the `Connection` selection. This enables queries on your local machine rather live queries on the MongoDB.

### Explore the raw data in Tableau Desktop
1. **Join the tables (papers & volumes) in the data source section.** Use the `_id` in the volume collection and `volume_id` in the papers collection to join the tables/collections.
2. **Create visualisations in Tableau**

### Establish a New Server Connection in Tableau Prep Builder (optional)
1. **Onyl needed if you intend to prepare the data as described in prerequisits 2.**
2. **Follow the same steps as for Tableau Desktop new server connection.** The driver and connector are already installed. It is only needed to set up the conneciton to our MongoDB in Tablea Prep Builder (Step 3).
3. **Once connected you can prepare the ceur_ws data as needed in Tableau Desktop.**
4. **An example of a data schema can be seen and used** `/tableau-bi/tableau_prep_builder_schema/ceur_ws_bi_tableau_prep_240617.tfl`


## Full Tableau Connector Installation Guides
- [MongoDB and Tableau Compatibility](https://www.mongodb.com/resources/products/compatibilities/mongodb-tableau?jmp=tbl)
- [Tableau Help - MongoDB](https://help.tableau.com/current/pro/desktop/en-us/examples_mongodb.htm)
- [MongoDB Atlas Data Federation with Tableau](https://www.mongodb.com/docs/atlas/data-federation/query/sql/tableau/connect/)
- [MongoDB Tableau Connector Download](https://www.mongodb.com/try/download/tableau-connector)

---
