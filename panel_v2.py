# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 17:58:44 2022

@author: William
"""

from requests import get
from bs4 import BeautifulSoup
import webbrowser
import PySimpleGUI as sg 
import re

api_key = "bbd408f385b3440096f9aa38321892d2"
icon = r"C:\Users\William\Desktop\ugc_logo.ico"

global layout

def validate_url(url):
    """
    Valider si l'URL est une URL de profil Steam valide, c'est-à-dire de la forme https://steamcommunity.com/profiles/<steam_id_64>
    ou https://steamcommunity.com/id/<custom_url>
    """
    return ("steamcommunity.com/profiles/" in url or "steamcommunity.com/id/" in url) and url.startswith("https://")

def validate_steam_id_32(steam_id_32: str) -> bool:
    """
    Validate if a string is a valid Steam ID 32.
    
    Parameters:
    - steam_id_32: str
    
    Returns:
    - bool
    """
    if not isinstance(steam_id_32, str):
        return False
    
    # Check if the string has the correct format
    if not re.match(r"^STEAM_0:\d:\d+$", steam_id_32):
        return False
    
    # Check if the digits are valid
    steam_id_32_parts = steam_id_32.split(":")
    try:
        y = int(steam_id_32_parts[1])
        z = int(steam_id_32_parts[2])
    except ValueError:
        return False
    
    if y != 0 and y != 1:
        return False
    
    return True
def validate_mode(mode):
    """
    Valider si mode est un mode valide, c'est-à-dire "banlist" ou "commslist"
    """
    return mode in ["banlist", "commslist"]

def validate_ip(value):
    # Valider si la valeur est une adresse IP valide
    parts = value.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        try:
            int_part = int(part)
        except ValueError:
            return False
        if not 0 <= int_part <= 255:
            return False
    return True

def getIPinfo(ip_address):
    assert type(ip_address) == str
    try:
        info = get(f"https://vpnapi.io/api/{ip_address}?key={api_key}").json()
        sec = info["security"]
        return sec
    except:
        pass

def getid32(steamurl):
    assert type(steamurl) == str
        
    
    
    if "steamrep" in steamurl:
        template=""
    else:
        if validate_url(steamurl):
            template = "https://steamrep.com/search?q="
        else:
            window["-error-"].update("Invalid URL")
            return ''
        
    site = get(template+steamurl).content.decode()
    
    
    soup = BeautifulSoup(site,"html.parser")
    id32 = soup.title.string.split(" | ")[-1]

    return id32


def openbans(mode,id32):
    if validate_mode(mode) and validate_steam_id_32(id32):
        url = f"https://ugc-gaming.net/sourcebans/index.php?p={mode}&searchText={id32}&Submit=Search"
        webbrowser.open(url)
    
    
sg.theme('DarkAmber')   
layout = [  [sg.Checkbox("BANS",default=True,key="banlist",enable_events=True),sg.Checkbox("COMMS",key="commslist",default = False, enable_events=True)],
            [sg.Text('Enter Steam url:'), sg.InputText(key="-URL-",size=(None,None))],
            [sg.Button('Fetch SB')],
            [sg.HorizontalSeparator()],
            [sg.Text("IP:"), sg.InputText(key="-IP-", size=(None,None))],
            [sg.Button("Get IP info")],
            [sg.Text("VPN:"),sg.Graph(canvas_size=(20,20),graph_bottom_left=(0,0), graph_top_right=(20,20),key="vpn"),
             sg.Text("Proxy:"),sg.Graph(canvas_size=(20,20),graph_bottom_left=(0,0), graph_top_right=(20,20),key="proxy"),
             sg.Text("Tor:"),sg.Graph(canvas_size=(20,20),graph_bottom_left=(0,0), graph_top_right=(20,20),key="tor"),
             sg.Text("Relay:"),sg.Graph(canvas_size=(20,20),graph_bottom_left=(0,0), graph_top_right=(20,20),key="relay")],
            [sg.Text("", size=(None, 1), key="-error-",text_color="red")],
            [sg.HorizontalSeparator()],
            [sg.Quit(button_color=("white","red"))]
            ]

layoutColonne = [[sg.Column(layout,justification="center", element_justification="center")]]
window = sg.Window('UGC Mod panel', layoutColonne, return_keyboard_events=True,finalize=True, margins=(10,10), element_padding=(3,3),
                   icon=icon)
window["-URL-"].bind("<Return>","_enter")
window["-IP-"].bind("<Return>","_enter")

while True:
    event, values = window.read()

    if event == "Get IP info" or event == "-IP-_enter":
        ip = values["-IP-"]
        if validate_ip(ip):
            window["-error-"].update("")
            info = getIPinfo(ip)

            try:
                for Type in info.keys():
                    if info[Type]:
                        color = "green"
                    else:
                        color = "red"
                    window[Type].draw_circle((10, 10), 10, fill_color=color)
            except Exception as e:
                window["-error-"].update(e)
        else:
            window["-error-"].update("IP address invalid")
            window["-IP-"].update("")
   
    if event in ["commslist", "banlist"]:
        other = "banlist" if event == "commslist" else "commslist"
    if values["commslist"] == values["banlist"]:
        window[other].update(not values[other])
            
    if event == sg.WIN_CLOSED or event == 'Quit': 
        break

    if event == "Fetch SB" or event=="-URL-_enter": 
        url = values["-URL-"]
        if values["commslist"]^values["banlist"] and len(url)!=0:
            mode = list(values.keys())[list(values.values()).index(True)]
            id32 = getid32(url)

            try:
                openbans(mode,id32)
            except Exception as e:
                print(e)
        else:
            pass
    

        window["-URL-"].update("")
        
window.close()
