#-----------------------------------------------------------------------
# regoverviews.py
# Author: Toluwanimi Ariyo, Michael Igbinoba
#-----------------------------------------------------------------------

'''
 OVERVIEW OF FUNCTIONALITY:
 Displays the classid, dept, coursenum, area, and title of each 
 class that matches the criteria specified by the user via command-line arguments
'''

# (TO-DO) Handle escape characters

import sqlite3
import argparse
import textwrap
import sys

def fetch_classes(dept=None, num=None, area=None, title=None, db_path="reg.sqlite"):
    """
    Queries the SQLite database to retrieve matching class details based on the provided filters.
    """
    query = """
        SELECT classes.classid, crosslistings.dept, crosslistings.coursenum, 
               courses.area, courses.title 
        FROM classes
        JOIN courses ON classes.courseid = courses.courseid
        JOIN crosslistings ON classes.courseid = crosslistings.courseid
        WHERE 1=1
    """
    params = []
    
    if dept:
        query += " AND LOWER(crosslistings.dept) LIKE ?"
        params.append(f"%{dept.lower()}%")
    if num:
        query += " AND LOWER(crosslistings.coursenum) LIKE ?"
        params.append(f"%{num.lower()}%")
    if area:
        query += " AND LOWER(courses.area) LIKE ?"
        params.append(f"%{area.lower()}%")
    if title:
        query += " AND LOWER(courses.title) LIKE ?"
        params.append(f"%{title.lower()}%")
    
    query += " ORDER BY crosslistings.dept ASC, crosslistings.coursenum ASC, classes.classid ASC"
    
    try: 
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.DatabaseError as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1) # Exit with status 1 on database error

    return []  # Return an empty list in case of an error

def print_table(results):
    """
    Prints the retrieved class data in a formatted table with column headers.
    """
    headers = ["ClsId", "Dept", "CrsNum", "Area", "Title"]
    header_line = "%-5s %-4s %-6s %-4s %-5s" % tuple(headers)
    underline = "{:<5} {:<4} {:<6} {:<4} {:<5}".format("-"*5, "-"*4, "-"*6, "-"*4, "-"*5)

    print(header_line)
    print(underline)
    
    if not results:
        return
    
    
    for row in results:
        classid, dept, coursenum, area, title = row
        row = '%5s %4s %6s %4s %s' % (classid, dept, coursenum, area, title)
        wrapped_text = textwrap.wrap(row, width=72, subsequent_indent=" " * 23)
        for line in wrapped_text:
            print(line)

def main():
    """
    Parses command-line arguments and retrieves and displays class information.
    """
    
    parser = argparse.ArgumentParser(description="Registrar application: show overviews of classes")
    parser.add_argument("-d", metavar="dept", help="show only those classes whose department contains dept")
    parser.add_argument("-n", metavar="num", help="show only those classes whose course number contains num")
    parser.add_argument("-a", metavar="area", help="show only those classes whose distrib area contains area")
    parser.add_argument("-t", metavar="title", help="show only those classes whose course title contains title")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        if "-h" in sys.argv or "--help" in sys.argv:  
            sys.exit(0)  # Ensure help message exits with 0
        sys.exit(2) # Exit with status 2 if argument parsing fails
    

    results = fetch_classes(dept=args.d, num=args.n, area=args.a, title=args.t)
    print_table(results)
    sys.exit(0)  # Exit with status 0 on success

if __name__ == "__main__":
    main()




# DESIGN REQUIREMENTS BELOW:
# Output must have have the appearance of a table
# Each column must have a title
# Each title must be underlined with hyphens
# The rows must sorted. The primary sort must be by dept in ascending order, the secondary sort must be by coursenum in ascending order, and tertiary sort must be by classid in ascending order.
# Within each row, each line must consist of no more than 72 characters, not including the newline character.
# Within each row, each line must end after a word, not within a word. That is, no newline characters may appear within words.
# Must use SQL prepared statements to protect the database against SQL injection attacks