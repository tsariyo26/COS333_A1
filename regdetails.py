import argparse
import sqlite3
import textwrap
import sys

def fetch_class_details(conn, classid):
    """Retrieve class details from the database."""
    try:
        cur = conn.cursor()
        
        # Fetch class information
        cur.execute("""
            SELECT c.classid, c.courseid, c.days, c.starttime, c.endtime, c.bldg, c.roomnum,
                   cr.area, cr.title, cr.descrip, cr.prereqs
            FROM classes c
            JOIN courses cr ON c.courseid = cr.courseid
            WHERE c.classid = ?
        """, (classid,))
        class_info = cur.fetchone()
        if not class_info:
            print(f"Error: No class found with classid {classid}", file=sys.stderr)
            sys.exit(1)
        
         # Fetch departments and course numbers
        cur.execute("""
            SELECT dept, coursenum FROM crosslistings
            WHERE courseid = ? ORDER BY dept ASC, coursenum ASC
        """, (class_info[1],))
        crosslistings = cur.fetchall()
        
        # Fetch professors
        cur.execute("""
            SELECT p.profname FROM profs p
            JOIN coursesprofs cp ON p.profid = cp.profid
            WHERE cp.courseid = ? ORDER BY p.profname ASC
        """, (class_info[1],))
        professors = cur.fetchall()
        
        return class_info, crosslistings, professors
    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)