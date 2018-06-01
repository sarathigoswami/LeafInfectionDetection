import cv2
import subprocess
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import portrait


def imageResizeing(image):
    resizedImage = image.resize((600, 400), Image.BILINEAR)
    resizedImage.save("image.jpg")

def imageOutputResize(image):
    resizedImage = image.resize((300, 200), Image.BILINEAR)
    return resizedImage    

def kmeans(segments, image):
    image=cv2.GaussianBlur(image,(7,7),0)
    vectorized = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    vectorized=image.reshape(-1,3)
    vectorized=np.float32(vectorized)
    criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans(vectorized,segments,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    res = center[label.flatten()]
    segmented_image = res.reshape((image.shape))
    return label.reshape((image.shape[0],image.shape[1])),segmented_image.astype(np.uint8),center

def extractComponent(image,label_image,label):
    component=np.zeros(image.shape,np.uint8)
    component[label_image==label]=image[label_image==label]
    return component

def toBinaryInage(img, inf):
    img_inv = cv2.bitwise_not(img)
    ret,img_bin = cv2.threshold(img_inv,30,255,cv2.THRESH_BINARY)
    ret,inf_bin = cv2.threshold(inf,100,255,cv2.THRESH_BINARY)
    cv2.imwrite("imageBinary.jpg", cv2.resize(img_bin, (300,200)))
    cv2.imwrite("infectedBinary.jpg", cv2.resize(inf_bin, (300,200)))
    return img_bin, inf_bin

def percentageCalculation(img, inf):
    imageArea = np.sum(img == 255)
    infectedArea = np.sum(inf == 255)
    return ((infectedArea/imageArea)*100)

def generateReport(percentage):
    c = canvas.Canvas("output.pdf", pagesize=portrait(A4))
    c.setFont("Helvetica-Bold", 18, leading=None)
    c.drawString(40, 800, "Infection Detection Report")
    c.drawString(40, 790, "----------------------------------------------------------------------------")
    c.setFont("Helvetica", 14, leading=None)
    c.drawString(40, 760, "Input image:")
    image = "image.jpg"
    c.drawImage(image, 50, 550, width=300, height=200)
    c.drawString(40, 535, "Infected region:")
    image = "infected.jpg"
    c.drawImage(image, 50, 325, width=300, height=200)
    c.drawString(40, 290, "Calculated percentage of infection:")    
    c.setFillColorRGB(1,0,0)
    c.setFont("Courier-Bold", 40, leading=None)
    c.drawString(60, 230, percentage)
    c.setFont("Helvetica", 10, leading=None)
    c.setFillColorRGB(0,0,1)
    c.drawString(40, 80, "* This calculation is an approximate estimation by the program,") 
    c.drawString(46, 67, "it does not promise 100% accuracy.")
    c.showPage()
    c.save()
    subprocess.Popen(["output.pdf"],shell=True)