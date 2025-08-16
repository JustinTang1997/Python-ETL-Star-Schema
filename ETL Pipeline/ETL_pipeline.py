#import modules
import pandas as pd
import requests
import sqlalchemy as sa
from sqlalchemy import text

#Extract API
url = 'http://127.0.0.1:8000/users'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data[:1])
else:
    print('Error',response.status_code)  

#Transform data
df = pd.json_normalize(data)
df.head()

#Load to Staging Layer
Driver = 'ODBC Driver 17 for SQL Server'
Server = 'Server_name'
Database = 'Database_name'

#Connection string using Windows Authentication
connection_string = f"mssql+pyodbc://@{Server}/{Database}?driver={Driver}&trusted_connection=yes"
print(f'Connected successfulty to: {Database}')

#Create Engine
engine = sa.create_engine(connection_string)

#Connect to Staging Layer
df.to_sql('Staging_layer', schema='Project', con=engine, if_exists='append', index=False)
print('Data inserted into staging table')

#Insert Data to Dimension Customer
insert_dim_customer_sql = """
INSERT INTO Project.Dim_Customer (Customer_ID, Name, Email, Address, Age, Phone_number)
SELECT DISTINCT
    S.Customer_ID,
    S.Name,
    S.Email,
    S.Address,
    S.Age,
    S.Phone_number
FROM Project.Staging_layer AS S
WHERE NOT EXISTS (
    SELECT 1 
    FROM Project.Dim_Customer AS C
    WHERE C.Customer_ID = S.Customer_ID
);
"""
with engine.begin() as conn:
    conn.execute(text(insert_dim_customer_sql))

print("Data inserted to Dimension Customer")

#Insert Data to Dimension Product
insert_dim_product_sql = """
INSERT INTO Project.Dim_Product (Product_ID, Product)
SELECT DISTINCT
    S.Product_ID,
    S.Product
FROM Project.Staging_layer AS S
WHERE NOT EXISTS (
    SELECT 1 
    FROM Project.Dim_Product as P
    WHERE P.Product_ID = S.Product_ID
);
"""
with engine.begin() as conn:
    conn.execute(text(insert_dim_product_sql))

print("Data inserted into Dimension Product")

#Insert Data to Dimension Region
insert_dim_region_sql = """
INSERT INTO Project.Dim_Region (Branch_ID, Store_Branch, Country)
SELECT DISTINCT
    S.Branch_ID,
    S.Store_Branch,
    S.Country
FROM Project.Staging_layer AS S
WHERE NOT EXISTS (
    SELECT 1 
    FROM Project.Dim_Region as R
    WHERE R.Branch_ID = S.Branch_ID
);
"""
with engine.begin() as conn:
    conn.execute(text(insert_dim_region_sql))

print('Data inserted to Dimension Region')

#Insert Data to Dimension Segment
insert_dim_segment_sql = """
INSERT INTO Project.Dim_Segment (Segment_ID, Segment)
SELECT DISTINCT
    S.Segment_ID,
    S.Segment
FROM Project.Staging_layer AS S
WHERE NOT EXISTS (
    SELECT 1
    FROM Project.Dim_Segment AS SE
    WHERE SE.Segment_ID = S.Segment_ID
);
"""
with engine.begin() as conn:
    conn.execute(text(insert_dim_segment_sql))

print('Data inserted to Dimension Segment')

#Insert Data to Dimension Status
insert_dim_status_sql = """
INSERT INTO Project.Dim_Status (Status_ID, Status)
SELECT DISTINCT 
    S.Status_ID,
    S.Status
FROM Project.Staging_layer AS S
WHERE NOT EXISTS (
    SELECT 1
    FROM Project.Dim_Status AS ST
    WHERE ST.Status_ID = S.Status_ID
);
"""

with engine.begin() as conn:
    conn.execute(text(insert_dim_status_sql))

print('Data inserted to Dimension Status')

#Insert Data to Dimension Date
insert_dim_date_sql = """
INSERT INTO Project.Dim_OrderDate (OrderDateKey, FullDate, Day, Month, MonthName, Quarter, Year)
SELECT DISTINCT
    CONVERT(INT, FORMAT(S.Order_Date, 'yyyyMMdd')) AS OrderDateKey,
    S.Order_Date AS FullDate,
    DAY(S.Order_Date) AS Day,
    MONTH(S.Order_Date) AS Month,
    DATENAME(MONTH, S.Order_Date) AS MonthName,
    DATEPART(QUARTER, S.Order_Date) AS Quarter,
    YEAR(S.Order_Date) AS Year
FROM Project.Staging_layer AS S
WHERE NOT EXISTS (
    SELECT 1
    FROM Project.Dim_OrderDate AS D
    WHERE D.OrderDateKey = CONVERT(INT, FORMAT(S.Order_Date, 'yyyyMMdd'))
);
"""
with engine.begin() as conn:
    conn.execute(text(insert_dim_date_sql))

print('Date inserted to Dimension Date')

#Insert Data to Facts Table
insert_fact_sql = """
INSERT INTO Project.FactOrders(CustomerKey, ProductKey, SegmentKey, StatusKey, BranchKey, OrderDatekey, Quantity, Profit, Price)
SELECT DISTINCT
    C.CustomerKey,
    P.ProductKey,
    SE.SegmentKey,
    ST.StatusKey,
    R.BranchKey,
    CONVERT(INT, FORMAT(S.Order_Date, 'yyyyMMdd')) AS OrderDateKey,
    S.Quantity,
    S.Profit,
    S.Price
FROM Project.Staging_layer AS S
JOIN Project.Dim_Customer AS C
    ON S.Customer_ID = C.Customer_ID
JOIN Project.Dim_Product AS P
    ON S.Product_ID = P.Product_ID
JOIN  Project.Dim_Segment AS SE
    ON S.Segment_ID = SE.Segment_ID
JOIN Project.Dim_Status AS ST
    ON S.Status_ID = ST.Status_ID
JOIN Project.Dim_Region AS R
    ON S.Branch_ID = R.Branch_ID
WHERE NOT EXISTS(
    SELECT 1
    FROM Project.FactOrders AS F
    WHERE F.CustomerKey = C.CustomerKey
    AND F.ProductKey = P.ProductKey
    AND F.SegmentKey = SE.SegmentKey
    AND F.StatusKey = ST.StatusKey
    AND F.BranchKey = R.BranchKey
    AND F.OrderDateKey = CONVERT(INT, FORMAT(S.Order_Date, 'yyyyMMdd'))
    AND F.Quantity = S.Quantity
    AND F.Profit = S.Profit
    AND F.Price = S.Price
);
"""
with engine.begin() as conn:
    conn.execute(text(insert_fact_sql))

print('Orders inserted to Fact table')
