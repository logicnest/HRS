import mysql.connector as mc
import PySimpleGUI as sg

from packs.admin import admin_interface
from packs.functions import log_user
from packs.login import login_interface
from packs.user import user_interface

cnx = mc.connect(host = "localhost", user = "root", password = "root")
cursor = cnx.cursor()
cursor.execute("use hospital")
cnx.autocommit = False

sg.theme("Dark")
sg.theme_background_color(color = "#181818")
sg.theme_element_background_color(color = "#181818")
sg.theme_text_element_background_color(color = "#181818")
sg.set_global_icon("textures/hospital_ico.ico")


while True:
    account_type,username = login_interface(cnx, cursor, sg)
    
    if account_type == "Admin": 
        admin_interface(cnx, mc, cursor, sg)
        
    if account_type == "User":
        log_user(username, cnx, cursor, mc)
        user_interface(cnx, mc, cursor,sg)
        
    if account_type == 0:
        break
