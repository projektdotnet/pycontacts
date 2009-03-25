#!/usr/bin/env python
#
# pyContacts v0.1.2 - Copyright Shawn "prjktdtnt" Thompson 2008
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
thefile=os.path.expanduser('~') + "/.pyContactsCSV"
#=End Variables===

#=Functions===

def fetch_contacts(filename):
    contacts_thefile=csv.reader(open(filename))
    for row in contacts_thefile:
        contacts_array.append( row )

def append_contact(input):
    contacts_array.append(input)
    write_contacts(thefile)

def prnt_contacts():
    contacts_array.sort()
    print ""
    print "name".ljust(15) + "- number"
    i=0
    j=1
    for row in contacts_array:
        pretty_number = contacts_array[i][1]
        concat_pretty = '(' + pretty_number[0:3] + ') ' + pretty_number[3:6] + '-' + pretty_number[6:]
        print str(j).rjust(3)+") "+contacts_array[i][0].ljust(15) + "- " + concat_pretty
        i=i+1
        j=j+1
    print ""

def remove_contact():
    if len(contacts_array) > 0:
        contacts_array.sort()
        i=0
        j=1
        print "Contacts: "
        print "ID, Name, Phone "
        for row in contacts_array:
            pretty_number = contacts_array[i][1]
            concat_pretty = '(' + pretty_number[0:3] + ') ' + pretty_number[3:6] + '-' + pretty_number[6:]
            print str(j).rjust(3) + ") " + contacts_array[i][0].ljust(15) + "- " + concat_pretty
            i=i+1
            j=j+1
        toremove=int(raw_input("Enter the contact ID to remove: "))
        toremove=toremove-1
        if toremove < i:
            print "Are you sure you want to remove "+ contacts_array[toremove][0]+"?"
            last_chance=str(raw_input("[y/n]"))
            if (last_chance.lower() == "y"):
                removed_name=contacts_array[toremove][0]
                del contacts_array[toremove]
                print "Removed "+removed_name
            else:
                print "Cancelled deletion of "+contacts_array[toremove][0]
        else:
            print "Invalid Contact"
    else:
        print "No Contacts"

def menu():
    print "Contacts Management"
    print "1. List Contacts"
    print "2. Add a Contact"
    print "3. Remove a Contact"
    print "q. Save and Quit"
    selection=raw_input("What do you want to do?: ")
    call_correct_function(selection)

def call_correct_function(selection):
    if selection == "1":
        prnt_contacts()
        menu()
    elif selection == "2":
        print "Add a contact"
        new_name=raw_input("What is the contact's name? ")
        new_name=new_name.capitalize()
        new_number=raw_input("What is the contact's phone number? ")
        input=[new_name,new_number]
        append_contact(input)
        another=str(raw_input("Add another?[y/n] "))
        if another == "y":
            call_correct_function("2")
        elif another == "n":
            menu()
        else:
            print "Your selection was invalid, bailing to menu"
            menu()
    elif selection == "3":
        remove_contact()
        hasdata=len(contacts_array)
        if hasdata > 0:
            another=str(raw_input("Remove Another?[y/n] "))
            if another == "y":
                call_correct_function("3")
            elif another =="n":
                menu()
            else:
                print "Your selection was invalid, bailing to menu"
                menu()
    elif selection == "q":
        write_contacts(thefile)
        quit()
    else:
        print "Unrecognized Option"
        menu()
    menu()

def write_contacts(filename):
    contacts_array.sort()
    output_thefile = csv.writer(open(filename, 'w'))
    output_thefile.writerows(contacts_array)

#=Start the program===

if os.path.exists(thefile):
    fetch_contacts(thefile)

menu()

#=End===
