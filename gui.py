# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 23:17:45 2018

@author: Chat
"""

import pip


def install():
    pip.main(['install', 'appJar'])
    pip.main(['install', 'requests'])
    pip.main(['install', 'beautifulsoup4'])
    pip.main(['install', 'weather-api'])

install()#installs dependencies

from appJar import gui
import weather_pjt as w


class MyApplication():

    def Prepare(self, app):
        app.setTitle("Weather Bot")
        app.setFont(16)
        app.setStopFunction(self.BeforeExit)
        app.startLabelFrame("Required Info")
        app.addLabel("location-lbl", "Location:")
        app.addEntry("location")
        app.addLabel("phone-lbl", "Phone Number:")
        app.addEntry("phone")
        app.addLabelOptionBox("Carrier", ["- Your Phone Carrier -", "Verizon", "AT&T", "T-Mobile", "Sprint"])
        app.stopLabelFrame()

        app.addButtons(["Send"], self.Submit, colspan=3)
        app.addMeter("progress")
        app.setMeterFill("progress", "green")

        return app
        
    def Start(self):
        app = gui()
        app = self.Prepare(app)
        self.app = app
        app.go()

    def BeforeExit(self):
        return self.app.yesNoBox("Confirm Exit", "Are you sure you want to exit the application?")
    

    def Submit(self):
        self.app.setMeter("progress", 0)
        your_location = self.app.getEntry("location")
        phone = self.app.getEntry("phone")
        carrier = self.app.getOptionBox("Carrier")
        if w.compose(carrier, phone, your_location) == {}:
            message = "Message Sent Successfully"
            print(message)
            self.app.setMeter("progress", 100, text=message)

if __name__ == '__main__':
    App = MyApplication()
    App.Start()