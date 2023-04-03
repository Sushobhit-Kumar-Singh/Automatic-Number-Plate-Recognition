from PIL import ImageTk
import PIL.Image
import cv2
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import numpy as np
import pytesseract
import pymysql
import time
from pathlib import Path
import datetime
from tkinter import ttk
import base64,csv
from IndianNameGenerator import *
import random
from tkinter import messagebox

## Generate random owner name
name_list = []
for row in range(550):
    name = randomGujarati()
    name_list.append(name)

## Generate random Manifacture date
def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', prop)

## Generate car name
car_name = ['Suzuki Swift','Swift Dzire','Ertiga','Baleno','Ciaz','Hyundai Creta','Hyundai Santro','Hyundai i10','Hyundai i20','Hyundai Verna'
            ,'Hyundai Tuscon','Hyundai Grand i10','Toyota Etios','Toyota Corolla Altis','Toyota Innova','Toyota Fortuner','Ford Figo','Ford Endeavour'
            ,'Skoda Kodiaq','Skoda Superb','Skoda Octavia','Polo']
###Connect to the database
connection = pymysql.connect(host='localhost',user='root',password='',db='lpr')
cursor = connection.cursor()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

#Size for displaying Image
w = 396;h = 280
size = (w, h)

## Main frame
windo = Tk()
windo.configure(background='white')
windo.title("ALPR: Automatic License Plate Recognition Application")
# width = windo.winfo_screenwidth()
# height = windo.winfo_screenheight()
# windo.geometry(f'{width}x{height}')
width = 1278
height = 720
windo.geometry('1278x720')

windo.iconbitmap('./meta/car.ico')
windo.resizable(0, 0)

ri = PIL.Image.open('./meta/main_screen1.jpg')
ri = ri.resize((1265, 648), PIL.Image.ANTIALIAS)
sad_img = ImageTk.PhotoImage(ri)
panel4 = Label(windo, image=sad_img, bg='white')
panel4.pack()
panel4.place(x=0, y=0)

id_l = tk.Label(windo, text="Enter ID", width=13, height=1, fg="black", bg="#24c4a2", font=('times', 14, ' bold '))
id_l.place(x=30, y=408)

def upload_im():
    try:
        clear_screen()
        global im,resized,cp,path,plate,read,op,op1,dn1,imageFrame,imageFrame1,display,display1,dn4,imageFrame2,display2,panel4,info_frame,lp_info,ow_info,veh_info,car_info,veh_date_info,car_n
        DB_table_name = 'user_records'
        sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                        (user_id varchar(20) NOT NULL,
                         img_name varchar(100) NOT NULL,
                         veh_name VARCHAR(50) NOT NULL,
                         veh_lpr VARCHAR(50) NOT NULL,
                         owner_name VARCHAR(50) NOT NULL,
                         veh_rgr_date VARCHAR(50) NOT NULL,
                         img_date VARCHAR(20) NOT NULL,
                         img_time VARCHAR(20) NOT NULL);
                        """

        cursor.execute(sql)

        imageFrame = tk.Frame(windo)
        imageFrame.place(x=385, y=90)
        path = askopenfilename()
        img_name = path.split('/')
        img_name = img_name[-1]
        im = PIL.Image.open(path)
        resized = im.resize(size, PIL.Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        display = tk.Label(imageFrame)
        display.imgtk = tkimage
        display.configure(image=tkimage)
        display.grid()
        dn1 = tk.Label(windo, text='Original Image: '+img_name, width=23, height=1, fg="white", bg="blue",
                       font=('times', 22, ' bold '))
        dn1.place(x=385, y=52)

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
            # read1 = read[0:2]+'_'+read[2:-4]+'_'+read[-4:]
            cv2.rectangle(img, (x, y), (x + w, y + h), (51, 51, 255), 2)
            cv2.rectangle(img, (x, y - 40), (x + w, y), (51, 51, 255), -1)
            cv2.putText(img, read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        op = PIL.Image.fromarray(img)
        resi = op.resize(size, PIL.Image.ANTIALIAS)
        tkimage1 = ImageTk.PhotoImage(resi)
        imageFrame1 = tk.Frame(windo)
        imageFrame1.place(x=825, y=90)
        dn4 = tk.Label(windo, text='Licence Plate Recognition', width=23, height=1, fg="white", bg="blue",
                           font=('times', 22, ' bold '))
        dn4.place(x=825, y=52)
        display1 = tk.Label(imageFrame1)
        display1.imgtk = tkimage1
        display1.configure(image=tkimage1)
        display1.grid()

        ## Plate processing
        plate1 = cv2.cvtColor(plate, cv2.COLOR_GRAY2RGB)
        op1 = PIL.Image.fromarray(plate1)
        resi1 = op1.resize((150,40), PIL.Image.ANTIALIAS)
        tkimage2 = ImageTk.PhotoImage(resi1)

        info_frame = tk.Canvas(windo, width=394, height=255, bg='blue')
        info_frame.place(x=827, y=380)

        veh_info = tk.Label(windo, text="Vehicle Information", width=18, height=1, fg='white', bg='black',
                            font=('times', 18, ' bold '))
        veh_info.place(x=900, y=385)

        lp_info = tk.Label(windo, text="License Plate: "+read, width=25, height=1, fg='white', bg='blue',
                           font=('times', 18, ' bold '))
        lp_info.place(x=840, y=425)

        ow_name = random.choice(name_list)
        ow_info = tk.Label(windo, text="Owner: "+ow_name, width=25, height=1, fg='white', bg='blue',
                           font=('times', 17, ' bold '))
        ow_info.place(x=840, y=465)

        car_n = random.choice(car_name)
        car_info = tk.Label(windo, text="Vehicle: "+car_n, width=25, height=1, fg='white', bg='blue',
                            font=('times', 17, ' bold '))
        car_info.place(x=840, y=505)

        veh_date = random_date("1/1/2002 1:30 PM", "1/1/2018 4:50 AM", random.random()).split(' ')
        veh_date_info = tk.Label(windo, text="Date: "+str(veh_date[0]), width=25, height=1, fg='white', bg='blue',
                                 font=('times', 17, ' bold '))
        veh_date_info.place(x=840, y=545)

        imageFrame2 = tk.Frame(windo)
        imageFrame2.place(x=940, y=585)
        display2 = tk.Label(imageFrame2)
        display2.imgtk = tkimage2
        display2.configure(image=tkimage2)
        display2.grid()

        ri = PIL.Image.open('./meta/t2.png')
        ri = ri.resize((50, 50), PIL.Image.ANTIALIAS)
        sad_img = ImageTk.PhotoImage(ri)
        panel4 = Button(windo, borderwidth=0,command = save_img,bg = 'blue', image=sad_img)
        panel4.image = sad_img
        panel4.pack()
        panel4.place(x=1155, y=580)

        ts = time.time()
        img_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        img_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        ## Insert into Table
        insert_sql = "insert into " + DB_table_name + """
        values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        rec_values = (account[0],img_name,car_n,read,ow_name,str(veh_date[0]),img_date,img_time)
        cursor.execute(insert_sql,rec_values)
        connection.commit()

    except Exception as e:
        print(e)
        noti = tk.Label(windo, text = 'Please upload an Image File', width=24, height=1, fg="white", bg="blue",
                            font=('times', 16, ' bold '))
        noti.place(x=10, y=200)
        windo.after(3000, destroy_widget, noti)

def ad_upload_im():
    try:
        clear_screen()
        global im,resized,cp,path,plate,read,op,op1,dn1,imageFrame,imageFrame1,display,display1,dn4,imageFrame2,display2,panel4,info_frame,lp_info,ow_info,veh_info,car_info,veh_date_info
        DB_table_name = 'user_records'
        sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                        (user_id varchar(20) NOT NULL,
                         img_name varchar(100) NOT NULL,
                         veh_name VARCHAR(50) NOT NULL,
                         veh_lpr VARCHAR(50) NOT NULL,
                         owner_name VARCHAR(50) NOT NULL,
                         veh_rgr_date VARCHAR(50) NOT NULL,
                         img_date VARCHAR(20) NOT NULL,
                         img_time VARCHAR(20) NOT NULL);
                        """

        cursor.execute(sql)

        imageFrame = tk.Frame(windo)
        imageFrame.place(x=385, y=90)
        path = askopenfilename()
        img_name = path.split('/')
        img_name = img_name[-1]
        im = PIL.Image.open(path)
        resized = im.resize(size, PIL.Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        display = tk.Label(imageFrame)
        display.imgtk = tkimage
        display.configure(image=tkimage)
        display.grid()
        dn1 = tk.Label(windo, text='Original Image: '+img_name, width=23, height=1, fg="white", bg="blue",
                       font=('times', 22, ' bold '))
        dn1.place(x=385, y=52)

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
            # read1 = read[0:2]+'_'+read[2:-4]+'_'+read[-4:]
            cv2.rectangle(img, (x, y), (x + w, y + h), (51, 51, 255), 2)
            cv2.rectangle(img, (x, y - 40), (x + w, y), (51, 51, 255), -1)
            cv2.putText(img, read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        op = PIL.Image.fromarray(img)
        resi = op.resize(size, PIL.Image.ANTIALIAS)
        tkimage1 = ImageTk.PhotoImage(resi)
        imageFrame1 = tk.Frame(windo)
        imageFrame1.place(x=825, y=90)
        dn4 = tk.Label(windo, text='Licence Plate Recognition', width=23, height=1, fg="white", bg="blue",
                           font=('times', 22, ' bold '))
        dn4.place(x=825, y=52)
        display1 = tk.Label(imageFrame1)
        display1.imgtk = tkimage1
        display1.configure(image=tkimage1)
        display1.grid()

        ## Plate processing
        plate1 = cv2.cvtColor(plate, cv2.COLOR_GRAY2RGB)
        op1 = PIL.Image.fromarray(plate1)
        resi1 = op1.resize((150,40), PIL.Image.ANTIALIAS)
        tkimage2 = ImageTk.PhotoImage(resi1)

        info_frame = tk.Canvas(windo, width=394, height=255, bg='blue')
        info_frame.place(x=827, y=380)

        veh_info = tk.Label(windo, text="Vehicle Information", width=18, height=1, fg='white', bg='black',
                            font=('times', 18, ' bold '))
        veh_info.place(x=900, y=385)

        lp_info = tk.Label(windo, text="License Plate: "+read, width=25, height=1, fg='white', bg='blue',
                           font=('times', 18, ' bold '))
        lp_info.place(x=840, y=425)

        ow_name = random.choice(name_list)
        ow_info = tk.Label(windo, text="Owner: "+ow_name, width=25, height=1, fg='white', bg='blue',
                           font=('times', 17, ' bold '))
        ow_info.place(x=840, y=465)

        car_info = tk.Label(windo, text="Vehicle: Hyundai Creta", width=25, height=1, fg='white', bg='blue',
                            font=('times', 17, ' bold '))
        car_info.place(x=840, y=505)

        veh_date = rdate = random_date("1/1/2002 1:30 PM", "1/1/2018 4:50 AM", random.random()).split(' ')
        veh_date_info = tk.Label(windo, text="Date: "+str(veh_date[0]), width=25, height=1, fg='white', bg='blue',
                                 font=('times', 17, ' bold '))
        veh_date_info.place(x=840, y=545)

        imageFrame2 = tk.Frame(windo)
        imageFrame2.place(x=940, y=585)
        display2 = tk.Label(imageFrame2)
        display2.imgtk = tkimage2
        display2.configure(image=tkimage2)
        display2.grid()

        ri = PIL.Image.open('./meta/t2.png')
        ri = ri.resize((50, 50), PIL.Image.ANTIALIAS)
        sad_img = ImageTk.PhotoImage(ri)
        panel4 = Button(windo, borderwidth=0,command = save_img,bg = 'blue', image=sad_img)
        panel4.image = sad_img
        panel4.pack()
        panel4.place(x=1155, y=580)

        ts = time.time()
        img_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        img_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        ## Insert into Table
        insert_sql = "insert into " + DB_table_name + """
        values (%s,%s,%s,%s,%s,%s,%s,%s)"""
        rec_values = (account[0],img_name,'Vehicle Name',read,ow_name,str(veh_date[0]),img_date,img_time)
        cursor.execute(insert_sql,rec_values)
        connection.commit()

    except Exception as e:
        print(e)
        noti = tk.Label(windo, text = 'Please upload an Image File', width=24, height=1, fg="white", bg="blue",
                            font=('times', 16, ' bold '))
        noti.place(x=10, y=315)
        windo.after(3000, destroy_widget, noti)

def check_report():
    # upload_im_b['state'] = 'disabled'
    # check_report_b['state'] = 'disabled'
    global tree,us_rep,panel5,panel6

    clear_screen()
    ri = PIL.Image.open('./meta/close.png')
    ri = ri.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img = ImageTk.PhotoImage(ri)
    panel5 = Button(windo, borderwidth=0,command = clear_report, bg='white', image=sad_img)
    panel5.image = sad_img
    panel5.pack()
    panel5.place(x=1167, y=70)

    ri1 = PIL.Image.open('./meta/dw.png')
    ri1 = ri1.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img1 = ImageTk.PhotoImage(ri1)
    panel6 = Button(windo, borderwidth=0,command = gen_csv, bg='white', image=sad_img1)
    panel6.image = sad_img1
    panel6.pack()
    panel6.place(x=1127, y=70)

    us_rep = tk.Label(windo, text=account[1]+"'s Report", width=20, height=1, fg='white', bg="#171d35",
                   font=('times', 22, ' bold '))
    us_rep.place(x=624, y=70)

    ## Add some style
    style = ttk.Style()
    style.configure("Treeview",background = '#171d35',foreground = 'white',font=('times', 10, 'bold '))
    # style.configure("Treeview.Heading",bg = 'blue', foreground='black')
    tree = ttk.Treeview(windo, column=("User ID", "Image Name", "Vehicle", 'License Plate', '', 'c6', 'c7', 'c8'), show='headings')

    tree.column("#1",  stretch=NO, minwidth=100,width=100)
    tree.heading("#1", text="User ID")

    tree.column("#2", stretch=NO, minwidth=100,width=100)
    tree.heading("#2", text="Image Name")

    tree.column("#3",stretch=NO, minwidth=100,width=100)
    tree.heading("#3", text="Vehicle")

    tree.column("#4",stretch=NO, minwidth=100,width=100)
    tree.heading("#4", text="License Plate")

    tree.column("#5", stretch=NO, minwidth=100,width=100)
    tree.heading("#5", text="Owner Name")

    tree.column("#6",stretch=NO, minwidth=100, width=100)
    tree.heading("#6", text="Vehicle Registration")

    tree.column("#7",stretch=NO, minwidth=100, width=100)
    tree.heading("#7", text="Upload Date")

    tree.column("#8",stretch=NO, minwidth=100, width=100)
    tree.heading("#8", text="Upload Time")

    tree.place(x=405,y=110)
    cursor.execute("SELECT * FROM user_records where user_id="+"'"+account[0]+"'")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def admin_own_report():
    # upload_im_b['state'] = 'disabled'
    # check_report_b['state'] = 'disabled'
    global tree,us_rep,panel5,panel6

    clear_screen()
    ri = PIL.Image.open('./meta/close.png')
    ri = ri.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img = ImageTk.PhotoImage(ri)
    panel5 = Button(windo, borderwidth=0,command = clear_report, bg='white', image=sad_img)
    panel5.image = sad_img
    panel5.pack()
    panel5.place(x=1167, y=70)

    ri1 = PIL.Image.open('./meta/dw.png')
    ri1 = ri1.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img1 = ImageTk.PhotoImage(ri1)
    panel6 = Button(windo, borderwidth=0,command = ad_gen_csv, bg='white', image=sad_img1)
    panel6.image = sad_img1
    panel6.pack()
    panel6.place(x=1127, y=70)

    us_rep = tk.Label(windo, text=account[1]+"'s Report", width=20, height=1, fg='white', bg="#171d35",
                   font=('times', 22, ' bold '))
    us_rep.place(x=624, y=70)

    ## Add some style
    style = ttk.Style()
    style.configure("Treeview",background = '#171d35',foreground = 'white',font=('times', 10, 'bold '))
    # style.configure("Treeview.Heading",bg = 'blue', foreground='black')
    tree = ttk.Treeview(windo, column=("User ID", "Image Name", "Vehicle", 'License Plate', '', 'c6', 'c7', 'c8'), show='headings')

    tree.column("#1",  stretch=NO, minwidth=100,width=100)
    tree.heading("#1", text="User ID")

    tree.column("#2", stretch=NO, minwidth=100,width=100)
    tree.heading("#2", text="Image Name")

    tree.column("#3",stretch=NO, minwidth=100,width=100)
    tree.heading("#3", text="Vehicle")

    tree.column("#4",stretch=NO, minwidth=100,width=100)
    tree.heading("#4", text="License Plate")

    tree.column("#5", stretch=NO, minwidth=100,width=100)
    tree.heading("#5", text="Owner Name")

    tree.column("#6",stretch=NO, minwidth=100, width=100)
    tree.heading("#6", text="Vehicle Registration")

    tree.column("#7",stretch=NO, minwidth=100, width=100)
    tree.heading("#7", text="Upload Date")

    tree.column("#8",stretch=NO, minwidth=100, width=100)
    tree.heading("#8", text="Upload Time")

    tree.place(x=405,y=110)
    cursor.execute("SELECT * FROM user_records where user_id="+"'"+account[0]+"'")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def admin_check_report():
    # upload_im_b['state'] = 'disabled'
    # check_report_b['state'] = 'disabled'
    global tree,us_rep,panel5,panel6

    clear_screen()
    ri = PIL.Image.open('./meta/close.png')
    ri = ri.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img = ImageTk.PhotoImage(ri)
    panel5 = Button(windo, borderwidth=0,command = clear_report, bg='white', image=sad_img)
    panel5.image = sad_img
    panel5.pack()
    panel5.place(x=1167, y=70)

    ri1 = PIL.Image.open('./meta/dw.png')
    ri1 = ri1.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img1 = ImageTk.PhotoImage(ri1)
    panel6 = Button(windo, borderwidth=0,command = ad_gen_all_csv, bg='white', image=sad_img1)
    panel6.image = sad_img1
    panel6.pack()
    panel6.place(x=1127, y=70)

    us_rep = tk.Label(windo, text="All Users Report", width=20, height=1, fg='white', bg="#171d35",
                   font=('times', 22, ' bold '))
    us_rep.place(x=624, y=70)

    ## Add some style
    style = ttk.Style()
    style.configure("Treeview",background = '#171d35',foreground = 'white',font=('times', 10, 'bold '))
    # style.configure("Treeview.Heading",bg = 'blue', foreground='black')
    tree = ttk.Treeview(windo, column=("User ID", "Image Name", "Vehicle", 'License Plate', '', 'c6', 'c7', 'c8'), show='headings')

    tree.column("#1",  stretch=NO, minwidth=100,width=100)
    tree.heading("#1", text="User ID")

    tree.column("#2", stretch=NO, minwidth=100,width=100)
    tree.heading("#2", text="Image Name")

    tree.column("#3",stretch=NO, minwidth=100,width=100)
    tree.heading("#3", text="Vehicle")

    tree.column("#4",stretch=NO, minwidth=100,width=100)
    tree.heading("#4", text="License Plate")

    tree.column("#5", stretch=NO, minwidth=100,width=100)
    tree.heading("#5", text="Owner Name")

    tree.column("#6",stretch=NO, minwidth=100, width=100)
    tree.heading("#6", text="Vehicle Registration")

    tree.column("#7",stretch=NO, minwidth=100, width=100)
    tree.heading("#7", text="Upload Date")

    tree.column("#8",stretch=NO, minwidth=100, width=100)
    tree.heading("#8", text="Upload Time")

    tree.place(x=405,y=110)
    cursor.execute("SELECT * FROM user_records where user_id!='ADMIN123';")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def admin_log_report():
    # upload_im_b['state'] = 'disabled'
    # check_report_b['state'] = 'disabled'
    global tree,us_rep,panel5,panel6

    clear_screen()
    ri = PIL.Image.open('./meta/close.png')
    ri = ri.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img = ImageTk.PhotoImage(ri)
    panel5 = Button(windo, borderwidth=0,command = clear_report, bg='white', image=sad_img)
    panel5.image = sad_img
    panel5.pack()
    panel5.place(x=1167, y=70)

    ri1 = PIL.Image.open('./meta/dw.png')
    ri1 = ri1.resize((40, 40), PIL.Image.ANTIALIAS)
    sad_img1 = ImageTk.PhotoImage(ri1)
    panel6 = Button(windo, borderwidth=0,command = ad_log_gen_csv, bg='white', image=sad_img1)
    panel6.image = sad_img1
    panel6.pack()
    panel6.place(x=1127, y=70)

    us_rep = tk.Label(windo, text="Users Login Report", width=20, height=1, fg='white', bg="#171d35",
                   font=('times', 22, ' bold '))
    us_rep.place(x=624, y=70)

    ## Add some style
    style = ttk.Style()
    style.configure("Treeview",background = '#171d35',foreground = 'white',font=('times', 10, 'bold '))
    # style.configure("Treeview.Heading",bg = 'blue', foreground='black')
    tree = ttk.Treeview(windo, column=("User ID", "User Name", "Status", 'Date','Time'), show='headings')

    tree.column("#1",  stretch=NO, minwidth=100,width=100)
    tree.heading("#1", text="User ID")

    tree.column("#2", stretch=NO, minwidth=100,width=100)
    tree.heading("#2", text="User Name")

    tree.column("#3",stretch=NO, minwidth=100,width=100)
    tree.heading("#3", text="Status")

    tree.column("#4",stretch=NO, minwidth=100,width=100)
    tree.heading("#4", text="Date")

    tree.column("#5", stretch=NO, minwidth=100,width=100)
    tree.heading("#5", text="Time")

    tree.place(x=555,y=110)
    cursor.execute("SELECT * FROM user_log;")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def gen_csv():
    dir2 = Path('Reports')
    if dir2.is_dir():
        pass
    else:
        os.mkdir('Reports')
    cursor.execute("SELECT * FROM user_records where user_id=" + "'" + account[0] + "'")
    rows = cursor.fetchall()
    ts1 = time.time()
    img_date = datetime.datetime.fromtimestamp(ts1).strftime('%Y-%m-%d').replace('-','_')
    img_time = datetime.datetime.fromtimestamp(ts1).strftime('%H:%M:%S').replace(':','_')
    file_name = './Reports/'+ account[0] +'_'+img_date+'_'+img_time+'.csv'
    with open(file_name, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(rows)
    not3 = tk.Label(windo, text='Report Saved Successfully!', width=22, height=1, fg="black",
                    bg="#37f713",
                    font=('times', 16, ' bold '))
    not3.place(x=10, y=190)
    windo.after(3000, destroy_widget, not3)

def ad_gen_all_csv():
    dir2 = Path('Reports')
    if dir2.is_dir():
        pass
    else:
        os.mkdir('Reports')
    cursor.execute("SELECT * FROM user_records;")
    rows = cursor.fetchall()
    ts1 = time.time()
    img_date = datetime.datetime.fromtimestamp(ts1).strftime('%Y-%m-%d').replace('-','_')
    img_time = datetime.datetime.fromtimestamp(ts1).strftime('%H:%M:%S').replace(':','_')
    file_name = './Reports/'+ account[0] +'_'+img_date+'_'+img_time+'.csv'
    with open(file_name, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(rows)
    not3 = tk.Label(windo, text='Report Saved Successfully!', width=22, height=1, fg="black",
                    bg="#37f713",
                    font=('times', 16, ' bold '))
    not3.place(x=10, y=315)
    windo.after(3000, destroy_widget, not3)

def ad_gen_csv():
    dir2 = Path('Reports')
    if dir2.is_dir():
        pass
    else:
        os.mkdir('Reports')
    cursor.execute("SELECT * FROM user_records where user_id=" + "'" + account[0] + "'")
    rows = cursor.fetchall()
    ts1 = time.time()
    img_date = datetime.datetime.fromtimestamp(ts1).strftime('%Y-%m-%d').replace('-','_')
    img_time = datetime.datetime.fromtimestamp(ts1).strftime('%H:%M:%S').replace(':','_')
    file_name = './Reports/'+ account[0] +'_'+img_date+'_'+img_time+'.csv'
    with open(file_name, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(rows)
    not3 = tk.Label(windo, text='Report Saved Successfully!', width=22, height=1, fg="black",
                    bg="#37f713",
                    font=('times', 16, ' bold '))
    not3.place(x=10, y=315)
    windo.after(3000, destroy_widget, not3)

def ad_log_gen_csv():
    dir2 = Path('Reports')
    if dir2.is_dir():
        pass
    else:
        os.mkdir('Reports')
    cursor.execute("SELECT * FROM user_log; ")
    rows = cursor.fetchall()
    ts1 = time.time()
    img_date = datetime.datetime.fromtimestamp(ts1).strftime('%Y-%m-%d').replace('-','_')
    img_time = datetime.datetime.fromtimestamp(ts1).strftime('%H:%M:%S').replace(':','_')
    file_name = './Reports/'+ account[0] +'_'+img_date+'_'+img_time+'.csv'
    with open(file_name, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(rows)
    not3 = tk.Label(windo, text='Report Saved Successfully!', width=22, height=1, fg="black",
                    bg="#37f713",
                    font=('times', 16, ' bold '))
    not3.place(x=10, y=315)
    windo.after(3000, destroy_widget, not3)

def clear_report():
    # upload_im_b['state'] = 'normal'
    # check_report_b['state'] = 'normal'
    tree.destroy()
    us_rep.destroy()
    panel5.destroy()
    panel6.destroy()

def save_img():
    name = "LPR_"+os.path.basename(path)
    name1 = read +'.jpg'
    dir2 = Path('Results')
    if dir2.is_dir():
        pass
    else:
        os.mkdir('Results')

    op.save('./Results/'+ name)
    op1.save('./Results/'+name1)

    not3 = tk.Label(windo, text='Results Saved Successfully!', width=22, height=1, fg="black",
                    bg="yellow",
                    font=('times', 16, ' bold '))
    not3.place(x=10, y=190)
    windo.after(3000, destroy_widget, not3)

def destroy_widget(widget):
    widget.destroy()

def limitSizeid(*args):
    value = idValue.get()
    if len(value) > 10: idValue.set(value[:10])

idValue = StringVar()
idValue.trace('w', limitSizeid)

def limitSizename(*args):
    value1 = nameValue.get()
    if len(value1) > 12: nameValue.set(value1[:12])

nameValue = StringVar()
nameValue.trace('w', limitSizename)

def clear_id():
    id_txt.delete(first=0, last=10)

def clear_name():
    name_txt.delete(first=0, last=15)

def clear_full_name():
    full_name_txt.delete(first=0, last=15)

def clear_reg_id():
    choose_id_txt.delete(first=0, last=15)

def clear_pass():
    pass_id_txt.delete(first=0, last=15)

def clear_c_pass():
    c_pass_id_txt.delete(first=0, last=15)

def login():
    global tb,time1,user_frame,user_start,user_res,user_clock,upload_im_b,check_report_b,account

    log_id = id_txt.get()
    log_pwd = name_txt.get()
    if log_id == '' or log_pwd =='':
        notif4 = tk.Label(windo, text="Please Enter the Data!", width=19, height=1, fg="black", bg="yellow",
                          font=('times', 14, ' bold '))
        notif4.place(x=30, y=560)
        windo.after(2000, destroy_widget, notif4)
    else:
        tb = 'user_log'
        log_sql = "CREATE TABLE IF NOT EXISTS " +tb + """
                        (user_id varchar(20) NOT NULL,
                         full_name varchar(100) NOT NULL,
                         status varchar(50) NOT NULL,
                         date VARCHAR(30) NOT NULL,
                         time VARCHAR(30) NOT NULL);
                        """
        cursor.execute(log_sql)

        values = (log_id,)
        login_sql = 'SELECT * FROM LPR_Registration WHERE ID = % s'
        cursor.execute(login_sql, values)
        account = cursor.fetchone()
        if account:
            account = list(account)
            if account[0] == log_id:
                account[2] = base64.b64decode(account[2]).decode("utf-8")
                if account[2] == log_pwd:
                    ## Enter the user log
                    log_ts = time.time()
                    user_date = datetime.datetime.fromtimestamp(log_ts).strftime('%Y-%m-%d')
                    user_time = datetime.datetime.fromtimestamp(log_ts).strftime('%H:%M:%S')
                    status = 'Logged In'

                    ## Insert into Table
                    log_insert_sql = "insert into " + tb + """
                    values (%s,%s,%s,%s,%s)"""
                    rec_values = (account[0], account[1], status,user_date,user_time )
                    cursor.execute(log_insert_sql, rec_values)
                    connection.commit()

                    ### USer side
                    clear_id()
                    clear_name()
                    user_frame = Frame(windo,width = width, height = height,bg = 'white')
                    user_frame.pack()
                    user_frame.place(x=0,y=0)

                    user_start = tk.Label(windo, text= "Welcome: "+account[1],
                                     bg="#171d35", fg="white", width=58,
                                     height=1, font=('times', 30, 'italic bold '))
                    user_start.place(x=0, y=0)

                    user_res = Button(windo, text='Sign out',command = user_on_closing, width=13, height=1, font=('times', 13, 'bold'), bg='white')
                    user_res.place(x=10, y=9)

                    def tick():
                        global time1
                        time2 = time.strftime('%H:%M:%S')
                        if time2 != time1:
                            time1 = time2
                            user_clock.config(text=time1)
                        user_clock.after(200, tick)

                    time1 = ''
                    user_clock = Label(windo, font=('times', 20, 'bold'), bg='white')
                    user_clock.place(x=1160, y=7)
                    tick()

                    upload_im_b = tk.Button(windo, text='Upload Image', command=upload_im, bg="#171d35", fg="white",
                                            width=18,
                                            height=1, font=('times', 20, 'italic bold '), activebackground='yellow')
                    upload_im_b.place(x=10, y=70)

                    check_report_b = tk.Button(windo, text='Check Reports',command = check_report, bg="#171d35", fg="white", width=18,
                                               height=1, font=('times', 20, 'italic bold '), activebackground='yellow')
                    check_report_b.place(x=10, y=130)
                else:
                    notif5 = tk.Label(windo, text="Wrong Password!", width=19, height=1, fg="black", bg="yellow",
                                      font=('times', 14, ' bold '))
                    notif5.place(x=30, y=560)
                    windo.after(2000, destroy_widget, notif5)
            else:
                notif8 = tk.Label(windo, text="No account found!", width=19, height=1, fg="black", bg="yellow",
                                  font=('times', 14, ' bold '))
                notif8.place(x=30, y=560)
                windo.after(2000, destroy_widget, notif8)
        else:
            notif6 = tk.Label(windo, text="No account found!", width=19, height=1, fg="black", bg="yellow",
                              font=('times', 14, ' bold '))
            notif6.place(x=30, y=560)
            windo.after(2000, destroy_widget, notif6)

def registration():
    full_n = full_name_txt.get()
    ch_id = choose_id_txt.get()
    r_pwd = pass_id_txt.get()
    c_pwd = c_pass_id_txt.get()
    if full_n == '' or ch_id == '' or r_pwd == '' or c_pwd=='':
        notif3 = tk.Label(windo, text="Please Enter the Data!", width=19, height=1, fg="black", bg="yellow",
                          font=('times', 14, ' bold '))
        notif3.place(x=920, y=580)
        windo.after(2000, destroy_widget, notif3)
    else:
        if r_pwd != c_pwd:
            notif = tk.Label(windo, text="Password not Matched!", width=19, height=1, fg="black", bg="yellow",
                                   font=('times', 14, ' bold '))
            notif.place(x=920, y=516)
            windo.after(3000, destroy_widget, notif)

        else:
            r_fname = full_name_txt.get()
            r_id = choose_id_txt.get()
            # Create the DB
            db_sql = """CREATE DATABASE IF NOT EXISTS LPR;
               """

            # Registration table
            table_sql = """CREATE TABLE IF NOT EXISTS LPR_Registration (
                ID varchar(100) NOT NULL,
                FULL_NAME varchar(100) NOT NULL,
                PASSWORD varchar(50) NOT NULL,
                PRIMARY KEY (ID)
            );
               """
            insert_sql = ("INSERT INTO LPR_Registration(ID,FULL_NAME,PASSWORD) VALUES (%s, %s, %s)")
            try:
                cursor.execute(db_sql)
                cursor.execute(table_sql)
                ## Match the ID, it should be unique
                values = (r_id,)
                match_id = 'SELECT * FROM LPR_Registration WHERE ID = % s'
                cursor.execute(match_id, values)
                match_account = cursor.fetchone()
                if match_account:
                    match_account = list(match_account)
                    if r_id == match_account[0]:
                        notif1 = tk.Label(windo, text=r_id+" already exist!", width=19, height=1, fg="black", bg="yellow",
                                         font=('times', 14, ' bold '))
                        notif1.place(x=920, y=362)
                        windo.after(3000, destroy_widget, notif1)
                    else:
                        r_pwd = base64.b64encode(r_pwd.encode("utf-8"))
                        print(r_pwd)
                        values = (r_id, r_fname, r_pwd)
                        cursor.execute(insert_sql, values)
                        connection.commit()
                        notif2 = tk.Label(windo, text="Registered Successfully!", width=19, height=1, fg="black",
                                          bg="yellow",
                                          font=('times', 14, ' bold '))
                        notif2.place(x=920, y=580)
                        windo.after(3000, destroy_widget, notif2)
                        clear_full_name()
                        clear_reg_id()
                        clear_pass()
                        clear_c_pass()
                else:
                    r_pwd = base64.b64encode(r_pwd.encode("utf-8"))
                    print(r_pwd)
                    values = (r_id, r_fname, r_pwd)
                    cursor.execute(insert_sql, values)
                    connection.commit()
                    notif2 = tk.Label(windo, text="Registered Successfully!", width=19, height=1, fg="black", bg="yellow",
                                      font=('times', 14, ' bold '))
                    notif2.place(x=920, y=580)
                    windo.after(3000, destroy_widget, notif2)
                    clear_full_name()
                    clear_reg_id()
                    clear_pass()
                    clear_c_pass()
            except pymysql.DatabaseError as ex:
                print(ex)

def admin_login():
    global time3,ad_frame,ad_start,ad_clock,res,account,ad_upload_im_b,ad_report_b

    # Registration table
    table_sql = """CREATE TABLE IF NOT EXISTS LPR_Admin (
           ID varchar(100) NOT NULL,
           FULL_NAME varchar(100) NOT NULL,
           PASSWORD varchar(50) NOT NULL,
           PRIMARY KEY (ID)
       );
          """
    cursor.execute(table_sql)

    log_id = id_txt.get()
    log_pwd = name_txt.get()
    if log_id == '' or log_pwd =='':
        notif4 = tk.Label(windo, text="Please Enter the Data!", width=19, height=1, fg="black", bg="yellow",
                          font=('times', 14, ' bold '))
        notif4.place(x=30, y=560)
        windo.after(2000, destroy_widget, notif4)
    else:
        values = (log_id,)
        login_sql = 'SELECT * FROM LPR_Admin WHERE ID = % s'
        cursor.execute(login_sql, values)
        account = cursor.fetchone()
        if account:
            account = list(account)
            if account[0] == log_id:
                if account[2] == log_pwd:
                    ### Admin side
                    clear_id()
                    clear_name()

                    ad_frame = Frame(windo,width = width, height = height,bg = 'white')
                    ad_frame.pack()
                    ad_frame.place(x=0,y=0)

                    ad_start = tk.Label(windo, text= "Welcome Admin: "+account[1],
                                     bg="#171d35", fg="white", width=58,
                                     height=1, font=('times', 30, 'italic bold '))
                    ad_start.place(x=0, y=0)

                    ad_upload_im_b = tk.Button(windo, text='Upload Image', command=ad_upload_im, bg="#171d35", fg="white",
                                            width=18,
                                            height=1, font=('times', 20, 'italic bold '), activebackground='yellow')
                    ad_upload_im_b.place(x=10, y=70)

                    ad_report_b = tk.Button(windo, text='Check User Reports',command = admin_check_report, bg="#171d35", fg="white", width=18,
                                               height=1, font=('times', 20, 'italic bold '), activebackground='yellow')
                    ad_report_b.place(x=10, y=130)

                    ad_ow_report_b = tk.Button(windo, text='Check Own Reports', command=admin_own_report, bg="#171d35",
                                            fg="white", width=18,
                                            height=1, font=('times', 20, 'italic bold '), activebackground='yellow')
                    ad_ow_report_b.place(x=10, y=190)

                    ad_login_history = tk.Button(windo, text='Login History', command=admin_log_report, bg="#171d35",
                                            fg="white", width=18,
                                            height=1, font=('times', 20, 'italic bold '), activebackground='yellow')
                    ad_login_history.place(x=10, y=250)

                    res = Button(windo, text='Sign out', command = admin_on_closing, width=13, height=1, font=('times', 13, 'bold'), bg='white')
                    res.place(x=10, y=9)

                    def tick():
                        global time3
                        time2 = time.strftime('%H:%M:%S')
                        if time2 != time3:
                            time3 = time2
                            ad_clock.config(text=time3)
                        ad_clock.after(200, tick)

                    time3 = ''
                    ad_clock = Label(windo, font=('times', 20, 'bold'), bg='white')
                    ad_clock.place(x=1160, y=7)
                    tick()
                else:
                    notif5 = tk.Label(windo, text="Wrong Password!", width=19, height=1, fg="black", bg="yellow",
                                      font=('times', 14, ' bold '))
                    notif5.place(x=30, y=560)
                    windo.after(2000, destroy_widget, notif5)
            else:
                notif8 = tk.Label(windo, text="No account found!", width=19, height=1, fg="black", bg="yellow",
                                  font=('times', 14, ' bold '))
                notif8.place(x=30, y=560)
                windo.after(2000, destroy_widget, notif8)
        else:
            notif6 = tk.Label(windo, text="No account found!", width=19, height=1, fg="black", bg="yellow",
                              font=('times', 14, ' bold '))
            notif6.place(x=30, y=560)
            windo.after(2000, destroy_widget, notif6)

def admin_logout():

    ad_frame.destroy()
    ad_start.destroy()
    ad_clock.destroy()
    res.destroy()
    ad_upload_im_b.destroy()
    ad_report_b.destroy()
    try:
        try:
           clear_report()
        except:
            pass
        user_frame.destroy()
        user_start.destroy()
        user_res.destroy()
        user_clock.destroy()
        check_report_b.destroy()
        upload_im_b.destroy()
        dn1.destroy()
        imageFrame.destroy()
        imageFrame1.destroy()
        display.destroy()
        display1.destroy()
        dn4.destroy()
        imageFrame2.destroy()
        display2.destroy()
        panel4.destroy()
        info_frame.destroy()
        veh_info.destroy()
        lp_info.destroy()
        ow_info.destroy()
        car_info.destroy()
        veh_date_info.destroy()
        clear_report()
    except:
        pass



def admin_on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Log Out", "Do you want to Logout from the System?"):
        admin_logout()

def user_logout():
    log_ts = time.time()
    user_date = datetime.datetime.fromtimestamp(log_ts).strftime('%Y-%m-%d')
    user_time = datetime.datetime.fromtimestamp(log_ts).strftime('%H:%M:%S')
    status = 'Sign Out'
    ## Insert into Table
    log_insert_sql = "insert into " + tb + """
    values (%s,%s,%s,%s,%s)"""
    rec_values = (account[0], account[1], status, user_date, user_time)
    cursor.execute(log_insert_sql, rec_values)
    connection.commit()
    try:
        try:
           clear_report()
        except:
            pass
        user_frame.destroy()
        user_start.destroy()
        user_res.destroy()
        user_clock.destroy()
        check_report_b.destroy()
        upload_im_b.destroy()
        dn1.destroy()
        imageFrame.destroy()
        imageFrame1.destroy()
        display.destroy()
        display1.destroy()
        dn4.destroy()
        imageFrame2.destroy()
        display2.destroy()
        panel4.destroy()
        info_frame.destroy()
        veh_info.destroy()
        lp_info.destroy()
        ow_info.destroy()
        car_info.destroy()
        veh_date_info.destroy()
        clear_report()
    except:
        pass

def clear_screen():
    try:
        dn1.destroy()
        imageFrame.destroy()
        imageFrame1.destroy()
        display.destroy()
        display1.destroy()
        dn4.destroy()
        imageFrame2.destroy()
        display2.destroy()
        panel4.destroy()
        info_frame.destroy()
        veh_info.destroy()
        lp_info.destroy()
        ow_info.destroy()
        car_info.destroy()
        veh_date_info.destroy()
        clear_report()
        us_rep.destroy()
        # upload_im_b.destroy()
        # check_report_b.destroy()
    except:
        pass

def user_on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Log Out", "Do you want to Logout from the System?"):
        user_logout()

def admin_switch():
    global admin_close_button, admin_login_button
    login_button["state"] = "disabled"

    admin_login_button = tk.Button(windo, text="Admin Login",command = admin_login, fg="white", bg="#171d35", width=10, height=1,
                             activebackground="yellow", font=('times', 15, ' bold '))
    admin_login_button.place(x=75, y=593)

    admin_close_button = tk.Button(windo, text="Close", command=close_admin, fg="white", bg="#171d35", width=10, height=1,
                             activebackground="yellow", font=('times', 15, ' bold '))
    admin_close_button.place(x=75, y=643)

def close_admin():
    admin_close_button.destroy()
    admin_login_button.destroy()
    login_button["state"] = "normal"

id_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '), textvariable=idValue)
id_txt.place(x=30, y=435)

name_l = tk.Label(windo, text="Enter Password", width=13, height=1, fg="black", bg="#24c4a2",
                  font=('times', 14, ' bold '))
name_l.place(x=30, y=485)

name_txt = tk.Entry(windo, width=13,show='*', bg="white", fg="black", font=('times', 22, ' bold '), textvariable=nameValue)
name_txt.place(x=30, y=512)

login_button = tk.Button(windo, text="Login", command = login, fg="white", bg="#171d35", width=10, height=1,
                         activebackground="yellow", font=('times', 15, ' bold '))
login_button.place(x=75, y=593)

admin_button = tk.Button(windo, text="Admin", command = admin_switch, fg="white", bg="#171d35", width=10, height=1,
                         activebackground="yellow", font=('times', 15, ' bold '))
admin_button.place(x=75, y=643)

## Sign UP (Register)

## Range password
def limitSize_pass(*args):
    value1 = pass_Value.get()
    if len(value1) > 12: pass_Value.set(value1[:12])

pass_Value = StringVar()
pass_Value.trace('w', limitSize_pass)

## Range confirm password
def limitSize_c_pass(*args):
    value1 = c_pass_Value.get()
    if len(value1) > 12: c_pass_Value.set(value1[:12])

c_pass_Value = StringVar()
c_pass_Value.trace('w', limitSize_c_pass)

## Range ID
def limitSize_rid(*args):
    value1 = rid_pass_Value.get()
    if len(value1) > 10: rid_pass_Value.set(value1[:10])

rid_pass_Value = StringVar()
rid_pass_Value.trace('w', limitSize_rid)

full_name_l = tk.Label(windo, text="Enter Name", width=13, height=1, fg="black", bg="#24c4a2",
                  font=('times', 14, ' bold '))
full_name_l.place(x=920, y=285)

full_name_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '))
full_name_txt.place(x=920, y=312)

choose_id_l = tk.Label(windo, text="Choose ID", width=13, height=1, fg="black", bg="#24c4a2",
                  font=('times', 14, ' bold '))
choose_id_l.place(x=920, y=362)

choose_id_txt = tk.Entry(windo, width=13, bg="white", fg="black", font=('times', 22, ' bold '),textvariable=rid_pass_Value)
choose_id_txt.place(x=920, y=389)

pass_id_l = tk.Label(windo, text="Password", width=13, height=1, fg="black", bg="#24c4a2",
                  font=('times', 14, ' bold '))
pass_id_l.place(x=920, y=439)

pass_id_txt = tk.Entry(windo, width=13, bg="white",show='*', fg="black", font=('times', 22, ' bold '),textvariable=pass_Value)
pass_id_txt.place(x=920, y=466)

c_pass_id_l = tk.Label(windo, text="Confirm Password", width=15, height=1, fg="black", bg="#24c4a2",
                  font=('times', 14, ' bold '))
c_pass_id_l.place(x=920, y=516)

c_pass_id_txt = tk.Entry(windo, width=13, bg="white", fg="black",show='*', font=('times', 22, ' bold '),textvariable=c_pass_Value)
c_pass_id_txt.place(x=920, y=543)

def on_closing():

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        windo.destroy()
windo.protocol("WM_DELETE_WINDOW", on_closing)

## Clear Buttons
clearButton = tk.Button(windo, command=clear_id, text="Clear", fg="white", bg="#171d35", width=5, height=1,
                        activebackground="yellow", font=('times', 12, ' bold '))
clearButton.place(x=250, y=437)

clearButton1 = tk.Button(windo, command=clear_name, text="Clear", fg="white", bg="#171d35", width=5, height=1,
                         activebackground="yellow", font=('times', 12, ' bold '))
clearButton1.place(x=250, y=514)

clearButton2 = tk.Button(windo, command=clear_full_name, text="Clear", fg="white", bg="#171d35", width=5, height=1,
                         activebackground="yellow", font=('times', 12, ' bold '))
clearButton2.place(x=1140, y=314)

clearButton3 = tk.Button(windo, command=clear_reg_id, text="Clear", fg="white", bg="#171d35", width=5, height=1,
                         activebackground="yellow", font=('times', 12, ' bold '))
clearButton3.place(x=1140, y=391)

clearButton4 = tk.Button(windo, command=clear_pass, text="Clear", fg="white", bg="#171d35", width=5, height=1,
                         activebackground="yellow", font=('times', 12, ' bold '))
clearButton4.place(x=1140, y=465)

clearButton5 = tk.Button(windo, command=clear_c_pass, text="Clear", fg="white", bg="#171d35", width=5, height=1,
                         activebackground="yellow", font=('times', 12, ' bold '))
clearButton5.place(x=1140, y=539)

register_button = tk.Button(windo, text="Register",command = registration, fg="white", bg="#171d35", width=10, height=1,
                         activebackground="yellow", font=('times', 15, ' bold '))
register_button.place(x=965, y=613)

windo.mainloop()