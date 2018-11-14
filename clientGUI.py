import wx

class ClientRoomSelector(wx.ScrolledWindow):

    def __init__(self, parent, x_min):
        
        super(ClientRoomSelector, self).__init__(parent, x_min)
        self.SetMinSize((x_min, 1))
        self.SetBackgroundColour((255, 255, 255))



class ClientMessageList(wx.ScrolledWindow):
    
    def __init__(self, parent):
        
        super(ClientMessageList, self).__init__(parent)
        self.SetBackgroundColour((0, 255, 255))



class ClientInput(wx.TextCtrl):
    
    def __init__(self, parent):
        
        super(ClientInput, self).__init__(parent)




class ClientGUI(wx.Frame):
    
    def __init__(self, title):
        
        super(ClientGUI, self).__init__(None, title=title, size=(1024, 1024))
        self.InitMenu()
        self.InitStructure()
        self.Centre()
        self.Maximize()
    
    
    def InitMenu(self):
        
        self.menu_bar = wx.MenuBar()
        # File menu
        self.file_menu = wx.Menu()
        self.file_menu__close = self.file_menu.Append(wx.ID_EXIT, '&Close', 'Close client')
        self.menu_bar.Append(self.file_menu, '&File')
        # User menu
        self.user_menu = wx.Menu()
        self.user_menu__change_nick = self.user_menu.Append(wx.ID_ANY, '&Change nick', 'Change current nick')
        self.menu_bar.Append(self.user_menu, '&User')
        # Set current menu bar
        self.SetMenuBar(self.menu_bar)
        
        # Events
        self.Bind(wx.EVT_MENU, self.OnQuit, self.file_menu__close)
        self.Bind(wx.EVT_MENU, self.OnChangeNick, self.user_menu__change_nick)
    
    
    def InitStructure(self):
        
        # Basic elements
        self.room_selector = ClientRoomSelector(self, 300)
        self.message_list = ClientMessageList(self)
        self.input = ClientInput(self)
        self.input.SetFocus()
        # Chat sizer
        self.chat_sizer = wx.BoxSizer(wx.VERTICAL)
        self.chat_sizer.Add(self.message_list, 1, wx.EXPAND|wx.ALL)
        self.chat_sizer.Add(self.input, 0, wx.EXPAND|wx.ALL)
        # Room selector sizer
        self.room_sizer = wx.BoxSizer(wx.VERTICAL)
        self.room_sizer.Add(self.room_selector, 1, wx.EXPAND|wx.ALL)
        # Main sizer
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.room_sizer, 0, wx.EXPAND|wx.ALL)
        self.main_sizer.Add(self.chat_sizer, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(self.main_sizer)
    
    
    def ChangeNick(self, new_nick):
        
        if len(new_nick) == 0:
            return False
        else:
            print("Nick change request send")
            return True
    
    
    def ShowError(self, message):
        
        wx.MessageDialog(self, message, style=wx.ICON_ERROR|wx.CENTRE).ShowModal()
    
    
    def OnQuit(self, event):
        
        self.Close()
    

    def OnChangeNick(self, event):
        
        self.TryChangeNick()
    
    
    def TryChangeNick(self):
        
        answer_input = wx.TextEntryDialog(self, 'Enter your desired nick:', 'Changing nick', '')
        answer_input.Centre()
        accept = answer_input.ShowModal()
        if accept == wx.ID_OK:
            nick = answer_input.GetValue()
            if not self.ChangeNick(nick):
                self.ShowError("Error changing nick")
                return False
            else:
                return True
        else:
            return False





def main():
    
    app = wx.App()
    client = ClientGUI("Client")
    client.Show(True)
    while not client.TryChangeNick():
        client.ShowError("You must type a nick")
    app.MainLoop()


if __name__ == "__main__":
    
    main()
