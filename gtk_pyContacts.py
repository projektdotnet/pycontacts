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

#==Imports==
import pygtk
pygtk.require('2.0')
import gtk
import csv,os,operator,sys
from pyContacts import Contact

#==Main gtkPyContacts window and primary functions==
class gtkPyContacts:

    def delete_event(self, widget, data=None):
        return False

    def destroy(self, widget, data=None):
        self.write_contacts()
        gtk.main_quit()

    def __init__(self):
        self.storage_file = os.path.expanduser('~') + "/.pyContactsCSVTest"
        self.contactsArray = []

        #Start window, declare the callbacks to close the program
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("pyContacts GTK")
        self.window.set_border_width(5)
        
        #Contact List
        self.contactsArrayList = gtk.ListStore(str, str, str)
        self.contactsListView = gtk.TreeView(self.contactsArrayList)

        #Columns for list
        self.clvId = gtk.TreeViewColumn('')
        self.clvfName = gtk.TreeViewColumn('First Name')
        self.clvlName = gtk.TreeViewColumn('Last Name')

        #Columns to correct order
        self.contactsListView.append_column(self.clvId)
        self.contactsListView.append_column(self.clvfName)
        self.contactsListView.append_column(self.clvlName)

        #Create the renderers, should always use CellRendererText here
        self.clvCellId = gtk.CellRendererText()
        self.clvCellfName = gtk.CellRendererText()
        self.clvCelllName = gtk.CellRendererText()

        #Cell Packing Renderers
        self.clvId.pack_start(self.clvCellId, True)
        self.clvfName.pack_start(self.clvCellfName, True)
        self.clvlName.pack_start(self.clvCelllName, True)

        #Packed renderers in cells, now pack those to columns
        self.clvId.set_attributes(self.clvCellId, text=0)
        self.clvfName.set_attributes(self.clvCellfName, text=1)
        self.clvlName.set_attributes(self.clvCelllName, text=2)

        #Wrap it in a scroll window
        self.clvScrollWrap = gtk.ScrolledWindow()
        self.clvScrollWrap.add(self.contactsListView)

        #Define buttons in this section
        btnQuit = gtk.Button("Quit")
        btnNew = gtk.Button("New Contact")
        btnShow = gtk.Button("Show Contact")
        btnEdit = gtk.Button("Edit Contact")
        btnRemove = gtk.Button("Delete Contact")
        btnSave = gtk.Button("Save Contacts")
        btnAbout = gtk.Button("About")

        #Connect callbacks here
        btnQuit.connect("released", self.destroy)
        btnNew.connect("released", self.add_contact)
        btnShow.connect("released", self.show_contact)
        btnEdit.connect("released", self.edit_contact)
        btnRemove.connect("released", self.remove_contact)
        btnSave.connect("released", self.write_contacts)
        btnAbout.connect("released", self.displayAbout)

        #Main window layout, using table style
        layoutGrid = gtk.Table(9, 2, True)

        #Window add bits
        self.window.add(layoutGrid)

        #Table attachments
        layoutGrid.attach(btnAbout, 1, 2, 0, 1)
        layoutGrid.attach(self.clvScrollWrap, 0, 2, 1, 6)
        layoutGrid.attach(btnNew, 0, 1, 6, 7)
        layoutGrid.attach(btnEdit, 1, 2, 6, 7)
        layoutGrid.attach(btnShow, 0, 1, 7, 8)
        layoutGrid.attach(btnRemove, 1, 2, 7, 8)
        layoutGrid.attach(btnSave, 0, 1, 8, 9)
        layoutGrid.attach(btnQuit, 1, 2, 8, 9)

        #Widget show calls
        btnAbout.show()
        btnNew.show()
        btnEdit.show()
        btnShow.show()
        btnRemove.show()
        btnSave.show()
        btnQuit.show()
        self.clvScrollWrap.show()
        self.contactsListView.show()
        layoutGrid.show()
        self.window.show()
        self.load_contacts()

    #Display Commands
    def reList(self):
        self.contactsArrayList.clear()
        for this_row in self.contactsArray:
            self.contactsArrayList.append([this_row.sayId(),this_row.sayfName(),this_row.saylName()])

    def displayAbout(self, widget, data=None):
        print "displayAbout()"

    #Primary Commands
    def perform_sorting(self):
        if len(self.contactsArray) > 0:
            contact_id_count = 1
            self.contactsArray.sort(key=operator.attrgetter('contact_fname'))
            for row in self.contactsArray:
                row.reId(contact_id_count)
                contact_id_count += 1
            self.reList()

    def load_contacts(self, data=None):
        load_from = csv.reader(open(self.storage_file))
        for row in load_from:
            self.contactsArray.append( Contact(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9]) )
        for this_row in self.contactsArray:
            self.contactsArrayList.append([this_row.sayId(),this_row.sayfName(),this_row.saylName()])

    def write_contacts(self, widget=None, data=None):
        self.perform_sorting()
        save_to = csv.writer(open(self.storage_file, 'w'))
        for row in self.contactsArray:
            save_to.writerow(row.writeMe())

    def add_contact(self, widget, data=None):
        print "add_contact()"

    def edit_contact(self, widget, data=None):
        print "edit_contact()"

    def show_contact(self, widget, data=None):
        print "show_contact()"

    def remove_contact(self, widget, data=None):
        toremoveList = self.get_selected()
        toremoveId = int(toremoveList[0])-1
        toremovefName = toremoveList[1]
        toremovelName = toremoveList[2]
        toremoveFullName = self.contactsArray[toremoveId].sayFullName()
        confirm_message = "Are you sure you want to remove " + toremoveFullName
        confirmRemove = gtk.MessageDialog(None, 0, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, confirm_message)
        resp = confirmRemove.run()
        if resp == gtk.RESPONSE_YES:
            del self.contactsArray[toremoveId]
            self.perform_sorting()
        elif resp == gtk.RESPONSE_NO:
            pass
        else:
            baderror=gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, "SOMETHING WENT TERRIBLY WRONG")
            baderror.run()
            baderror.destroy()
        confirmRemove.destroy()

    def get_selected(self):
        liststore, treeiter = self.contactsListView.get_selection().get_selected()
        self.selected = [liststore.get(treeiter, 0)[0], liststore.get(treeiter,1)[0], liststore.get(treeiter, 2)[0]]
        return self.selected

    def main(self):
        gtk.main()

if __name__ == "__main__":
    gtkPyContacts = gtkPyContacts()
    gtkPyContacts.main()
    gtkPyContacts.write_contacts()
