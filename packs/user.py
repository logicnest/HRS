from .functions import check_item, countries

def user_interface(cnx, mc, cursor,sg):
    
    def isalphaspace(string):
        for substring in string.split(" "):
            
            if not substring.isalpha():
                return False
            
        return True
    
    headings = ["Health_Card_No", "Name", "Age", "Gender", "Nationality", "Emergency", "Date_Time"]
# ###############   

    def add_patient():
        
        if user_v["add_card_no"] == "":
            return sg.popup_auto_close("Please enter the Health Card No.", no_titlebar = True)
        
        elif check_item(cursor, "patient_checkin", "health_card_no", user_v["add_card_no"]):
            return sg.popup_auto_close(f'Health Card No: {user_v["add_card_no"]} ALREADY EXIST!')
        
        elif not user_v["add_card_no"].isdigit():
            return sg.popup_auto_close("Invalid Health Card No.", no_titlebar = True)
            
        elif user_v["add_name"] == "":
            return sg.popup_auto_close("Please enter the Name.", no_titlebar = True)
        
        elif not isalphaspace(user_v["add_name"]):
            return sg.popup_auto_close("Invalid Name.", no_titlebar = True)
            
        elif user_v["add_age"] == "":
            return sg.popup_auto_close("Please enter the Age.", no_titlebar = True)
        
        elif not user_v["add_age"].isdigit():
            return sg.popup_auto_close("Invalid Age.", no_titlebar = True)
            
        elif user_v["add_male"] == False and user_v["add_female"] == False:
            return sg.popup_auto_close("Please choose a Gender", no_titlebar = True)
            
        elif user_v["yes"] == False and user_v["no"] == False:
            return sg.popup_auto_close("Please choose Emergency.", no_titlebar = True)

        elif user_v["add_nation"] == "None":
            return sg.popup_auto_close("Please choose Nationality.", no_titlebar = True)
        
        else:
            card_no = user_v["add_card_no"]
            name = user_v["add_name"].strip().title()
            age = user_v["add_age"]
            nation = user_v["add_nation"]
            
            if user_v["add_male"]:
                gender = "Male"
                
            if user_v["add_female"]:
                gender = "Female"
                
            if user_v["yes"]:
                imp = "Yes"
                
            if user_v["no"]:
                imp = "No" 
                
            query = f'''INSERT INTO patient_checkin(health_card_no, name, age, gender, nationality, emergency, date_time) 
                    values({card_no}, "{name}", {age}, "{gender}", "{nation}", "{imp}", CURRENT_TIMESTAMP)'''
            
            cursor.execute(query)
            cnx.commit()
            return sg.popup_notify("Successfully Executed.", fade_in_duration = 20, display_duration_in_ms = 500)
                
    def remove_patient():
        
        if check_item(cursor, "patient_checkin", "health_card_no", user_v["remove_card_no"]):
            card_no = user_v["remove_card_no"]
            query = f"delete from patient_checkin where health_card_no = {card_no}"
            cursor.execute(query)
            sg.popup_notify("Successfully Executed.", fade_in_duration = 20, display_duration_in_ms = 500)
            cnx.commit()
            
        elif not check_item(cursor, "patient_checkin", "health_card_no", user_v["remove_card_no"]):
            sg.popup_auto_close(f'Health Card No: {user_v["remove_card_no"]} does not EXIST!')
    
    def display_patient():
        
        cursor.execute("select * from patient_checkin")
        cursor.fetchall()
        
        if cursor.rowcount == 0:
            cnx.commit()
            return sg.popup_auto_close("Table is Empty", no_titlebar = True)
        
        cursor.execute("select * from patient_checkin order by date_time desc")
        results = cursor.fetchall() 
        user_window.size=(900, 463)
        user_window["Table"].update(values = results)
        cnx.commit()
        
    def get_results():
        cursor.execute("select * from patient_checkin")
        cursor.fetchall()
        
        if cursor.rowcount == 0:
            cnx.commit()
            results = ["", "", "", "", "           ", "", ""]
            return results
        
        cursor.execute("select * from patient_checkin order by date_time desc")
        return cursor.fetchall()
        
    results = ["", "", "", "", "           ", "", ""]
    ############################################
    add_layout = [
        [sg.T("Health Card number"), sg.InputText(key = "add_card_no", size = (15, 1), focus = True, border_width = 0)], 
        [sg.T("                    Name"), sg.InputText(key = "add_name", size = (30, 1), border_width = 0)], 
        [sg.T("                      Age"), sg.InputText(key = "add_age", size = (4, 1), border_width = 0)], 
        [sg.T("Gender      "), sg.Radio("Male", "add_gender", key = "add_male"), sg.Radio("Female", "add_gender", key = "add_female")], 
        [sg.T("Emergency"), sg.Radio("Yes", "imp", key = "yes", ), sg.Radio("No", "imp", key = "no")], 
        [sg.T("Nationality"), sg.Combo(countries, default_value = "None", key = "add_nation", )], 
        [sg.T("    "), 
        sg.B(key = "Save", image_filename = "textures/button_save.png",
              button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0), 
        sg.T("                                              "), 
        sg.T("    ")
        ]
        ]

    modify_layout = [
        [sg.T("                      Health Card No", font = "20")], 
        [sg.InputText(key = "modify_card_no", font = "20", size = (40, 1), focus = True, border_width = 0)], 
        [sg.T("                                                   "), sg.B(image_filename = "textures/button_modify.png", key = "Modify"
                                                                           , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)], 
        ]
    
    change_layout = [
        [sg.T("Modifying for Health Card No."), sg.InputText(default_text = "", key = "change_card_no", readonly = True, disabled_readonly_text_color = "#000000")], 
        [sg.T("                    Name"), sg.InputText(key = "change_name", size = (30, 1), border_width = 0)], 
        [sg.T("                      Age"), sg.InputText(key = "change_age", size = (4, 1), border_width = 0)], 
        [sg.T("Gender      "), sg.Radio("Male", "change_gender", key = "change_male"), sg.Radio("Female", "change_gender", key = "change_female")], 
        [sg.T("Nationality"), sg.Combo(countries, default_value = "None", key = "change_nation")], 
        [sg.T("    "),  
        sg.B(key = "modify_Save", image_filename = "textures/button_save.png", button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0), 
        sg.T("                     "), 
        sg.B(key = "Cancel", image_filename = "textures/button_cancel.png", button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0), 
        sg.T("    ")
        ]
        ]

    remove_layout = [
        [sg.T("                      Health Card No", font = "20")], 
        [sg.InputText(key = "remove_card_no", font = "20", size = (40, 1), focus = True, border_width = 0)], 
        [sg.T("                                 "), sg.B(image_filename = "textures/button_remove-patient.png", key = "Remove"
                                                         , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)]
        ]

    display_layout = [
        [sg.T("Sort:"), sg.B(image_filename = "textures/button_sort.png", key = "Name_Sort", disabled = False,button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0),sg.B(image_filename = "textures/button_time_sort.png", key = "Time_Sort", disabled = True,button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0)],
        [sg.Table(get_results(), headings, key = "Table", max_col_width = 25, justification = "center"
                  , header_background_color = "#3c3c3c", header_text_color = "#f4d47c")], 
        ]

# ##################
    
    btn_layout = [ 
        [sg.B(key = "1", disabled = True, image_filename = "textures/button_add-patient-record.png"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0, pad = (20, 10))], 
        [sg.B(key = "2", image_filename = "textures/button_modify-patient-record.png"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0, pad = (20, 10))], 
        [sg.B(key = "3", image_filename = "textures/button_remove-patient-record.png"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0, pad = (20, 10))], 
        [sg.B(key = "4", image_filename = "textures/button_display-patient-record.png"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0, pad = (20, 10))], 
        [sg.T("", background_color = "#000000")],
        [sg.T("    ", background_color = "#000000"),sg.Image(filename="textures/Daco.png",background_color="#000000")],
        [sg.B(key = "Logout", image_filename = "textures/button_logout.png"
              , button_color = (sg.theme_background_color(), sg.theme_background_color()), border_width = 0, pad = (20, 10))],
        [sg.T("", background_color = "#000000")],
        [sg.T("", background_color = "#000000")]
        ]        
    
    user_layout = [
        [sg.Column(btn_layout, background_color = "#000000", pad = (0, 0)), 
         sg.VSep(), 
         sg.Column(add_layout, key = 'col1'), 
         sg.Column(modify_layout, visible = False, key = 'col2'), 
         sg.Column(remove_layout, visible = False, key = 'col3'), 
         sg.Column(change_layout, visible = False, key = 'col22'), 
         sg.Column(display_layout, visible = False, key = 'col4'), 
        ]
        ]


    user_window = sg.Window("Record System", user_layout, size = (600, 463))
    layout = 1
    
    while True:
        user_e, user_v = user_window.read()
        
        if user_e == None:
            break
        
        if user_e in "1234" and layout != 22:
            user_window.size = (600, 463)
            user_window[f'col{layout}'].update(visible = False)
            user_window[f'{layout}'].update(disabled = False)
            layout = int(user_e)
            user_window[f'col{layout}'].update(visible = True)
            user_window[f'{layout}'].update(disabled = True)
            
        if layout == 22 and user_e in "1234":
            user_window[f'col{layout}'].update(visible = False)
            user_window[f'2'].update(disabled = False)
            layout = int(user_e)
            user_window[f'col{layout}'].update(visible = True)
            user_window[f'{layout}'].update(disabled = True)
            
        if user_e == "Save":
            add_patient()

        if user_e == "Modify":
            
            if not check_item(cursor, "patient_checkin", "health_card_no", user_v["modify_card_no"]):
                sg.popup_auto_close(f'Health Card No: {user_v["modify_card_no"]} does not EXIST!')
            
            elif check_item(cursor, "patient_checkin", "health_card_no", user_v["modify_card_no"]):
                card_no = user_v["modify_card_no"]
                user_window[f'col{layout}'].update(visible = False)
                layout = 22
                user_window[f'col{layout}'].update(visible = True)
                user_window["change_card_no"].update(f"{card_no}")
                
        if user_e == "modify_Save":
            
            if not user_v["change_name"] == "" or  not user_v["change_age"] == "" or  not user_v["change_male"] == None or user_v["change_female"] == None or not user_v["change_nation"] == "None":
                
                if not user_v["change_name"] == "":
                    name = user_v["change_name"].strip().title()
                    cursor.execute(f"update patient_checkin set name = '{name}' where health_card_no = {card_no}")
                    cnx.commit()
                    
                if not user_v["change_age"] == "":
                    age = user_v["change_age"]
                    cursor.execute(f"update patient_checkin set age = '{age}' where health_card_no = {card_no}")
                    cnx.commit()
                    
                if not user_v["change_male"] == None and user_v["change_female"] == None:
                    
                    if user_v["change_male"]:
                        gender = "Male"
                        
                    if user_v["change_female"]:
                        gender = "Female"
                    cursor.execute(f"update patient_checkin set gender = '{gender}' where health_card_no = {card_no}")
                
                if not user_v["change_nation"] == "None":
                    nation = user_v["change_nation"]
                    cursor.execute(f"update patient_checkin set nationality = '{nation}' where health_card_no = {card_no}")
                    cnx.commit()
                    
                sg.popup_notify("Successfully Executed.", fade_in_duration = 20, display_duration_in_ms = 500)
    
        if user_e == "Remove":
            remove_patient()
        
        if user_e == "4":
            display_patient()
            
        if user_e == "Name_Sort":
            cursor.execute("select * from patient_checkin order by name asc")
            user_window.Element("Name_Sort").update(disabled = True)
            user_window.Element("Time_Sort").update(disabled = False)
            user_window.Element("Table").update(values = cursor.fetchall())
            cnx.commit()
        
        if user_e == "Time_Sort":
            cursor.execute("select * from patient_checkin order by date_time desc")
            user_window.Element("Time_Sort").update(disabled = True)
            user_window.Element("Name_Sort").update(disabled = False)
            user_window.Element("Table").update(values = cursor.fetchall())
            cnx.commit()
        
        if user_e == "Cancel":
            user_window[f'col{layout}'].update(visible = False)
            layout = 2
            user_window[f'col{layout}'].update(visible = True)
        
        if user_e == "Logout":
            user_window.close()
            break
