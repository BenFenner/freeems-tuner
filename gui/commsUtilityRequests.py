#   Copyright 2008, 2009 Aaron Barnes
#
#   This file is part of the FreeEMS project.
#
#   FreeEMS software is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   FreeEMS software is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with any FreeEMS software.  If not, see <http://www.gnu.org/licenses/>.
#
#   We ask that if you make any changes to this file you send them upstream to us at admin@diyefi.org


import wx
import gui, commsConnectWarning, comms


class commsUtilityRequests(wx.BoxSizer):

    options = {}
    choices = []
    text = None
    input = None
    send = None

    ID_SEND_REQUEST = wx.NewId()


    def __init__(self, parent):
        '''Setup UI elements'''
        wx.BoxSizer.__init__(self, wx.VERTICAL)
        
        self._controller = parent.controller

        self.text = wx.StaticText(parent, -1, 'Data to request', style=wx.ALIGN_CENTER)

        self.options = comms.getConnection().getProtocol().UTILITY_REQUEST_PACKETS
        self.choices = self.options.keys()

        self.input = wx.Choice(parent, -1, choices=self.choices)
        self.send = wx.Button(parent, self.ID_SEND_REQUEST, 'Send Request')

        self.Add((0,0), 1)
        self.Add(self.text, 3, wx.EXPAND)
        self.Add((0,0), 1)
        self.Add(self.input, 5, wx.EXPAND)
        self.Add((0,0), 1)
        self.Add(self.send, 5, wx.EXPAND)
        self.Add((0,0), 1)

        self.send.Bind(wx.EVT_BUTTON, self.sendRequest, id=self.ID_SEND_REQUEST)


    def sendRequest(self, event):
        '''Send utility request'''
        
        # Check connected
        if not commsConnectWarning.confirmConnected(gui.frame):
            return

        selection = self.input.GetSelection()

        # Correct small bug where selection will be -1 if input has not
        # been in focus
        if selection < 0:
            selection = 0

        data = {'type': self.options[self.choices[selection]]}
        self._controller.action('comms.sendUtilityRequest', data)
