from .functions import check_item, encryptor

def admin_interface(cnx, mc, cursor, sg):

    def show_accounts():
        
        cursor.execute("select * from account")
        cursor.fetchall()
        
        if cursor.rowcount == 0:
            cnx.commit()
            return sg.popup_auto_close("Table is Empty", no_titlebar = True)
        
        cnx.commit()
        admin_window.hide()
        
        try:
            cursor.execute("select * from account") 
            headings = ["Username", "Password_hash", "Account_Type"]
            
            show_layout = [ 
            [sg.Table(cursor.fetchall(), headings, max_col_width = 25, justification = "center"
                      , header_background_color = "#3c3c3c", header_text_color = "#f4d47c")], 
            [sg.B(image_filename = "textures/button_back.png", key = "Back"
                  , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)]
            ]   
            cnx.commit()
            show_window = sg.Window("Accounts", show_layout, force_toplevel = True)
            
            while True:
                display_e, display_v = show_window.read()
                
                if display_e == None or display_e == "Back":
                    show_window.Close()
                    admin_window.un_hide()
                    break
                
        except mc.Error as error:
            
            print(f"An error has occurred:\n{error}\n")
            cnx.rollback()
    
    def reset_table():
        
        cursor.execute("drop table patient_checkin")
        cursor.execute('''create table patient_checkin (Health_Card_No int(10), Name varchar(30) , Age int(5), Gender varchar(10),
                        Nationality varchar(40), Emergency varchar(3), Date_Time timestamp)''')
        sg.popup_notify("Successfully Executed.", fade_in_duration = 20, display_duration_in_ms = 400)

    def logs():
        
        cursor.execute("select * from log")
        cursor.fetchall()
        
        if cursor.rowcount == 0:
            cnx.commit()
            return sg.popup_auto_close("Table is Empty", no_titlebar = True)
        
        cnx.commit()
        admin_window.hide()
        
        try:
            cursor.execute("select * from log") 
            headings = ["Username", "Date_Time"]
            logs_layout = [ 
            [sg.Table(cursor.fetchall(), headings, max_col_width = 25, justification = "center"
                      , header_background_color = "#3c3c3c", header_text_color = "#f4d47c")], 
            [sg.B(image_filename = "textures/button_back.png", key = "Back"
                  , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)]
            ]   
            cnx.commit()
            logs_window = sg.Window("Logs", logs_layout, force_toplevel = True)
            
            while True:
                display_e, display_v = logs_window.read()
                
                if display_e == None or display_e == "Back":
                    logs_window.Close()
                    admin_window.un_hide()
                    break
                
        except mc.Error as error:
            print(f"An error has occurred:\n{error}\n")
            cnx.rollback()

    def add_account():    
           
        username = admin_v["Username"]
        password = admin_v["Password"]
        c_password = admin_v["Conf_Password"]
        
        if username == "":
            return sg.popup_auto_close("Enter username!", no_titlebar = True)
        
        elif check_item(cursor, "account", "username", username):
            return sg.popup_auto_close("Username already taken!", no_titlebar = True)
        
        elif  password == "" or c_password == "":
            return sg.popup_auto_close("Password Cannot be left empty!", no_titlebar = True)
        
        elif password != c_password:
            return sg.popup_auto_close("Passwords do not match!", no_titlebar = True)
        
        else:
            password_hash = encryptor(password)
            cursor.execute(f"insert into account values('{username}', '{password_hash}', 'User')")
            return sg.popup_notify("Successfully Executed.", fade_in_duration = 20, display_duration_in_ms = 400)
    
    def query_execute():
        
        query = admin_v["Query"]
        
        if query == "":
            return sg.popup_auto_close("Invalid Query!", no_titlebar = True)
        
        try:
            
            cursor.execute(f"{query}")
            cnx.commit()
            sg.popup_notify("Successfully Executed.", fade_in_duration = 20, display_duration_in_ms = 400)
        
        except:
            sg.popup_auto_close("Invalid Query!", no_titlebar = True)
            
    add_layout = [
        [sg.T("            Username"), sg.InputText(size = (25, 1), key = "Username", border_width = 0)], 
        [sg.T("            Password"), sg.InputText(size = (25, 1), key = "Password", border_width = 0)], 
        [sg.T("Confirm Password"), sg.InputText(size = (25, 1), key = "Conf_Password", border_width = 0)], 
        [sg.B(image_filename = "textures/button_create-account.png", key = "Create"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)]
    ]
    
    query_layout = [
        [sg.InputText(key = "Query", size = (23, 1), border_width = 0)], 
        [sg.B(image_filename = "textures/button_execute.png", key = "Execute"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)]
    ]
    
    button_layout = [
        [sg.B(image_filename = "textures/button_show-accounts.png", key = "Show"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)], 
        [sg.B(image_filename = "textures/button_reset-table.png", key = "Reset"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0), 
        sg.B(image_filename = "textures/button_logs.png", key = "Logs"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)], 
        [sg.Frame("MySQL Query", query_layout)]
    ]
    
    admin_layout = [
        [sg.Image(filename = "textures/Daco.png"), sg.Frame("", button_layout, border_width = 0)], 
        [sg.Frame("New Account", add_layout)]
    ]
    
    admin_window = sg.Window("Admin", admin_layout)

    while True:
        admin_e, admin_v = admin_window.read()    
        if admin_e == "Show":
            show_accounts()
            
        if admin_e == "Reset":
            reset_table()
        
        if admin_e == "Logs":
            logs()
        
        if admin_e == "Create":
            add_account()
        
        if admin_e == "Execute":
            query_execute()
            
        if admin_e == None:
            admin_window.close()
            break