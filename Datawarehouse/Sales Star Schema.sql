--Staging Layer Table
CREATE TABLE Project.Staging_layer(
	Row_ID INT IDENTITY(1,1) PRIMARY KEY,
	Customer_ID VARCHAR(200),
	Name VARCHAR(200),
	Email VARCHAR(200),
	Address VARCHAR(200),
	Age INT,
	Phone_number VARCHAR(200),
	Order_ID VARCHAR(200),
	Order_Date Date,
	Product_ID VARCHAR(200),
	Product VARCHAR(200),
	Segment VARCHAR(200),
	Segment_ID VARCHAR(200),
	Status VARCHAR(200),
	Status_ID VARCHAR(200),
	Price INT,
	Profit INT,
	Quantity INT,
	Branch_ID VARCHAR(200),
	Store_Branch VARCHAR(200),
	Country VARCHAR(200)
);
SELECT * FROM Project.Staging_layer;

--Dimension Customer
CREATE TABLE Project.Dim_Customer(
	CustomerKey INT IDENTITY(1,1) PRIMARY KEY,
	Customer_ID VARCHAR(200),
	Name VARCHAR(200),
	Email VARCHAR(200),
	Address VARCHAR(200),
	Age INT,
	Phone_number VARCHAR(200)
);
SELECT * FROM Project.Dim_Customer;

--Dimension Product
CREATE TABLE Project.Dim_Product(
	ProductKey INT IDENTITY(1,1) PRIMARY KEY,
	Product_ID VARCHAR(200),
	Product VARCHAR(200),
);
SELECT * FROM Project.Dim_Product;

--Dimension Segment
CREATE TABLE Project.Dim_Segment(
	SegmentKey INT IDENTITY(1,1) PRIMARY KEY,
	Segment_ID VARCHAR(200),
	Segment VARCHAR(200)
);
SELECT * FROM Project.Dim_Segment;

--Dimension Status
CREATE TABLE Project.Dim_Status(
	StatusKey INT IDENTITY(1,1) PRIMARY KEY,
	Status_ID VARCHAR(200),
	Status VARCHAR(200)
);
SELECT * FROM Project.Dim_Status

--Dimension Region
CREATE TABLE Project.Dim_Region(
	BranchKey INT IDENTITY(1,1) PRIMARY KEY,
	Branch_ID VARCHAR(200),
	Store_Branch VARCHAR(200),
	Country VARCHAR(200)
);

SELECT * FROM Project.Dim_Region;

-- Dimension Order Date
CREATE TABLE Project.Dim_OrderDate (
    OrderDateKey INT PRIMARY KEY,          -- YYYYMMDD
    FullDate DATE,
    Day INT,
    Month INT,
    MonthName VARCHAR(20),
    Quarter INT,
    Year INT,
);

SELECT * FROM Project.Dim_OrderDate;


-- Fact Order Table
CREATE TABLE Project.FactOrders (
    OrderKey INT IDENTITY(1,1) PRIMARY KEY,
    CustomerKey INT NOT NULL,
    ProductKey INT NOT NULL,
	SegmentKey INT NOT NULL,
	StatusKey INT NOT NULL,
	BranchKey INT NOT NULL,
    OrderDateKey INT NOT NULL,
    Quantity INT,
	Profit INT,
    Price INT,
    FOREIGN KEY (CustomerKey) REFERENCES Project.Dim_Customer(CustomerKey),
    FOREIGN KEY (ProductKey) REFERENCES Project.Dim_Product(ProductKey),
	FOREIGN KEY (SegmentKey) REFERENCES Project.Dim_Segment(SegmentKey),
	FOREIGN KEY (StatusKey) REFERENCES Project.Dim_Status(Statuskey),
	FOREIGN KEY (BranchKey) REFERENCES Project.Dim_Region(BranchKey),
    FOREIGN KEY (OrderDateKey) REFERENCES Project.Dim_OrderDate(OrderDateKey),
);

SELECT * FROM Project.FactOrders;





