"# Nav_App" 

To compile:
pyinstaller -F -i "evasion29.ico" Window.py --hidden-import=pkg_resources.py2_warn
pyinstaller -F -i "update.ico" update.py --hidden-import=pkg_resources.py2_warn