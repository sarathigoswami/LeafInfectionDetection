import infectionDetection
from tkinter import *
from tkinter import filedialog
from PIL import Image,ImageTk,ImageFilter,ImageOps
import cv2
isInputPresent = False

root = Tk()
root.title("Leaf Infection Detection")
root.configure(background="#d0e5d3l")

image_cluster = ImageTk.PhotoImage(Image.open("IMG/cluster.png"))
image_add = ImageTk.PhotoImage(Image.open("IMG/add.png"))

# ********** Click function definitions *************

def addImageClicked(event):
    fname = filedialog.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("JPEG files", "*.jpeg")))
    imageInput = ImageTk.PhotoImage(Image.open(fname))
    imageInput2 = Image.open(fname)
    print(imageInput2)
    #image = infectionDetection.imageResizeing(600,400,imageInput)
    #imageShow = infectionDetection.imageResizeing(200,200,imageInput)
    #image_mainImage.configure(image = imageInput)
    #image_mainImage.image = imageInput
    

def clusterSubmitClicked(event):
    print("Infected Cluster")

def resetClicked(event):
    print("Reset all")

def printResultClicked(event):
    print("Print result")

def quitEventClicked(event):
    root.destroy()

def quitClicked():
    root.destroy()

def doNothing():
    print("Ok, I wont..!")

# *********** Main Menu ***********
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label = "File", menu = subMenu)
subMenu.add_command(label="New", command=doNothing)
subMenu.add_command(label="Add image", command=addImageClicked)
subMenu.add_separator()
subMenu.add_command(label="Save", command=doNothing)
subMenu.add_command(label="Quit", command=quitClicked)

editMenu = Menu(menu)
menu.add_cascade(label = "Help", menu = editMenu)
editMenu.add_command(label="Support", command=doNothing)
editMenu.add_command(label="About", command=doNothing)


#************** Creating widgets and filling grid ***************

label_mainImage = Label(root, text = "Main Image")
label_cluster0 = Label(root, text = "Cluster 0")
label_cluster1 = Label(root, text = "Cluster 1")
label_cluster2 = Label(root, text = "Cluster 2")

image_mainImage = Label(root, image=image_add)
image_cluster0 = Label(root, image=image_cluster)
image_cluster1 = Label(root, image=image_cluster)
image_cluster2 = Label(root, image=image_cluster)

button_addImage = Button(root, text="     Add image     ",font=("Calibri", 10), bg="#093a0d", fg="#ffffff", bd=2)
clusterInputFrame = Frame(root, bg="#d0e5d3l")
label_clusterSelect = Label(clusterInputFrame, text="Enter the cluster number fit to be infected region to calculate:  ", bg="#d0e5d3l")
entry_infectedClusterNo = Entry(clusterInputFrame)
button_selectCluster = Button(clusterInputFrame, text="   Calculate   ",font=("Calibri", 12), bg="#0060af", fg="#ffffff", bd=2)
label_clusterSelect.pack(side=LEFT)
entry_infectedClusterNo.pack(side=LEFT, padx=5)
button_selectCluster.pack(side=LEFT, padx=5)

image_binary0 = Label(root, image=image_cluster)
image_binary1 = Label(root, image=image_cluster)
label_binary0 = Label(root, text = "Binary of original main image")
label_binary1 = Label(root, text = "Binary of infected region")

displayFrame = Frame(root, bg="#d0e5d3l")
displayPercentage = Label(displayFrame, text="21.35%", font=("Calibri", 36), pady=30, bg="#d0e5d3l", fg="#ff7700" )
lable_output = Label(displayFrame, text = "Percentage of infection (approx.)", font=("Calibri", 12), pady=40, bg="#d0e5d3l")
displayPercentage.pack()
lable_output.pack()

butttonFrame = Frame(root, bg="#d0e5d3l")
button_print = Button(butttonFrame, text="Print",font=("Calibri", 14), bg="#093a0d", fg="#ffffff", bd=4)
button_reset = Button(butttonFrame, text="Reset",font=("Calibri", 14), bg="#093a0d", fg="#ffffff", bd=4)
button_quit = Button(butttonFrame, text="Quit",font=("Calibri", 14), bg="#093a0d", fg="#ffffff")
button_print.pack(fill=X, padx=20, pady=10)
button_reset.pack(fill=X, padx=20, pady=10)
button_quit.pack(fill=X, padx=20, pady=10)

label_mainImage.grid(row=0,column=0, padx=30, pady=5, sticky=N+E+S+W)
label_cluster0.grid(row=0,column=1, padx=30, pady=5, sticky=N+E+S+W)
label_cluster1.grid(row=0,column=2, padx=30, pady=5, sticky=N+E+S+W)
label_cluster2.grid(row=0,column=3, padx=30, pady=5, sticky=N+E+S+W)

image_mainImage.grid(row=1,column=0, padx=10, pady=5)
image_cluster0.grid(row=1,column=1, padx=10, pady=5)
image_cluster1.grid(row=1,column=2, padx=10, pady=5)
image_cluster2.grid(row=1,column=3, padx=10, pady=5)

button_addImage.grid(row=2,column=0, sticky=N)
clusterInputFrame.grid(row=2,column=1, columnspan=3, sticky=N, pady=20)

image_binary0.grid(row=3, column=0, padx=10, pady=5)
image_binary1.grid(row=3, column=1, padx=10, pady=5)
displayFrame.grid(row=3, column=2, padx=10, pady=5, sticky=N+E+S+W)
butttonFrame.grid(row=3, column=3, padx=10, rowspan=2, pady=5, sticky=N+E+S+W)
label_binary0.grid(row=4, column=0, padx=30, pady=5, sticky=N+E+S+W)
label_binary1.grid(row=4, column=1, padx=30, pady=5, sticky=N+E+S+W)



root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(3, weight=1)

#************** Managing Button clicks ****************
button_addImage.bind("<Button-1>", addImageClicked)
button_quit.bind("<Button-1>", quitEventClicked)

root.mainloop()