# Imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from tkcalendar import *
import xlsxwriter as xw

#region Window Config
# Define colors
mainColor = "#70A0A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)
aFont = ("Times New Roman", 20)


def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Fullscreen
sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

budgetFrame = Frame(root, background = mainColor)
budgetFrame.grid(row = 0, column = 0, sticky = "nsew")

showFrame(budgetFrame)
#endregion Window config

#region Frame1
#============Frame 1 ==============# 

#region Frame configuration
# Variables
activeUser = "test"
entries = []

tableFrame = Frame(budgetFrame, background = accentColor)
tableFrame.place(height = 700, width = 1000, relx = 0.5, rely = 0.5, anchor = CENTER)
# Create subframe
viewFrame = Frame(tableFrame, bg = accentColor)
#viewFrame.place(height = 500, width = 1000, relx = 0.5, rely = 0.05, anchor = N)
viewFrame.grid(row = 0, column = 0, columnspan = 5)
viewFrame.config(highlightbackground='black', highlightthickness=0)

# Scrollbar and table setup
tableScroll = ttk.Scrollbar(viewFrame, orient = 'vertical')
tableScroll.pack(side = RIGHT, fill = Y)
budgetTree = ttk.Treeview(viewFrame, yscrollcommand= tableScroll.set)
tableScroll.config(command = budgetTree.yview)

# Define columns
budgetTree['columns'] = ("Date", "Name", "Planned", "Actual", "Difference", "Notes")

# Format columns
budgetTree.column("#0", width = 0, stretch = NO)
budgetTree.column("Date", width = 140, anchor = W)
budgetTree.column("Name", width = 120, anchor = W)
budgetTree.column("Planned", width = 150, anchor = E)
budgetTree.column("Actual", width = 150, anchor = E)
budgetTree.column("Difference", width = 150, anchor = E)
budgetTree.column("Notes", width = 270, anchor = E)

#testTree.heading("#0", text = "Label", anchor = W)
budgetTree.heading("Date", text = "Date", anchor = CENTER)
budgetTree.heading("Name", text = "Name", anchor = CENTER)
budgetTree.heading("Planned", text = "Planned", anchor = CENTER)
budgetTree.heading("Actual", text = "Actual", anchor = CENTER)
budgetTree.heading("Difference", text = "Difference", anchor = CENTER)
budgetTree.heading("Notes", text = "Notes", anchor = CENTER)

budgetTree.tag_configure('oddrow', background = "white")
budgetTree.tag_configure('evenrow', background = "blue")

#endregion Frame Configuration

# Generate tuple from data for updates/insertions
def toTuple(date, name, planned, actual, notes = ""):
    a = date
    b = name
    c = '${:,.2f}'.format(float(planned)) 
    d = '${:,.2f}'.format(float(actual)) 
    e = round(float(planned) - float(actual), 2)
    e = '-${:,.2f}'.format(-e) if e < 0 else '${:,.2f}'.format(e)
    if notes:
        f = notes
    else:
        f = ""
    return (a, b, c, d, e, f)


#Read in csv data
expenseCount = 0
with open('UserData/'+ activeUser + '.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            tempTuple = toTuple(line[0], line[1], line[2], line[3], line[4])
            if expenseCount % 2 == 0:
                budgetTree.insert(parent = '', index = 'end', iid = expenseCount, values = tempTuple, tags = ('evenrow',))
            else:
                budgetTree.insert(parent = '', index = 'end', iid = expenseCount, values = tempTuple, tags = ('oddrow',))
            expenseCount += 1

# JUNK DATA
'''
for i in range(40):
    if expenseCount % 2 == 0:
        testTree.insert(parent = '', index = 'end', iid = expenseCount,values = ext("jdate", "jname", randint(0, 100), 30.493), tags = ('evenrow'))
    else:
        testTree.insert(parent = '', index = 'end', iid = expenseCount, values = ext("jdate", "jname", randint(0, 200), randint(30, 240)), tags = ('oddrow',))
    expenseCount += 1
'''


# Pack table
budgetTree.pack()

#region Button Functions
# ========= Button functions =========== #

# Add expense to table
def addExpense():
    global expenseCount
    date = monthEntry + "/" + dayEntry + "/" + yearEntry
    budgetTree.insert(parent = '', index = 'end', iid = expenseCount, values = toTuple(date, nameEntry.get(), plannedEntry.get(), actualEntry.get(), notesEntry.get()))
    expenseCount += 1
    with open('UserData/' + activeUser + '.csv', 'a', newline = '') as cFile:
        cWriter = csv.writer(cFile, delimiter=',')
        cWriter.writerow([date, nameEntry.get(), plannedEntry.get(), actualEntry.get(), notesEntry.get()])
    updateData()
    # Delete entries
    #for col in entryEditList:
    #    col.delete(0, END)


def openAddMenu():
    top = Toplevel()
    top.geometry("%dx%d" % (sx*.25, sy*0.6))
    top.config(background = accentColor)
    addCal = Calendar(top, selectmode = 'day', year = 2021, month = 6, day = 22, date_pattern = 'mm/dd/yyyy')
    addCal.grid(row = 0, column = 0, pady = 20, padx = 20, columnspan = 2, rowspan = 3)

    global monthEntry, dayEntry, yearEntry
    global nameEntry, plannedEntry, actualEntry, notesEntry
    
    selDateLabel = Label(top, text = "Selected Date: __/__/__", bg = accentColor)
    selDateLabel.grid(row = 1, column = 2, columnspan = 2, pady = 10, sticky = E)


    def grabDate():
        global monthEntry, dayEntry, yearEntry
        selectedDate = addCal.get_date()
        selDateLabel.config(text = selectedDate)
        monthEntry = selectedDate[:2]
        dayEntry = selectedDate[3:5]
        yearEntry = selectedDate[-4:]



    getDateButton = Button(top, text = "Use this date", command = grabDate)
    getDateButton.grid(row = 0, column = 2, rowspan = 2, columnspan = 2)

    nameLabel = Label(top, text = "Name:", bg = accentColor)
    plannedLabel = Label(top, text = "Planned:", bg = accentColor)
    actualLabel = Label(top, text = "Actual:", bg = accentColor)
    notesLabel = Label(top, text = "Notes:", bg = accentColor)

    nameLabel.grid(row = 3, column = 0, pady = 10)
    plannedLabel.grid(row = 4, column = 0, pady = 10)
    actualLabel.grid(row = 5, column = 0, pady = 10)
    notesLabel.grid(row = 6, column = 0, pady = 10)

    nameEntry = Entry(top)
    plannedEntry = Entry(top)
    actualEntry = Entry(top)
    notesEntry = Entry(top)

    nameEntry.grid(row = 3, column = 1, pady = 10)
    plannedEntry.grid(row = 4, column = 1, pady = 10)
    actualEntry.grid(row = 5, column = 1, pady = 10)
    notesEntry.grid(row = 6, column = 1, pady = 10)

    addEntryButton = Button(top, text = "Add Entry", command = addExpense)
    addEntryButton.grid(row = 3, column = 3, rowspan = 2, columnspan = 3, ipadx = 30, ipady = 20, pady = 10, sticky = NW)

    cancelAddButton = Button(top, text = "Cancel", command = lambda: top.destroy())
    cancelAddButton.grid(row = 5, column = 3, rowspan = 2, columnspan = 3, ipadx = 30, ipady = 20, pady = 10, sticky = NW)


# Update entry in table
def updateExpense():
    selected = budgetTree.focus()
    date = umonthEntry + "/" + udayEntry + "/" + uyearEntry

    # Save new info
    budgetTree.item(selected, text = "", values = toTuple(date, unameEntry.get(), uplannedEntry.get(), uactualEntry.get(), unotesEntry.get()))
    updateData()


def openUpdateMenu():
    utop = Toplevel()
    utop.geometry("%dx%d" % (sx*.25, sy*0.6))
    utop.config(background = accentColor)

    global umonthEntry, udayEntry, uyearEntry
    global unameEntry, uplannedEntry, uactualEntry, unotesEntry
    
    selDateLabel = Label(utop, text = "Selected Date: __/__/__", bg = accentColor)
    selDateLabel.grid(row = 1, column = 2, columnspan = 2, pady = 10, sticky = E)

    # Get date from calendar
    def grabDate():
        global umonthEntry, udayEntry, uyearEntry
        selectedDate = updCal.get_date()
        selDateLabel.config(text = selectedDate)
        umonthEntry = selectedDate[:2]
        udayEntry = selectedDate[3:5]
        uyearEntry = selectedDate[-4:]



    getDateButton = Button(utop, text = "Use this date", command = grabDate)
    getDateButton.grid(row = 0, column = 2, rowspan = 2, columnspan = 2)

    nameLabel = Label(utop, text = "Name:", bg = accentColor)
    plannedLabel = Label(utop, text = "Planned:", bg = accentColor)
    actualLabel = Label(utop, text = "Actual:", bg = accentColor)
    notesLabel = Label(utop, text = "Notes:", bg = accentColor)

    nameLabel.grid(row = 3, column = 0, pady = 10)
    plannedLabel.grid(row = 4, column = 0, pady = 10)
    actualLabel.grid(row = 5, column = 0, pady = 10)
    notesLabel.grid(row = 6, column = 0, pady = 10)

    unameEntry = Entry(utop)
    uplannedEntry = Entry(utop)
    uactualEntry = Entry(utop)
    unotesEntry = Entry(utop)

    unameEntry.grid(row = 3, column = 1, pady = 10)
    uplannedEntry.grid(row = 4, column = 1, pady = 10)
    uactualEntry.grid(row = 5, column = 1, pady = 10)
    unotesEntry.grid(row = 6, column = 1, pady = 10)

    selected = budgetTree.focus()
    tempValues = budgetTree.item(selected, 'values')

    unameEntry.insert(0, tempValues[1])
    uplannedEntry.insert(0, tempValues[2].replace('$',''))
    uactualEntry.insert(0, tempValues[3].replace('$',''))
    unotesEntry.insert(0, tempValues[5])

    tm = tempValues[0][:2]
    td = tempValues[0][3:5]
    ty = tempValues[0][-4:]
    updCal = Calendar(utop, selectmode = 'day', year = int(ty), month = int(tm), day = int(td), date_pattern = 'mm/dd/yyyy')
    updCal.grid(row = 0, column = 0, pady = 20, padx = 20, columnspan = 2, rowspan = 3)
    grabDate()


    updateButton = Button(utop, text = "Update Entry", command = updateExpense)
    updateButton.grid(row = 3, column = 3, rowspan = 2, columnspan = 3, ipadx = 30, ipady = 20, pady = 10, sticky = W)

    cancelAddButton = Button(utop, text = "Cancel", command = lambda: utop.destroy())
    cancelAddButton.grid(row = 5, column = 3, rowspan = 2, columnspan = 3, ipadx = 45, ipady = 20, pady = 10, sticky = W)


# Remove expense from table
def deleteExpense():
    global expenseCount
    c = messagebox.askokcancel("Warning", "Are you sure you want to delete selected item(s)? (This cannot be undone)")
    if c:
        for record in budgetTree.selection():
            budgetTree.delete(record)
            expenseCount -= 1
    updateData()


# Export file as xlsx
def export():
    newXS = xw.Workbook('HELLO THERE.xlsx')
    s1 = newXS.add_worksheet('Current Month')
    rnum = 1
    cnum = 0
    messagebox.showinfo("File Alert", "Excel file has been created!")

    bold = newXS.add_format({'bold': True})
    s1.write(rnum, cnum + 1, "Date", bold)
    s1.write(rnum, cnum + 2, "Name", bold)
    s1.write(rnum, cnum + 3, "Planned", bold)
    s1.write(rnum, cnum + 4, "Actual", bold)
    s1.write(rnum, cnum + 5, "Difference", bold)
    s1.write(rnum, cnum + 6, "Notes", bold)
    rnum += 1
    with open('UserData/'+activeUser+'.csv', 'r') as file:
        reader = csv.reader(file)
        for d, n, p, a, m in reader:
            s1.write(rnum, cnum + 1, d)
            s1.write(rnum, cnum + 2, n)
            s1.write(rnum, cnum + 3, float(p))
            s1.write(rnum, cnum + 4, float(a))
            s1.write(rnum, cnum + 5, float(p)-float(a))
            s1.write(rnum, cnum + 6, m)
            rnum += 1
    newXS.close()


# Update CSV with current table data
def updateData():
    with open('UserData/' + activeUser + '.csv', 'w', newline = '') as uFile:
        cWriter = csv.writer(uFile, delimiter = ',')
        for record in budgetTree.get_children():
            t = budgetTree.item(record)['values']
            temp = [t[0], t[1], str(t[2]).replace('$', '').replace(',',''), str(t[3]).replace('$','').replace(',',''), t[5]]
            cWriter.writerow(temp)
    uFile.close()

#endregion ButtonFunctions


# Main Entry Buttons
addButton = Button(tableFrame, text = "Add expense", command = openAddMenu, font = usernameFont, height = 4, width = 15)
addButton.grid(row = 3, column = 0, pady = 20)
addButton.config(bg = '#40c25c')

updateButton = Button(tableFrame, text = "Edit Entry", font = usernameFont, command = openUpdateMenu, height = 4, width = 15)
updateButton.grid(row = 3, column = 2, pady = 20)
updateButton.config(bg = '#e0be36')

removeButton = Button(tableFrame, text = "Delete Entry", font = usernameFont, command = deleteExpense, height = 4, width = 15)
removeButton.grid(row = 3, column = 4, pady = 20)
removeButton.config(bg = '#d14232')

convertButton = Button(budgetFrame, text = "Convert", command = export, font = usernameFont, height = 3, width = 15, bg = accentColor)
convertButton.grid(row = 0, column = 0, pady = 0)

# Formatting (font changes)
style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 12))
style.configure("Treeview", font = ("Verdana", 16), rowheight = 50)


# KEEP THIS CALENDAR. FOR SOME REASON CODE GLITCHES W/O IT EVEN THOUGH IT'S NOT EVEN PACKED IN
cal = Calendar(root)

#endregion

root.mainloop()