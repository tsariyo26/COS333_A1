#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregoverviews.py
# Author: Toluwanimi Ariyo, Michael Igbinoba
#-----------------------------------------------------------------------

import os
import sys

#-----------------------------------------------------------------------

MAX_LINE_LENGTH = 72
UNDERLINE = '-' * MAX_LINE_LENGTH

#-----------------------------------------------------------------------

def print_flush(message):
    print(message)
    sys.stdout.flush()

#-----------------------------------------------------------------------

def exec_command(program, args):

    print_flush(UNDERLINE)
    command = 'python3 ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('usage: ' + sys.argv[0] + ' regprogram', file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    exec_command(program, '-d COS')
    exec_command(program, '-d COS -a qr -n 2 -t intro')

    # Add more tests here.

    # Boundary (alias corner case) Test Cases
    exec_command(program, '-d XYZ')  # Non-existent department (should return no results)
    exec_command(program, '-n 9999')  # Non-existent course number
    exec_command(program, '-t ""')    # Empty string as filter (should be ignored or handled)
    exec_command(program, '-t " "')  # Space as input  
    exec_command(program, '-t "!@#$%^&*()"')    # Special characters in filters (SQL safety test)
    exec_command(program, '-t "A Very Long Course Title That Exceeds 72 Characters For Testing"') # Long course title (should wrap properly)
    exec_command(program, '-d ELE')  # Courses with multiple cross-listings (should appear under all relevant depts)
    exec_command(program, '-n 999') # Course with no professor assigned (should handle missing professor case)
   
    # Statement Test Cases
    exec_command(program, '')  # Default behavior (fetch all courses, no filters applied)
    exec_command(program, '-h') # Help message (triggers argparse help function)
    #  Argument parsing (all valid filters) other than -d COS (already done earlier)
    exec_command(program, '-n 333')   
    exec_command(program, '-a QR')    
    exec_command(program, '-t intro')  
    # Invalid arguments (ensures error handling)
    exec_command(program, '-x')  # Unknown flag  
    exec_command(program, '-a')  # Missing argument value  
    exec_command(program, '-d')  # Missing department value  
    exec_command(program, 'a qr')  # Incorrect format 

    

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main()
