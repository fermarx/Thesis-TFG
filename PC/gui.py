import sys
from tkinter.scrolledtext import ScrolledText
from database import *
from tkinter import *
import webbrowser

def w_get_unit():
    """
    Create the first window, for letting the user decide wether if they want C or F
    """
    def accept():
        """
        Sets global variable "unit"
        """
        global unit
        unit = opcion.get()
        window_get_unit.destroy()

    # Configuration of the window for getting the units
    window_get_unit = Tk()
    window_get_unit.geometry("350x110+0+0") # window size
    window_get_unit.resizable(0, 0) # no maximize
    window_get_unit.title("Know your plants") # window title 
    window_get_unit.config(bg="burlywood") # bg color
    Label(window_get_unit, text="Choose the units you would like to get your data.", font="Helvetica 10 bold", bg="burlywood").pack()
    opcion = IntVar()
    Radiobutton(window_get_unit, text="Celsius (ºC)", variable=opcion, value=0, font="Helvetica 10", bg="burlywood").pack()
    Radiobutton(window_get_unit, text="Farenheit (ºF)", variable=opcion, value=1, font="Helvetica 10", bg="burlywood").pack()
    Button(window_get_unit, text="Accept", command=accept, font="Helvetica 10", bg="burlywood").pack()
    window_get_unit.mainloop() # loop of application

w_get_unit()

app = Tk() # Creating the window
app.geometry("1000x700+0+0") # window size
app.resizable(0, 0) # no maximize
app.title("Know your plants") # window title 
app.config(bg="burlywood") # bg color

def update_clock():
    """
    Updates the label where the time and temperature is shown
    """
    global currentTinF
    global currentTinC
    global text_currentT
    currentTinF, currentTinC, text_currentT = arduino_read_T(arduino, unit)
    
    label_title.config(text = text_currentT)
    app.after(1000,update_clock) # Here is the change

# Create top frame
top_frame = Frame(app, relief=FLAT) 
top_frame.pack(side=TOP)
# Create label where time and temperature will be shown
label_title = Label(top_frame, text=" ", font="Helvetica 30 bold", bg="burlywood", width=40)
label_title.grid(row=0, column=0)
update_clock()

# Create right frame
right_frame = Frame(app, bg="burlywood", relief=FLAT)
right_frame.pack(side=RIGHT)

def delete_right_frame():
    """
    Clean right frame for new frames not appearing on top
    """
    if right_frame.winfo_children():
        for widget in right_frame.winfo_children():
            widget.destroy()

def frame_get_T_by_plant():   
    """
    Creates the frame where it will be shown if the temeprature is good for planting the plant "name".
    """ 
    delete_right_frame()
    # Create frame where label with the information will be shown
    frame_info_plant = Frame(right_frame, relief=FLAT, bg="burlywood")
    frame_info_plant.pack(side=BOTTOM)
    label_info_plant = Label(frame_info_plant, text=" ", font="Helvetica 10", bg="burlywood", wraplength=550)

    def plant_list(name, tk):
        """
        Delete button for it not to get accumulated

        :param name: name of the plant to be passed to plant()
        :param tk: Window to delete
        """
        tk.destroy()
        plant(name)

    def show_info_button(name, boton):
        """
        Delete info for it not to get accumulated
        
        :param name: name of the plant to be passed to plant()
        :param boton: Button to delete
        """
        boton.destroy()
        show_info(name)

    def plant(name_plant):
        """
        When pressing the button "Submit" 
        
        :param name_plant: Name/List of names to search in th DB
        """
        text_can_i_plant = get_T_by_plant(cursor, currentTinF, currentTinC, unit, name_plant)
        label_info_plant.grid(row=0, columnspan=2)
        if (type(text_can_i_plant) == list) and text_can_i_plant[0] != name_plant:
            list_plants = text_can_i_plant
            # Create new window for selecting the plants that matched
            select_plant = Tk()
            select_plant.geometry("300x400+0+0") # window size
            select_plant.resizable(0, 0) # no maximize
            select_plant.title("Know your plants") # window title 
            select_plant.config(bg="burlywood") # bg color
            Label(select_plant, text="We have found options!", font="Helvetica 10 bold", bg="burlywood").pack()
            text = Text(select_plant, background="burlywood", bg="burlywood")
            text.pack(side='left', fill='both', expand=0)
            sb = Scrollbar(select_plant, command=text.yview)
            sb.pack(side="right", fill='both', expand=0)
            text.configure(yscrollcommand=sb.set)
            created_buttons = []

            boton = Button(text, text=list_plants[0], bg="burlywood", command=lambda name=list_plants[0], tk=select_plant:plant_list(name, tk), font="Helvetica 10 bold", width=30)
            created_buttons.append(boton)
            created_buttons[0].grid(row=0)
            text.window_create("end", window=created_buttons[0])

            for i in range(1, len(list_plants)):
                current_name = list_plants[i]
                boton = Button(text, text=current_name, bg="burlywood", command=lambda name=current_name, tk=select_plant:plant_list(name, tk), font="Helvetica 10 bold", width=30)
                created_buttons.append(boton)
                created_buttons[i].grid(row=i)
                text.window_create("end", window=created_buttons[i])
                text.insert("end", "\n")
            text.configure(state="disabled")
        elif text_can_i_plant[0] == name_plant:
            text = get_T_by_plant(cursor, currentTinF, currentTinC, unit, text_can_i_plant[0])
            label_info_plant.config(text="")
            label_info_plant.config(text=text)
            if "*****" in text: pass
            else: implement_as_button(name_plant)
        else:
            label_info_plant.config(text="")
            label_info_plant.config(text=text_can_i_plant)
            if "*****" in text_can_i_plant: pass
            else: implement_as_button(name_plant)
        
    # Create frame where input will be asked
    frame_get_input_name = Frame(right_frame, relief=FLAT, bg="burlywood")
    frame_get_input_name.pack(side=TOP, anchor=CENTER)
    Label(frame_get_input_name, text="Enter the name of a plant and it will tell you if the current temperature is good for planting.", font="Helvetica 10 bold", bg="burlywood").grid(row=0, columnspan=3)
    Label(frame_get_input_name, text=" ", font="Helvetica 10 bold", bg="burlywood").grid(row=1, columnspan=3)
    Label(frame_get_input_name, text="Name of the plant", font="Helvetica 10 bold", bg="burlywood").grid(row=2, column=0)
    name = Entry(frame_get_input_name)
    name.grid(row=2, column=1)
    sub_btn = Button(frame_get_input_name,text='Submit', command=lambda:plant(name.get()), font="Helvetica 10", bg="burlywood")
    sub_btn.grid(row=2,column=2)

    def implement_as_button(name):
        """
        Create button for getting more information about the plant "name"

        :param name: Name of the plant to show information
        """
        button_name = Frame(right_frame, relief=FLAT, bg="burlywood")
        button_name.pack()
        boton = Button(button_name, text=f"Show more info about {name}", bg="burlywood",  font="Helvetica 10 bold", width=50)
        boton.grid(row=0, column=0)
        boton.config(command=lambda:show_info_button(name, button_name))

def frame_get_plant_by_currentT():
    """
    Creates the frame where it will be shown the plants recommended for the current temperature
    """ 
    if (currentTinF == -1): return
    delete_right_frame()
    list_names = db_select_plants_by_T(cursor, float(currentTinF))    
    info = Frame(right_frame, relief=FLAT, bg="burlywood")
    info.pack(side=TOP)
    window_get_T_by_plant_info = Frame(right_frame, relief=FLAT, bg="burlywood")
    window_get_T_by_plant_info.pack(side=BOTTOM)
    
    if unit==1: Label(info, text=f"With {currentTinF}ºF you can plant:", font="Helvetica 10 bold", bg="burlywood").grid(row=0, column=0)
    else: Label(info, text=f"With {currentTinC}ºC you can plant:", font="Helvetica 10 bold", bg="burlywood").grid(row=0, column=0)
    
    if (len(list_names) > 1):
        text = Text(window_get_T_by_plant_info, background="burlywood", bg="burlywood",width=30)
        text.pack(side='left', fill='both', expand=0)
        sb = Scrollbar(window_get_T_by_plant_info, command=text.yview)
        sb.pack(side="right", fill='both', expand=0)
        text.configure(yscrollcommand=sb.set)
        created_buttons = []

        boton = Button(text, text=list_names[0][1], bg="burlywood", command=lambda name=list_names[0][1]:show_info(name), font="Helvetica 10 bold", width=30)
        created_buttons.append(boton)
        created_buttons[0].grid(row=0)
        text.window_create("end", window=created_buttons[0])
        
        for i in range(1, len(list_names)):
            name = list_names[i][1]
            boton = Button(text, text=name, bg="burlywood", command=lambda name=name:show_info(name), font="Helvetica 10 bold", width=30)
            created_buttons.append(boton)
            created_buttons[i].grid(row=i)
            text.window_create("end", window=created_buttons[i])
            text.insert("end", "\n")
        text.configure(state="disabled") 
    else: show_info(list_names[0][1])
    
def frame_search_by_filer():
    delete_right_frame()

    # Create frame where input will be asked
    frame_get_input = Frame(right_frame, relief=FLAT, bg="burlywood")
    frame_get_input.pack(side=TOP)
    Label(frame_get_input, text="Name of the plant", font="Helvetica 10 bold", bg="burlywood").grid(row=0, column=0)
    name = Entry(frame_get_input)
    name.grid(row=0, column=1)
    easygrow = IntVar()
    Checkbutton(frame_get_input, text="Easy to grow", font="Helvetica 10 bold", bg="burlywood", variable=easygrow).grid(row=0, column=2)
    Label(frame_get_input, text=" ", font="Helvetica 10 bold", bg="burlywood").grid(row=1, column=0)
    jan = IntVar()
    Checkbutton(frame_get_input, variable=jan , text="January", font="Helvetica 10 bold", bg="burlywood").grid(row=1, column=0)
    feb = IntVar()
    Checkbutton(frame_get_input, variable=feb , text="February", font="Helvetica 10 bold", bg="burlywood").grid(row=1, column=1)
    mar = IntVar()
    Checkbutton(frame_get_input, variable=mar , text="March", font="Helvetica 10 bold", bg="burlywood").grid(row=1, column=2)
    apr = IntVar()
    Checkbutton(frame_get_input, variable=apr , text="April", font="Helvetica 10 bold", bg="burlywood").grid(row=2, column=0)
    may = IntVar()
    Checkbutton(frame_get_input, variable=may , text="May", font="Helvetica 10 bold", bg="burlywood").grid(row=2, column=1)
    jun = IntVar()
    Checkbutton(frame_get_input, variable=jun , text="June", font="Helvetica 10 bold", bg="burlywood").grid(row=2, column=2)
    jul = IntVar()
    Checkbutton(frame_get_input, variable=jul , text="July", font="Helvetica 10 bold", bg="burlywood").grid(row=3, column=0)
    aug = IntVar()
    Checkbutton(frame_get_input, variable=aug , text="August", font="Helvetica 10 bold", bg="burlywood").grid(row=3, column=1)
    sep = IntVar()
    Checkbutton(frame_get_input, variable=sep , text="September", font="Helvetica 10 bold", bg="burlywood").grid(row=3, column=2)
    oct = IntVar()
    Checkbutton(frame_get_input, variable=oct , text="October", font="Helvetica 10 bold", bg="burlywood").grid(row=4, column=0)
    nov = IntVar()
    Checkbutton(frame_get_input, variable=nov , text="November", font="Helvetica 10 bold", bg="burlywood").grid(row=4, column=1)
    dec = IntVar()
    Checkbutton(frame_get_input, variable=dec , text="December", font="Helvetica 10 bold", bg="burlywood").grid(row=4, column=2)

    sub_btn = Button(frame_get_input,text='Submit', command=lambda:get_by_filter(name.get(), easygrow.get(), jan.get(), feb.get(), mar.get(),
                                                                                 apr.get(), may.get(), jun.get(), jul.get(), aug.get(), 
                                                                                 sep.get(), oct.get(), nov.get(), dec.get(), frame_get_input), font="Helvetica 10", bg="burlywood")
    sub_btn.grid(row=5,column=1)

def get_by_filter(name, easygrow, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec, frame_get_input):
    text_info = db_get_by_filter(cursor, name, easygrow, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec)
    names = []
    for name in text_info:
        names.append(name)
    show_recommended("", names, frame_get_input)

def frame_search_by_name():
    """
    Creates the frame for showing all the plants and choose wich one you want to select
    """
    delete_right_frame()
    # panel buttons
    window_get_T_by_plant = Frame(right_frame, relief=FLAT, bg="burlywood")
    window_get_T_by_plant.pack(side=TOP, anchor=CENTER)

    Label(window_get_T_by_plant, text="Enter the name or the partial name of a plant, for getting information about it.", font="Helvetica 10 bold", bg="burlywood").grid(row=0, columnspan=3)
    Label(window_get_T_by_plant, text=" ", font="Helvetica 10 bold", bg="burlywood").grid(row=1, columnspan=3)
    Label(window_get_T_by_plant, text="Name of the plant", font="Helvetica 10 bold", bg="burlywood").grid(row=2, column=0)
    name = Entry(window_get_T_by_plant)
    name.grid(row=2, column=1)
    sub_btn=Button(window_get_T_by_plant,text='Submit', command=lambda:show_info(name.get()), font="Helvetica 10", bg="burlywood")
    sub_btn.grid(row=2,column=2)

def show_info(name):
    """
    Create window for choosing the plant and show info
    """
    text_info = db_select_plant_by_name(cursor, name)
    # Configuration of the window for getting the units
    info = Tk()
    info.geometry("700x300+0+0") # window size
    info.resizable(0, 0) # no maximize
    info.title("Know your plants") # window title 
    info.config(bg="burlywood") # bg color
    if (len(text_info) > 1) and text_info[0][1] != name:
        text = Text(info, background="burlywood", bg="burlywood")
        text.pack(side="left")
        sb = Scrollbar(info, command=text.yview)
        sb.pack(side="right")
        text.configure(yscrollcommand=sb.set)
        created_buttons = []

        boton = Button(text, text=text_info[0][1], bg="burlywood", command=lambda name=text_info[0][1]:show_info(name), font="Helvetica 10 bold", width=50)
        created_buttons.append(boton)
        created_buttons[0].grid(row=0, column=0)
        text.window_create("end", window=boton)

        for i in range(1, len(text_info)):
            name = text_info[i][1]
            boton = Button(text, text=name, bg="burlywood", command=lambda name=name:show_info(name), font="Helvetica 10 bold", width=50)
            created_buttons.append(boton)
            created_buttons[i].grid(row=i, column=0)
            text.window_create("end", window=boton)
            text.insert("end", "\n")
        text.configure(state="disabled")
    elif len(text_info) == 0: Label(info, text=f"Sorry! We did not found any coincidence with '{name}' in our DB.", font="Helvetica 20", bg="burlywood", wraplength=650).pack()
    else:
        if text_info[0][2]: Label(info, text=f"{text_info[0][1]} also known as {text_info[0][2]}.", font="Helvetica 10 bold", bg="burlywood", wraplength=650).pack()
        else: Label(info, text=f"{text_info[0][1]}.", font="Helvetica 10 bold", bg="burlywood", wraplength=650).pack()
        if text_info[0][23]: Label(info, text=f"It is easy to grow!", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        
        if text_info[0][3]: Label(info, text=f"Sow instructions: {text_info[0][3]}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        if text_info[0][4]: Label(info, text=f"Plant around {text_info[0][4]} inches between any other plant", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        if text_info[0][5]: Label(info, text=f"Harvest instructions: {text_info[0][5]}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        if text_info[0][6]: Label(info, text=f"Plants that are compatible: {text_info[0][6]}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        if text_info[0][7]: Label(info, text=f"To avoid: {text_info[0][7]}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        if text_info[0][8]: Label(info, text=f"Culinary hints: {text_info[0][8]}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        if text_info[0][9]: Label(info, text=f"Culinary preservation: {text_info[0][9]}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()
        def callback(url):
            webbrowser.open_new(url)
        if text_info[0][10]: 
            link = Label(info, text="For more information visit this link.", fg="blue",  bg="burlywood", cursor="hand2")
            link.pack()
            link.bind("<Button-1>", lambda e: callback(text_info[0][10]))
        growIn = ""
        if text_info[0][11]: growIn += "January, "
        if text_info[0][12]: growIn += "Februay, "
        if text_info[0][13]: growIn += "March, "
        if text_info[0][14]: growIn += "April, "
        if text_info[0][15]: growIn += "May, "
        if text_info[0][16]: growIn += "June, "
        if text_info[0][17]: growIn += "July, "
        if text_info[0][18]: growIn += "August, "
        if text_info[0][19]: growIn += "September, "
        if text_info[0][20]: growIn += "October, "
        if text_info[0][21]: growIn += "November, "
        if text_info[0][22]: growIn += "December, "
        
        Label(info, text=f"Ideal to grow in: {growIn}", font="Helvetica 10", bg="burlywood", wraplength=650).pack()

        if unit == 0:
            Label(info, text=f"Minimum temperature: {round((text_info[0][24] - 32) * 5/9, 2)}ºC. Maximum temperature: {round((text_info[0][25] - 32) * 5/9, 2)}ºC", font="Helvetica 10", bg="burlywood").pack()
        else: Label(info, text=f"Minimum temperature: {text_info[0][24]}ºF. Maximum temperature {text_info[0][25]}ºF", font="Helvetica 10", bg="burlywood").pack()

    info.mainloop()

def frame_get_recommendation():
    """
    Creates the frame for showing all the plants and choose wich one you want to select
    """
    delete_right_frame()
    # panel buttons
    dicc_recommendations = db_get_recommentadion(cursor)
    widget_recommended = Frame(right_frame, relief=FLAT, bg="burlywood")
    widget_recommended.pack(side=LEFT, anchor=CENTER)
    widget_recommended_list = Frame(widget_recommended, relief=FLAT, bg="burlywood")
    widget_recommended_list.pack(side=RIGHT)

    Label(widget_recommended, text=f"Select a plant form your db", font="Helvetica 10 bold", bg="burlywood").pack()

    text = Text(widget_recommended, background="burlywood", bg="burlywood",width=30)
    text.pack(side='left', fill='both', expand=0)
    sb = Scrollbar(widget_recommended, command=text.yview)
    sb.pack(side="right", fill='both', expand=0)
    text.configure(yscrollcommand=sb.set)
    created_buttons = []
    # un boton que le des a my_plant yqu ete enseñe lo  q te recomeinda
    i=0
    for my_plant, list_recommended in dicc_recommendations.items():
        boton = Button(text, text=my_plant, bg="burlywood", command=lambda my_plant=my_plant, list_recommended=list_recommended, widget_recommended_list=widget_recommended_list:show_recommended(my_plant,list_recommended,widget_recommended_list), font="Helvetica 10 bold", width=30)
        created_buttons.append(boton)
        created_buttons[i].grid(row=i)
        text.window_create("end", window=created_buttons[i])
        text.insert("end", "\n")
        i+=1
    text.configure(state="disabled") 

def show_recommended(my_plant, list_recommended, widget_recommended_list):
    if widget_recommended_list.winfo_children():
        for widget in widget_recommended_list.winfo_children():
            widget.destroy()

    if my_plant=="": Label(widget_recommended_list, text=f"Plants found", font="Helvetica 10 bold", bg="burlywood").pack()
    else: Label(widget_recommended_list, text=f"Compatible plants with {my_plant}", font="Helvetica 10 bold", bg="burlywood").pack()
    
    text = Text(widget_recommended_list, background="burlywood", bg="burlywood",width=30)
    text.pack(side='left', fill='both', expand=0)
    sb = Scrollbar(widget_recommended_list, command=text.yview)
    sb.pack(side="right", fill='both', expand=0)
    text.configure(yscrollcommand=sb.set)
    created_buttons = []
    i=0
    for recommended in list_recommended:
        boton = Button(text, text=recommended[1], bg="burlywood", command=lambda name=recommended[1]:show_info(name), font="Helvetica 10 bold", width=30)
        created_buttons.append(boton)
        created_buttons[i].grid(row=i)
        text.window_create("end", window=created_buttons[i])
        text.insert("end", "\n")
        i+=1
    text.configure(state="disabled") 

def frame_add_plant_db():
    """
    Creates the frame for showing all the plants and choose wich one you want to select
    """
    delete_right_frame()
    # panel buttons
    window_get_T_by_plant = Frame(right_frame, relief=FLAT, bg="burlywood")
    window_get_T_by_plant.pack(side=TOP, anchor=CENTER)

    Label(window_get_T_by_plant, text="Enter the name or the partial name of a plant, for adding to your DB", font="Helvetica 10 bold", bg="burlywood").grid(row=0, columnspan=3)
    Label(window_get_T_by_plant, text=" ", font="Helvetica 10 bold", bg="burlywood").grid(row=1, columnspan=3)
    Label(window_get_T_by_plant, text="Name of the plant", font="Helvetica 10 bold", bg="burlywood").grid(row=2, column=0)
    name = Entry(window_get_T_by_plant)
    name.grid(row=2, column=1)
    sub_btn=Button(window_get_T_by_plant,text='Submit', command=lambda:db_add_plant(name.get()), font="Helvetica 10", bg="burlywood")
    sub_btn.grid(row=2,column=2)


def db_add_plant(name):
    """
    Create window for choosing the plant and show info
    """
    text_info = db_select_plant_by_name(cursor, name)
    # Configuration of the window for getting the units
    info = Tk()
    info.geometry("700x300+0+0") # window size
    info.resizable(0, 0) # no maximize
    info.title("Know your plants") # window title 
    info.config(bg="burlywood") # bg color
    if (len(text_info) > 1) and text_info[0][1] != name:
        text = Text(info, background="burlywood", bg="burlywood")
        text.pack(side="left")
        sb = Scrollbar(info, command=text.yview)
        sb.pack(side="right")
        text.configure(yscrollcommand=sb.set)
        created_buttons = []

        boton = Button(text, text=text_info[0][1], bg="burlywood", command=lambda name=text_info[0][1]:db_add_plant(name), font="Helvetica 10 bold", width=50)
        created_buttons.append(boton)
        created_buttons[0].grid(row=0, column=0)
        text.window_create("end", window=boton)

        for i in range(1, len(text_info)):
            name = text_info[i][1]
            boton = Button(text, text=name, bg="burlywood", command=lambda name=name:db_add_plant(name), font="Helvetica 10 bold", width=50)
            created_buttons.append(boton)
            created_buttons[i].grid(row=i, column=0)
            text.window_create("end", window=boton)
            text.insert("end", "\n")
        text.configure(state="disabled")
    elif len(text_info) == 0: Label(info, text=f"Sorry! We did not found any coincidence with '{name}' in our DB.", font="Helvetica 20", bg="burlywood", wraplength=650).pack()
    else:
        done = db_add_plant_to_my_db(cursor, text_info[0][1])
        if done == "succesful": Label(info, text=f"{text_info[0][1]} introduced correctly!", font="Helvetica 20", bg="burlywood", wraplength=650).pack()
        elif done == "exists": Label(info, text=f"{text_info[0][1]} already in DB!", font="Helvetica 20", bg="burlywood", wraplength=650).pack()

    info.mainloop()

# Create left frame
left_frame = Frame(app, relief=FLAT)
left_frame.pack(side=LEFT)
# Buttons
buttons = ["Get if the current temperature is good for a plant", "Get which plants are good for the current T", "Search by filter", "Get recommendation by my plants DB", "Add plant to my DB"]
created_buttons = []
col = 0
# Add buttons to left frame 
for boton in buttons:
    boton = Button(left_frame, text=boton.title(), bg="burlywood",  font="Helvetica 10 bold", width=50)
    created_buttons.append(boton)
    boton.grid(row=col, column=0)
    col+=1
created_buttons[0].config(command=frame_get_T_by_plant) # Add what to do when pushing the button
created_buttons[1].config(command=frame_get_plant_by_currentT) # Add what to do when pushing the button
created_buttons[2].config(command=frame_search_by_filer) # Add what to do when pushing the button
##created_buttons[3].config(command=frame_search_by_name) # Add what to do when pushing the button -------------- almost like search by filetr...
created_buttons[3].config(command=frame_get_recommendation) # Add what to do when pushing the button
created_buttons[4].config(command=frame_add_plant_db) # Add what to do when pushing the button

# make the top right close button colse all windows
def close_window(): sys.exit()
app.protocol("WM_DELETE_WINDOW", close_window)

app.mainloop() # loop of application
  