#
# pyContacts - Copyright Shawn "prjktdtnt" Thompson
# Simple contact manager for my own use
# This program is distributed under the GNU GPLv3 license
#
# Features: *Add, remove, store contact information
#           *Display easily readable and formatted info
#            to the user
#
#=Imports===
import csv
import os
#=End Imports===

#=Major Variables===
contacts_array = []
#thefile="/home/trash/.contacts.csv"
#thefile=""
#=End Variables===


#=Functions===

#Retreive the contacts and place them in an array
def fetch_contacts(filename):
    contacts_thefile=csv.reader(open(filename))
    for row in contacts_thefile:
        contacts_array.append( row )

#add a contact to the array
def append_contact(input):
    contacts_array.append(input)

def prnt_contacts():
    print "\n"
    print "name, number"
    i=0
    for row in contacts_array:
        print contacts_array[i][0] + ", " + contacts_array[i][1]
        i=i+1
    print "\n"

#the menu for this program shall be defined here
def menu():
    print "Contacts Management"
    print "1. List Contacts"
    print "2. Add a contact"
    print "q. quit"
    selection=raw_input("What do you want to do?: ")
    call_correct_function(selection)

#after the menu selection has been made, determine user input and
#call the correct function
def call_correct_function(selection):
    if selection == "1":
        prnt_contacts()
        menu()
    elif selection == "2":
        print "\nAdd a contact\n"
        menu()
    elif selection == "q":
        quit()
    else:
        print "\nUnrecognized Option\n"
        menu()
        

#write contacts to thefile after sorting
def write_contacts(filename):
    contacts_array.sort()
    output_thefile = csv.writer(open(thefile, 'w'))
    output_thefile.writerows(contacts_array)
    
#=Start the program===
#thefile="/home/trash/.contacts.csv"
#menu()
#fetch_contacts(thefile)
#contacts_array.sort()
#print contacts_array
#write_contacts(thefile)
thefile=raw_input("Input your contact file: ")
if thefile=="":
    thefile=os.path.expanduser('~') + "/.contacts.csv"
    print "No file selected, defaulting to " + thefile 
fetch_contacts(thefile)
menu()

#=End===
