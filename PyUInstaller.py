import wx           # Main WX UI Lib
import wx.xrc       # WX additional Lib
import subprocess   # Subprocess Lib
import shlex        # Shlex Lib
import threading    # Threading for Multithread Lib
import json         # Json Lib for Presets and Settings
import pathlib      # Pathlib Lib to find file locations
import os           # OS Lib for OS Paths
import gettext      # GetText Lib
_ = gettext.gettext # GetText additional Lib

# MainFrame class
class MainFrame ( wx.Frame ):

    # MainFrame Init
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=_(u"PyUInstaller"), pos=wx.DefaultPosition,
                          size=wx.Size(500, 800), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # Main Sizer setup
        self.SetSizeHints( wx.Size( 500,800 ), wx.Size( 500,800 ) )

        # Variables declaration
        self.ConfigDir = pathlib.Path("Config")                 # Config Dir
        self.ConfigDir.mkdir(exist_ok=True)                     # Config Dir maker if it is not present
        self.PresetDir = self.ConfigDir / "Presets"             # Preset Dir
        self.PresetDir.mkdir(parents=True, exist_ok=True)       # Preset Dir maker if it is not present
        self.SessionFile = self.ConfigDir / "LastSession.json"  # Session File
        self.BaseDir = pathlib.Path(__file__).parent.resolve()  # App base Dir
        self.ScriptDir = self.BaseDir / "Build"                 # Script Dir
        self.IconDir = self.ScriptDir / "Icon"                  # Icon Dir
        self.OutputDir = self.BaseDir / "Compile"               # Compile Dir
        self.SpecDir = self.ScriptDir / "Spec"                  # Spec Dir

        # SpecFile creator Frame variable declaration
        self.spec_creator = None

        # Presets variable declaration
        self.Presets = None

        # Base AutoSave setup
        self.AutoSaveSession = True

        # Main MenuBar setup
        self.MM_MenuBar = wx.MenuBar(0)

        # File menu Tab
        self.M_MenuFile = wx.Menu()

        # Quit menu SubTab
        self.MI_Quit = wx.MenuItem(self.M_MenuFile, wx.ID_ANY, _(u"Quit") + u"\t" + u"ALT+F4", wx.EmptyString,
                                   wx.ITEM_NORMAL)
        # Quit Bitmap for Quit button
        # noinspection PyTypeChecker
        self.MI_Quit.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_MENU))
        # Quit SubTab add to Main menu
        self.M_MenuFile.Append(self.MI_Quit)

        # File menu add to MenuBar
        self.MM_MenuBar.Append(self.M_MenuFile, _(u"File"))

        # Settings tab Setup
        self.M_MenuSettings = wx.Menu()
        # Settings tab SubTab
        self.MI_AutoSave = self.M_MenuSettings.AppendCheckItem(
           wx.ID_ANY, _(u"Auto-Save Session") + u"\t" + u"CTRL+T"
        )
        # Base state for AutoSave
        self.MI_AutoSave.Check(True)

        # Settings Tab add to MainBer
        self.MM_MenuBar.Append(self.M_MenuSettings, _(u"Settings"))

        # About menu tab Setup
        self.M_MenuAbout = wx.Menu()
        self.MI_Help = wx.MenuItem(self.M_MenuAbout, wx.ID_ANY, _(u"Help") + u"\t" + u"CTRL+H", wx.EmptyString,
                                   wx.ITEM_NORMAL)

        # Help Bitmap for Help button
        # noinspection PyTypeChecker
        self.MI_Help.SetBitmap(wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_MENU))
        # About Tab add to MainMenu
        self.M_MenuAbout.Append(self.MI_Help)

        # About Tab add to MenuBar
        self.MM_MenuBar.Append(self.M_MenuAbout, _(u"About"))

        # Set MenuBar
        self.SetMenuBar(self.MM_MenuBar)

        # VB for MainApp
        VB_MainSizer = wx.BoxSizer(wx.VERTICAL)

        # Source Section WxPanel setup
        self.WP_SourcePanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # VB source panel setup
        VB_SourcePanelSizer = wx.BoxSizer(wx.VERTICAL)

        # VB setup with Source name on it
        VB_SourcePanel = wx.StaticBoxSizer(wx.StaticBox(self.WP_SourcePanel, wx.ID_ANY, _(u"Source")),
                                           wx.VERTICAL)

        # HB in Source VB
        HB_SourcePanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text Label for Script line
        self.Txt_ScriptPath = wx.StaticText(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, _(u"Script:"),
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_ScriptPath.Wrap(-1)

        # Text Label add to HB Source
        HB_SourcePanel.Add(self.Txt_ScriptPath, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL for Script location
        self.TxtCTRL_Script = wx.TextCtrl(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                          wx.DefaultPosition,
                                          wx.DefaultSize, wx.TE_READONLY | wx.TE_RICH | wx.TE_RICH2)
        # Text CTRL tooltip
        self.TxtCTRL_Script.SetToolTip(_(u"Main .py script location"))

        # Set Color of TextCTRL
        self.TxtCTRL_Script.SetBackgroundColour(wx.Colour(240, 240, 240))

        # Text CTRL add to Source HB
        HB_SourcePanel.Add(self.TxtCTRL_Script, 1, wx.ALL, 5)

        # Button of Browse Script
        self.Btn_BrowseScript = wx.Button(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, _(u"Browse Script"),
                                          wx.DefaultPosition, wx.DefaultSize, 0)

        # Button add to Source HB
        HB_SourcePanel.Add(self.Btn_BrowseScript, 0, wx.ALL, 5)

        # VB add of Source HB
        VB_SourcePanel.Add(HB_SourcePanel, 1, wx.EXPAND, 5)

        # Icon HB setup
        HB_IconPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text label Icon path
        self.Txt_Icon = wx.StaticText(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, _(u"Icon:"), wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        self.Txt_Icon.Wrap(-1)

        # Text label add to Icon HB
        HB_IconPanel.Add(self.Txt_Icon, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL for Icon path
        self.TxtCTRL_IconPath = wx.TextCtrl(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize,
                                            wx.TE_READONLY | wx.TE_RICH | wx.TE_RICH2)

        # Set Background for Text CTRL
        self.TxtCTRL_IconPath.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        # Text CTRL Tooltip
        self.TxtCTRL_IconPath.SetToolTip(_(u"Icon used in .py script location"))

        # Optionally, you can make it have some visual "grid" style by adding a background color
        self.TxtCTRL_IconPath.SetBackgroundColour(wx.Colour(240, 240, 240))

        # Text CTRL add to Icon HB
        HB_IconPanel.Add(self.TxtCTRL_IconPath, 1, wx.ALL, 5)

        # Button browse Icon
        self.Btn_BrowseIcon = wx.Button(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, _(u"Browse Icon"),
                                        wx.DefaultPosition, wx.DefaultSize, 0)

        # Button add to Icon HB
        HB_IconPanel.Add(self.Btn_BrowseIcon, 0, wx.ALL, 5)

        # Icon HB add to VB source
        VB_SourcePanel.Add(HB_IconPanel, 1, wx.EXPAND, 5)

        # Extra script HB setup
        HB_ExtraScriptPanel = wx.BoxSizer(wx.HORIZONTAL)

        # CheckBox for use of extra Scripts
        self.ChC_UseExtraScript = wx.CheckBox(VB_SourcePanel.GetStaticBox(), wx.ID_ANY,
                                              _(u"Use Additional Scripts:"),
                                              wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT)

        # CheckBox add for Extra script HB
        HB_ExtraScriptPanel.Add(self.ChC_UseExtraScript, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL of Extra script
        self.TxtCTRL_ExtraScripts = wx.TextCtrl(VB_SourcePanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize, wx.TE_RICH | wx.TE_RICH2)
        # Text CTRL Tooltip
        self.TxtCTRL_ExtraScripts.SetToolTip(
            _(u"Add any Additional Scripts which are Imported in your main .py script, separate by comma"))

        # Disable the TextCtrl by default
        self.TxtCTRL_ExtraScripts.Enable(False)

        # Text CTRL add to Extra script HB
        HB_ExtraScriptPanel.Add(self.TxtCTRL_ExtraScripts, 1, wx.ALL, 5)

        # HB add to VB source
        VB_SourcePanel.Add(HB_ExtraScriptPanel, 1, wx.EXPAND, 5)

        # VB source add to Main WP source
        VB_SourcePanelSizer.Add(VB_SourcePanel, 1, wx.EXPAND | wx.ALL, 5)

        # WxPanel setup
        self.WP_SourcePanel.SetSizer(VB_SourcePanelSizer)
        self.WP_SourcePanel.Layout()
        VB_SourcePanelSizer.Fit(self.WP_SourcePanel)
        VB_MainSizer.Add(self.WP_SourcePanel, 0, wx.EXPAND, 5)

        # WxPanel for Output setup
        self.WP_OutputPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # VB OutputPanel setup
        VB_OutputPanelSizer = wx.BoxSizer(wx.VERTICAL)

        # VB setup with Output label
        VB_OutputFolderPanel = wx.StaticBoxSizer(wx.StaticBox(self.WP_OutputPanel, wx.ID_ANY,
                                                              _(u"Output")), wx.VERTICAL)

        # HB Output setup
        HB_OutputPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text label for Output folder
        self.Txt_OutputFolder = wx.StaticText(VB_OutputFolderPanel.GetStaticBox(), wx.ID_ANY,
                                              _(u"Output folder:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_OutputFolder.Wrap(-1)

        # Text label add to HB Output panel
        HB_OutputPanel.Add(self.Txt_OutputFolder, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL for Output folder
        self.TxtCTRL_OutputFolder = wx.TextCtrl(VB_OutputFolderPanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize, 0)
        # Text CTRL Tooltip
        self.TxtCTRL_OutputFolder.SetToolTip(_(u"Output path where .exe will be saved"))

        # Text CTRL add to HB Output panel
        HB_OutputPanel.Add(self.TxtCTRL_OutputFolder, 1, wx.ALL, 5)

        # Button Browse Output folder
        self.Btn_BrowseOutputFolder = wx.Button(VB_OutputFolderPanel.GetStaticBox(), wx.ID_ANY,
                                                _(u"Browse Output"), wx.DefaultPosition, wx.DefaultSize, 0)

        # Button add to HB Output panel
        HB_OutputPanel.Add(self.Btn_BrowseOutputFolder, 0, wx.ALL, 5)

        # HB add to VB Output panel
        VB_OutputFolderPanel.Add(HB_OutputPanel, 0, wx.EXPAND, 5)

        # VB with extra import panel
        VB_ImportsPanel = wx.StaticBoxSizer(wx.StaticBox(VB_OutputFolderPanel.GetStaticBox(), wx.ID_ANY,
                                                         _(u"Imports")), wx.VERTICAL)

        # HB for HiddenImports
        HB_HiddenImportPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text label for HiddenImports
        self.Txt_HiddenImports = wx.StaticText(VB_ImportsPanel.GetStaticBox(), wx.ID_ANY,
                                               _(u"Hidden imports (comma-separated):"), wx.DefaultPosition,
                                               wx.DefaultSize, 0)
        self.Txt_HiddenImports.Wrap(-1)

        # Text label add to HB HiddenImports
        HB_HiddenImportPanel.Add(self.Txt_HiddenImports, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL for HiddenImports
        self.TxtCTRL_HiddenImports = wx.TextCtrl(VB_ImportsPanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        # Tooltip setup
        self.TxtCTRL_HiddenImports.SetToolTip(
            _(u"Add hidden imports (dependencies), which PyInstaller did not found by usual Import statement "
              u"in script"))

        # Text CTRL add to HB HiddenImports
        HB_HiddenImportPanel.Add(self.TxtCTRL_HiddenImports, 1, wx.ALL, 5)

        # HB add to VB Imports panel
        VB_ImportsPanel.Add(HB_HiddenImportPanel, 1, wx.EXPAND, 5)

        # HB Addi panel setup
        HB_AddiDataPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text label AddiData
        self.Txt_AddiData = wx.StaticText(VB_ImportsPanel.GetStaticBox(), wx.ID_ANY,
                                          _(u"Add-data (format: dest;src):"),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_AddiData.Wrap(-1)

        # Text label add to HB Addi
        HB_AddiDataPanel.Add(self.Txt_AddiData, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL AddiData
        self.TxtCTRL_AddiData = wx.TextCtrl(VB_ImportsPanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        # Text CTRL Tooltip
        self.TxtCTRL_AddiData.SetToolTip(_(u"Add folder/file with extra assets used by script (image, etc..)"))

        # Text CTRL add to HB Addi
        HB_AddiDataPanel.Add(self.TxtCTRL_AddiData, 1, wx.ALL, 5)

        # HB Addi add to VB Imports
        VB_ImportsPanel.Add(HB_AddiDataPanel, 1, wx.EXPAND, 5)

        # VB Imports add to VB Panel
        VB_OutputFolderPanel.Add(VB_ImportsPanel, 1, wx.EXPAND, 5)

        # VB panel add to Main VB
        VB_OutputPanelSizer.Add(VB_OutputFolderPanel, 1, wx.EXPAND | wx.ALL, 5)

        # WxPanel setup
        self.WP_OutputPanel.SetSizer(VB_OutputPanelSizer)
        self.WP_OutputPanel.Layout()
        VB_OutputPanelSizer.Fit(self.WP_OutputPanel)
        VB_MainSizer.Add(self.WP_OutputPanel, 0, wx.EXPAND, 5)

        # WxPanel setup for controls
        self.WP_Controls = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # VB ControlPanel setup
        VB_ControlPanelSizer = wx.BoxSizer(wx.VERTICAL)

        # VB Controls label
        VB_ControlsPanel = wx.StaticBoxSizer(wx.StaticBox(self.WP_Controls, wx.ID_ANY,
                                                          _(u"Controls")), wx.VERTICAL)

        # HB Controls setup
        HB_ControlsPanel = wx.BoxSizer(wx.HORIZONTAL)

        # VB Packing panel setup
        VB_PackingModePanel = wx.StaticBoxSizer(
            wx.StaticBox(VB_ControlsPanel.GetStaticBox(), wx.ID_ANY, _(u"Packaging Mode")), wx.VERTICAL)

        # OneDir CheckBox setup
        self.ChB_OneDir = wx.CheckBox(VB_PackingModePanel.GetStaticBox(), wx.ID_ANY, _(u"One Dir"),
                                      wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        # OneDir Tooltip
        self.ChB_OneDir.SetToolTip(_(u"Adds: \"--onedir\" command"))

        # CheckBox add to VB Panel
        VB_PackingModePanel.Add(self.ChB_OneDir, 0, wx.ALL, 5)

        # OneFile CheckBox setup
        self.ChB_OneFile = wx.CheckBox(VB_PackingModePanel.GetStaticBox(), wx.ID_ANY, _(u"One File"),
                                       wx.DefaultPosition, wx.DefaultSize, 0)
        # OneFile Tooltip
        self.ChB_OneFile.SetToolTip(_(u"Uses: \"--onefile\" command"))

        # CheckBox add to VB Panel
        VB_PackingModePanel.Add(self.ChB_OneFile, 0, wx.ALL, 5)

        # NoConsole CheckBox setup
        self.ChB_NoConsole = wx.CheckBox(VB_PackingModePanel.GetStaticBox(), wx.ID_ANY, _(u"No Console"),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        # NoConsole Tooltip
        self.ChB_NoConsole.SetToolTip(_(u"Uses: \"--noconsole\" command"))

        # CheckBox add to VB Panel
        VB_PackingModePanel.Add(self.ChB_NoConsole, 0, wx.ALL, 5)

        # VB add to HB Controls
        HB_ControlsPanel.Add(VB_PackingModePanel, 1, wx.EXPAND, 5)

        # VB BuildBehavior setup
        VB_BuildBehaviorPanel = wx.StaticBoxSizer(
            wx.StaticBox(VB_ControlsPanel.GetStaticBox(), wx.ID_ANY, _(u"Build Behavior")), wx.VERTICAL)

        # CleanBuild CheckBox setup
        self.ChB_CleanBuild = wx.CheckBox(VB_BuildBehaviorPanel.GetStaticBox(), wx.ID_ANY, _(u"Clean Build"),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        # CleanBuild Tooltip
        self.ChB_CleanBuild.SetToolTip( _(u"Uses: \"--clean\" command") )

        # CheckBox add to VB Panel
        VB_BuildBehaviorPanel.Add(self.ChB_CleanBuild, 0, wx.ALL, 5)

        # OverWrite CheckBox setup
        self.ChB_ConfirmOverwrite = wx.CheckBox(VB_BuildBehaviorPanel.GetStaticBox(), wx.ID_ANY,
                                                _(u"Confirm Overwrite"), wx.DefaultPosition, wx.DefaultSize, 0)
        # OverWrite Tooltip
        self.ChB_ConfirmOverwrite.SetToolTip(_(u"Uses: \"--confirm-overwrite\" command"))

        # CheckBox add to VB Panel
        VB_BuildBehaviorPanel.Add(self.ChB_ConfirmOverwrite, 0, wx.ALL, 5)

        # Debug CheckBox setup
        self.ChB_DebugMode = wx.CheckBox(VB_BuildBehaviorPanel.GetStaticBox(), wx.ID_ANY, _(u"Debug Mode"),
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        # Debug Tooltip
        self.ChB_DebugMode.SetToolTip(_(u"Uses: \"--debug\" command"))

        # CheckBox add to VB Panel
        VB_BuildBehaviorPanel.Add(self.ChB_DebugMode, 0, wx.ALL, 5)

        # VB add to HB Controls
        HB_ControlsPanel.Add(VB_BuildBehaviorPanel, 1, wx.EXPAND, 5)

        # VB Optimization setup
        VB_OptimizationSettingsPanel = wx.StaticBoxSizer(
            wx.StaticBox(VB_ControlsPanel.GetStaticBox(), wx.ID_ANY, _(u"Optimization Settings")),
            wx.VERTICAL)

        # StripBinaries CheckBox setup
        self.ChB_StripBinaries = wx.CheckBox(VB_OptimizationSettingsPanel.GetStaticBox(), wx.ID_ANY,
                                             _(u"Strip Binaries"), wx.DefaultPosition, wx.DefaultSize, 0)
        # StripBinaries Tooltip
        self.ChB_StripBinaries.SetToolTip(_(u"Uses: \"--strip\" command"))

        # CheckBox add to VB Panel
        VB_OptimizationSettingsPanel.Add(self.ChB_StripBinaries, 0, wx.ALL, 5)

        # NoUPX CheckBox setup
        self.ChB_NoUPX = wx.CheckBox(VB_OptimizationSettingsPanel.GetStaticBox(), wx.ID_ANY, _(u"No UPX"),
                                     wx.DefaultPosition, wx.DefaultSize, 0)
        # NoUPX Tooltip
        self.ChB_NoUPX.SetToolTip(_(u"Uses: \"--noupx\" command"))

        # CheckBox add to VB Panel
        VB_OptimizationSettingsPanel.Add(self.ChB_NoUPX, 0, wx.ALL, 5)

        # ForceNoCache CheckBox setup
        self.ChB_ForceNoCache = wx.CheckBox(VB_OptimizationSettingsPanel.GetStaticBox(), wx.ID_ANY,
                                            _(u"Force No-Cache"), wx.DefaultPosition, wx.DefaultSize, 0)
        # ForceNoCache Tooltip
        self.ChB_ForceNoCache.SetToolTip(_(u"Uses: \"--no-cache\" command"))

        # CheckBox add to VB Panel
        VB_OptimizationSettingsPanel.Add(self.ChB_ForceNoCache, 0, wx.ALL, 5)

        # VB add to HB Controls
        HB_ControlsPanel.Add(VB_OptimizationSettingsPanel, 1, wx.EXPAND, 5)

        # HB add to VB Controls panel
        VB_ControlsPanel.Add(HB_ControlsPanel, 0, wx.EXPAND, 5)

        # VB Command preview setup
        VB_CommandPreviewPanel = wx.StaticBoxSizer(
            wx.StaticBox(VB_ControlsPanel.GetStaticBox(), wx.ID_ANY, _(u"Command preview:")), wx.VERTICAL)

        # Text CTRL for CommandPreview
        self.TxtCTRL_CommandPreview = wx.TextCtrl(
            VB_CommandPreviewPanel.GetStaticBox(), wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
            wx.TE_MULTILINE | wx.TE_CHARWRAP
        )
        self.TxtCTRL_CommandPreview.SetMinSize(wx.Size(-1, 45))

        # Text CTRL add to VB CommandPreview
        VB_CommandPreviewPanel.Add(self.TxtCTRL_CommandPreview, 1, wx.EXPAND | wx.ALL, 5)

        # VB add to ControlsPanel
        VB_ControlsPanel.Add(VB_CommandPreviewPanel, 1, wx.EXPAND, 5)

        # VB Compile button setup
        VB_CompileButton = wx.BoxSizer(wx.VERTICAL)

        # Button Compile setup
        self.Btn_Compile = wx.Button(VB_ControlsPanel.GetStaticBox(), wx.ID_ANY, _(u"Compile"),
                                     wx.DefaultPosition, wx.DefaultSize, 0)

        # Compile button add to VB Compile
        VB_CompileButton.Add(self.Btn_Compile, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # VB add to VB Controls
        VB_ControlsPanel.Add(VB_CompileButton, 0, wx.EXPAND, 5)

        # VB add to VB Controls panel
        VB_ControlPanelSizer.Add(VB_ControlsPanel, 1, wx.EXPAND | wx.ALL, 5)

        # WxPanel setup
        self.WP_Controls.SetSizer(VB_ControlPanelSizer)
        self.WP_Controls.Layout()
        VB_ControlPanelSizer.Fit(self.WP_Controls)
        VB_MainSizer.Add(self.WP_Controls, 0, wx.EXPAND, 5)

        # WxPanel setup for OutputLog
        self.WP_OutputLogPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        VB_OutputLogPanelSizer = wx.BoxSizer(wx.VERTICAL)

        # Text label for OutputLog
        VB_OutputLogPanel = wx.StaticBoxSizer(wx.StaticBox(self.WP_OutputLogPanel, wx.ID_ANY,
                                                           _(u"Output log")),wx.VERTICAL)

        # Text CTRL for OutputLog setup
        self.TextCTRL_Output = wx.TextCtrl(VB_OutputLogPanel.GetStaticBox(), wx.ID_ANY, "", wx.DefaultPosition,
                                           wx.DefaultSize,wx.TE_MULTILINE)

        # Text CTRL add to CV OutputLog
        VB_OutputLogPanel.Add(self.TextCTRL_Output, 1, wx.EXPAND | wx.ALL, 5)

        # VB add to VB OutputSizer
        VB_OutputLogPanelSizer.Add(VB_OutputLogPanel, 1, wx.EXPAND | wx.ALL, 5)

        # WxPanel Setup
        self.WP_OutputLogPanel.SetSizer(VB_OutputLogPanelSizer)
        self.WP_OutputLogPanel.Layout()
        VB_OutputLogPanelSizer.Fit(self.WP_OutputLogPanel)
        VB_MainSizer.Add(self.WP_OutputLogPanel, 1, wx.EXPAND, 5)

        # WxPanel Presets setup
        self.WP_PresetsPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # VB Presets setup
        VB_PresetPanelSizer = wx.BoxSizer(wx.VERTICAL)

        # VB Presets label setup
        VB_PresetPanel = wx.StaticBoxSizer(wx.StaticBox(self.WP_PresetsPanel, wx.ID_ANY, _(u"Presets")),
                                           wx.VERTICAL)

        # HB Presets setup
        HB_PresetSelectionPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text label for Presets
        self.Txt_Preset = wx.StaticText(VB_PresetPanel.GetStaticBox(), wx.ID_ANY, _(u"Preset:"),
                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_Preset.Wrap(-1)

        # Text label add to HB Presets
        HB_PresetSelectionPanel.Add(self.Txt_Preset, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # ChoiceBox for Presets selection setup
        self.CCH_PresetChoiceBox = wx.Choice(VB_PresetPanel.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition,
                                             wx.DefaultSize, [], 0)
        # ChoiceBox Tooltip
        self.CCH_PresetChoiceBox.SetToolTip(_(u"Select from existing presets or use Default one"))

        # ChoiceBox add to HB Presets
        HB_PresetSelectionPanel.Add(self.CCH_PresetChoiceBox, 1, wx.ALL, 5)

        # Button SavePresets setup
        self.Btn_SavePreset = wx.Button(VB_PresetPanel.GetStaticBox(), wx.ID_ANY, _(u"Save Preset"),
                                        wx.DefaultPosition, wx.DefaultSize, 0)

        # Button add to HB Presets
        HB_PresetSelectionPanel.Add(self.Btn_SavePreset, 0, wx.ALL, 5)

        # HB Presets add to VB Presets panel
        VB_PresetPanel.Add(HB_PresetSelectionPanel, 1, wx.EXPAND, 5)

        # Splitter for Presets and Spec file
        self.SplitterPresetsSpecFile = wx.StaticLine(VB_PresetPanel.GetStaticBox(), wx.ID_ANY,
                                                     wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)

        # Splitter add to VB Presets panel
        VB_PresetPanel.Add(self.SplitterPresetsSpecFile, 0, wx.EXPAND, 5)

        # HB SpecFile setup
        HB_UseSpecPanel = wx.BoxSizer(wx.HORIZONTAL)

        # CheckBox for use of SpecFile
        self.ChB_UseSpecFile = wx.CheckBox(VB_PresetPanel.GetStaticBox(), wx.ID_ANY,
                                           _(u" Use .spec file instead of script"), wx.DefaultPosition, wx.DefaultSize,
                                           0)

        # ChoiceBox add to HB SpecFile
        HB_UseSpecPanel.Add(self.ChB_UseSpecFile, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # SpecFile creator Button
        self.Btn_CreateSpecFile = wx.Button( VB_PresetPanel.GetStaticBox(), wx.ID_ANY, _(u"SpecFile Creator"),
                                             wx.DefaultPosition, wx.DefaultSize, 0 )

        # Button add to SpecFile HB
        HB_UseSpecPanel.Add( self.Btn_CreateSpecFile, 0, wx.ALL, 5 )


        # HB add to VB Presets
        VB_PresetPanel.Add(HB_UseSpecPanel, 1, wx.EXPAND, 5)

        # HB SpecPanel Setup
        HB_SpecFilePanel = wx.BoxSizer(wx.HORIZONTAL)

        # Text label for Spec File
        self.Txt_SpecFile = wx.StaticText(VB_PresetPanel.GetStaticBox(), wx.ID_ANY, _(u"Spec file:"),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_SpecFile.Wrap(-1)

        # Text label add to HB SpecPanel
        HB_SpecFilePanel.Add(self.Txt_SpecFile, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Text CTRL for SpecFile
        self.TxtCTRL_SpecFile = wx.TextCtrl(VB_PresetPanel.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize,
                                             wx.TE_READONLY | wx.TE_RICH | wx.TE_RICH2)
        # SpecFile Tooltip
        self.TxtCTRL_SpecFile.SetToolTip(_(u"Location of .spec file for compilation instead of .py file"))

        # Text CTRL Color change
        self.TxtCTRL_SpecFile.SetBackgroundColour(wx.Colour(240, 240, 240))

        # Text CTRL add to HB SpecPanel
        HB_SpecFilePanel.Add(self.TxtCTRL_SpecFile, 1, wx.ALL, 5)

        # Button Browse SpecFile
        self.Btn_BrowseSpecFile = wx.Button(VB_PresetPanel.GetStaticBox(), wx.ID_ANY, _(u"Browse Spec"),
                                            wx.DefaultPosition, wx.DefaultSize, 0)

        # Button add to HB SpecPanel
        HB_SpecFilePanel.Add(self.Btn_BrowseSpecFile, 0, wx.ALL, 5)

        # HB add to VB PresetPanel
        VB_PresetPanel.Add(HB_SpecFilePanel, 1, wx.EXPAND, 5)

        # VB add to main VB
        VB_PresetPanelSizer.Add(VB_PresetPanel, 1, wx.EXPAND | wx.ALL, 5)

        # WxPanel setup
        self.WP_PresetsPanel.SetSizer(VB_PresetPanelSizer)
        self.WP_PresetsPanel.Layout()

        # VB Presets panel setup
        VB_PresetPanelSizer.Fit(self.WP_PresetsPanel)
        # VB Main setup
        VB_MainSizer.Add(self.WP_PresetsPanel, 0, wx.EXPAND, 5)

        # Main sizer Set and Layout
        self.SetSizer(VB_MainSizer)
        self.Layout()

        # Center UI and UI setup End
        self.Centre(wx.BOTH)

        # Bind events for buttons
        self.Btn_BrowseScript.Bind(wx.EVT_BUTTON, self.BrowseScript)            # .py Script button
        self.Btn_BrowseIcon.Bind(wx.EVT_BUTTON, self.BrowseIcon)                # Icon button
        self.Btn_BrowseOutputFolder.Bind(wx.EVT_BUTTON, self.BrowseOutput)      # Output folder button
        self.Btn_Compile.Bind(wx.EVT_BUTTON, self.Compile)                      # Compile button

        # Get all CheckBox states
        for cb in [self.ChB_OneFile, self.ChB_OneDir, self.ChB_NoConsole, self.ChB_CleanBuild,
                   self.ChB_ConfirmOverwrite, self.ChB_DebugMode, self.ChB_StripBinaries, self.ChB_NoUPX,
                   self.ChB_ForceNoCache, self.ChC_UseExtraScript]:
            cb.Bind(wx.EVT_CHECKBOX, self.UpdateCommandPreview)                 # States of CheckBoxes to UpdateCommand

        # Get all Text CTRL states
        for txt in [self.TxtCTRL_Script, self.TxtCTRL_IconPath, self.TxtCTRL_ExtraScripts, self.TxtCTRL_OutputFolder,
                    self.TxtCTRL_HiddenImports, self.TxtCTRL_AddiData]:
            txt.Bind(wx.EVT_TEXT, self.UpdateCommandPreview)                    # States of Text CTRL to UpdateCommand

        # Additional Binds for Buttons
        self.Btn_BrowseSpecFile.Bind(wx.EVT_BUTTON, self.BrowseSpec)            # .spec file Browse button
        self.Btn_SavePreset.Bind(wx.EVT_BUTTON, self.SavePreset)                # Save preset button
        # Additional Bind for CheckBox
        self.ChB_UseSpecFile.Bind(wx.EVT_CHECKBOX, self.ToggleSpecUsage)        # Use .spec file CheckBox
        # Additional Bind for ChoiceBox
        self.CCH_PresetChoiceBox.Bind(wx.EVT_CHOICE, self.LoadSelectedPreset)   # Load selected Preset

        # Load presets in first run
        self.LoadPresets()
        # Load last session from json file
        self.LoadLastSession()
        # Lastly load selected preset
        self.LoadSelectedPreset(self)

        # Unique IDs for your shortcuts
        ID_QUIT = wx.NewIdRef()             # Quit ID
        ID_AUTOSAVE_TOGGLE = wx.NewIdRef()  # AutoSave ID
        ID_HELP = wx.NewIdRef()             # Help ID
        ID_COMPILE = wx.NewIdRef()          # Compile ID

        # Define the accelerator table
        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, wx.WXK_F4, ID_QUIT),             # ALT+F4 for Quit
            (wx.ACCEL_CTRL, ord('T'), ID_AUTOSAVE_TOGGLE),  # CTRL+T for AutoSave Toggle
            (wx.ACCEL_CTRL, ord('H'), ID_HELP),             # CTRL+H for Help
            (wx.ACCEL_NORMAL, wx.WXK_F5, ID_COMPILE),       # F5 Key for Compile
        ])

        # Set AccelTable with ShortCuts
        self.SetAcceleratorTable(accel_tbl)

        # Bind events to Accel table
        self.Bind(wx.EVT_MENU, self.OnClose, id=ID_QUIT)                    # Bind event for Quit
        self.Bind(wx.EVT_MENU, self.ToggleAutoSave, id=ID_AUTOSAVE_TOGGLE)  # Bind event for AutoSave
        self.Bind(wx.EVT_MENU, self.Help, id=ID_HELP)                       # Bind event for Help
        self.Bind(wx.EVT_MENU, self.Compile, id=ID_COMPILE)                 # Bind event for Compile

        # Bind the key down event for Backspace
        self.TxtCTRL_Script.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)            # Bind event to clean Script file
        self.TxtCTRL_IconPath.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)          # Bind event to clean Icon file
        self.TxtCTRL_SpecFile.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)          # Bind event to clean Spec file

        # Bind Event for ExtraScript CheckBox
        self.ChC_UseExtraScript.Bind(wx.EVT_CHECKBOX, self.OnCheckboxToggle) # Bind event for ExtraScript CheckBox

        # Bind menu item events for Quit and Help
        self.Bind(wx.EVT_MENU, self.OnClose, self.MI_Quit)                   # Bind event for Quit menu button
        self.Bind(wx.EVT_MENU, self.Help, self.MI_Help)                      # Bind event for Help menu button

        # Bind SpecFile Button to open SpecFile Creator
        self.Btn_CreateSpecFile.Bind(wx.EVT_BUTTON, self.OnOpenSpecCreator)  # Bind event for

    # Handles the checkbox toggle to enable or disable TxtCTRL_ExtraScripts based on selection
    def OnCheckboxToggle(self, event):
        if self.ChC_UseExtraScript.IsChecked():
            # Enable TextCtrl if checkbox is checked
            self.TxtCTRL_ExtraScripts.Enable(True)
            self.UpdateCommandPreview(self)
        else:
            # Disable TextCtrl if checkbox is unchecked
            self.TxtCTRL_ExtraScripts.Enable(False)
            self.UpdateCommandPreview(self)

    # Toggle if app should AutoSave it´s state to session file or not
    def ToggleAutoSave(self, event):

        # Get state and check if AutoSave is ticked
        current_state = self.MI_AutoSave.IsChecked()
        self.MI_AutoSave.Check(not current_state)
        self.AutoSaveSession = not current_state
        # Show small popup with AutoSave Enabled or Disabled based on Tick state
        msg = "Auto-Save is now " + ("enabled" if self.AutoSaveSession else "disabled")
        # Show message
        AutoSaveInfoPopUp(self, msg)

    # Help dialog setup from menu
    def Help(self, event):
        # Call Dialog and show it
        dlg = DG_HelpDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    # Load Json file
    @staticmethod
    def LoadJson( file):
        if file.exists():
            # Read Json file
            with open(file, "r") as f:
                return json.load(f)
        # Return what is in Json file
        return {}

    # Save Json file
    @staticmethod
    def SaveJson(file, data):
        # Write Json file
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    # Browse Icon folder where Icon for app is saved
    def BrowseScript(self, event):

        # Default Dir set for first time in Build
        default_dir = self.ScriptDir if not self.TxtCTRL_Script.GetValue() else ""

        # Open Dialog to select folder
        with wx.FileDialog(self, "Choose script", defaultDir=str(default_dir),
                           wildcard="Python files (*.py)|*.py") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                # Get folder place from dialog
                self.TxtCTRL_Script.SetValue(dlg.GetPath())
                # Update CommandPreview window
                self.UpdateCommandPreview(None)

    # Browse Icon folder where Icon for app is saved
    def BrowseIcon(self, event):

        # Default Dir set for first time in Build
        default_dir = self.IconDir if not self.TxtCTRL_IconPath.GetValue() else ""

        # Open Dialog to select folder
        with wx.FileDialog(self, "Choose icon", defaultDir=str(default_dir),
                           wildcard="Icon files (*.ico)|*.ico") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                # Get folder place from dialog
                self.TxtCTRL_IconPath.SetValue(dlg.GetPath())
                # Update CommandPreview window
                self.UpdateCommandPreview(None)

    # Browse Output folder where final EXE will be saved to based on Flags settings
    def BrowseOutput(self, event):

        # Default Dir set for first time in App/Compile
        default_dir = self.OutputDir if not self.TxtCTRL_OutputFolder.GetValue() else ""

        # Open Dialog to select folder
        with wx.DirDialog(self, "Choose output folder", defaultPath=str(default_dir)) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                # Get folder place from dialog
                self.TxtCTRL_OutputFolder.SetValue(dlg.GetPath())
                # Update CommandPreview window
                self.UpdateCommandPreview(None)

    # Build command into command preview window from flags
    def BuildCommand(self):

        # Start with PyInstaller and then rest
        cmd = ["pyinstaller"]

        # Ensure mutually exclusive flags are not used together - OneDir X OneFile
        if self.ChB_OneDir.GetValue() and self.ChB_OneFile.GetValue():
            wx.MessageBox("You can't use --onedir and --onefile together.", "Flags conflict",
                          wx.ICON_ERROR)
            # If used clean both to make sure no conflict happens
            self.ChB_OneDir.SetValue(False)     # Set OneDir to False
            self.ChB_OneFile.SetValue(False)    # Set OneFile to False

        # Ensure mutually exclusive flags are not used together - Clean X NoUPX
        if self.ChB_CleanBuild.GetValue() and self.ChB_NoUPX.GetValue():
            wx.MessageBox("You can't use --clean and --noupx together.", "Flags conflict",
                          wx.ICON_ERROR)
            # If used clean both to make sure no conflict happens
            self.ChB_CleanBuild.SetValue(False) # Set Clean to False
            self.ChB_NoUPX.SetValue(False)      # Set NoUPX to False

        # Add the relevant flags based on user input
        if self.ChB_OneDir.GetValue():
            cmd.append("--onedir")                  # OneDir flag
        if self.ChB_OneFile.GetValue():
            cmd.append("--onefile")                 # OneFile flag
        if self.ChB_NoConsole.GetValue():
            cmd.append("--noconsole")               # NoConsole flag
        if self.ChB_CleanBuild.GetValue():
            cmd.append("--clean")                   # Clean flag
        if self.ChB_ConfirmOverwrite.GetValue():
            cmd.append("--confirm-overwrite")       # OverWrite flag
        if self.ChB_DebugMode.GetValue():
            cmd.append("--debug")                   # Debug flag
        if self.ChB_StripBinaries.GetValue():
            cmd.append("--strip")                   # Strip flag
        if self.ChB_NoUPX.GetValue():
            cmd.append("--noupx")                   # NoUPX flag
        if self.ChB_ForceNoCache.GetValue():
            cmd.append("--no-cache")                # NoCache flag

        # Add the icon path if specified
        icon = self.TxtCTRL_IconPath.GetValue()
        if icon:
            cmd.append(f"--icon={icon}")

        # Add the output path if specified
        output = self.TxtCTRL_OutputFolder.GetValue()
        if output:
            cmd.append(f"--distpath={output}")

        # Add hidden imports if specified
        hidden = self.TxtCTRL_HiddenImports.GetValue().strip()
        if hidden:
            for imp in hidden.split(','):
                cmd.append(f"--hidden-import={imp.strip()}")

        # Add additional data if specified
        data = self.TxtCTRL_AddiData.GetValue().strip()
        if data:
            cmd.append(f"--add-data={data}")

        # Add the main script file
        script = self.TxtCTRL_Script.GetValue()
        if script:
            cmd.append(script)

        # Check if the "Use Additional Scripts" checkbox is checked
        if self.ChC_UseExtraScript.GetValue():
            # Get the extra scripts from the text control
            extra_scripts = self.TxtCTRL_ExtraScripts.GetValue().strip()
            if extra_scripts:
                for extra_script in extra_scripts.split(','):
                    cmd.append(f"--hidden-import={extra_script.strip()}")
        else:
            # If checkbox is unchecked, remove any extra scripts from the command
            extra_scripts = self.TxtCTRL_ExtraScripts.GetValue().strip()
            if extra_scripts:
                # To remove any extra scripts previously added, we need to check and remove them
                cmd = [arg for arg in cmd if not arg.startswith("--hidden-import=")]

        # Return full Command into CMD variable
        return cmd

    # Update Command preview Window in app
    def UpdateCommandPreview(self, event):

        # Get data from Build Command
        cmd = self.BuildCommand()

        # If we use .spec file ignore Script file and use .spec file
        if self.ChB_UseSpecFile.GetValue():
            if self.TxtCTRL_SpecFile.GetValue():
                # Get .spec file else go for Script
                cmd.append(self.TxtCTRL_SpecFile.GetValue())
        else:
            # Get Script file as .spec is not ticked
            if self.TxtCTRL_Script.GetValue():
                cmd.append(self.TxtCTRL_Script.GetValue())

        # Set preview of command in TextCTRL
        self.TxtCTRL_CommandPreview.SetValue(" ".join(shlex.quote(c) for c in cmd))

    # Main Compile Function which generates full command for RunPyInstaller
    def Compile(self, event):

        #Get data from Text CTRLs
        script = self.TxtCTRL_Script.GetValue().strip()         # Get Main script
        icon = self.TxtCTRL_IconPath.GetValue().strip()         # Get Icon
        output = self.TxtCTRL_OutputFolder.GetValue().strip()   # Get Output location
        spec_file = self.TxtCTRL_SpecFile.GetValue().strip()    # Get .spec file

        # Check for missing fields
        if not script and not spec_file or not icon or not output:
            wx.MessageBox(
                "Script path, Icon path, Output path, and (optional) Spec file must be set. "
                "There's nothing to compile.",
                "Required Data Missing",
                wx.OK | wx.ICON_ERROR
            )
            return

        # Check if either the script or spec file is valid
        if not (os.path.isfile(script) or os.path.isfile(spec_file)):
            wx.MessageBox(
                "The specified script or .spec file is not valid or doesn't exist. "
                "Please check the file paths.",
                "Invalid File",
                wx.OK | wx.ICON_ERROR
            )
            return

        # Check if icon path is a valid file (optional)
        if not os.path.isfile(icon):
            wx.MessageBox(
                "The icon file path is invalid. Please check the file path.",
                "Invalid Icon File",
                wx.OK | wx.ICON_ERROR
            )
            return

        # Check if output folder is valid (optional)
        if not os.path.isdir(output):
            wx.MessageBox(
                "The output folder is invalid. Please check the output path.",
                "Invalid Output Folder",
                wx.OK | wx.ICON_ERROR
            )
            return

        # Build the command and start the compilation process
        cmd = self.BuildCommand()
        # Print Compiling info to Output window
        self.TextCTRL_Output.SetValue("Compiling...\n")
        # Put it on separate thread
        thread = threading.Thread(target=self.RunPyinstaller, args=(cmd,))
        thread.start()

    # Run PyInstaller from "created" command
    def RunPyinstaller(self, cmd):

        try:
            # Get process of CMD to put Command in
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in process.stdout:
                # Print state to Output window
                wx.CallAfter(self.TextCTRL_Output.AppendText, line)
            process.wait()
            # Finish with Done in Output window
            wx.CallAfter(self.TextCTRL_Output.AppendText, "\nDone.")
            # If any errors are found print it
        except Exception as e:
            wx.CallAfter(self.TextCTRL_Output.AppendText, f"\nError: {str(e)}")

    # Load Presets from file
    def LoadPresets(self):

        # Preset Variable setup
        self.Presets = {}
        # Clean ChoiceBox
        self.CCH_PresetChoiceBox.Clear()

        # Get all presets in PresetDirectory - .json file
        for file in self.PresetDir.glob("*.json"):
            name = file.stem

            # Get name of preset and Load it - .json file
            self.Presets[name] = self.LoadJson(file)
            self.CCH_PresetChoiceBox.Append(name)

        # If there are none then Set selection to 0
        if self.CCH_PresetChoiceBox.GetCount() > 0:
            self.CCH_PresetChoiceBox.SetSelection(0)

    # Save Presets from CurrentState + Show name dialog
    def SavePreset(self, event):

        # Open Preset name dialog
        dlg = wx.TextEntryDialog(self, "Enter preset name:")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue().strip()
            if not name:
                return

            # Save individual file
            preset_path = self.PresetDir / f"{name}.json"
            self.SaveJson(preset_path, self.GetCurrentState())

            # Run LoadPreset to see them immediately after Save
            self.LoadPresets()
            self.CCH_PresetChoiceBox.SetStringSelection(name)

    # Load data from Preset file
    def LoadSelectedPreset(self, event):

        # Get Preset ChoiceBox selection
        name = self.CCH_PresetChoiceBox.GetStringSelection()

        # Get data from preset and Update UI + Commands
        if name in self.Presets:
            self.SetState(self.Presets[name])
            self.UpdateCommandPreview(None)

    # Get CurrentState of Controls in App
    def GetCurrentState(self):
        return {
            # Main 3 Text CTRLs data getters
            "script_path": self.TxtCTRL_Script.GetValue(),
            "icon_path": self.TxtCTRL_IconPath.GetValue(),
            "extra_path": self.TxtCTRL_ExtraScripts.GetValue(),

            # Output Text CTRL data getters
            "output_path": self.TxtCTRL_OutputFolder.GetValue(),

            # Addi Text CTRL data getters
            "hidden_imports": self.TxtCTRL_HiddenImports.GetValue(),
            "add_data": self.TxtCTRL_AddiData.GetValue(),

            # SpecFile Text CTRL data getters
            "spec_path": self.TxtCTRL_SpecFile.GetValue(),

            # Controls CheckBoxes data getters
            "onedir": self.ChB_OneDir.GetValue(),
            "onefile": self.ChB_OneFile.GetValue(),
            "noconsole": self.ChB_NoConsole.GetValue(),
            "clean-build": self.ChB_CleanBuild.GetValue(),
            "confirm-overwrite": self.ChB_ConfirmOverwrite.GetValue(),
            "debug": self.ChB_DebugMode.GetValue(),
            "strip-bin": self.ChB_StripBinaries.GetValue(),
            "no-upx": self.ChB_NoUPX.GetValue(),
            "no-cache": self.ChB_ForceNoCache.GetValue(),
            "use-spec": self.ChB_UseSpecFile.GetValue(),

            # Preset file selection data getters
            "preset-name": self.CCH_PresetChoiceBox.GetStringSelection()
        }

    # SetState of Controls from App
    def SetState(self, data):

        # Main 3 Text CTRLs Value sets from Preset
        self.TxtCTRL_Script.SetValue(data.get("script_path", ""))
        self.TxtCTRL_IconPath.SetValue(data.get("icon_path", ""))
        self.TxtCTRL_ExtraScripts.SetValue(data.get("extra_path", ""))

        # Output Text CTRL Value sets from Preset
        self.TxtCTRL_OutputFolder.SetValue(data.get("output_path", ""))

        # Addi Text CTRL Value sets from Preset
        self.TxtCTRL_HiddenImports.SetValue(data.get("hidden_imports", ""))
        self.TxtCTRL_AddiData.SetValue(data.get("add_data", ""))

        # SpecFile Text CTRL Value sets from Preset
        self.TxtCTRL_SpecFile.SetValue(data.get("spec_path", ""))

        # Controls CheckBoxes Value sets from Preset
        self.ChB_OneDir.SetValue(data.get("onedir", False))
        self.ChB_OneFile.SetValue(data.get("onefile", False))
        self.ChB_NoConsole.SetValue(data.get("noconsole", False))
        self.ChB_CleanBuild.SetValue(data.get("clean-build", False))
        self.ChB_ConfirmOverwrite.SetValue(data.get("confirm-overwrite", False))
        self.ChB_DebugMode.SetValue(data.get("debug", False))
        self.ChB_StripBinaries.SetValue(data.get("strip-bin", False))
        self.ChB_NoUPX.SetValue(data.get("no-upx", False))
        self.ChB_ForceNoCache.SetValue(data.get("no-cache", False))
        self.ChB_UseSpecFile.SetValue(data.get("use-spec", False))

        # Preset file selection
        PresetName = data.get("preset-name", "")

        # Select last preset in Preset ChoiceBox
        if PresetName and PresetName in self.Presets:

            # Set selection in ChoiceBox
            self.CCH_PresetChoiceBox.SetStringSelection(PresetName)

        # Rest pass
        self.ToggleSpecUsage(None)

    # Save last session to file
    def SaveLastSession(self):

        # Get current state and save it to file
        self.SaveJson(self.SessionFile, self.GetCurrentState())

    # Load last session from SessionFile
    def LoadLastSession(self):

        # Check if SessionFile exists
        if self.SessionFile.exists():
            # If yes load it
            self.SetState(self.LoadJson(self.SessionFile))
            self.UpdateCommandPreview(None)

    # Toggle for using Spec file from usual .py scrip
    def ToggleSpecUsage(self, event):

        # Get CheckBox value
        UsingSpec = self.ChB_UseSpecFile.GetValue()
        self.TxtCTRL_Script.Enable(not UsingSpec)

    # Browse Spec file location with dialog
    def BrowseSpec(self, event):

        # Open with FileDialog to select SpecFile
        with wx.FileDialog(
                self,"Choose .spec file", defaultDir=str(self.SpecDir),
                wildcard="Spec files (*.spec)|*.spec") as dlg:

            # Get Selected Spec file and load it to Command
            if dlg.ShowModal() == wx.ID_OK:
                self.TxtCTRL_SpecFile.SetValue(dlg.GetPath())
                self.UpdateCommandPreview(None)

    # Handles key down events for the Backspace key
    def OnKeyDown(self, event):

        # Setup local variables
        FocusedCtrl = self.FindFocus()
        KeyCode = event.GetKeyCode()

        # Handle Backspace (WXK_BACK) for read-only text controls
        if FocusedCtrl in (self.TxtCTRL_Script, self.TxtCTRL_IconPath, self.TxtCTRL_SpecFile):
            if KeyCode == wx.WXK_BACK:
                # noinspection PyUnresolvedReferences
                FocusedCtrl.Clear()  # Clear the text of the focused read-only TextCtrl
                return  # Prevent further handling of the key event

        event.Skip()  # Allow normal behavior for other controls

    # Open SpecFile Creator Window - Frame
    def OnOpenSpecCreator(self, event):

        Data = {
            "script": self.TxtCTRL_Script.GetValue(),
            "app_name": pathlib.Path(self.TxtCTRL_Script.GetValue()).stem if self.TxtCTRL_Script.GetValue() else "",
            "icon": self.TxtCTRL_IconPath.GetValue(),
            "bin_folder": "bin",
            "console": not self.ChB_NoConsole.GetValue(),
            "onedir": self.ChB_OneDir.GetValue(),
            "onefile": self.ChB_OneFile.GetValue(),
            "hidden_imports": self.TxtCTRL_HiddenImports.GetValue(),
            "data_file": self.TxtCTRL_AddiData.GetValue(),
            "binaries": "",  # You can fetch from somewhere if applicable
            "pathex": str(self.ScriptDir),
            "excludes": ""
        }

        dlg = DG_SpecFileCreator(self, Data)
        dlg.ShowModal()

    # Close app + Confirm dialog
    def OnClose(self, event):

        # Small confirm dialog setup
        dlg = wx.MessageDialog(
            self,
            "Are you sure you want to quit?",
            "Quit PyUInstaller",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        )

        # Show dialog
        result = dlg.ShowModal()
        dlg.Destroy()

        # If Pressed yes in dialog close app
        if result == wx.ID_YES:
            if getattr(self, "AutoSaveSession", False):  # Safe check
                self.SaveLastSession()
            # Close app
            self.Destroy()

    # CleanUp function
    def __del__( self ):
        pass
# Autosave information dialog PopUp
class AutoSaveInfoPopUp(wx.Dialog):

    # Dialog init Setup
    def __init__(self, parent, message, timeout=500):  # timeout in milliseconds
        super().__init__(parent, title="", style=wx.STAY_ON_TOP | wx.BORDER_SIMPLE)

        # Background setup
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.timeout = timeout

        # Create simple UI layout
        VB_MainSizer = wx.BoxSizer(wx.VERTICAL)
        Txt_Label = wx.StaticText(self, label=message)
        VB_MainSizer.Add(Txt_Label, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.SetSizerAndFit(VB_MainSizer)

        # Center UI
        self.CenterOnParent()
        self.Show()

        # Automatically close after timeout
        wx.CallLater(self.timeout, self.Close)

# Help Dialog setup
class DG_HelpDialog ( wx.Dialog ):

    # Help dialog Init
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"PyUInstaller Help"),
                             pos = wx.DefaultPosition,  size=wx.Size(500, 600), style = wx.DEFAULT_DIALOG_STYLE )

        # Set Dialog size
        self.SetSizeHints( wx.Size( 500,600 ), wx.DefaultSize )

        # VB Main sizer setup
        VB_MainSizer = wx.BoxSizer( wx.VERTICAL )

        # WxPanel setup
        self.WP_MainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        # VB Help label sizer
        VB_HelpText = wx.StaticBoxSizer( wx.StaticBox( self.WP_MainPanel, wx.ID_ANY, _(u"Help") ),
                                         wx.VERTICAL )

        # TextCTRL with help text
        self.TxtCTRL_HelpText = wx.TextCtrl( VB_HelpText.GetStaticBox(), wx.ID_ANY,
                                             _(u"PyUInstaller - Help Guide\n==========================\n\nThis "
                                               u"application is a GUI front-end for PyInstaller to make creating "
                                               u"standalone executables from Python scripts easier."
                                               u"\n\n--------------------------------------------------\n1. "
                                               u"Basic Workflow\n--------------------------------------------------\n1."
                                               u" Select your main Python script using the [Browse Script] button.\n2. "
                                               u"Optionally choose an icon using [Browse Icon].\n3. Choose output "
                                               u"folder where the executable will be saved.\n4. Optionally add:\n   "
                                               u"- Additional hidden imports\n   - Data files (e.g., images, configs)\n"
                                               u"   - Additional scripts\n5. Customize build options using the "
                                               u"checkboxes:\n   - One File vs. One Dir\n   - No Console, Clean Build,"
                                               u" Debug Mode, etc.\n6. Click [Compile] to generate the executable."
                                               u"\n\n--------------------------------------------------\n2. Key"
                                               u" Features\n--------------------------------------------------\n-"
                                               u" **Presets**:\n  Save and load configurations for different projects."
                                               u"\n- **Spec File Support**:\n  Use .spec file instead of standard "
                                               u"script build.\n- **Auto-Save**:\n  Automatically stores session data"
                                               u" (can be disabled in Settings)."
                                               u"\n\n--------------------------------------------------\n3. Panel "
                                               u"Overview\n--------------------------------------------------\n- "
                                               u"**Source Panel**:\n  - Script: Main .py file\n  - Icon: Optional "
                                               u".ico file\n  - Use Additional Scripts: Include imported scripts"
                                               u" manually\n  \n- **Output Panel**:\n  - Output Folder: Where final "
                                               u".exe is placed\n  - Hidden Imports: Include modules PyInstaller may "
                                               u"miss\n  - Add-Data: Format `src;dest` (e.g., `assets;assets`)\n\n-"
                                               u" **Controls Panel**:\n  - Build flags like --onedir, --onefile, "
                                               u"--noconsole, --debug, etc.\n  - Real-time command preview at bottom"
                                               u"\n\n- **Output Log**:\n  - Shows compilation output and errors\n\n- "
                                               u"**Presets Panel**:\n  - Load, save, and manage build presets\n  - "
                                               u".spec file toggle if you want full PyInstaller control"
                                               u"\n\n--------------------------------------------------\n4. "
                                               u"Tips & Notes\n--------------------------------------------------\n- "
                                               u"Avoid using --onedir and --onefile together (mutually exclusive).\n- "
                                               u"Same for --clean and --noupx – cannot be used together.\n- Ensure "
                                               u"paths are correct (valid file/folder).\n- Script and icon must exist "
                                               u"and be accessible.\n- Data folders in Add-Data must use `src;dest` "
                                               u"format.\n\n--------------------------------------------------\n5. "
                                               u"Keyboard Shortcuts\n-------------------------------------------------"
                                               u"-\n- ALT + F4 : Quit\n- CTRL + T : Toggle Auto-Save\n- CTRL + H : "
                                               u"Help\n- F5       : Compile\n\n---------------------------------------"
                                               u"-----------\n6. Troubleshooting\n------------------------------------"
                                               u"--------------\n- If nothing compiles, check if required paths are "
                                               u"missing.\n- Ensure dependencies are correctly added in Hidden Imports."
                                               u"\n- Read output log for PyInstaller errors."
                                               u"\n\n--------------------------------------------------\n7. Spec "
                                               u"File Creator (Advanced)"
                                               u"\n--------------------------------------------------\n- Use the"
                                               u" [SpecFile Creator] button to generate a .spec file for full control"
                                               u" over your build.\n- Fill in:\n  - Script Path: Main Python file\n  - "
                                               u"App Name: Executable name\n  - Icon Path (optional)\n  - Additional "
                                               u"inputs like hidden imports, binaries, data files, path exclusions, "
                                               u"etc.\n- A live preview of the spec file is shown in the preview box."
                                               u"\n- When ready, click **Generate** to save the .spec file anywhere.\n-"
                                               u" You can then use this .spec file from the main window by enabling the"
                                               u" **Use .spec file** option in the Presets panel."
                                               u"\n\n--------------------------------------------------\nThank you "
                                               u"for using PyUInstaller!"),
                                             wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER|wx.TE_MULTILINE|
                                             wx.TE_READONLY|wx.TE_RICH2|wx.TE_RIGHT )

        # Text CTRL Font settings
        self.TxtCTRL_HelpText.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(),
                                                wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                                                False, wx.EmptyString ) )

        # TextCTRL add to VB Help label
        VB_HelpText.Add( self.TxtCTRL_HelpText, 1, wx.ALL|wx.EXPAND, 5 )

        # VB Help label add to main WxPanel
        self.WP_MainPanel.SetSizer( VB_HelpText )
        self.WP_MainPanel.Layout()

        # VB add to WxPanel
        VB_HelpText.Fit( self.WP_MainPanel )
        VB_MainSizer.Add( self.WP_MainPanel, 1, wx.EXPAND |wx.ALL, 5 )

        # VB Close button setup
        VB_CloseButton = wx.BoxSizer( wx.VERTICAL )

        # CloseButton setup
        self.Btn_Close = wx.Button( self, wx.ID_ANY, _(u"Ok"), wx.DefaultPosition, wx.DefaultSize, 0 )

        # Close button add to VB CloseButton
        VB_CloseButton.Add( self.Btn_Close, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        # Close button VB add to Main VB
        VB_MainSizer.Add( VB_CloseButton, 0, wx.EXPAND, 5 )

        # Sizer setup
        self.SetSizer( VB_MainSizer )

        # UI Layout
        self.Layout()

        # UI Center
        self.Centre( wx.BOTH )

        # Bind Event for Close button
        self.Btn_Close.Bind(wx.EVT_BUTTON, self.CloseHelpDG)

    # Close dialog from Close Button
    def CloseHelpDG(self, event):
        self.EndModal(wx.ID_OK)

    # CleanUp function
    def __del__( self ):
        pass


# Spec file creator class
class DG_SpecFileCreator ( wx.Dialog ):
    def __init__(self, parent, Data=None):

        # Dialog main setup
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"SpecFile Creator"), pos = wx.DefaultPosition,
                             size = wx.Size( 700,700 ), style = wx.DEFAULT_DIALOG_STYLE )


        # Variables declaration
        self.script_path = None
        self.app_name = None
        self.icon_path = None
        self.bin_name = None
        self.chk_console = None
        self.bin_name = None
        self.chk_onefile = None
        self.hidden_imports = None
        self.datas = None
        self.binaries = None
        self.pathex = None
        self.excludes = None
        self.preview = None

        # Dialog main frame size
        self.SetSizeHints( wx.Size( 700,700 ), wx.Size( 700,700 ) )

        # Main Sizer setup
        VB_MainSizer = wx.BoxSizer( wx.VERTICAL )

        # Source WxPanel setup
        self.WP_SourcePanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        VB_Source = wx.BoxSizer( wx.VERTICAL )

        # Source VerticalBox sizer setup
        VB_SourceSizer = wx.StaticBoxSizer( wx.StaticBox( self.WP_SourcePanel, wx.ID_ANY, _(u"Source") ), wx.VERTICAL )

        # HorizontalBox for Script setup
        HB_ScriptSizer = wx.BoxSizer( wx.HORIZONTAL )

        # Text label for Script
        self.Txt_Script = wx.StaticText( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, _(u"Script Path:"),
                                         wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_Script.Wrap( -1 )

        # Text label add to HorizontalBox Script
        HB_ScriptSizer.Add( self.Txt_Script, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control for script setup
        self.TxtCTRL_Script = wx.TextCtrl( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_ScriptSizer.Add( self.TxtCTRL_Script, 1, wx.ALL, 5 )

        # Script Browse setup
        self.Btn_Script = wx.Button( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, _(u"Browse"),
                                     wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_ScriptSizer.Add( self.Btn_Script, 0, wx.ALL, 5 )

        # Script HorizontalBox add to Source VerticalBox
        VB_SourceSizer.Add( HB_ScriptSizer, 1, wx.EXPAND, 5 )

        # HorizontalBox AppName setup
        HB_AppName = wx.BoxSizer( wx.HORIZONTAL )

        # Text label AppName setup
        self.Txt_AppName = wx.StaticText( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, _(u"App Name:"),
                                          wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_AppName.Wrap( -1 )

        # Text label add to AppName HorizontalBox
        HB_AppName.Add( self.Txt_AppName, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control setup of AppName
        self.TxtCTRL_AppName = wx.TextCtrl( VB_SourceSizer.GetStaticBox(), wx.ID_ANY,
                                            wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_AppName.Add( self.TxtCTRL_AppName, 1, wx.ALL, 5 )

        # AppName HorizontalBox add to Source VerticalBox
        VB_SourceSizer.Add( HB_AppName, 1, wx.EXPAND, 5 )

        # Icon HorizontalBox setup
        HB_Icon = wx.BoxSizer( wx.HORIZONTAL )

        # Text label Icon setup
        self.Txt_Icon = wx.StaticText( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, _(u"Icon Path (optional):"),
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_Icon.Wrap( -1 )

        # Text label add to Icon HorizontalBox
        HB_Icon.Add( self.Txt_Icon, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control setup of Icon
        self.TxtCTRL_Icon = wx.TextCtrl( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                         wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_Icon.Add( self.TxtCTRL_Icon, 1, wx.ALL, 5 )

        # Browse Icon setup for Icon
        self.Btn_Icon = wx.Button( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, _(u"Browse"),
                                   wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_Icon.Add( self.Btn_Icon, 0, wx.ALL, 5 )

        # Icon HorizontalBox add to Source VerticalBox
        VB_SourceSizer.Add( HB_Icon, 1, wx.EXPAND, 5 )

        # BinFolder HorizontalBox setup
        HB_BinFolder = wx.BoxSizer( wx.HORIZONTAL )

        # Text label of BinFolder setup
        self.Txt_BinFolder = wx.StaticText( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, _(u"Binary Folder Name (Bin):"),
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_BinFolder.Wrap( -1 )

        # Text label add to BinFolder HorizontalBox
        HB_BinFolder.Add( self.Txt_BinFolder, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control setup for BinFolder
        self.TxtCTRL_BinFolder = wx.TextCtrl( VB_SourceSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                              wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_BinFolder.Add( self.TxtCTRL_BinFolder, 1, wx.ALL, 5 )

        # BinFolder HorizontalBox add to Source VerticalBox
        VB_SourceSizer.Add( HB_BinFolder, 1, wx.EXPAND, 5 )

        # Source VerticalBox add to Main Source VerticalBox
        VB_Source.Add( VB_SourceSizer, 1, wx.EXPAND|wx.ALL, 5 )

        # Source WxPanel layout and add to Main Sizer
        self.WP_SourcePanel.SetSizer( VB_Source )
        self.WP_SourcePanel.Layout()
        VB_Source.Fit( self.WP_SourcePanel )
        VB_MainSizer.Add( self.WP_SourcePanel, 1, wx.EXPAND, 5 )

        # Controls WxPanel setup
        self.WP_ControlsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        VB_Controls = wx.BoxSizer( wx.VERTICAL )

        # Controls Sizer setup
        VB_ControlsSizer = wx.StaticBoxSizer( wx.StaticBox( self.WP_ControlsPanel, wx.ID_ANY, _(u"Controls") ),
                                              wx.VERTICAL )

        # Console mode CheckBox setup
        self.ChCB_ConsoleMode = wx.CheckBox(VB_ControlsSizer.GetStaticBox(), wx.ID_ANY, _(u"Console Mode"),
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        VB_ControlsSizer.Add(self.ChCB_ConsoleMode, 0, wx.ALL, 5)

        # OneDir CheckBox setup
        self.ChCB_OneDir = wx.CheckBox( VB_ControlsSizer.GetStaticBox(), wx.ID_ANY, _(u"OneDir"), wx.DefaultPosition,
                                        wx.DefaultSize, 0 )
        VB_ControlsSizer.Add( self.ChCB_OneDir, 0, wx.ALL, 5 )

        # OneFile CheckBox setup
        self.ChCB_OneFile = wx.CheckBox( VB_ControlsSizer.GetStaticBox(), wx.ID_ANY, _(u"OneFile"), wx.DefaultPosition,
                                         wx.DefaultSize, 0 )
        VB_ControlsSizer.Add( self.ChCB_OneFile, 0, wx.ALL, 5 )

        # Controls sizer add to Main Controls sizer
        VB_Controls.Add( VB_ControlsSizer, 1, wx.EXPAND|wx.ALL, 5 )

        # Controls WxPanel layout and add to Main Sizer
        self.WP_ControlsPanel.SetSizer( VB_Controls )
        self.WP_ControlsPanel.Layout()
        VB_Controls.Fit( self.WP_ControlsPanel )
        VB_MainSizer.Add( self.WP_ControlsPanel, 1, wx.EXPAND, 5 )

        # AddiControls WxPanel setup
        self.WP_AddiControlsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        VB_AddiControls = wx.BoxSizer( wx.VERTICAL )

        # AddiControls VerticalBox setup
        VB_AddiControlsSizer = wx.StaticBoxSizer( wx.StaticBox( self.WP_AddiControlsPanel, wx.ID_ANY,
                                                                _(u"Additional Controls") ), wx.VERTICAL )

        # HiddenImport HorizontalBox setup
        HB_HiddenImports = wx.BoxSizer( wx.HORIZONTAL )

        # Text label HiddenImports setup
        self.Txt_HiddenImports = wx.StaticText( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY,
                                                _(u"Hidden Imports (comma-separated):"), wx.DefaultPosition,
                                                wx.DefaultSize, 0 )
        self.Txt_HiddenImports.Wrap( -1 )

        # Text label add to HiddenImports HorizontalBox
        HB_HiddenImports.Add( self.Txt_HiddenImports, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control setup of HiddenImports
        self.TxtCTRL_HiddenImports = wx.TextCtrl( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY,
                                                  wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_HiddenImports.Add( self.TxtCTRL_HiddenImports, 1, wx.ALL, 5 )

        # HiddenImports HorizontalBox add to AddiControls VerticalBox
        VB_AddiControlsSizer.Add( HB_HiddenImports, 1, wx.EXPAND, 5 )

        # DataFile HorizontalBox setup
        HB_DataFile = wx.BoxSizer( wx.HORIZONTAL )

        # Text label Data setup
        self.Txt_DataFile = wx.StaticText( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, _(u"Data File (src;dest):"),
                                           wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_DataFile.Wrap( -1 )

        # Text label add to Data HorizontalBox
        HB_DataFile.Add( self.Txt_DataFile, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control of Data setup
        self.TxtCTRL_DataFile = wx.TextCtrl( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_DataFile.Add( self.TxtCTRL_DataFile, 1, wx.ALL, 5 )

        # Data file HorizontalBox add to AddiData VerticalBox
        VB_AddiControlsSizer.Add( HB_DataFile, 1, wx.EXPAND, 5 )

        # Binaries HorizontalBox setup
        HB_Bins = wx.BoxSizer( wx.HORIZONTAL )

        # Text label Binaries setup
        self.Txt_Bins = wx.StaticText( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, _(u"Binaries (src;dest):"),
                                       wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_Bins.Wrap( -1 )

        # Text label add to Binaries HorizontalBox
        HB_Bins.Add( self.Txt_Bins, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control Binaries setup
        self.TxtCTRL_Bins = wx.TextCtrl( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                         wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_Bins.Add( self.TxtCTRL_Bins, 1, wx.ALL, 5 )

        # Binaries HorizontalBox add to AddiControls VerticalBox
        VB_AddiControlsSizer.Add( HB_Bins, 1, wx.EXPAND, 5 )

        # PythonPath HorizontalBox setup
        HB_PythonPath = wx.BoxSizer( wx.HORIZONTAL )

        # Text label PythonPath setup
        self.Txt_PythonPath = wx.StaticText( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY,
                                             _(u"Python Paths (pathex):"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_PythonPath.Wrap( -1 )

        # PythonPath add to PythonPath HorizontalBox
        HB_PythonPath.Add( self.Txt_PythonPath, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control PythonPath setup
        self.TxtCTRL_PythonPath = wx.TextCtrl( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                               wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_PythonPath.Add( self.TxtCTRL_PythonPath, 1, wx.ALL, 5 )

        # PythonPath HorizontalBox add to AddiControls VerticalBox
        VB_AddiControlsSizer.Add( HB_PythonPath, 1, wx.EXPAND, 5 )

        # ExcludeModule HorizontalBox setup
        HB_ExcludeModule = wx.BoxSizer( wx.HORIZONTAL )

        # Text label ExcludeModule setup
        self.Txt_Exclude = wx.StaticText( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, _(u"Exclude Modules:"),
                                          wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Txt_Exclude.Wrap( -1 )

        # Text label add to ExcludeModule HorizontalBox
        HB_ExcludeModule.Add( self.Txt_Exclude, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        # Text Control ExcludeModule setup
        self.TxtCTRL_Exclude = wx.TextCtrl( VB_AddiControlsSizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        HB_ExcludeModule.Add( self.TxtCTRL_Exclude, 1, wx.ALL, 5 )

        # ExcludeModule HorizontalBox add to AddiControls VerticalBox
        VB_AddiControlsSizer.Add( HB_ExcludeModule, 1, wx.EXPAND, 5 )

        # AddiControls add to MainAddiControls Sizer
        VB_AddiControls.Add( VB_AddiControlsSizer, 1, wx.EXPAND, 5 )

        # AddiControls WxPanel Layout and add to Main Sizer
        self.WP_AddiControlsPanel.SetSizer( VB_AddiControls )
        self.WP_AddiControlsPanel.Layout()
        VB_AddiControls.Fit( self.WP_AddiControlsPanel )
        VB_MainSizer.Add( self.WP_AddiControlsPanel, 1, wx.EXPAND|wx.ALL, 5 )

        # Generate spec WxPanel setup
        self.WP_GeneratePanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        VB_GenerateSizer = wx.BoxSizer( wx.VERTICAL )

        # Generate spec Button setup
        self.Btn_Generate = wx.Button( self.WP_GeneratePanel, wx.ID_ANY, _(u"Generate .spec File"), wx.DefaultPosition, wx.DefaultSize, 0 )
        VB_GenerateSizer.Add( self.Btn_Generate, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        # Generate WxPanel layout and add to Main Sizer
        self.WP_GeneratePanel.SetSizer( VB_GenerateSizer )
        self.WP_GeneratePanel.Layout()
        VB_GenerateSizer.Fit( self.WP_GeneratePanel )
        VB_MainSizer.Add( self.WP_GeneratePanel, 0, wx.EXPAND, 5 )

        # Preview spec WxPanel setup
        self.WP_SpecPreviewPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        VB_SpecSizer = wx.BoxSizer( wx.VERTICAL )

        # PreviewSpec VerticalBox setup
        VB_SpecPreview = wx.StaticBoxSizer( wx.StaticBox( self.WP_SpecPreviewPanel, wx.ID_ANY, _(u"SpecFile Preview")
                                                          ), wx.VERTICAL )

        # PreviewSpec Text Controls setup in read only mode
        self.TxtCTRL_SpecPreview = wx.TextCtrl( VB_SpecPreview.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                wx.DefaultPosition, wx.DefaultSize,
                                                wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH|wx.TE_RICH2 )
        VB_SpecPreview.Add( self.TxtCTRL_SpecPreview, 1, wx.ALL|wx.EXPAND, 5 )

        # SpecFile Preview VerticalBox add to Main Spec VerticalBox
        VB_SpecSizer.Add( VB_SpecPreview, 1, wx.EXPAND|wx.ALL, 5 )

        # PreviewSpec WxPanel layout and add to Main Sizer
        self.WP_SpecPreviewPanel.SetSizer( VB_SpecSizer )
        self.WP_SpecPreviewPanel.Layout()
        VB_SpecSizer.Fit( self.WP_SpecPreviewPanel )
        VB_MainSizer.Add( self.WP_SpecPreviewPanel, 1, wx.EXPAND, 5 )

        # Main frame layout and center
        self.SetSizer( VB_MainSizer )
        self.Layout()
        self.Centre( wx.BOTH )

        # Bind Events for buttons
        self.Btn_Script.Bind(wx.EVT_BUTTON, self.OnBrowseScript)
        self.Btn_Icon.Bind(wx.EVT_BUTTON, self.OnBrowseIcon)
        self.Btn_Generate.Bind(wx.EVT_BUTTON, self.GenerateSpec)

        # Bind Events for Text fields
        self.TxtCTRL_Script.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_AppName.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_Icon.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_BinFolder.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_HiddenImports.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_DataFile.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_Bins.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_PythonPath.Bind(wx.EVT_TEXT, self.OnFormUpdated)
        self.TxtCTRL_Exclude.Bind(wx.EVT_TEXT, self.OnFormUpdated)

        # Bind Events for CheckBoxes
        self.ChCB_OneFile.Bind(wx.EVT_CHECKBOX, self.EnforceCheckboxRules)
        self.ChCB_OneDir.Bind(wx.EVT_CHECKBOX, self.EnforceCheckboxRules)
        self.ChCB_ConsoleMode.Bind(wx.EVT_CHECKBOX, self.EnforceCheckboxRules)

        # Base Values fill for our Data so we don't get errors
        self.script_path = self.TxtCTRL_Script                              # Script value
        self.app_name = self.TxtCTRL_AppName                                # App name value
        self.icon_path = self.TxtCTRL_Icon                                  # Icon value
        self.bin_name = self.TxtCTRL_BinFolder                              # BinFolder value
        self.chk_console = self.ChCB_ConsoleMode                            # ConsoleMode checkbox value
        self.chk_onedir = self.ChCB_OneDir                                  # OneDir checkbox value
        self.chk_onefile = self.ChCB_OneFile                                # OneFile checkbox value
        self.hidden_imports = self.TxtCTRL_HiddenImports                    # HiddenImport value
        self.datas = self.TxtCTRL_DataFile                                  # DataFiles value
        self.binaries = self.TxtCTRL_Bins                                   # Binaries value
        self.pathex = self.TxtCTRL_PythonPath                               # PythonPath value
        self.excludes = self.TxtCTRL_Exclude                                # Excludes value

        # If data was passed, populate fields
        if Data:
            self.SetInitialValues(Data)

    # Set initial values for our Data from Main app
    def SetInitialValues(self, Data):
        self.TxtCTRL_Script.SetValue(Data.get("script", ""))                    # Script value
        self.TxtCTRL_AppName.SetValue(Data.get("app_name", ""))                 # App name value
        self.TxtCTRL_Icon.SetValue(Data.get("icon", ""))                        # Icon value
        self.TxtCTRL_BinFolder.SetValue(Data.get("bin_folder", "bin"))          # BinFolder value
        self.ChCB_ConsoleMode.SetValue(Data.get("console", False))              # ConsoleMode checkbox value
        self.ChCB_OneDir.SetValue(Data.get("onedir", False))                    # OneDir checkbox value
        self.ChCB_OneFile.SetValue(Data.get("onefile", False))                  # OneFile checkbox value
        self.TxtCTRL_HiddenImports.SetValue(Data.get("hidden_imports", ""))     # HiddenImport value
        self.TxtCTRL_DataFile.SetValue(Data.get("data_file", ""))               # DataFiles value
        self.TxtCTRL_Bins.SetValue(Data.get("binaries", ""))                    # Binaries value
        self.TxtCTRL_PythonPath.SetValue(Data.get("pathex", ""))                # PythonPath value
        self.TxtCTRL_Exclude.SetValue(Data.get("excludes", ""))                 # Excludes value

    # Prevent OneFile or OneDir checkboxes to be enabled together
    def EnforceCheckboxRules(self, event=None):
        if self.ChCB_OneFile.GetValue() and self.ChCB_OneDir.GetValue():
            wx.MessageBox("'One Dir' or 'One File' flags can't be enabled together.",
                          "Wrong combination of flags has been selected",
                          wx.ICON_WARNING)
            # Uncheck the one that was *just* checked
            if event.GetEventObject() == self.ChCB_OneFile:
                self.ChCB_OneDir.SetValue(False)
            else:
                self.ChCB_OneFile.SetValue(False)

        # Console mode logic - just pass
        if self.ChCB_ConsoleMode.GetValue():
            pass

    # Script browse file dialog
    def OnBrowseScript(self, event):
        with wx.FileDialog(self, "Select script", wildcard="Python files (*.py)|*.py") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.TxtCTRL_Script.SetValue(dlg.GetPath())

    # Icon browse file dialog
    def OnBrowseIcon(self, event):
        with wx.FileDialog(self, "Select icon", wildcard="Icon files (*.ico)|*.ico") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                self.TxtCTRL_Icon.SetValue(dlg.GetPath())

    # Update spec file preview Text Control
    def OnFormUpdated(self, event):
        spec = self.GenerateSpecText()
        self.TxtCTRL_SpecPreview.SetValue(spec)

    # Generate spec file text so we can use it for generation
    def GenerateSpecText(self):
        from pprint import pformat

        def parse_list(input_text):
            return [item.strip() for item in input_text.split(',') if item.strip()]

        def parse_tuple_list(input_text):
            return [tuple(item.split(';')) for item in input_text.split(',') if ';' in item]

        # Get main values from fields
        script = self.script_path.GetValue()
        app_name = self.app_name.GetValue() or "app"
        icon = self.icon_path.GetValue() or None
        dll_folder = self.bin_name.GetValue() or f"{app_name}_main"
        console = self.chk_console.GetValue()
        hidden_imports = parse_list(self.hidden_imports.GetValue())
        datas = parse_tuple_list(self.datas.GetValue())
        binaries = parse_tuple_list(self.binaries.GetValue())
        pathex = parse_list(self.pathex.GetValue())
        excludes = parse_list(self.excludes.GetValue())

        # Get Icon for our app
        icon_line = f"icon={repr(icon)}," if icon else ""

    # Create whole spec file text
        return f"""
    # -*- mode: python ; coding: utf-8 -*-
    block_cipher = None
    
    a = Analysis(
        [{repr(script)}],
        pathex={pformat(pathex)},
        binaries={pformat(binaries)},
        datas={pformat(datas)},
        hiddenimports={pformat(hidden_imports)},
        hookspath=[],
        runtime_hooks=[],
        excludes={pformat(excludes)},
        win_no_prefer_redirects=False,
        win_private_assemblies=False,
        cipher=block_cipher,
    )

    pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

    exe = EXE(
        pyz,
        a,
        name={repr(app_name)},
        console={console},
        {icon_line}
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name={repr(dll_folder)}
    )
    """.strip()

    # Generate spec file from Data we get from main app or from it been filled by hand
    def GenerateSpec(self, event=None):

        spec = self.GenerateSpecText()
        self.TxtCTRL_SpecPreview.SetValue(spec)     # Show spec file preview in TextControl field

        # Check for script path as it is mandatory for spec to be created
        script = self.script_path.GetValue()
        if not script:
            wx.MessageBox("Script path is required to save the .spec file.", "Missing Data",
                          wx.ICON_WARNING)
            return

        # Get default name for our app from original script
        default_name = os.path.splitext(os.path.basename(script))[0] + ".spec"

        # Get app folder where your python script is located
        app_folder = os.path.dirname(os.path.abspath(__file__))
        desired_folder = os.path.join(app_folder, "Spec")

        # Make sure the folder exists (optional)
        if not os.path.exists(desired_folder):
            os.makedirs(desired_folder)

        # Save spec with file dialog into App\Spec folder with app name
        with wx.FileDialog(
                self,
                "Save .spec file",
                defaultDir=desired_folder,
                wildcard="Spec files (*.spec)|*.spec",
                defaultFile=default_name,
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as dlg:

            if dlg.ShowModal() == wx.ID_OK:
                spec_file_path = dlg.GetPath()
                try:
                    with open(spec_file_path, "w") as f:
                        f.write(spec)
                    wx.MessageBox(f"Spec file saved to:\n{spec_file_path}", "Successfully saved",
                                  wx.OK | wx.ICON_INFORMATION)
                except Exception as e:
                    wx.MessageBox(f"Failed to save file:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    # CleanUp function
    def __del__( self ):
        pass

# Main App loop
app = wx.App(False)
frame = MainFrame(None)
frame.Show()
frame.Bind(wx.EVT_CLOSE, frame.OnClose)    # Bind for CloseEvent
app.MainLoop()