import datetime
import pyodbc
import serial


server = 'mysqlserver-tfg2022.database.windows.net'
database = 'plants'
username = 'azureuser'
password = 'pwd'   
driver= '{ODBC Driver 17 for SQL Server}'
conn =  pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
cursor = conn.cursor()


def arduino_read_T(arduino, unit):
    """ 
    In this function, the current temperature will be read from the aruino.

    :param arduino: HW it is going to use for checking the T
    :param unit: If the user prefers ºF or ºC

    :return: f, c: current temerature in farenheit and celisus
                txt_currentT: Text that will be shown on the gui
    """
    global fbefore
    global cbefore
    x = datetime.datetime.now()
    arduino.write(bytes("readT", 'utf-8'))
    value =  arduino.readline()
    try:
        value = str(value).lstrip("b'")
        value = str(value).rstrip("'")
        f, c = str(value).split(",")
    except:
        try:
            f = fbefore
            c = cbefore
        except: 
            f=65.3
            c=18.5
    fbefore=f
    cbefore=c
    #print(f"{x.hour}:{x.minute}:{x.second}, {c}")
    if unit == 1: txt_currentT = (f"Today, {x.day}/{x.month}/{x.year} at {x.hour}:{x.minute}:{x.second} it's {f}ºF")
    elif unit == 0: txt_currentT = (f"Today, {x.day}/{x.month}/{x.year} at {x.hour}:{x.minute}:{x.second} it's {c}ºC")
    else: txt_currentT = ""
    return float(f), float(c), txt_currentT


def arduino_write_cold(arduino):
    arduino.write(bytes("cold", 'utf-8'))


def arduino_write_hot(arduino):
    arduino.write(bytes("hot", 'utf-8'))


def get_unit():
    """
    In this function the user decides if they prefer the data in D or F

    :return: unit: If the user prefers ºF or ºC
    """
    unit = -1
    while unit == -1:
        unit = input("Would you rather get the temperature in \n1 - ºC\n2 - ºF\n>> ") # Takeing input from user
        try:
            if (int(unit) == 1): return (int(unit) - 1) # in celsius = 0
            elif (int(unit) == 2): return (int(unit) - 1) # in farenheit = 1
            else: 
                print("*****Enter a number from the list*****")
                unit = -1
        except: 
            print("*****Enter a number from the list*****")
            unit = -1


def get_T_by_plant(cursor, currentTinF, currentTinC, unit, name):
    """ 
    In this function, you will enter a plant name and it will return you if the 
    current temeprature is good for planting the plant "name".

    :param cursor: DB in which it is going to look up for all the plants
    :param currentTinF: Current temperature in farenheit
    :param currentTinC: Current temperature in celsius
    :param unit: If the user prefers ºF or ºC
    :param name: The name of the plat to look for
    """
    list_of_names = db_select_plant_by_name(cursor, name)
    if (not list_of_names): 
        return(f"*****There was no coincidences with '{name}'*****")
        
    if len(list_of_names) > 1 and list_of_names[0][1] != name:
        names = []
        for i in range(len(list_of_names)):
            names.append(list_of_names[i][1])
        return names
    else: idx = 0

    minTuser = list_of_names[idx][24]
    maxTuser = list_of_names[idx][25]
    minTuserC = round((minTuser - 32) * 5/9, 2)
    maxTuserC = round((maxTuser - 32) * 5/9, 2)

    if ((float(currentTinF) > minTuser) and (float(currentTinF) < maxTuser)):
        in_F = "You can plant " + list_of_names[idx][1] + "! The plant you choosed, lives between " + str(minTuser) + "ºF and " + str(maxTuser) + "ºF. The current temperature is " + str(currentTinF) + "ºF"
        in_C = "You can plant " + list_of_names[idx][1] + "! The plant you choosed, lives between " + str(minTuserC) + "ºC and " + str(maxTuserC) + "ºC. The current temperature is " + str(currentTinC) + "ºC"
    else:
        in_F = "You can not plant " + list_of_names[idx][1] + "! The plant you choosed, lives between " + str(minTuser) + "ºF and " + str(maxTuser) + "ºF. The current temperature is " + str(currentTinF) + "ºF"
        in_C = "You can not plant " + list_of_names[idx][1] + "! The plant you choosed, lives between " + str(minTuserC) + "ºC and " + str(maxTuserC) + "ºC. The current temperature is " + str(currentTinC) + "ºC"
    
    if (unit == 0): return (in_C) # in celsius
    else: return (in_F) # in farenheit
    

def get_plant_by_currentT(cursor, currentTinF, unit):
    """ 
    Having the current temperature, return the plants that could live
    in the current temperature.

    :param cursor: DB in which it is going to look up for all the plants
    :param currentTinF: Current temperature in farenheit
    :param unit: If the user prefers ºF or ºC
    """
    list_of_names = db_select_plants_by_T(cursor, currentTinF)

    if (unit == 0):
        print(f"The plants that you could plant are:\nName\t\t\tminT\t\tmaxT")
        for i in range(len(list_of_names)):
            print(f"{list_of_names[i][1]}\t\t{round((list_of_names[i][24] - 32) * 5/9, 2)}ºC\t{round((list_of_names[i][25] - 32) * 5/9, 2)}ºC") # printing the names of the plants C
    else:
        print(f"The plants that you could plant are:\nName\t\t\tminT\t\tmaxT")
        for i in range(len(list_of_names)):
            print(f"{list_of_names[i][1]}\t\t{list_of_names[i][24]}ºF\t{list_of_names[i][25]}ºF") # printing the names of the plants F
        

def db_get_by_filter(cursor, name, easygrow, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec):

    query = f"SELECT * FROM plants_db WHERE Name LIKE '%{name}%'"

    if easygrow==1: query += f" AND easyGrow = {easygrow}"

    if jan==1: query += f" AND sowMonthJan = {jan}"
    if feb==1: query += f" AND sowMonthFeb = {feb}"
    if mar==1: query += f" AND sowMonthMar = {mar}"
    if apr==1: query += f" AND sowMonthApr = {apr}"
    if may==1: query += f" AND sowMonthMay = {may}"
    if jun==1: query += f" AND sowMonthJun = {jun}"
    if jul==1: query += f" AND sowMonthJul = {jul}"
    if aug==1: query += f" AND sowMonthAug = {aug}"
    if sep==1: query += f" AND sowMonthSep = {sep}"
    if oct==1: query += f" AND sowMonthOct = {oct}"
    if nov==1: query += f" AND sowMonthNov = {nov}"
    if dec==1: query += f" AND sowMonthDec = {dec}"

    cursor.execute(query) # Send query and execute
    row = cursor.fetchone() # Move to the next row; 
    list_of_names = []
    while row:
        list_of_names.append(row)
        row = cursor.fetchone() # Move to the next row
    
    return list_of_names


def db_select_plant_by_name(cursor, plant):
    """ 
    In this function, you will enter a name of a plant and it will return all the 
    plants in the database that match with the name of the plant

    :param cursor: DB in which it is going to look up for all the plants
    :param plant: Name of the plant you want to take a look

    :return: list_of_names: List with all the plants that were matched (by name) of the database.
                            This list contains the rows of each match.
    """
    cursor.execute("SELECT * FROM plants_db") # Send query and execute
    # row = [id, Name, ..., maxTinF]
    row = cursor.fetchone() # Move to the next row; 
    list_of_names = []
    while row:
        if (plant.lower() in str(row[1]).lower()):
            # list_of_names = [row[0], row[1], ..., row[x]]
            list_of_names.append(row)
        row = cursor.fetchone() # Move to the next row

    return list_of_names


def db_select_plants_by_T(cursor, currentTinF):
    """ 
    In this function, the current temperature in farenheit will be given
    and it will return all the plants in the database that can grow in that specific climate.
    Is only given in ºF as the DB stores everything in ºF

    :param cursor: DB in which it is going to look up for all the plants
    :param currentTinF: Current temperature on farenheit

    :return: list_of_names: List with all the plants that were matched of the database.
                            This list contains the rows of each match.
    """
    query = f"""SELECT * FROM plants_db 
                WHERE minTinF <= {currentTinF} AND maxTinF >= {currentTinF};"""
    cursor.execute(query) # Send query and execute

    # row = [id, Name, ..., maxTinF]
    row = cursor.fetchone() # Move to the next row; 
    list_of_names = []
    while row:
        list_of_names.append(row)
        row = cursor.fetchone() # Move to the next row

    return list_of_names


def db_get_recommentadion(cursor):
    """ 
    In this function, the current temperature in farenheit will be given
    and it will return all the plants in the database that can grow in that specific climate.
    Is only given in ºF as the DB stores everything in ºF

    :param cursor: DB in which it is going to look up for all the plants
    :param currentTinF: Current temperature on farenheit

    :return: list_of_names: List with all the plants that were matched of the database.
                            This list contains the rows of each match.
    """
    cursor.execute("SELECT * FROM my_plants") # Send query and execute
    # row = [id, Name, ..., maxTinF]
    rows = cursor.fetchall()
    dicc_of_names = {}
    for row in rows:
        list_compatible_plants = db_get_recommentadion_db(cursor, row[1])
        for i in range(len(list_compatible_plants)):
            if str(row[1]).lower() in list_compatible_plants[i][6].lower():
                dicc_of_names[row[1]] = list_compatible_plants
        # row = cursor.fetchone() # Move to the next row

    return dicc_of_names


def db_get_recommentadion_db(cursor, name):
    
    cursor.execute(f"SELECT * FROM plants_db WHERE compatiblePlants LIKE '%{name}%' OR compatiblePlants LIKE '%{name.lower()}%'") # Send query and execute
    # row = [id, Name, ..., maxTinF]
    row = cursor.fetchone() # Move to the next row; 
    list_of_names = []
    while row:
        list_of_names.append(row)
        row = cursor.fetchone() # Move to the next row
    return list_of_names


def db_add_plant_to_my_db(cursor, plant):
    cursor.execute("SELECT * FROM plants_db") # Send query and execute
    # row = [id, Name, ..., maxTinF]
    row = cursor.fetchone() # Move to the next row; 
    list_of_names = []
    while row:
        if (plant.lower() in str(row[1]).lower()):
            # list_of_names = [row[0], row[1], ..., row[x]]
            list_of_names.append(row)
        row = cursor.fetchone() # Move to the next row
    for i in range(len(list_of_names[0])):
        if None == list_of_names[0][i]:
            list_of_names[0][i]="NULL"
    
    print(list_of_names)
    cursor.execute("SELECT * FROM my_plants") # Send query and execute
    row = cursor.fetchone() # Move to the next row; 
    list_i_have = []
    while row:
        # list_of_names = [row[0], row[1], ..., row[x]]
        list_i_have.append(row)
        row = cursor.fetchone() # Move to the next row
    
    print(list_i_have)
    if list_of_names[0][1] in list_i_have: return "exists"
    idx = list_i_have[-1][0]
    list_of_names[0][0] = idx+1

    cursor.execute(f"INSERT INTO my_plants (Column1, Name, alternateName, sowInstructions, spaceInstructionsInches, harvestInstructions, compatiblePlants, avoidInstructions, culinaryHints, culinaryPreservation, url, sowMonthJan, sowMonthFeb, sowMonthMar, sowMonthApr, sowMonthMay, sowMonthJun, sowMonthJul, sowMonthAug, sowMonthSep, sowMonthOct, sowMonthNov, sowMonthDec, easyGrow, minTinF, maxTinF) VALUES {list_of_names[0]};") # Send query and execute
    return "succesful"


def check_table(currentTinF):
    query = f"""SELECT * FROM plants_db 
            WHERE minTinF <= {currentTinF} AND maxTinF >= {currentTinF};"""

