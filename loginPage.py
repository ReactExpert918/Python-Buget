# Imports
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import re
#from PIL import ImageTk, Image
import csv

# Define colors
mainColor = "#56C3A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)

def showFrame(frame):
    frame.tkraise()

# Creating window
root=Tk()
root.state("zoomed")  #Makes it fullscreen automatically


# Configurations
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

loginFrame = Frame(root, background = mainColor)
registerFrame = Frame(root, background = mainColor)

for frame in (loginFrame, registerFrame):
    frame.grid(row = 0, column = 0, sticky = "nsew")

# Starting frame
showFrame(loginFrame)

sx = root.winfo_screenwidth() 
sy = root.winfo_screenheight()

# Set the window size
root.geometry("%dx%d" % (sx, sy))
root.title("Budget Boi")
root.iconbitmap("img/WayneStateLogo.ico")

#region Frame1
#============Frame 1 ==============# 
# Variables
activeUser = ""

# Functions
def submitLogin():
    global activeUser
    print("Login submit button clicked")
    userEntry = uInput.get()
    passEntry = pInput.get()
    foundFlag = False
    # Check username
    print("Userentry", userEntry, uInput.get())
    with open('UserData/userList.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            if line[0].lower().strip() == userEntry.lower() and line[1].strip() == passEntry:
                print("In file")
                foundFlag = True
                activeUser = userEntry
                messagebox.showinfo("Success!", "Welcome " + activeUser + "!")
                break
        if not foundFlag:
            print("Username (" + userEntry + ") not found")
            messagebox.showwarning("User not found")
            #warningLabel = Label(loginMenu, text = "Incorrect credentials", fg = "#FF890A", bg = accentColor)
            #warningLabel.config(font = ("Verdana", 12))
            #warningLabel.grid(row = 6, column = 1)
    uInput.delete(0, END)
    pInput.delete(0, END)
    print("Active user:", activeUser)

# Create subframe
widthAdjuster = 0.4
heightAdjuster = 0.2
loginMenu = Frame(loginFrame, bg = accentColor)
#loginMenu.grid(row = 0, column = 0, padx = sx * widthAdjuster, pady = sy * heightAdjuster, ipadx = 0, ipady = 0)
#loginMenu.place(height = 500, width = 400, anchor = CENTER, rely = 0.5, relx = 0.5)
loginMenu.pack()
loginMenu.config()
# Labels
loginTitle = Label(loginMenu, text = "Login", font = ("Courier", 80), bg = accentColor)
loginTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

usernameLabel = Label(loginMenu, text = "Username:", font = usernameFont, bg = accentColor)
usernameLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

passwordLabel = Label(loginMenu, text = "Password: ", font = usernameFont, bg = accentColor)
passwordLabel.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

# Create entry boxes
uInput = Entry(loginMenu, width = 20, font = inputFont)
uInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

pInput = Entry(loginMenu, width = 20, font = inputFont, show = '*')
pInput.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

# Create buttons
submitButton = Button(loginMenu, text = "Submit", bg = "#A9e451", padx = 10, pady = 0, font = ("Verdana", 15), command = submitLogin)
submitButton.grid(row = 5, column = 1, padx = 20, pady = 10, sticky = 'ew')
registerButton = Button(loginMenu, text = "Make new account", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(registerFrame))
registerButton.grid(row = 5, column = 0, padx = 20, pady = 10, sticky = 'ew')

#endregion

# Strong Password Check Function
#####################################################################################################


def uppercase_check(passEntry):
    if re.search('[A-Z]', passEntry): #atleast one uppercase character
        return True
    return False

def lowercase_check(passEntry):
    if re.search('[a-z]', passEntry): #atleast one lowercase character
        return True
    return False

def digit_check(passEntry):
    if re.search('[0-9]', passEntry): #atleast one digit
        return True
    return False

def spCr_check(passEntry):
    if re.search('[_@$!#%&?/\-]', passEntry): #atleast one digit
        return True
    return False



#####################################################################################################

# ===============Frame 2=====================#

# Functions
def registerAccount():
    print("Register account clicked")

    # Store entries
    userEntry = urInput.get()
    passEntry = prInput.get()
    confEntry = pcInput.get()
    foundFlag = False

    # Check username
    with open('UserData/userList.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            print(line)
            if line[0].lower().strip() == userEntry.lower():
                print("User already exists")
                messagebox.showwarning("Error", "User already exists")
                foundFlag = True
                

        if not foundFlag:
                #messagebox.showwarning("Password", "Must be in \n 1) Minimum 8 characters.\n 2) The alphabets must be between [a-z].\n 3) At least one alphabet should be of Upper Case [A-Z].\n 4) At least 1 number or digit between [0-9].")
            if passEntry != confEntry:
                messagebox.showerror("Error", "Passwords don't match")

            elif len(passEntry) >= 8 and uppercase_check(passEntry) and lowercase_check(passEntry) and digit_check(passEntry) and spCr_check(passEntry) :
                messagebox.showinfo("Excelent", "Your password is strong")
                with open ('UserData/userList.csv', 'a') as file:
                    writer = csv.writer(file, lineterminator="\n")
                    writer.writerow([userEntry, passEntry])
                print("User ", userEntry, "added!")
                messagebox.showinfo("Success!", "User is added successfully!")  
            else:
                messagebox.showwarning("Warning!", "Password is weak \n Password Must be in \n 1). Minimum 8 characters.\n 2). The alphabets must be between [a-z].\n 3). At least one alphabet should be of Upper Case [A-Z].\n 4). At least 1 number or digit between [0-9].\n 5). At least 1 special character ")
                
    
    urInput.delete(0, END)
    prInput.delete(0, END)
    pcInput.delete(0, END)



widthAdjuster2 = 0.37
heightAdjuster2 = 0.2
registerMenu = Frame(registerFrame, bg = accentColor)
#registerMenu.grid(row = 0, column = 0, padx = sx * widthAdjuster2, pady = sy * heightAdjuster2, ipadx = 0, ipady = 0)
registerMenu.place(height = 500, width = 460, anchor = CENTER, rely = 0.5, relx = 0.5)


# Create labels for login and place them
registerTitle = Label(registerMenu, text = "Register!", font = ("Courier", 60), bg = accentColor)
registerTitle.grid(row = 0, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "ew")

usernameLabel = Label(registerMenu, text = "Username: ", font = usernameFont, bg = accentColor)
usernameLabel.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = "w")

passwordLabel = Label(registerMenu, text = "Password: ", font = usernameFont, bg = accentColor)
passwordLabel.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')

passwordConLabel = Label(registerMenu, text = "Confirm Password: ", font = usernameFont, bg = accentColor)
passwordConLabel.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'w')


# Create input box for username and password
urInput = Entry(registerMenu, width = 20, font = inputFont)
urInput.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

prInput = Entry(registerMenu, width = 20, font = inputFont, show = '*')
prInput.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

pcInput = Entry(registerMenu, width = 20, font = inputFont, show = '*')
pcInput.grid(row = 6, column = 0, padx = 10, pady = 10, columnspan = 2,sticky = 'ew')

#Create buttons
confirmButton = Button(registerMenu, text = "Register", bg = "#A9E451", padx = 10, pady = 0, font = ("Verdana", 15), command = registerAccount)
confirmButton.grid(row = 7, column = 1, padx = 20, pady = 10, sticky = 'ew')

returnButton = Button(registerMenu, text = "Return to login", font = ("Verdana", 10), bg = mainColor, command = lambda: showFrame(loginFrame))
returnButton.grid(row = 7, column = 0, padx = 20, pady = 10, sticky = 'ew')


root.mainloop()