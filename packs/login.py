from .functions import password_matches

def login_interface(cnx, cursor, sg):
    
    login_layout = [
        [sg.T("  Username"), sg.InputText(key = "Username", size = (24, 1), border_width = 0)],
        [sg.T("  Password"), sg.InputText(key = "Password", password_char = "*", size = (24, 1), border_width = 0)], 
        [sg.T("  "), 
        sg.B(image_filename = "textures/button_exit.png", key = "Exit"
             , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0), 
        sg.T("                     "), 
        sg.B(image_filename = "textures/button_login.png", bind_return_key=True, key = "Login"
             , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)] 
    ]

    login_window = sg.Window("Record System", login_layout, size=(300,100))

    while True:
        login_e, login_v = login_window.read()
        
        if login_e == "Login":
            username = login_v["Username"]
            password = login_v["Password"]
            cursor.execute(f"select username from account where username = '{username}'")
            cursor.fetchall()
            
            if cursor.rowcount > 0:
                cursor.execute(f"select password_hash from account where username = '{username}'")
                login_password_hash = cursor.fetchall()
                cnx.commit()
                
                if password_matches(password, login_password_hash[0][0]):
                    cursor.execute(f"select account_type from account where username = '{username}'")
                    account_type = cursor.fetchall()
                    cnx.commit()
                    account_type = account_type[0][0]
                    
                    if account_type in ("User", "Admin"):
                        login_window.close()
                        return account_type,username
                        break
            else:
                sg.popup_auto_close("Invalid Username or Password!")
        
        if login_e == None or login_e == "Exit":
            login_window.close()
            return 0,0
            break
