import wx
import server
from threading import Thread
import traceback

class ServerGUI(wx.Frame):
    
    def __init__(self, title):
        
        super(ServerGUI, self).__init__(None, title=title, size=(512, 512))
        self.InitMenu()
        self.InitRoomsview()
        self.Centre()
        self.Maximize()
        # Server initialization
        self.server = server.server(3856, 2)
        self.thread = Thread(target=self.ReceptorThread)
        self.thread.start()
        self.server.set_user_connected_to_room_callback(self.UserConnectedToRoomCallback)
        self.server.set_user_disconnected_callback(self.UserDisconnectedCallback)
        self.server.set_user_nick_changed_callback(self.UserNickChangedCallback)
    
    
    def ReceptorThread(self):
        
        self.server.listen()
    

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
        self.room_users = []
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
            self.room_users.append([])
            self.server.add_room_name(room_name)
            return True
    
    
    def DeleteRoom(self, room_id):
        
        self.server.del_room_name(self.room_names[room_id])
        for user in self.room_users[room_id]:
            self.rooms_view.Delete(user[0])
            user[0].Unset()
        del self.room_users[room_id]
        del self.room_names[room_id]
        self.rooms_view.Delete(self.room_nodes[room_id])
        self.room_nodes[room_id].Unset()
        del self.room_nodes[room_id]
        return True
    
    
    def UserNickChangedCallback(self, room_name, old_nick, new_nick):
        
        self.DeleteUser(room_name, old_nick)
        self.AddUser(room_name, new_nick)
    
    
    def UserConnectedToRoomCallback(self, old_room_name, new_room_name, nick):
        
        self.DeleteUser(old_room_name, nick)
        self.AddUser(new_room_name, nick)
    
    
    def UserDisconnectedCallback(self, nick, current_room_name):
        
        self.DeleteUser(current_room_name, nick)
    
    
    def AddUser(self, room_name, user_name):
        
        if room_name != None:
            try:
                room_index = self.room_names.index(room_name)
                user_item = self.rooms_view.AppendItem(self.room_nodes[room_index], user_name)
                self.room_users[room_index].append([user_item, user_name])
            except Exception as e:
                traceback.print_exc()
                print(e)
                raise
    
    
    def DeleteUser(self, room_name, user_name):
        
        if room_name != None:
            room_index = self.room_names.index(room_name)
            for user_item in self.room_users[room_index]:
                if user_item[1] == user_name:
                    self.rooms_view.Delete(user_item[0])
                    user_item[0].Unset()
                    self.room_users[room_index].remove(user_item)
                    break
    
    
    def OnQuit(self, event):
        
        self.server.signal_close()
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
            traceback.print_exc()
            pass




def main():
    
    app = wx.App()
    window = ServerGUI("Server")
    window.AddRoom("SalaPrueba")
    window.Show(True)
    app.MainLoop()
    window.server.signal_close()



if __name__ == "__main__":
    
    main()
