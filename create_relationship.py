"""
Description:
 Creates the relationships table in the Social Network database
 and populates it with 100 fake relationships.

Usage:
 python create_relationships.py
"""
from random import randint, choice
from faker import Faker
import os
import sqlite3


# Determine the path of the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'social_network.db')

def main():
    create_relationships_table()
    populate_relationships_table()

def create_relationships_table():
    """Creates the relationships table in the DB"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # SQL query that creates a table named 'relationships'.
    create_relationships_tbl_query = """
    CREATE TABLE IF NOT EXISTS relationships
    (
    id INTEGER PRIMARY KEY,
    member1_id INTEGER NOT NULL,
    member2_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    start_date DATE NOT NULL,
    FOREIGN KEY (member1_id) REFERENCES people (id),
    FOREIGN KEY (member2_id) REFERENCES people (id)
    );
    """
    # Execute the SQL query to create the 'relationships' table.
    cur.execute(create_relationships_tbl_query)
    con.commit()
    con.close()

def populate_relationships_table():
    """Adds 100 random relationships to the DB"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    # Hint: See example code in lab instructions entitled "Populate the Relationships Table"
    add_relationship_query = """
    INSERT INTO relationships
    (
    member1_id,
    member2_id,
    type,
    start_date
    )
    VALUES (?, ?, ?, ?);
    """

    fake = Faker()

    for _ in range(100):
        member1_id = randint(1, 200)
        member2_id = randint(1, 200)
        while member2_id == member1_id:
            member2_id = randint(1, 200)

        rel_type = choice(('friend', 'spouse', 'partner', 'relative'))
        start_date = fake.date_between(start_date='-50y', end_date='today')
        new_relationship = (member1_id, member2_id, rel_type, start_date)

        cur.execute(add_relationship_query, new_relationship)
    con.commit()
    con.close()

if __name__ == '__main__':
    main()
