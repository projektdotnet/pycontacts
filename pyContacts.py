#
# pyContacts v0.1 - Copyright Shawn "prjktdtnt" Thompson 2008
# Simple contact manager for my own use
#
"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
    write_contacts(thefile)

#Display contacts if requested
def prnt_contacts():
    contacts_array.sort()
    print "\n"
    print "name, number"
    i=0
    for row in contacts_array:
        print contacts_array[i][0] + ", " + contacts_array[i][1]
        i=i+1
    print "\n"

#how to remove a contact from the list
def remove_contact():
    if len(contacts_array) > 0:
        contacts_array.sort()
        i=0
        j=1
        print "Contacts: \n"
        print "ID, Name, Phone \n"
        for row in contacts_array:
            print str(j) + ") " + contacts_array[i][0] + ", " + contacts_array[i][1]
            i=i+1
            j=j+1
        toremove=int(raw_input("Enter the contact ID to remove: "))
        toremove=toremove-1
        del contacts_array[toremove]
    else:
        print "No Contacts\n\n"

#the menu for this program shall be defined here
def menu():
    print "Contacts Management"
    print "1. List Contacts"
    print "2. Add a Contact"
    print "3. Remove a Contact"
    print "q. Save and Quit"
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
        new_name=raw_input("What is the contact's name? ")
        new_name=new_name.capitalize()
        print "\n"
        new_number=raw_input("What is the contact's phone number? ")
        input=[new_name,new_number]
        append_contact(input)
        another=str(raw_input("\nAdd another?[y/n] "))
        if another == "y":
            call_correct_function("2")
        elif another == "n":
            menu()
        else:
            print "Your selection was invalid, bailing to menu\n\n"
            menu()
    elif selection == "3":
        remove_contact()
        hasdata=len(contacts_array)
        if 0 < hasdata:
            another=str(raw_input("\nRemove Another?[y/n] "))
            if another == "y":
                call_correct_function("3")
            elif another =="n":
                menu()
            else:
                print "Your selection was invalid, bailing to menu\n\n"
                menu()
    elif selection == "q":
        write_contacts(thefile)
        quit()
    else:
        print "\nUnrecognized Option\n"
        menu()
    menu()

#write contacts to thefile after sorting
def write_contacts(filename):
    contacts_array.sort()
    output_thefile = csv.writer(open(filename, 'w'))
    output_thefile.writerows(contacts_array)

#=Start the program===

#ask the user if they have a file the would like to use
thefile=raw_input("Input your contact file: ")
#If user doesn't specify a file assign the default or check to see if file exists
if thefile=="":
    thefile=os.path.expanduser('~') + "/.contacts.csv"
    print "\nNo file selected, defaulting to " + thefile +"\n"
if os.path.exists(thefile):
    fetch_contacts(thefile)
else:
    print "No contacts stored there, will create a new file on exit"
menu()

#=End===
