"""
Description:
 Generates a CSV report containing all married couples in
 the Social Network database.

Usage:
 python marriage_report.py
"""
import os
import sqlite3
import csv
from create_relationships import db_path, script_dir

def main():
    # Query DB for list of married couples
    married_couples = get_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(script_dir, 'married_couples.csv')
    save_married_couples_csv(married_couples, csv_path)

def get_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, start_date) of married couples 
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    query = """
    SELECT p1.name, p2.name, r.start_date
    FROM relationships r
    JOIN people p1 ON r.member1_id = p1.id
    JOIN people p2 ON r.member2_id = p2.id
    WHERE r.type = 'spouse';
    """
    
    cur.execute(query)
    married_couples = cur.fetchall()
    con.close()
    
    return married_couples

def save_married_couples_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  

    Args:
        married_couples (list): (name1, name2, start_date) of married couples
        csv_path (str): Path of CSV file
    """
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name1', 'Name2', 'Start Date'])
        writer.writerows(married_couples)

if __name__ == '__main__':
    main()
