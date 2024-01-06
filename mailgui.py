from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# from smtplib import SS
from tkinter import *
from tkinter import filedialog
# from sendemail import EmailMessage

attachements = []

master = Tk()
master.geometry('500x400')
master.title("Email")

# functions

def sendEmail():

    msg = EmailMessage()


    fromaddr = temp_username.get()
    toaddr = temp_receiver.get()
    password = temp_password.get()
    to       = temp_receiver.get()
    subject  = temp_subject.get()
    body     = temp_body.get()
    # instance of MIMEMultipart
    
    # storing the senders email address  
    msg['From'] = fromaddr
    
    # storing the receivers email address 
    msg['To'] = toaddr
    
    # storing the subject 
    msg['Subject'] = "Subject of the Mail"
    
    # string to store the body of the mail
    body = "Body_of_the_mail"
    
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # attachment = attachements[0]

    p = MIMEBase('application', 'octet-stream')
        
    filename = attachements[0]
    filetype = filename.split('.')
    filetype = filetype[1]
    if filetype == "jpg" or filetype == "JPG" or filetype == "png" or filetype == "PNG":
        import imghdr
        with open(filename, 'rb') as f:
            file_data = f.read()
            image_type = imghdr.what(filename)
            msg.add_attachment(file_data, maintype='image', subtype=image_type, filename=f.name)
    else:
        with open(filename, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=f.name)

    s = smtplib.SMTP('smtp.outlook.com', 587)
  
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(fromaddr, password)
    
    # Converts the Multipart msg into a string
    text = msg.as_string()
    
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    
    # terminating the session
    s.quit()

def selectFile():
    filename = filedialog.askopenfilename(initialdir='d:/',title='Please select a file')
    attachements.append(filename)
    notif.config(fg='green', text = 'Attached ' + str(len(attachements)) + ' files')


def reset():
    usernameEntry.delete(0,'end')
    passwordEntry.delete(0,'end')
    receiverEntry.delete(0,'end')
    subjectEntry.delete(0,'end')
    bodyEntry.delete(0,'end') 

def destroy():
    master.destroy()



Label(master, text="Please use the form below to send an email",bg= "black",fg='white', font=('Calibri',11)).grid(row=1, padx=5 ,pady=10)

Label(master, text="Email",fg='black', font=('Calibri', 11)).grid(row=2,sticky=W, padx=70,pady = 8)
Label(master, text="Password",fg='black',font=('Calibri', 11)).grid(row=3,sticky=W, padx=70, pady=8)
Label(master, text="To",fg='black',font=('Calibri', 11)).grid(row=4,sticky=W, padx=70, pady=8)
Label(master, text="Subject",fg='black',font=('Calibri', 11)).grid(row=5,sticky=W, padx=70, pady=8)
Label(master, text="Body",fg='black' ,font=('Calibri', 11)).grid(row=6,sticky=W, padx=70, pady=8)
notif = Label(master, text="", font=('Calibri', 11),fg="red")
notif.grid(row=10,sticky=S)


temp_username = StringVar()
temp_password = StringVar()
temp_receiver = StringVar()
temp_subject  = StringVar()
temp_body     = StringVar()


usernameEntry = Entry(master, textvariable = temp_username)
usernameEntry.grid(row=2,column=0, ipadx = 35)
passwordEntry = Entry(master, show="*", textvariable = temp_password)
passwordEntry.grid(row=3,column=0,ipadx = 35)
receiverEntry  = Entry(master, textvariable = temp_receiver)
receiverEntry.grid(row=4,column=0,ipadx = 35)
subjectEntry  = Entry(master, textvariable = temp_subject)
subjectEntry.grid(row=5,column=0,ipadx = 35 )
bodyEntry     = Entry(master, textvariable = temp_body)
bodyEntry.grid(row=6,column=0,ipadx = 35 , pady = 10)


Button(master, text = "Send",width =11,fg= 'black',font =('georgia',8,'bold'), command=sendEmail).grid(row=7,   sticky=W,  pady=10, padx=70)
Button(master, text = "Reset",width =11,fg= 'black',font =('georgia',8,'bold'), command=reset).grid(row=7,  sticky=W,  padx=220, pady=10)
Button(master, text = "Attachments",width =11,fg= 'black',font =('georgia',8,'bold') , command=selectFile).grid(row=8,  sticky=W,  padx=70 , pady = 10)
Button(master,text ="Exit" ,width =11,fg= 'black',font =('georgia',8,'bold'),command=destroy).grid(row=8,  sticky=W,  padx=220 , pady = 10)

master.mainloop()