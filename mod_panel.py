# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 17:58:44 2022

@author: William
"""

from requests import get
from bs4 import BeautifulSoup
import webbrowser
import PySimpleGUI as sg 

api_key = "" #your api key here

global layout

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
        template = "https://steamrep.com/search?q="
        
    site = get(template+steamurl).content.decode()
    
    
    soup = BeautifulSoup(site,"html.parser")
    id32 = soup.title.string.split(" | ")[-1]
    
    return id32

def openbans(mode,id32):
    if mode not in ["banlist","commslist"]:
        raise Exception 
    url = f"https://ugc-gaming.net/sourcebans/index.php?p={mode}&searchText={id32}&Submit=Search"
    webbrowser.open(url)
    
    
sg.theme('DarkAmber')   
layout = [  [sg.Checkbox("BANS",default=True,key="banlist",enable_events=True),sg.Checkbox("COMMS",key="commslist",default = False, enable_events=True)],
            [sg.Text('Enter Steam url:'), sg.InputText(key="-URL-")],
            [sg.Button('Fetch SB')],
            [sg.Text("IP:"), sg.InputText(key="-IP-")],
            [sg.Button("Get IP info")],
            [sg.Text(size=(50,1),key="-ipinfo-")],
            [sg.Button('Quit')]]

window = sg.Window('UGC Mod panel', layout, return_keyboard_events=True,finalize=True)
window["-URL-"].bind("<Return>","_enter")
window["-IP-"].bind("<Return>","_enter")

while True:
    event, values = window.read()

    if event == "Get IP info" or event == "-IP-_enter":
        info = getIPinfo(values["-IP-"])
        window["-ipinfo-"].update(repr(info).strip("{}"))
    if event == "commslist" or event == "banlist":
        if event == "commslist":
            other = "banlist"
        elif event == "banlist":
            other = "commslist"
        if not(values["commslist"]^values["banlist"]):
            window[other].update(not(values[other]))
            
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
