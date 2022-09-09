from tkinter import *
import opencv_test2
import itchat
import threading

# log in WeChat
itchat.auto_login(hotReload=True)


window = Tk()
button_frame = Frame(window)

window.title('Automatic Alarm System')
window.geometry('600x200')
label_1 = Label(window, text='Name')
label_2 = Label(window, text='Password')
entry_1 = Entry(window)
entry_2 = Entry(window, show='*')

label_1.grid(row=1, sticky=W)
label_2.grid(row=2, sticky=E)

entry_1.grid(row=1, column=1, sticky=E, padx=3)
entry_2.grid(row=2, column=1, sticky=E, padx=3)


def start():
    name = entry_1.get()
    password = entry_2.get()

    f = open("Data.txt", "r")
    lines = f.readlines()
    existornot = 0
    for line in lines:
        line = eval(line)
        if name == line['user'] and password == line['psd']:
            existornot = 1
            break

    if existornot == 1:
        l_msg['text'] = 'login successfully'
        l_msg['fg'] = 'green'

        opencv_test2.detect_motion()

    else:
        l_msg.configure(text='log in failed!', fg='red')

    f.close()


def register():
    name = entry_1.get()
    password = entry_2.get()
    f = open("Data.txt", "a")
    dict = {"user": name, "psd": password}
    f.write(str(dict)+"\n")
    l_msg['text'] = 'register successful'
    l_msg['fg'] = 'green'
    f.close()

def quitt():
    exit()


l_msg = Label(window, text='')
l_msg.grid(row=0, columnspan=2)

button_1 = Button(button_frame, text="start", width=6, command=start)
button_2 = Button(button_frame, text="register", width=6, command=register)
button_3 = Button(button_frame, text="quit", width=6, command=quitt)
button_1.grid(row=0, column=0)
button_2.grid(row=0, column=1)
button_3.grid(row=0, column=2)
button_frame.grid(row=3, columnspan=3, pady=10)

window.mainloop()