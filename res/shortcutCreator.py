import os, winshell, sysconfig, sys

SHORTCUT = "myTCL"
try:
    SHORTCUT = sys.argv[1]
except Exception as e:
    pass

SHORTCUT_NAME = ("%s.lnk" % SHORTCUT)
DESCRIPTION = "My Smart App"
#START_MENU_FOLDER = winshell.get_special_folder_path("CSIDL_STARTMENU")
START_MENU_FOLDER = winshell.get_folder_by_name("CSIDL_STARTMENU")
SHORTCUT_FOLDER = os.path.join(START_MENU_FOLDER, SHORTCUT)

scriptsDir = sysconfig.get_path('scripts')
pythonRoot = os.path.split(sys.executable)[0]

try:
    os.mkdir(SHORTCUT_FOLDER)
except Exception as e:
    pass

SHORTCUTS_TO_CREATE = [winshell.desktop(), SHORTCUT_FOLDER]

for directory in SHORTCUTS_TO_CREATE:
    winshell.CreateShortcut(
      Path=os.path.join(directory, SHORTCUT_NAME),
      Target=os.path.join(scriptsDir, "%s.exe" % SHORTCUT),
      Icon=( os.path.join(pythonRoot, "python.exe"), 0),
      Description=DESCRIPTION,
      Arguments= "-p myKey",
      StartIn = "",
    )

"""
"CSIDL_APPDATA"

"CSIDL_COMMON_STARTMENU"
"CSIDL_STARTMENU"

"CSIDL_COMMON_DESKTOPDIRECTORY"
"CSIDL_DESKTOPDIRECTORY"

"CSIDL_COMMON_STARTUP"
"CSIDL_STARTUP"

"CSIDL_COMMON_PROGRAMS"
"CSIDL_PROGRAMS"

"CSIDL_FONTS"
"""
