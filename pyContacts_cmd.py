#!/usr/bin/env python
##
# pyContacts v0.4.0 - Copyright Shawn "prjktdtnt" Thompson 2008
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
#
##

import csv,os,operator,cmd,sys
from pyContacts import Contact

class pyCCMD(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = """
    pyContacts is free software, licensed under GPLv3, see http://www.gnu.org/licenses/ for further information.
    Type help to see commands and their uses
        """
        self.prompt = "pyContacts> "
        self.storage_file = os.path.expanduser('~') + "/.pyContactsCSV"
        self.contacts_array = []

    def perform_sorting(self):
        if len(self.contacts_array) > 0:
            contact_id_count = 1
            self.contacts_array.sort(key=operator.attrgetter('contact_fname'))
            for row in self.contacts_array:
                row.reId(contact_id_count)
                contact_id_count += 1

    def load_contacts(self):
        load_from = csv.reader(open(self.storage_file))
        for row in load_from:
            self.contacts_array.append( Contact(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]) )
        self.perform_sorting()

    def do_save(self, noargs=""):
        """Write contacts to main file"""

        self.perform_sorting()
        save_to = csv.writer(open(self.storage_file, 'w'))
        for row in self.contacts_array:
            save_to.writerow(row.writeMe())
        print "Saved"
        print

    def do_quit(self, line):
        """Save contacts and Quit."""

        print
        self.do_save()
        sys.exit()

    def do_list(self, noargs):
        """List contacts"""

        self.perform_sorting()
        for row in self.contacts_array:
            row.listMe()
    
    def do_show(self, cid):
        """Show a contact's information"""
        if cid == '':
            self.do_list("")
            cid = int(raw_input("Enter a contact ID: "))
            cid -= 1
        else:
            cid = int(cid)
            cid -= 1
        if cid < len(self.contacts_array):
            self.contacts_array[cid].fullInfo()
            print
        else:
            print "Invalid contact ID"
            print

    def do_remove(self, cid):
        """Remove a contact"""
        
        if cid == '':
            self.do_list("")
            cid = int(raw_input("Enter a contact ID: "))
            cid -= 1
        else:
            cid = int(cid)
            cid -= 1
        if cid < len(self.contacts_array):
            self.contacts_array[cid].fullInfo()
            last_chance = str(raw_input("Are you sure you want to remove this contact? [y/n]: "))
            if last_chance.lower() == 'y':
                removed_name = self.contacts_array[cid].sayfName()
                del self.contacts_array[cid]
                print "Removed " + removed_name
                print
            else:
                print "Did not delete " + self.contacts_array[cid].sayfName()
                print
        else:
            print "Invalid contact ID"
            print

    def do_add(self, noargs):
        """Add a new contact"""
        print "All questions in the following selection except for a name are optional"
        print "just press enter to skip a question"
        print
        fname=str(raw_input("What is the contact's first name?:    "))
        lname=str(raw_input("What is the contact's last name?:     "))
        phone=str(raw_input("What is the contact's phone number?:  "))
        email=str(raw_input("What is the contact's E-mail address? "))
        print "The following will have you enter the contact's residential address"
        print "intended for US-Mailing address, this is also optional"
        print
        address1=str(raw_input("Address 1: "))
        address2=str(raw_input("Address 2: "))
        city=str(raw_input("City: "))
        state=str(raw_input("State: "))
        zip=str(raw_input("Zipcode: "))
        print "The new contact's information is displayed below:"
        print
        new_id=len(self.contacts_array)+1
        self.contacts_array.append(Contact(str(new_id),fname,lname,phone,email,address1,address2,city,state,zip))
        self.contacts_array[new_id-1].fullInfo()
        print
        correct=str(raw_input("Press enter to continue"))
        self.perform_sorting()

    def do_edit(self, what=""):
        """ Update a contact's information
   Example: edit address
        """

        #If what is not defined then define it
        if what == '':
            print "What would you like to edit?"
            print "1. First and/or Last name"
            print "2. Phone number"
            print "3. E-mail Address"
            print "4. Street Address"
            what_sel=str(raw_input("Selection: "))
            if what_sel=='1':
                what="name"
            elif what_sel=='2':
                what="phone"
            elif what_sel=='3':
                what="email"
            elif what_sel=='4':
                what="address"
            else:
                print
                print "That wasn't an option"

        #Once what is defined, make sure it is valid
        if what == 'name':
            pass
        elif what == 'phone':
            pass
        elif what == 'email':
            pass
        elif what == 'address':
            pass
        else:
            print
            print "Invalid edit selection"
            what = "invalid"
            cid = len(self.contacts_array)+2

        #Check to see if there is a contact ID already selected,
        #if not ask user to select one
        self.do_list("")
        cid = str(raw_input("Which contact do you want to edit?  "))

        #Make sure cid actually exists
        if (int(cid)-1) > len(self.contacts_array):
            print
            print "Invalid Contact"
            cid = "invalid"

        #Check to make sure there was not an error above, if there was pass back to main menu
        if cid != "invalid" and what != "invalid":
            cid = int(cid)-1
            self.perform_edit(cid,what)
        else:
            print
            print "There was an error, please try again"
            print

    #if no error during do_edit then perform the edit
    def perform_edit(self, cid, what):
        if what == 'name':
            old_fname=self.contacts_array[cid].sayfName()
            old_lname=self.contacts_array[cid].saylName()
            old_fullName=self.contacts_array[cid].sayFullName()
            print "You are about to update " + old_fullName
            print "to make no change just press enter at the prompt"
            print
            new_fname=str(raw_input("First Name: "))
            new_lname=str(raw_input("Last Name:  "))
            if new_fname == '':
                new_fname = old_fname
            if new_lname == '':
                new_lname = old_lname
            self.contacts_array[cid].reName(new_fname,new_lname)

        elif what == 'phone':
            old_phone=self.contacts_array[cid].sayPhone()
            print "You are about to update the phone number for " + self.contacts_array[cid].sayFullName()
            print "to cancel just press enter"
            print
            new_phone=str(raw_input("New Phone: "))
            if new_phone == '':
                new_phone=old_phone
            self.contacts_array[cid].rePhone(new_phone)

        elif what == 'email':
            old_email=self.contacts_array[cid].sayEmail()
            print "Updating e-mail address for " + self.contacts_array[cid].sayFullName()
            print "to cancel just press enter"
            print
            new_email=str(raw_input("New Email: "))
            if new_email == '':
                new_email = old_email
            self.contacts_array[cid].reEmail(new_email)

        elif what == 'address':
            old_address=self.contacts_array[cid].sayAddress()
            print "Updating e-mail address for " + self.contacts_array[cid].sayFullName()
            print "to cancel this leave all fields blank"
            print
            address1=str(raw_input("Address 1: "))
            address2=str(raw_input("Address 2: "))
            city=str(raw_input("City: "))
            state=str(raw_input("State: "))
            zip=str(raw_input("Zip: "))
            new=[address1,address2,city,state,zip]
            if len(new[0]) == 0 and len(new[1]) == 0 and len(new[2]) == 0 and len(new[3]) == 0 and len(new[4]) == 0:
                new=old_address
            self.contacts_array[cid].reAddress(new)

        else:
            print "Something has gone terribly wrong!!!" #If you get here, there's a SERIOUS issue somewhere


    def do_version(self, noargs):
        """Show program version"""
        print
        print "  pyContacts v0.4.0"
        print
    
#Internal start
def main():
    pyCCMD_cmd = pyCCMD()
    pyCCMD_cmd.load_contacts()
    pyCCMD_cmd.cmdloop()

#External start
if __name__ == "__main__":
    main()
