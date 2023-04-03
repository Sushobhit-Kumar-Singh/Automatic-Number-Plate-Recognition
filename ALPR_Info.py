from PIL import ImageTk
import PIL.Image
import cv2
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import numpy as np
import pytesseract
import random,time
from IndianNameGenerator import *

## Generate random owner name
name_list = []
for row in range(550):
    name = randomGujarati()
    name_list.append(name)

## Generate Fastag Bank list
banks = ['Airtel bank','Allahabad Bank','Axis Bank Ltd','Bank of Baroda','Canara Bank','Central Bank of India','City Union Bank Ltd','HDFC Bank','ICICI Bank','Kotak Mahindra Bank','PAYTM Bank','State Bank of India','Union Bank of India','Yes Bank Ltd','Bank of Maharashtra']

## State List
states={"AN":"Andaman and Nicobar","AP":"Andhra Pradesh","AR":"Arunachal Pradesh","AS":"Assam","BR":"Bihar",
        "CH":"Chandigarh","DN":"Dadra and Nagar Haveli","DD":"Daman and Diu","DL":"Delhi","GA":"Goa","GJ":"Gujarat",
        "HR":"Haryana","HP":"Himachal Pradesh","JK":"Jammu and Kashmir","KA":"Karnataka","KL":"Kerala","LD":"Lakshadweep",
        "MP":"Madhya Pradesh","MH":"Maharashtra","MN":"Manipur","ML":"Meghalaya","MZ":"Mizoram","NL":"Nagaland","OD":"Odissa",
        "PY":"Pondicherry","PN":"Punjab","RJ":"Rajasthan","SK":"Sikkim","TN":"TamilNadu","TR":"Tripura","UP":"Uttar Pradesh",
        "WB":"West Bengal","CG":"Chhattisgarh","TS":"Telangana","JH":"Jharkhand","UK":"Uttarakhand"}

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

windo = Tk()
windo.configure(background='white')
windo.title("Licence Plate Recognition App")
width  = 1278
height = 720
windo.geometry(f'{width}x{height}')

windo.iconbitmap('./meta/car.ico')
windo.resizable(0,0)

#Size for displaying Image
w = 400;h = 280
size = (w, h)


## Generate random Manifacture date
def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)

def upload_im():
    try:
        global im,resized,cp,path
        imageFrame = tk.Frame(windo)
        imageFrame.place(x=415, y=60)
        path = askopenfilename()
        im = PIL.Image.open(path)
        resized = im.resize(size, PIL.Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        display = tk.Label(imageFrame)
        display.imgtk = tkimage
        display.configure(image=tkimage)
        display.grid()
        dn1 = tk.Label(windo, text='Original\ud83d\ude80 Image ', width=20, height=1, fg="white", bg="deep pink",
                       font=('times', 22, ' bold '))
        dn1.place(x=444, y=20)
        cp = tk.Button(windo, text='Detect Licence Plate',command = prediction, bg="blue", fg="white", width=20,
                       height=1, font=('times', 22, 'italic bold '),activebackground = 'yellow')
        cp.place(x=440, y=370)
    except:
        noti = tk.Label(windo, text = 'Please upload an Image\ud83d\ude80 File', width=29, height=1, fg="white", bg="blue",
                            font=('times', 15, ' bold '))
        noti.place(x=20, y=450)
        windo.after(5000, destroy_widget, noti)

def destroy_widget(widget):
    widget.destroy()

def prediction():
    # try:
        global op,tkimage4,img,plate,op1,read,plate
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        nplate = cascade.detectMultiScale(gray, 1.1, 7)

        for (x, y, w, h) in nplate:
            a, b = (int(0.02 * img.shape[0]), int(0.025 * img.shape[1]))
            plate = img[y + a:y + h - a, x + b:x + w - b, :]
            #plate = img[y:y + h, x:x + w]
            kernel = np.ones((1, 1), np.uint8)
            plate = cv2.dilate(plate, kernel, iterations=1)
            plate = cv2.erode(plate, kernel, iterations=1)
            plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
            (thresh, plate) = cv2.threshold(plate_gray, 127, 255, cv2.THRESH_BINARY)
            read = pytesseract.image_to_string(plate)
            read = ''.join(e for e in read if e.isalnum())
            cv2.rectangle(img, (x, y), (x + w, y + h), (51, 51, 255), 2)
            cv2.rectangle(img, (x, y - 40), (x + w, y), (51, 51, 255), -1)
            cv2.putText(img, read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        op = PIL.Image.fromarray(img)
        resi = op.resize(size, PIL.Image.ANTIALIAS)
        tkimage4 = ImageTk.PhotoImage(resi)
        imageFrame4 = tk.Frame(windo)
        imageFrame4.place(x=845, y=60)

        dn4 = tk.Label(windo, text='Licence Plate Recognition', width=20, height=1, fg="white", bg="navy",
                           font=('times', 22, ' bold '))
        dn4.place(x=874, y=20)
        display4 = tk.Label(imageFrame4)
        display4.imgtk = tkimage4
        display4.configure(image=tkimage4)
        display4.grid()
        if read != '':
            ## Plate processing
            plate1 = cv2.cvtColor(plate, cv2.COLOR_GRAY2RGB)
            op1 = PIL.Image.fromarray(plate1)
            resi1 = op1.resize((150, 40), PIL.Image.ANTIALIAS)
            tkimage2 = ImageTk.PhotoImage(resi1)

            info_frame = tk.Canvas(windo, width=394, height=255, bg='blue')
            info_frame.place(x=845, y=380)

            veh_info = tk.Label(windo, text="Plate: "+read, width=18, height=1, fg='white', bg='black',
                                font=('times', 18, ' bold '))
            veh_info.place(x=918, y=385)

            stat = read[0:2]
            try:
                lp_info = tk.Label(windo, text="State: " + states[stat], width=25, height=1, fg='white', bg='blue',
                                   font=('times', 18, ' bold '))
                lp_info.place(x=858, y=425)
            except:
                lp_info = tk.Label(windo, text="State not recognised!", width=25, height=1, fg='white', bg='blue',
                                   font=('times', 18, ' bold '))
                lp_info.place(x=858, y=425)

            ow_name = random.choice(name_list)
            ow_info = tk.Label(windo, text="Owner: " + ow_name, width=25, height=1, fg='white', bg='blue',
                               font=('times', 17, ' bold '))
            ow_info.place(x=858, y=465)

            fastag_bank = random.choice(banks)
            car_info = tk.Label(windo, text="Fastag: "+fastag_bank, width=25, height=1, fg='white', bg='blue',
                                font=('times', 17, ' bold '))
            car_info.place(x=858, y=505)

            veh_date = random_date("1/1/2002 1:30 PM", "1/1/2020 4:50 AM", random.random()).split(' ')
            veh_date_info = tk.Label(windo, text="Date: " + str(veh_date[0]), width=25, height=1, fg='white', bg='blue',
                                     font=('times', 17, ' bold '))
            veh_date_info.place(x=858, y=545)

            imageFrame2 = tk.Frame(windo)
            imageFrame2.place(x=973, y=585)
            display2 = tk.Label(imageFrame2)
            display2.imgtk = tkimage2
            display2.configure(image=tkimage2)
            display2.grid()

            ri = PIL.Image.open('./meta/t2.png')
            ri = ri.resize((50, 50), PIL.Image.ANTIALIAS)
            sad_img = ImageTk.PhotoImage(ri)
            panel4 = Button(windo, borderwidth=0, command=save_img, bg='blue', image=sad_img)
            panel4.image = sad_img
            panel4.pack()
            panel4.place(x=1173, y=580)
        else:
            pass

    # except Exception as e:
    #     notip = tk.Label(windo, text = 'Licence Plate not found in Image\ud83d\ude80!!', width=29, height=1, fg="white", bg="midnightblue",
    #                         font=('times', 15, ' bold '))
    #     notip.place(x=20, y=450)
    #     windo.after(7000, destroy_widget, notip)
    #     print(e)

def save_img():
    name = "LPR_"+os.path.basename(path)
    name1 = read +'.jpg'
    op.save('./results/'+ name)
    op1.save('./results/'+name1)
    not3 = tk.Label(windo, text= name+' Saved', width=29, height=1, fg="white",
                     bg="midnightblue",
                     font=('times', 15, ' bold '))
    not3.place(x=20, y=450)

    not4 = tk.Label(windo, text= name1+' Saved', width=29, height=1, fg="black",
                     bg="gold",
                     font=('times', 15, ' bold '))
    not4.place(x=20, y=490)
    windo.after(5000, destroy_widget, not3)
    windo.after(5000, destroy_widget, not4)


dn = tk.Label(windo, text='Licence Plate Recognition', width=20, height=1, fg="white", bg="blue2",
              font=('times', 22, ' bold '))
dn.place(x=24, y=20)

ri = PIL.Image.open('./meta/np.jpg')
ri =ri.resize((349,303), PIL.Image.ANTIALIAS)
sad_img = ImageTk.PhotoImage(ri)
panel4 = Label(windo, image=sad_img,bg = 'white')
panel4.pack()
panel4.place(x=20, y=60)

up = tk.Button(windo,text = 'Upload\ud83d\ude80 Image',bg="medium spring green", fg="black", width=20,
                   height=1, font=('times', 22, 'italic bold '),command = upload_im, activebackground = 'yellow')
up.place(x=20, y=370)

windo.mainloop()