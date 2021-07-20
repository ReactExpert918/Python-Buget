from loginPage import digit_check
import tkinter as tk
from tkinter.constants import *
from tkinter import *
from tkinter import Listbox, PhotoImage, Scrollbar, Widget, ttk
from tkinter import simpledialog
from tkinter.filedialog import askopenfile
from typing import Sized, ValuesView
import matplotlib.pyplot as plot
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from tkinter import messagebox
import re
#from PIL import ImageTk, Image
import csv


LARGEFONT =("Verdana", 18)
SMALLFONT =("Verdana", 12)
# Define colors
mainColor = "#56C3A2"
accentColor = "#57729E"

# Define fonts
buttonFont = ("Helvetica", 24)
inputFont = ("Verdana", 20)
usernameFont = ("Verdana", 16)
reciepts = {}

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		for F in (StartPage, Page1, Page2, Page3, Page4):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
	category = {}
	def category(self):
		def displayData():
			with open('CategoryData/categoryDataList.csv', 'r') as file:
				category = csv.reader(file)
				rows = []
				j = 0
				i = 0
				title = ["Category", "Extra", "Amount"]
				for j in range(1):
					cols = []	
					k = 0
					for item1 in title:
						e = Entry(categoryViewer)
						e.grid(row = 4, column = k, sticky = NSEW)
						e.insert(END, '%s' % (item1))
						cols.append(e)
						k += 1
					rows.append(cols)
					k = 0

				for line in category:
					cols = []	
					for item in line:
						e = Entry(categoryViewer)
						e.grid(row = j + 5, column = i, sticky = NSEW)
						e.insert(END, '%s' % (item))
						cols.append(e)
						i += 1
					rows.append(cols)
					j += 1
					i = 0
				j = 0

		# This is where users can scroll through past receipts
		def addCategory():
			categoryEntry1 = categoryInput1.get()
			categoryEntry2 = categoryInput2.get()
			amountEntry = amountInput.get()
			if amountEntry != "":
				if digit_check(amountEntry):
					with open('CategoryData/categoryDataList.csv', 'a', newline='') as f:
						writer = csv.writer(f)
						writer.writerow([categoryEntry1, categoryEntry2, amountEntry])
						messagebox.showinfo("Excellent", "Successfully added")
						categoryInput1.delete(0, END)
						categoryInput2.delete(0, END)
						amountInput.delete(0, END)
				else:
					messagebox.showwarning("Error", "Amount only needs number")
			else:
					messagebox.showwarning("Error", "Amount field reqired")
		def digit_check(value):
			if re.search('[0-9]', value): #atleast one digit
				return True
			return False

		categoryViewer = tk.Tk()
		categoryViewer.title("Category")
		categoryViewer.geometry('500x400')
		categoryViewer['background']='yellow'
		# Create input box for Category and Amount
		categoryInput1 = ttk.Combobox(categoryViewer, 
									values=[
											"Housing", 
											"Insurance",
											"Utilities",
											"Transportation",
											"Debt",
											"Groceries",
											"Subscriptions",
											"Entertainment",
											"Recreation/Leisure",
											"Investing",
											"misc"])
		categoryInput1.grid(column=0, row=0)
		categoryInput1.current(0)

		categoryInput2 = ttk.Combobox(categoryViewer, 
									values=[
											"",
											"saving", 
											"wants",
											"needs"])
		categoryInput2.grid(column=1, row=0)
		categoryInput2.current(0)

		amountInput = Entry(categoryViewer, width = 5)
		amountInput.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = 'ew')
		
		addButton = ttk.Button(categoryViewer, text ="add", command = addCategory)
		addButton.grid(row = 3, column = 0, padx = 10, pady = 10)

		refreshButton = ttk.Button(categoryViewer, text ="refresh", command = displayData)
		refreshButton.grid(row = 3, column = 2, padx = 10, pady = 10)
		
		function_name = "displayData"
		eval(function_name + "()")


	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		# label of frame Layout 2
		label = ttk.Label(self, text ="Startpage", font = LARGEFONT)
		
		# putting the grid in its place by using
		# grid
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		button1 = ttk.Button(self, text ="Receipt Vault",
		command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		## button to show frame 2 with text layout2
		button2 = ttk.Button(self, text ="Spedning Graph",
		command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		button3 = ttk.Button(self, text = "category",
		command= lambda : self.category())

		# putting the button in its place by
		# using grid
		button3.grid(row = 3, column = 1, padx = 10, pady = 10)

		button4 = ttk.Button(self, text = "Support",
		command = lambda : controller.show_frame(Page4))

		# putting the button in its place by
		# using grid
		button4.grid(row = 4, column = 1, padx = 10, pady = 10)

		


# second window frame page1
class Page1(tk.Frame):

	def recieptBook(self):
		# This is where users can scroll through past receipts
		recieptViewer = tk.Toplevel(app)
		recieptViewer.title("Wallet")
		recieptViewer.geometry('400x300')

		recieptsList = Listbox(recieptViewer)
		recieptsList.pack(side = LEFT, fill = BOTH, expand=True)
		scroll = Scrollbar(recieptViewer)
		scroll.pack(side= RIGHT, fill=BOTH)
		recieptsList.config(yscrollcommand=scroll.set)
		scroll.config(command=recieptsList.yview)

		for i in reciepts:
			recieptsList.insert(END, i)

		recieptsList.bind('<<ListboxSelect>>', self.CurSelect)

	# helper function for upload
	def open_file(self):
		file_path = askopenfile(mode='r', filetypes=[('Image Files', '*jpg')])
		if file_path is not None:
			exp = simpledialog.askinteger(title="Expense Report", prompt="Total Expense for Receipt")
			reciepts[file_path.name] = exp
			pass
	
	def CurSelect(self, event):

		widget = event.widget
		selection= widget.curselection()
		picked = widget.get(selection[0])
		loaded = Image.open(picked)
		loaded = loaded.resize((400,400))
		render = ImageTk.PhotoImage(loaded)
		
		imageShow = tk.Toplevel(app)
		imageShow.title(reciepts[picked])
		imageShow.geometry('400x400')
		img = ttk.Label(imageShow, image=render)
		img.image = render
		img.place(x=0,y=0)
		print(picked)

	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Receipt Vault", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="StartPage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(self, text ="Spending Graph",
							command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)


		#This is the button for inputting receipt
		image_input = ttk.Button(self, text="Input Receipt", command= lambda : self.open_file())
		image_input.grid(row = 1, column=5)

		#This is the button for viewing receipt
		image_input = ttk.Button(self, text="Show Wallet", command= lambda : self.recieptBook())
		image_input.grid(row = 2, column=5)




# third window frame page2
class Page2(tk.Frame):

	# refresh the frame
	def refresh(self, parent, controller):
		plot.tight_layout()
		# This is where the plot is generated
		fig = Figure(figsize=(4,3), dpi=80)
		x = []
		for i in range(1,len(reciepts)+1):
			x.append(i)
		plt= fig.add_subplot(111)
		plt.plot(x, reciepts.values())
		plt.autoscale()
		plt.set_xticks(x)
		plt.set_xlabel("Receipt Number")
		plt.set_ylabel("Amount ($)")
		
		canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
		canvas.draw()
		canvas.get_tk_widget().grid(row=2, column= 4, ipadx = 60, ipady = 60,)

		toolbar = tk.Frame(self)
		toolbar.update()
		canvas.get_tk_widget().grid(row=2, column= 4, ipadx = 60, ipady = 60)

	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Spending Graph", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Receipt Vault",
							command = lambda : controller.show_frame(Page1))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 3 with text
		# layout3
		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

		print("rendering ploit page")

		# button to REFRESH
		refresh_button = ttk.Button(self, text ="Refresh",
							command = lambda : self.refresh(parent, controller))
	
		# putting the button in its place by
		# using grid
		refresh_button.grid(row = 1, column = 4, padx = 10, pady = 10)

class Page3(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Receipt Vault", font = LARGEFONT)
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="StartPage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button2 = ttk.Button(self, text ="Spending Graph",
							command = lambda : controller.show_frame(Page2))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)

class Page4(tk.Frame):

	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Support", font = LARGEFONT)
		label.grid(row = 0, column = 0, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="StartPage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place
		# by using grid
		button1.grid(row = 1, column = 0, padx = 10, pady = 10)
		
		input = ttk.Label(self, text = "How to create account and sign in", font = LARGEFONT)
		input.grid(row = 2, column = 0, padx = 8, pady = 8)

		input1 = ttk.Label(self, text = "1.Click the 'make new account' button on Login Page\nYou can write your account information\nPassword Must be in \n 1). Minimum 8 characters.\n 2). The alphabets must be between [a-z].\n 3). At least one alphabet should be of Upper Case [A-Z].\n 4). At least 1 number or digit between [0-9].\n 5). At least 1 special character\n2. You can write your username and password and click 'submit' button ", font = SMALLFONT)
		input1.grid(row = 3, column = 0, padx = 8, pady = 8)

		input2 = ttk.Label(self, text = "How to add receipt and show Spending Graph", font = LARGEFONT)
		input2.grid(row = 4, column = 0, padx = 8, pady = 8)

		input3 = ttk.Label(self, text = "1.Open the Receiptgraph page how to click Receipt Vault on StartPage\n 1).Click the 'Input Receipt' button\n  - Select Image(Only JPG) and Open\n  - Write Total Expense and OK Click\n 2).Click 'Show Wallet' and you can see the list of receipt and \n see each receipt to click each item\n2.Click 'Spending graph' and then Click 'Refresh' button", font = SMALLFONT)
		input3.grid(row = 5, column = 0, padx = 8, pady = 8)

		input4 = ttk.Label(self, text = "How to add and show category", font = LARGEFONT)
		input4.grid(row = 6, column = 0, padx = 8, pady = 8)

		input5 = ttk.Label(self, text = "Click 'category' button\n1.You can write the category, extra category and amount and click 'add'\n  ✨The category and amount field is required\n2.You can see list of categories to click 'refresh'", font = SMALLFONT)
		input5.grid(row = 7, column = 0, padx = 8, pady = 8)
	

# Driver Code
app = tkinterApp()
app.geometry('800x700')
app.mainloop()
