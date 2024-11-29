from database import engine
from models import Base

def update_database_schema():
    """
    Updates the database schema to match the current models.

    This function ensures that all tables defined in `models.py` are created
    in the database. If a table already exists, it will not be recreated, 
    preventing data loss.

    Raises:
        Exception: If there is an error connecting to the database 
        or applying the schema changes.
    """
    try:
        # Create or update all tables in the database
        Base.metadata.create_all(engine)
        print("Database schema updated successfully!")
    except Exception as e:
        print(f"Error updating the database schema: {e}")

if __name__ == "__main__":
    """
    Executes the schema update when this script is run directly.

    This block invokes the `update_database_schema` function to apply
    any new changes to the database schema.
    """
    update_database_schema()
