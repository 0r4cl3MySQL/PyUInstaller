import wx
import Extrascript
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        btn = wx.Button(panel, label="Run Extra Script")
        btn.Bind(wx.EVT_BUTTON, self.on_click)

        vbox.Add(btn, flag=wx.ALL | wx.CENTER, border=10)
        panel.SetSizer(vbox)

        self.SetSize((300, 200))
        self.SetTitle("Test WX App")
        self.SetIcon(wx.Icon(resource_path("appicon.ico")))

    def on_click(self, event):
        wx.MessageBox(Extrascript.say_hello(), "Message", wx.OK | wx.ICON_INFORMATION)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None)
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()