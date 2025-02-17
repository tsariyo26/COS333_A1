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
                   cr.area, cr.title, cr.descrip, IFNULL(cr.prereqs, '')
            FROM classes c
            JOIN courses cr ON c.courseid = cr.courseid
            WHERE c.classid = ?
        """, (classid,))
        class_info = cur.fetchone()
        if not class_info:
            print(f"regdetails.py: no class "
            f"with classid {classid} exists",
            file=sys.stderr)
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
    # Format and print the class details
    classid, courseid, days, \
    starttime, endtime, bldg, \
    roomnum, area, title, descrip, prereqs = class_info
    print("-" * 13)
    print("Class Details")
    print("-" * 13)
    print(f"Class Id: {classid}")
    print(f"Days: {days}")
    print(f"Start time: {starttime}")
    print(f"End time: {endtime}")
    print(f"Building: {bldg}")
    print(f"Room: {roomnum}")
    print("-" * 14)
    print("Course Details")
    print("-" * 14)
    print(f"Course Id: {courseid}")
    if crosslistings:
        for dept, coursenum in crosslistings:
            print(f'Dept and Number: {dept} {coursenum}')
    print(f"Area: {area.strip()}"
    if area and area.strip() else "Area:".rstrip())
    prefix = "Title: "
    title_text = textwrap.fill(
    title, width=72, initial_indent=prefix, subsequent_indent=" " * 3
    )
    print(title_text)
    prefix = "Description: "
    descrip_text = textwrap.fill(
    descrip, width=72, initial_indent=prefix, subsequent_indent=" " * 3
    )
    print(descrip_text)
    prefix = "Prerequisites: "
    prereq_text = (
    textwrap.fill(
        prereqs, width=72,
        initial_indent=prefix,
        subsequent_indent=" " * 3
    )
    if prereqs.strip() else prefix.rstrip()
    )
    print(prereq_text)
    if professors:
        for prof in professors:
            print(f'Professor: {prof[0]}')

def main():
    parser = argparse.ArgumentParser(description=
    "Registrar application: show details about a class")
    parser.add_argument("classid",
    type=int, help=
    "the id of the class whose details should be shown")
    args = parser.parse_args()
    try:
        conn = sqlite3.connect("reg.sqlite")
    except sqlite3.Error as e:
        print(f"Error opening database: {e}", file=sys.stderr)
        sys.exit(1)
    class_info, crosslistings, \
    professors = fetch_class_details(conn, args.classid)
    format_output(class_info, crosslistings, professors)
    conn.close()

if __name__ == "__main__":
    main()
