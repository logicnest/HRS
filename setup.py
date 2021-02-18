import mysql.connector as mc


cnx = mc.connect(host = "localhost", user = "root", password = "root")
cursor = cnx.cursor()
cnx.autocommit = True

def setup():
    
    cursor.execute("create database hospital")
    print(".")
    cursor.execute("use hospital")
    print(".")
    cursor.execute('''create table patient_checkin (Health_Card_No int(10), Name varchar(30) , Age int(5),
                    Gender varchar(10), Nationality varchar(40), Emergency varchar(3), Date_Time timestamp)''')
    print(".")
    cursor.execute("create table log (Username varchar(16), Date_Time timestamp)")
    print(".")
    cursor.execute("create table account (Username varchar(16), Password_Hash varchar(40), Account_Type varchar(5))")
    print(".")
    cursor.execute("insert into account values('test', '7110eda4d09e062aa5e4a390b0a572ac0d2c0220', 'User')")
    print(".")
    cursor.execute("insert into account values('admin', '7110eda4d09e062aa5e4a390b0a572ac0d2c0220', 'Admin')")
    print("successful")

def proper_setup():   
     
    try:
        setup()
        
    except mc.DatabaseError:
        print("Deleting existing database")
        cursor.execute("drop database hospital")
        setup()
        
proper_setup()