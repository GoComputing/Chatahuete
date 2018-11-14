import wx
import wx.lib.scrolledpanel as scrolled


class ClientRoom(wx.Panel):
    
    def __init__(self, parent, x_min, y_min, room_name):
        
        super(ClientRoom, self).__init__(parent)
        self.background_colour = self.GetBackgroundColour()
        self.parent = parent
        self.x_padding = 50
        self.SetMinSize((x_min, y_min))
        self.text = wx.StaticText(self, wx.ID_ANY, room_name, pos=(self.x_padding, self.GetSize()[1]/1.8))
        self.Bind(wx.EVT_LEFT_DOWN, self.OnSelected)
        self.selected = True
        self.Unselect()
        self.room_name = room_name
        self.select_callback = None
    
    
    def Select(self):
        
        if not self.selected:
            self.selected = True
            colour = self.background_colour
            new_colour = (colour[0]*0.9, colour[1]*0.9, colour[2]*0.9, colour[3])
            self.SetBackgroundColour(new_colour)
            self.Refresh()
            self.parent.Refresh()
    
    
    def Unselect(self):
        
        if self.selected:
            self.selected = False
            colour = self.background_colour
            new_colour = (colour[0]*0.8, colour[1]*0.8, colour[2]*0.8, colour[3])
            self.SetBackgroundColour(colour)
            self.Refresh()
    
    
    def SetSelectCallback(self, fnc):
        
        self.select_callback = fnc
    
    
    def OnSelected(self, event):
        
        self.Select()
        if self.select_callback != None:
            self.select_callback(self.room_name)




class ClientRoomSelector(scrolled.ScrolledPanel):

    def __init__(self, parent, x_min):
        
        super(ClientRoomSelector, self).__init__(parent, x_min)
        self.x_min = x_min
        self.y_min = 50
        self.SetMinSize((self.x_min, 1))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.rooms = []
        
        
    def AddRoom(self, room_name):
        
        room = ClientRoom(self, self.x_min, self.y_min, room_name)
        room.SetSelectCallback(self.OnSelectCallback)
        self.rooms.append(room)
        self.sizer.Add(room, 0, wx.EXPAND|wx.ALL)
        self.sizer.AddSpacer(2)
        self.Layout()
        self.SetupScrolling()
    
    
    def OnSelectCallback(self, room_name):
        
        for i,current_room in enumerate(self.rooms):
            if current_room.room_name == room_name:
                current_room.Select()
            else:
                current_room.Unselect()


class ClientMessage(wx.Panel):
    
    def __init__(self, parent, user, message):
        
        super(ClientMessage, self).__init__(parent)
        self.y_tam = 32
        self.x_padding = 20
        # Frames
        self.user_frame = wx.Panel(self)
        self.message_frame = wx.Panel(self)
        # Frame setup
        self.user_frame.SetMinSize((100, self.y_tam))
        self.user_frame.SetMaxSize((100, self.y_tam))
        #self.user_frame.SetBackgroundColour((255, 0, 255))
        colour = self.message_frame.GetBackgroundColour()
        new_colour = (colour[0]*0.9, colour[1]*0.9, colour[2]*0.9, colour[3])
        self.message_frame.SetBackgroundColour(new_colour)
        self.message_frame.SetMaxSize((1000000, self.y_tam))
        # Sizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.user_frame, 0, wx.EXPAND|wx.ALL)
        self.sizer.Add(self.message_frame, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(self.sizer)
        # Text
        self.user_text = wx.StaticText(self.user_frame, wx.ID_ANY, user, pos=(self.x_padding, 5))
        self.message = wx.StaticText(self.message_frame, wx.ID_ANY, message, pos=(self.x_padding, 5))
        self.message_frame.SetMinSize((self.message.GetSize()[0]+3*self.x_padding, self.y_tam))


class ClientMessageList(scrolled.ScrolledPanel):
    
    def __init__(self, parent):
        
        super(ClientMessageList, self).__init__(parent)
        self.parent = parent
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.messages = []
        self.SetSizer(self.sizer)
    
    
    def NewMessage(self, user, message):
        
        message = ClientMessage(self, user, message)
        self.sizer.Add(message, proportion)
        self.sizer.AddSpacer(20)
        self.messages.append(message)
        self.Layout()
        self.SetupScrolling(scrollToTop=False)
        self.ScrollChildIntoView(self.messages[-1])
        self.parent.chat_sizer.Layout()
        self.parent.Fit()



class ClientInput(wx.TextCtrl):
    
    def __init__(self, parent):
        
        super(ClientInput, self).__init__(parent, style=wx.TE_PROCESS_ENTER)




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
        
        # Sizers
        self.chat_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Basic elements
        self.room_selector = ClientRoomSelector(self, 300)
        self.message_list = ClientMessageList(self)
        #self.message_list = ClientMessage(self, "Carlos", "Carlos")
        self.input = ClientInput(self)
        # Chat sizer
        self.chat_sizer.Add(self.message_list, 1, wx.EXPAND|wx.ALL)
        self.chat_sizer.Add(self.input, 0, wx.EXPAND|wx.ALL)
        # Room selector sizer
        self.room_sizer = wx.BoxSizer(wx.VERTICAL)
        self.room_sizer.Add(self.room_selector, 1, wx.EXPAND|wx.ALL)
        # Main sizer
        self.main_sizer.Add(self.room_sizer, 0, wx.EXPAND|wx.ALL)
        self.main_sizer.Add(self.chat_sizer, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(self.main_sizer)
        # Input setup
        self.input.SetFocus()
        self.Bind(wx.EVT_TEXT_ENTER, self.OnNewMessage, self.input)
        
        for i in range(0, 20):
            self.OnNewRoom("Prueba"+str(i))
    
    
    def ChangeNick(self, new_nick):
        
        if len(new_nick) == 0:
            return False
        else:
            print("Nick change request send")
            return True
    
    
    def ShowError(self, message):
        
        wx.MessageDialog(self, message, style=wx.ICON_ERROR|wx.CENTRE).ShowModal()
    
    
    def OnNewMessage(self, event):
        
        if len(self.input.GetValue()) > 0:
            message = self.input.GetValue()
            self.input.SetValue('')
            self.message_list.NewMessage("Carlos", message)
    
    
    def OnNewRoom(self, room_name):
        
        self.room_selector.AddRoom(room_name)
    
    
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
