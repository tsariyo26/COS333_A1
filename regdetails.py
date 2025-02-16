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

def format_output(class_info, crosslistings, professors):
    """Format and print the class details."""
    classid, courseid, days, starttime, endtime, bldg, roomnum, area, title, descrip, prereqs = class_info
    
    print("Class Details")
    print("=" * 40)
    print(f"Class ID:   {classid}")
    print(f"Course ID:  {courseid}")
    print(f"Schedule:   {days} {starttime}-{endtime}")
    print(f"Location:   {bldg} {roomnum}")
    print(f"Area:       {area}")
    print(f"Title:      {title}")
    
    print("\nDescription:")
    for line in textwrap.wrap(descrip, width=72):
        print(line)
    
    if prereqs:
        print("\nPrerequisites:")
        for line in textwrap.wrap(prereqs, width=72):
            print(line)
    
    print("\nDepartments and Course Numbers:")
    for dept, coursenum in crosslistings:
        print(f"  {dept} {coursenum}")
    
    if professors:
        print("\nProfessors:")
        for profname, in professors:
            print(f"  {profname}")

def main():
    parser = argparse.ArgumentParser(description="Registrar application: show details about a class")
    parser.add_argument("classid", type=int, help="the id of the class whose details should be shown")
    args = parser.parse_args()
    
    try:
        conn = sqlite3.connect("reg.sqlite")
    except sqlite3.Error as e:
        print(f"Error opening database: {e}", file=sys.stderr)
        sys.exit(1)
    
    class_info, crosslistings, professors = fetch_class_details(conn, args.classid)
    format_output(class_info, crosslistings, professors)
    
    conn.close()

if __name__ == "__main__":
    main()

    # return class_info, crosslistings, professors
    # except sqlite3.Error as e:
    # print(f"Database error: {e}", file=sys.stderr)
    # sys.exit(1)
