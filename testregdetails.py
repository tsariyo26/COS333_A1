#!/usr/bin/env python

#-----------------------------------------------------------------------
# testregdetails.py
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
    command = 'python ' + program + ' ' + args
    print_flush(command)
    exit_status = os.system(command)
    if os.name == 'nt':  # Running on MS Windows?
        print_flush('Exit status = ' + str(exit_status))
    else:
        print_flush('Exit status = ' + str(os.WEXITSTATUS(exit_status)))

#-----------------------------------------------------------------------

def main():

    if len(sys.argv) != 2:
        print('Usage: ' + sys.argv[0] + ' regdetailsprogram',
            file=sys.stderr)
        sys.exit(1)

    program = sys.argv[1]

    exec_command(program, '8321')

    # Boundary Test Cases
    exec_command(program, '')  # Empty input
    exec_command(program, '9034')  # Non-existent course
    exec_command(program, 'abc1234')  # Non-integer course-ID
    exec_command(program, '9032 8231')  # Two courses at once
    exec_command(program, '-1')  # Negative course ID
    exec_command(program, '0')  # Course ID of zero
    exec_command(program, '999999999999')  # Extremely large course ID
    exec_command(program, '@#$$!')  # Special characters
    

if __name__ == '__main__':
    main()
