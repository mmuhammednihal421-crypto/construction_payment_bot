import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Get Supabase details
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SECRET_KEY")

# Check that values exist
if not url or not key:
    print("❌ Supabase details are missing.")
    exit()

# Connect to Supabase
supabase = create_client(url, key)

print("✅ Supabase connected successfully!")