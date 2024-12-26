import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    "tenant_a": os.getenv("TENANT_A_DB_URL"),
    "tenant_b": os.getenv("TENANT_B_DB_URL"),
}

# Add more configuration settings as needed