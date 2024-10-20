import sqlite3


def _create_tables_if_not_exist(cursor):
    # Create tables if they don't exist
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS PersonalInformation (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        phone_number TEXT
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS PropertyDetails (
        id INTEGER PRIMARY KEY,
        personal_id INTEGER,
        address TEXT,
        loan_amount TEXT,
        surface TEXT,
        description TEXT,
        FOREIGN KEY (personal_id) REFERENCES PersonalInformation (id)
    )
    """
    )


def load_data(data: dict):
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("TP1_SOAP/real_estate.db")
    cursor = conn.cursor()
    _create_tables_if_not_exist(cursor=cursor)
    # Insert data into the database
    personal_info = data["personal_information"]
    property_info = data["property_details"]
    # Insert personal information
    cursor.execute(
        """
    INSERT INTO PersonalInformation (name, email, phone_number)
    VALUES (?, ?, ?)
    """,
        (
            personal_info["name"],
            personal_info["email"],
            personal_info["phone_number"],
        ),
    )
    # Get the id of the newly inserted personal information
    personal_id = cursor.lastrowid
    # Prepare property details (with a description as a string)
    description_str = ", ".join(property_info["description"])
    # Insert property details
    cursor.execute(
        """
    INSERT INTO PropertyDetails (personal_id, address, loan_amount, surface, description)
    VALUES (?, ?, ?, ?, ?)
    """,
        (
            personal_id,
            property_info.get("address", ""),
            property_info.get("loan_amount", ""),
            property_info.get("surface", ""),
            description_str,
        ),
    )
    # Commit changes and close the connection
    conn.commit()
    conn.close()
