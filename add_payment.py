import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import date

# Load environment variables
load_dotenv()

# Get Supabase details
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")

# Connect to Supabase
supabase = create_client(url, key)

# Payment details
worker_name = input("Enter worker name: ")
amount = float(input("Enter amount: "))
description = input("Enter description (optional): ")

# Today's date
payment_date = date.today().isoformat()

# Insert payment into Supabase
data = {
    "worker_name": worker_name,
    "amount": amount,
    "payments_date": payment_date,
    "description": description
}

response = supabase.table("payments").insert(data).execute()

print("\n✅ Payment saved successfully!")
print("Worker:", worker_name)
print("Amount: ₹", amount)
print("Date:", payment_date)