from sqlalchemy import create_engine, text

# Replace with your SQLite database URI
engine = create_engine('sqlite:///development.db')

with engine.begin() as connection:
    # Turn off foreign key constraints
    connection.execute(text("PRAGMA foreign_keys=off;"))
    
    # Begin transaction
    connection.execute(text("BEGIN TRANSACTION;"))
    
    # Create a new table with the desired schema (adjust column types/constraints as needed)
    connection.execute(text("""
        CREATE TABLE customer_new (
            phone_number INTEGER PRIMARY KEY,
            name VARCHAR(100),
            vin VARCHAR(255)
        );
    """))
    
    # Copy data from the old table to the new table
    connection.execute(text("""
        INSERT INTO customer_new (phone_number, name, vin)
        SELECT phone_number, name, vin FROM customer;
    """))
    
    # Drop the old table
    connection.execute(text("DROP TABLE customer;"))
    
    # Rename the new table to the original table name
    connection.execute(text("ALTER TABLE customer_new RENAME TO customer;"))
    
    # Commit the transaction
    connection.execute(text("COMMIT;"))
    
    # Re-enable foreign key constraints
    connection.execute(text("PRAGMA foreign_keys=on;"))
