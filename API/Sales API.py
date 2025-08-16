from faker import Faker
from fastapi import FastAPI
import random
import uvicorn
import nest_asyncio
import asyncio
import datetime

#Apply nest_asyncio to make event loop compatible with Jupyter Notebook
nest_asyncio.apply()

#Create Instances
app = FastAPI()
fake = Faker()

#In_memory data store
data_cache = []

#For Product Name and Product Code
Product_ID = {
    'ballpen': 'P001',
    'paper': 'P002',
    'notepad': 'P003',
    'notebook': 'P004',
    'pencil': 'P005',
    'folder': 'P006',
    'envelope': 'P007'
}

#For the Segment and Segment Code
Segment_ID = {
    'Office Supply': 'S001',
    'School Supply': 'S002'
}

#For Branch and Branch Code
Branch_ID = {
    'Caloocan City': 'MM01',
    'Las Piñas City': 'MM02',
    'Makati City': 'MM03',
    'Malabon City': 'MM04',
    'Mandaluyong City': 'MM05',
    'Manila City': 'MM06',
    'Marikina City': 'MM07',
    'Muntinlupa City': 'MM08',
    'Navotas City': 'MM09',
    'Parañaque City': 'MM10',
    'Pasay City': 'MM11',
    'Pasig City': 'MM12',
    'Quezon City': 'MM13',
    'San Juan City': 'MM14',
    'Taguig City': 'MM15',
    'Valenzuala': 'MM16',
    'Pateros': 'MM17'
}

#Function to generate random Order date between 2020 and 2024
def random_date(start_year=2020, end_year=2024):
    start_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, 12, 31)
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + datetime.timedelta(days=random_days)

#For Status Update
Status_ID = {
    'Delivered': 'ST01',
    'Ongoing': 'ST02',
    'Returned': 'ST03'
}


#Create the generated data
def generate_data(count: int = 9900):
    return [
         {
            'Customer_ID': fake.uuid4(),
            'Name': fake.name(),
            'Email': fake.email(),
            'Address': fake.address(),
            'Age': random.randint(20,50),
            'Phone_number': fake.basic_phone_number(),
            'Order_ID': fake.uuid4(),
            'Order_Date': random_date(),
            'Product': (prod := random.choice(list(Product_ID.keys()))),
            'Product_ID': Product_ID[prod],
            'Segment': (prod := random.choice(list(Segment_ID.keys()))),
            'Segment_ID': Segment_ID[prod],
            'Status': (prod := random.choice(list(Status_ID.keys()))),
            'Status_ID': Status_ID[prod],
            'Price': round(random.uniform(20,150),2),
            'Profit': round(random.uniform(10,50),2),
            'Quantity': random.randint(1,20),
            'Store_Branch': (prod := random.choice(list(Branch_ID.keys()))),
            'Branch_ID': Branch_ID[prod],
            'Country': 'Philippines'
        }
        for i in range(count)
    ]

#Create API
@app.get("/users")
def get_users():
    return data_cache

#Manual scheduler loop
async def scheduler():
    global data_cache
    while True:
        data_cache[:] = generate_data()
        print('Refreshed in notebook')
        await asyncio.sleep(60)

loop = asyncio.get_event_loop()
loop.create_task(scheduler())  # scheduler runs in background

#for API server
uvicorn.run(app, host="127.0.0.1", port=8000)

