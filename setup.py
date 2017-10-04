import codecs
import os
import re
from setuptools import setup, find_packages
import sysconfig
import sys

if sys.platform == 'win32':
    from win32com.client import Dispatch
    import winreg

def errorExit(msg):
    """Send error message to stderr and exit"""
    msgString = ("Error: " + msg + "\n")
    sys.stderr.write(msgString)
    sys.exit()

def get_reg(name,path):
    # Read variable from Windows Registry
    # From https://stackoverflow.com/a/35286642
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        errorExit("no se completo la instalacion")
        return None

def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

def get_reg2(name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                       winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

def post_install():
    # Creates a Desktop shortcut to the installed software

    # Package name
    packageName = 'pyBOT'

    # Scripts directory (location of launcher script)
    scriptsDir = sysconfig.get_path('scripts')

    # Target of shortcut
    target = os.path.join(scriptsDir, packageName + '.exe')

    # Name of link file
    linkName = packageName + '.lnk'

    # Read location of Windows desktop folder from registry
    regName = 'Desktop'
    regPath = r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
    desktopFolder = os.path.normpath(get_reg(regName,regPath))

    # Path to location of link file
    pathLink = os.path.join(desktopFolder, linkName)
    print("pathlink: ", pathLink)
    print("target: ", target)
    print("scriptsDir: ", scriptsDir)
    print("desktopFolder: ", desktopFolder)
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(pathLink)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = scriptsDir
    shortcut.IconLocation = target
    shortcut.save()
    #errorExit("no se completo la instalacion")


###################################################################

NAME = "pyBOT-MDY"
PACKAGES = find_packages(where=".")
#PACKAGES = find_packages(where=".")
META_PATH = os.path.join("./", "__init__.py")
KEYWORDS = ["class", "attribute", "boilerplate"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = ["flask","pymongo","pyqt5", "pyqt5-tools"]

###################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=find_meta("uri"),
        version=find_meta("version"),
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=read("README.rst"),
        packages=PACKAGES,
        package_dir={"": ".."},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        python_requires='>=3',
        #data_files=[('', [''])],

        package_data={
            # If any package contains *.txt files, include them:
            '': ['*.txt'],
            # And include any *.dat files found in the 'data' subdirectory
            # of the 'mypkg' package, also:
            '': ['data/*.dat'],
        },
        include_package_data=True,    # include everything in source control

        # ...but exclude README.txt from all packages
        exclude_package_data={'': ['README.txt']},
        dependency_links=[
            "http://peak.telecommunity.com/snapshots/"
        ],

        entry_points={
            'console_scripts': [
                'runnerCli = runner:vp_start_gui',
                'myTCLCLI = runner:vp_start_gui',
                'pyBOT = runner:runner',
            ],
            'gui_scripts': [
                'pyBOT = runner:runner',
            ]
        },
    )
if (sys.argv[1] == 'install' or sys.argv[1] == '-install') and sys.platform == 'win32':
    post_install()
#python setup.py sdist bdist_wheel
#pip wheel .
#pip wheel . --wheel-dir ./myWheels
#python setup.py clean --all
