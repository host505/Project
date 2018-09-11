#######################################################################
 # ----------------------------------------------------------------------------
 # "THE BEER-WARE LICENSE" (Revision 42):
 # As long as you retain this notice you can do whatever you want with this
 # stuff. If we meet some day, and you think this stuff is worth it, you can 
 # buy me a beer in return. - Muad'Dib
 # ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Tantrum Advanced Settings
# Addon id: plugin.program.tantrumadvsettings
# Addon Provider: MuadDib

import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os

ADDON      = xbmcaddon.Addon(id='plugin.program.tantrumadvsettings')
DATA_PATH  = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.program.tantrumadvsettings'), '')
ADDON_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.tantrumadvsettings', ''))
SETTINGS_PATH = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.tantrumadvsettings', 'xml_settings'))
XML_PATH      = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.program.tantrumadvsettings'), 'XML_FILES')

def addon():
    return ADDON

def viewtype():
    return ADDON.getSetting('viewtype')
	
def xml_files():
    return create_directory(DATA_PATH, "XML_FILES")
	
def xml_file():
    return create_file(XML_PATH, "advancedsettings.xml")
	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
	
create_directory(DATA_PATH, "")
create_directory(DATA_PATH, "XML_FILES")
create_file(XML_PATH, "advancedsettings.xml")

		
