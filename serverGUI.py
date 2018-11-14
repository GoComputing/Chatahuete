import wx

class ServerGUI(wx.Frame):
    
    def __init__(self, title):
        
        super(ServerGUI, self).__init__(None, title=title, size=(512, 512))
        self.InitMenu()
        self.InitRoomsview()
        self.Centre()
        self.Maximize()
    

    def InitMenu(self):
        
        self.menu_bar = wx.MenuBar()
        # File menu
        self.file_menu = wx.Menu()
        self.file_menu__close = self.file_menu.Append(wx.ID_EXIT, 'Close', 'Close server')
        self.menu_bar.Append(self.file_menu, '&File')
        # Rooms menu
        self.rooms_menu = wx.Menu()
        self.rooms_menu__create = self.rooms_menu.Append(wx.ID_ANY, '&Create room', 'Create a new room')
        self.rooms_menu__delete = self.rooms_menu.Append(wx.ID_ANY, '&Delete room', 'Delete an existing room')
        self.menu_bar.Append(self.rooms_menu, '&Rooms')
        # Set current menu bar
        self.SetMenuBar(self.menu_bar)
        
        # Events
        self.Bind(wx.EVT_MENU, self.OnQuit, self.file_menu__close)
        self.Bind(wx.EVT_MENU, self.OnCreateRoom, self.rooms_menu__create)
        self.Bind(wx.EVT_MENU, self.OnDeleteRoom, self.rooms_menu__delete)
    
    
    def InitRoomsview(self):
        
        # Tree
        self.rooms_view = wx.TreeCtrl(self, wx.ID_ANY, (0,0))
        self.root_node = self.rooms_view.AddRoot("List of rooms created")
        self.room_nodes = []
        self.room_names = []
        self.rooms_view.ExpandAll()
        # Popup menu
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnRightClick)
        self.rooms_view_menu = wx.Menu()
        self.rooms_view_menu__add = self.rooms_view_menu.Append(wx.ID_ANY, 'Create', 'Create a room')
        self.rooms_view_menu__delete = self.rooms_view_menu.Append(wx.ID_ANY, 'Delete', 'Delete this item')
        self.Bind(wx.EVT_MENU, self.OnCreateRoom, self.rooms_view_menu__add)
        self.Bind(wx.EVT_MENU, self.OnDeleteRoomPopup, self.rooms_view_menu__delete)
    
    
    def AddRoom(self, room_name):
        
        if len(room_name) == 0 or room_name in self.room_names:
            return False
        else:
            self.room_nodes.append(self.rooms_view.AppendItem(self.root_node, room_name))
            self.rooms_view.ExpandAll()
            self.room_names.append(room_name)
            return True
    
    
    def DeleteRoom(self, room_id):
        
        del self.room_names[room_id]
        self.rooms_view.Delete(self.room_nodes[room_id])
        self.room_nodes[room_id].Unset()
        del self.room_nodes[room_id]
        return True
    
    
    def OnQuit(self, event):
        
        self.Close()
    

    def ShowError(self, message):
        
        wx.MessageDialog(self, message, style=wx.ICON_ERROR|wx.CENTRE).ShowModal()
    
    
    def OnCreateRoom(self, event):
        
        answer_input = wx.TextEntryDialog(self, "Enter the room name:", "Room creation", '')
        answer_input.Centre()
        accept = answer_input.ShowModal()
        if accept == wx.ID_OK:
            room_name = answer_input.GetValue()
            if not self.AddRoom(room_name):
                self.ShowError("Error creating room")
    
    
    def OnDeleteRoom(self, event):
        
        if len(self.room_names) == 0:
            self.ShowError("There are not any room")
        else:
            answer_input = wx.SingleChoiceDialog(self, "Select room to be deleted:",
                                                 "Room delete", self.room_names, wx.CENTRE)
            accept = answer_input.ShowModal()
            if accept == wx.ID_OK:
                room_id = answer_input.GetSelection()
                if not self.DeleteRoom(room_id):
                    self.ShowError("Error deleting room '"+self.room_names[room_id]+"'")
    
    
    def OnRightClick(self, event):
        
        self.selected_item = event.GetItem()
        self.PopupMenu(self.rooms_view_menu, event.GetPoint())
    
    
    def OnDeleteRoomPopup(self, event):
        
        try:
            index = self.room_nodes.index(self.selected_item)
            room_name = self.room_names[index]
            if not self.DeleteRoom(index):
                self.ShowError("Error deleting room '"+room_name+"'")
        except:
            pass




def main():
    
    app = wx.App()
    window = ServerGUI("Server")
    window.Show(True)
    app.MainLoop()



if __name__ == "__main__":
    
    main()
