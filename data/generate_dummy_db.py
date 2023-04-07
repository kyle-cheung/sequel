import sqlite3
import random
import string
import faker
from datetime import datetime, timedelta

fake = faker.Faker()
# Connect to database and create tables
conn = sqlite3.connect('../backend/bi_tool.db')
c = conn.cursor()

# Create customers table
c.execute('''CREATE TABLE IF NOT EXISTS customers
             (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT)''')

# Create sales table
c.execute('''CREATE TABLE IF NOT EXISTS sales
             (id INTEGER PRIMARY KEY, customer_id INTEGER, bike TEXT, sale_date DATE, price INTEGER, sales_person_id INTEGER)''')

# Create sales person table
c.execute('''CREATE TABLE IF NOT EXISTS sales_person
                (id INTEGER PRIMARY KEY, name TEXT)''')

# Generate and insert dummy customer data
for i in range(100):
    # Generate random real names using Faker
    first_name = fake.first_name()
    name = f'{first_name} {fake.last_name()}'
    email = f'{first_name.lower()}@example.com'
    phone = f'+1{random.randint(100, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}'
    c.execute(f"INSERT INTO customers VALUES ({i+1}, '{name}', '{email}', '{phone}')")
    
    bike = random.choice(['Road Bike', 'Mountain Bike', 'Hybrid Bike', 'Electric Bike'])
    sale_date = datetime.now() - timedelta(days=random.randint(1, 365))
    price = random.randint(100, 5000)
    customer_id = random.randint(1,100)
    sales_person = random.randint(1,12)
    c.execute(f"INSERT INTO sales VALUES ({i+1}, {customer_id}, '{bike}', '{sale_date.date()}', {price}, {sales_person})")

for i in range(12):
    # Generate random real names using Faker
    first_name = fake.first_name()
    name = f'{first_name} {fake.last_name()}'
    c.execute(f"INSERT INTO sales_person VALUES ({i+1}, '{name}')")

# Commit changes and close connection
conn.commit()
conn.close()
