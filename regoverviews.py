#-----------------------------------------------------------------------
# regoverviews.py
# Author: Toluwanimi Ariyo, Michael Igbinoba
#-----------------------------------------------------------------------

'''
 OVERVIEW OF FUNCTIONALITY:
 Displays the classid, dept, coursenum, area, and title of each 
 class that matches the criteria specified by the user via command-line arguments
'''




# DESIGN REQUIREMENTS BELOW:
# Output must have have the appearance of a table
# Each column must have a title
# Each title must be underlined with hyphens
# The rows must sorted. The primary sort must be by dept in ascending order, the secondary sort must be by coursenum in ascending order, and tertiary sort must be by classid in ascending order.
# Within each row, each line must consist of no more than 72 characters, not including the newline character.
# Within each row, each line must end after a word, not within a word. That is, no newline characters may appear within words.
# Must use SQL prepared statements to protect the database against SQL injection attacks