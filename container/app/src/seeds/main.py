import sys
import traceback
from app.core.environment import DB_HOST, DB_USER, DB_PASS, DB_NAME
from seeds.seed import seed_data

DB_URL: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

if __name__ == "__main__":
    try:
        print("Starts seeding data.")
        seed_data.seed(url=DB_URL)
        print("Data seeding is complete.")
    except Exception as e:
        print("Data seeding failed.")
        print(str(e), file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
