import infectionDetection
from tkinter import *
from tkinter import filedialog, StringVar
from PIL import Image,ImageTk,ImageFilter,ImageOps
import cv2
import numpy as np
import test

root = Tk()
root.title("Leaf Infection Detection")
root.configure(background="#d0e5d3l")

isInputPresent = 0
segments = 3
percentageInfection = StringVar()
percentageInfection.set("Give Image")

image_cluster = ImageTk.PhotoImage(Image.open("IMG/cluster.png"))
image_add = ImageTk.PhotoImage(Image.open("IMG/add.png"))

# ********************* Clicks and function definitions **********************

def addImageClicked():
    fname = filedialog.askopenfilename(filetypes=(("JPEG files", "*.jpg"), ("JPEG files", "*.jpeg")))
    imageInput = Image.open(fname)
    imageShow = ImageTk.PhotoImage(infectionDetection.imageOutputResize(imageInput))
    image_mainImage.configure(image = imageShow)
    image_mainImage.image = imageShow
    infectionDetection.imageResizeing(imageInput)
    image = cv2.imread("image.jpg")
    global isInputPresent
    isInputPresent = True
    imageSegment(image)

def imageSegment(image):
    global segments, percentageInfection
    label,result,center=infectionDetection.kmeans(segments, image)
    
    for i in list(range(segments)) :
        extracted_cluster = infectionDetection.extractComponent(image,label,i)
        name = "extracted" + str(i)
        cv2.imwrite(name+".jpg",extracted_cluster)
        extractedShow = cv2.resize(extracted_cluster, (300,200))
        nameShow = "extractedShow" + str(i) + ".jpg"
        cv2.imwrite(nameShow,extractedShow)
        
    imageShow = ImageTk.PhotoImage(Image.open("extractedShow0.jpg"))
    image_cluster0.configure(image = imageShow)
    image_cluster0.image = imageShow
    imageShow = ImageTk.PhotoImage(Image.open("extractedShow1.jpg"))
    image_cluster1.configure(image = imageShow)
    image_cluster1.image = imageShow
    imageShow = ImageTk.PhotoImage(Image.open("extractedShow2.jpg"))
    image_cluster2.configure(image = imageShow)
    image_cluster2.image = imageShow
    percentageInfection.set("Processing...")
        
def clusterSubmitClicked():
    image = cv2.imread("image.jpg", 0)
    inputClusterNumber = entry_infectedClusterNo.get()
    infectedName = "extracted" + inputClusterNumber + ".jpg"
    infected = cv2.imread(infectedName)
    cv2.imwrite("infected.jpg", infected)
    infected = cv2.imread("infected.jpg", 0)
    binImage, binInfected = infectionDetection.toBinaryInage(image, infected)
    imageShow = ImageTk.PhotoImage(Image.open("imageBinary.jpg"))
    image_binary0.configure(image = imageShow)
    image_binary0.image = imageShow
    imageShow = ImageTk.PhotoImage(Image.open("infectedBinary.jpg")) 
    image_binary1.configure(image = imageShow)
    image_binary1.image = imageShow
    percentageOutput(binImage, binInfected)
    
def percentageOutput(image, infected):
    percentage = infectionDetection.percentageCalculation(image, infected)
    percentage = format(percentage, '.2f')
    percentageString = str(percentage) + " %"
    global percentageInfection
    percentageInfection.set(percentageString)
    

def resetClicked():
    image_mainImage.configure(image = image_add)
    image_mainImage.image = image_add
    image_cluster0.configure(image = image_cluster)
    image_cluster0.image = image_cluster
    image_cluster1.configure(image = image_cluster)
    image_cluster1.image = image_cluster   
    image_cluster2.configure(image = image_cluster)
    image_cluster2.image = image_cluster
    image_binary0.configure(image = image_cluster)
    image_binary0.image = image_cluster
    image_binary1.configure(image = image_cluster)
    image_binary1.image = image_cluster
    percentageInfection.set("Give image")

def printResultClicked():
    per = percentageInfection.get()
    infectionDetection.generateReport(per)

def quitClicked():
    root.destroy()
    
def helpClicked():
    pass

def aboutClicked():
    pass


# ******************************* Main Menu **********************************
menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label = "File", menu=subMenu)
subMenu.add_command(label="New", command=resetClicked)
subMenu.add_command(label="Add image", command=addImageClicked)
subMenu.add_separator()
subMenu.add_command(label="Print", command=printResultClicked)
subMenu.add_command(label="Quit", command=quitClicked)

editMenu = Menu(menu)
menu.add_cascade(label = "Help", menu=editMenu)
editMenu.add_command(label="Support", command=helpClicked)
editMenu.add_command(label="About", command=aboutClicked)


#********************** Creating widgets and filling grid ********************

label_mainImage = Label(root, text = "Main Image")
label_cluster0 = Label(root, text = "Cluster 0")
label_cluster1 = Label(root, text = "Cluster 1")
label_cluster2 = Label(root, text = "Cluster 2")

image_mainImage = Label(root, image=image_add)
image_cluster0 = Label(root, image=image_cluster)
image_cluster1 = Label(root, image=image_cluster)
image_cluster2 = Label(root, image=image_cluster)

button_addImage = Button(root, text="     Add image     ",font=("Calibri", 10), bg="#0060af", fg="#ffffff", bd=2, command=addImageClicked)
clusterInputFrame = Frame(root, bg="#d0e5d3l")
label_clusterSelect = Label(clusterInputFrame, text="Enter the cluster number fit to be infected region to calculate:  ", bg="#d0e5d3l")
entry_infectedClusterNo = Entry(clusterInputFrame)
button_selectCluster = Button(clusterInputFrame, text="   Calculate   ",font=("Calibri", 12), bg="#0060af", fg="#ffffff", bd=2, command=clusterSubmitClicked)
label_clusterSelect.pack(side=LEFT)
entry_infectedClusterNo.pack(side=LEFT, padx=5)
button_selectCluster.pack(side=LEFT, padx=5)

image_binary0 = Label(root, image=image_cluster)
image_binary1 = Label(root, image=image_cluster)
label_binary0 = Label(root, text = "Binary of original main image")
label_binary1 = Label(root, text = "Binary of infected region")

displayFrame = Frame(root, bg="#d0e5d3l")
displayPercentage = Label(displayFrame, textvariable=percentageInfection, font=("Calibri", 36), pady=30, bg="#d0e5d3l", fg="#ff7700" )
lable_output = Label(displayFrame, text = "Percentage of infection (approx.)", font=("Calibri", 12), pady=40, bg="#d0e5d3l")
displayPercentage.pack()
lable_output.pack()

butttonFrame = Frame(root, bg="#d0e5d3l")
button_print = Button(butttonFrame, text="Print",font=("Calibri", 14), bg="#093a0d", fg="#ffffff", bd=4, command=printResultClicked)
button_reset = Button(butttonFrame, text="Reset",font=("Calibri", 14), bg="#093a0d", fg="#ffffff", bd=4, command=resetClicked)
button_quit = Button(butttonFrame, text="Quit",font=("Calibri", 14), bg="#093a0d", fg="#ffffff", command=quitClicked)
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

root.mainloop()