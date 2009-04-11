#!/usr/bin/env python
#
# pyContacts v0.3.1 - Copyright Shawn "prjktdtnt" Thompson 2008
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

#=START Imports===
import csv
import os
import operator

#=END Imports===

#=START Variables===
global contacts_array
contacts_array = [] #Used later to track all contacts
contacts_file = os.path.expanduser('~') + "/.pyContactsCSV"
running = True #Used for looping menu function instead of multiple re-calling
#=END Variables===

#=START Classes===
class Contact:
    def __init__(self, id="", fname="", lname="", phone="", email="", address1="", address2="", city="", state="", zip=""):
        self.contact_id = id
        self.contact_fname = fname
        self.contact_lname = lname
        self.phone = phone
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip = zip
        self.makePhonePretty()

    #listMe used to print a clean looking version with proper spacing
    def listMe(self):
        print str(self.contact_id).rjust(3) + ") " + self.contact_fname.ljust(15) + "- " + self.pretty_phone.ljust(17) + "- " + self.email

    #List output for other functions to use
    def writeMe(self):
        return [self.contact_id,self.contact_fname,self.contact_lname,self.phone,self.email,self.address1,self.address2,self.city,self.state,self.zip]

    #Return only a name, primarily used in remove function
    def sayName(self):
        return self.contact_fname
    
    #Return the full name of a user
    def sayFullName(self):
        myFullName = self.contact_fname + " " + self.contact_lname
        return myFullName

    #Return the User ID
    def sayId(self):
        return self.contact_id

    #Create a user readable phone
    def makePhonePretty(self):
        if len(self.phone) == 7:
            self.pretty_phone = self.phone[0:3] + '-' + self.phone[3:] #ex 555-1234
        elif len(self.phone) == 10:
            self.pretty_phone = '(' + self.phone[0:3] + ') ' + self.phone[3:6] + '-' + self.phone[6:] #ex (866) 555-1234
        else:
            self.pretty_phone = self.phone # If we don't know the correct output then don't attempt to format ex 815551234

    #If user moves up or down in the array they'll need a new ID number
    def reId(self, id):
        self.contact_id = id

    #Edit contact first and last name
    def reName(self):
        fname = str(raw_input("What is the contact's first name? "))
        lname = str(raw_input("What is the contact's last name?  "))
        print ""
        print "Name: " + fname + " " + lname
        print ""
        name_correct = str(raw_input("Does this look correct? [y/n]"))
        if name_correct == "y":
            self.contact_fname = fname
            self.contact_lname = lname
        elif name_correct == "n":
            self.reName()
        else:
            print "Invalid Response"

    #Prettify the output for rePhone(self)
    def rePhonePretty(self, phone=""):
        if len(phone) == 7:
            returned_number = phone[0:3] + "-" + phone[3:]
            return returned_number
        elif len(phone) == 10:
            returned_number = '(' + phone[0:3] + ') ' + phone[3:6] + "-" + phone[6:]
            return returned_number
        else:
            return phone

    #Ability to edit phone number
    def rePhone(self):
        new_phone = str(raw_input("What is the contact's phone number?: "))
        print ""
        print "Phone: " + self.rePhonePretty(new_phone)
        print ""
        phone_correct = str(raw_input("Does this look correct? [y/n]"))
        if phone_correct == "y":            
            self.phone = new_phone
            self.makePhonePretty()
        elif phone_correct == "n":
            self.rePhone()
        else:
            print "Invalid Response"

    #Ability to add a street address
    def reAddress(self):
        new_address1 = str(raw_input("Address 1: "))
        new_address2 = str(raw_input("Address 2: "))
        new_city = str(raw_input("City: "))
        new_state = str(raw_input("State: "))
        new_zip = str(raw_input("Zip: "))
        print ""
        print "Full Address: "
        print ""
        print self.contact_fname + " " + self.contact_lname
        if len(new_address2) > 0:
            print new_address1
            print new_address2
        else:
            print new_address1
        if len(new_state) == 2:
            new_state = new_state.upper()
        else:
            new_state = new_state.capitalize()
        print new_city.capitalize() + ", " + new_state + " " + new_zip
        print ""
        address_correct = str(raw_input("Does this look correct? [y/n] "))
        if address_correct == "y":
            new_city = new_city.capitalize()
            self.address1 = new_address1
            self.address2 = new_address2
            self.city = new_city
            self.state = new_state
            self.zip = new_zip
        elif address_correct == "n":
            self.reAddress()
        else:
            "Invalid Response"

    #Ability to add/edit e-mail address
    def reEmail(self):
        new_email = str(raw_input("What is the contact's e-mail? "))
        print ""
        print "Email: " + new_email
        print ""
        email_correct = str(raw_input("Does this look correct? [y/n]"))
        if email_correct == "y":
            self.email = new_email
        elif email_correct == "n":
            self.reEmail()
        else:
            "Invalid Response"

    def fullInfo(self):
        print "Name:    " + self.sayFullName()
        print "Phone:   " + self.pretty_phone
        print "Email:   " + self.email
        if len(self.address1) > 0:
            print "Address: " + self.address1
            if len(self.address2) > 0:
                print "         " + self.address2
            print "         " +self.city + ", " + self.state + " " + self.zip
        else:
            print "Address: "

#=END Contact Class===

#=END Classes===

#=START Primary Functions===
def perform_sorting():
    contact_id_count = 1
    global contacts_array
    if len(contacts_array) > 0:
        contacts_array.sort(key=operator.attrgetter('contact_fname'))
        for row in contacts_array:
            row.reId(contact_id_count)
            contact_id_count += 1

def write_contacts(filename):
    perform_sorting()
    output_contacts_file = csv.writer(open(filename, 'w'))
    for row in contacts_array:
        output_contacts_file.writerow(row.writeMe())

def fetch_contacts(filename):
    contacts_contacts_file=csv.reader(open(filename))
    for row in contacts_contacts_file:
        contacts_array.append ( Contact(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]) ) #Split row into class attributes
    perform_sorting()

def print_contacts():
    for row in contacts_array:
        row.listMe()


def add_contact():
    add_loop = True
    while add_loop:
        print "Add a Contact: "
        fname=str(raw_input("What is the contact's first name?: "))
        lname=str(raw_input("What is the contact's last name?:  "))
        number=str(raw_input("What is the contact's number?:     "))
        email=str(raw_input("What is the contact's e-mail?:     "))
        print "Does this look right?"
        fullname = fname.capitalize() + " " + lname.capitalize()
        print "Name:   " + fullname
        pretty_number = ""
        if len(number) == 7:
            pretty_number = number[0:3] + "-" + number[3:]
        elif len(number) == 10:
            pretty_number = "(" + number[0:3] + ") " + number[3:6] + "-"+ number[6:]
        print "Phone:  " + pretty_number
        print "E-mail: " + email
        correct=str(raw_input("[y/n]"))
        if correct == "y":
            fname = fname.capitalize()
            lname = lname.capitalize()
            contacts_array.append(Contact("",fname,lname,number,email))
        elif correct == "n":
            pass
        else:
            print "Not an option!"
        another=str(raw_input("Add another? [y/n]: "))
        if another == "y":
            pass
        elif another == "n":
            add_loop = False
        else:
            print "Not an option!"
    perform_sorting()


def remove_contact():
    remove_loop = True
    while remove_loop:
        if len(contacts_array) > 0:
            perform_sorting()
            print_contacts()
            toremove=int(raw_input("Enter ID to remove: "))
            toremove -= 1
            if toremove < len(contacts_array):
                print "Are you sure you want to remove " + contacts_array[toremove].sayName()
                last_chance=str(raw_input("[y/n]"))
                if (last_chance.lower() == "y"):
                    removed_name=contacts_array[toremove].sayName()
                    del contacts_array[toremove]
                    print "Removed " + removed_name
                else:
                    print "Did NOT delete "+contacts_array[toremove].sayName()
            else:
                print "Invalid contact id"
            another=str(raw_input("Remove another? [y/n]"))
            if another.lower() == "y":
                pass
            else:
                remove_loop = False
        else:
            print "No Contacts!"
            remove_loop = False
    perform_sorting()

def append_contact():
    append_loop = True
    while append_loop:
        print ""
        print_contacts()
        append_to=int(raw_input("Which contact would you like to add to? "))
        append_to -= 1
        if append_to < len(contacts_array):
            print ""
            print "Append/Edit Options"
            print "1. First and Last Name"
            print "2. Phone"
            print "3. Email"
            print "4. Address"
            print "5. Wrong Contact"
            append_selection=str(raw_input("What would you like to edit/append on " + contacts_array[append_to].sayFullName() + "?"))
            if append_selection == "1":
                contacts_array[append_to].reName()
            elif append_selection == "2":
                contacts_array[append_to].rePhone()
            elif append_selection == "3":
                contacts_array[append_to].reEmail()
            elif append_selection == "4":
                contacts_array[append_to].reAddress()
            else:
                pass
        else:
            print "Not a valid contact"
        append_another = str(raw_input("Edit More? [y/n]"))
        if append_another == "y":
            append_loop = True
        elif append_another == "n":
            append_loop = False
        else:
            append_loop = False
    perform_sorting()

def showContactInfo():
    showMeLoop = True
    while showMeLoop:
        if len(contacts_array) > 0:
            print_contacts()
            print ""
            which_contact = int(raw_input("Which contact? "))
            which_contact -= 1
            if which_contact < len(contacts_array):
                print ""
                contacts_array[which_contact].fullInfo()
                print ""
            else:
                print "Invalid Contact"
            exitloop = str(raw_input("Display Another? [y/n]"))
            if exitloop == "y":
                pass
            elif exitloop == "n":
                showMeLoop = False
            else:
                "Not a valid option"
                

        
#=END Primary Functions===

#=START Menu and Selector Functions===
def menu():
    print ""
    print "Menu:"
    print "1. List Contacts"
    print "2. Add a Contact"
    print "3. Remove a Contact"
    print "4. Edit a Contact"
    print "5. List a Contact's Full Info"
    print "q. Save and Quit"
    print ""
    call_correct_function(raw_input("What to do?: "))

def call_correct_function(selection):
    if str(selection) == "q":
        global running
        running = False
    elif str(selection) == "1":
        print_contacts()
    elif str(selection) == "2":
        add_contact()
    elif str(selection) == "3":
        remove_contact()
    elif str(selection) == "4":
        append_contact()
    elif str(selection) == "5":
        showContactInfo()
    else:
        print "Error, not a valid item"

#=END Menu and Selector Functions===

#=START Initial file check and menu loop===
if os.path.exists(contacts_file):
    fetch_contacts(contacts_file)

while running:
    menu()

#=END Menu Loop, write to contacts file===

write_contacts(contacts_file)

#=END===
