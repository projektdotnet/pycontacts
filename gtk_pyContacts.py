#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class gtkPyContacts:

    def delete_event(self, widget, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    #Generic callback to use as temporary connector while GTK
    #Items are added before all the callbacks are complete
    def callback(self, widget, data=None):
        print "%s button pressed" % data

    def __init__(self):
        #Start window, declare the callbacks to close the program
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title("pyContacts GTK")
        self.window.set_border_width(5)

        #Define buttons in this area
        btnQuit = gtk.Button("Quit")
        btnNew = gtk.Button("New Contact")
        btnShow = gtk.Button("Show Contact")
        btnEdit = gtk.Button("Edit Contact")
        btnRemove = gtk.Button("Delete Contact")
        btnSave = gtk.Button("Save Contacts")

        #Connect callbacks here
        btnQuit.connect("released", self.destroy)
        btnNew.connect("released", self.callback, "New")
        btnShow.connect("released", self.callback, "Show")
        btnEdit.connect("released", self.callback, "Edit")
        btnRemove.connect("released", self.callback, "Remove")
        btnSave.connect("released", self.callback, "Save")

        #Main window layout, using table style
        buttonTable = gtk.Table(3, 2, True)

        #Window add bits
        self.window.add(buttonTable)

        #Table attachments
        buttonTable.attach(btnNew, 0, 1, 0, 1)
        buttonTable.attach(btnEdit, 1, 2, 0, 1)
        buttonTable.attach(btnShow, 0, 1, 1, 2)
        buttonTable.attach(btnRemove, 1, 2, 1, 2)
        buttonTable.attach(btnSave, 0, 1, 2, 3)
        buttonTable.attach(btnQuit, 1, 2, 2, 3)

        #Widget show calls
        btnNew.show()
        btnEdit.show()
        btnShow.show()
        btnRemove.show()
        btnSave.show()
        btnQuit.show()
        buttonTable.show()
        self.window.show()


    def main(self):
        gtk.main()

if __name__ == "__main__":
    gtkPyContacts = gtkPyContacts()
    gtkPyContacts.main()
