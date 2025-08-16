
# 🗄️ ETL Data Pipeline Project with Mock API, SQL Data Warehouse & Power BI

## 📌 Project Overview

This project demonstrates a full **ETL (Extract, Transform, Load) pipeline** built from scratch using Python, SQL Server (T-SQL), and Power BI for visualization.

The goal is to simulate a real-world data engineering project by:

* Generating mock sales data using a **FastAPI-based Mock API**
* Building an **ETL pipeline in Python** to extract data from the API, transform it, and load it into a **SQL Server data warehouse**
* Creating a **star schema data model** with dimensions and fact tables
* Visualizing insights using **Power BI dashboards**

---

## ⚙️ Tech Stack

* **Python**: Data extraction (API requests), transformation (Pandas), and loading (SQLAlchemy, PyODBC)
* **FastAPI**: Mock API for sales order data
* **SQL Server (T-SQL)**: Data warehouse design (staging, dimensions, facts)
* **Power BI**: Business intelligence and visualization

---

## 🛠️ Project Workflow

1. **Mock API (FastAPI + Faker)**

   * Generates synthetic sales transactions (Customers, Products, Segments, Status, Store Branches, etc.)
   * Refreshes data every 60 seconds to simulate real-time orders

2. **ETL Pipeline (Python)**

   * **Extract**: Calls the Mock API using `requests`
   * **Transform**: Cleans and structures data using `pandas`
   * **Load**: Inserts data into a SQL Server staging layer, then populates dimension and fact tables

3. **Data Warehouse (SQL Server)**

   * **Staging Layer**: Raw data ingestion
   * **Star Schema**: Dimensions (`Customer`, `Product`, `Segment`, `Status`, `Region`, `Date`) and Fact table (`Orders`)

4. **Visualization (Power BI)**

   * Connects to SQL Server fact & dimension tables
   * Provides dashboards for sales performance, profit analysis, segment trends, and regional distribution

---

## 📊 Data Model (Star Schema)

* **FactOrders** → Measures: Quantity, Price, Profit
* **Dimensions**:

  * `Dim_Customer` (Customer details)
  * `Dim_Product` (Products)
  * `Dim_Segment` (Business Segment)
  * `Dim_Status` (Order Status)
  * `Dim_Region` (Store Branch & Country)
  * `Dim_OrderDate` (Date dimension for time analysis)

---

## 🚀 How to Run the Project

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Run the Mock API**

   ```bash
   python mock_api.py
   ```

   * API will run on `http://127.0.0.1:8000/users`

3. **Run the ETL Pipeline**

   * Configure your SQL Server connection in `etl_pipeline.py`
   * Run the script to load data into SQL Server

   ```bash
   python etl_pipeline.py
   ```

4. **Open Power BI Dashboard**

   * Connect to your SQL Server database
   * Load the fact and dimension tables
   * Use the provided `.pbix` file to view visualizations


---

## 📂 Repository Structure

```
📦 your-repo-name
 ┣ 📜 mock_api.py          # FastAPI mock data generator
 ┣ 📜 etl_pipeline.py      # ETL pipeline script
 ┣ 📜 warehouse_schema.sql # SQL Server DDL for staging, dimensions, and fact
 ┣ 📜 sales_dashboard.pbix # Power BI dashboard
 ┣ 📜 README.md            # Project documentation
```

---

## 🔑 Key Learnings

* Building a complete **ETL pipeline** using Python and SQL Server
* Designing a **data warehouse schema** (Star Schema)
* Automating data refresh and integration with BI tools
* Hands-on experience with **end-to-end data engineering workflow**

---

## 📬 Contact

👤 **Your Name**

* 📧 Email: [jj.tang34@gmail.com](mailto:your-email@example.com)
* 💼 LinkedIn: [linkedin.com/in/john-justin-tang](https://linkedin.com/in/your-profile)



