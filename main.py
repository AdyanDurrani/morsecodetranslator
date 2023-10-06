import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox
import pyperclip
import pygame
pygame.init()
import time
from PIL import Image, ImageTk

open_mouth = 0
closed_mouth = 0

resolution = "300x500"
alphabet = {
    ".-" : "A",
    "-..." : "B",
    "-.-." : "C",
    "-.." : "D",
    "." : "E",
    "..-." : "F",
    "--." : "G",
    "...." : "H",
    ".." : "I",
    ".---" : "J",
    "-.-"  : "K",
    ".-.." : "L",
    "--" : "M",
    "-." : "N",
    "---" : "O",
    ".--." : "P",
    "--.-" : "Q",
    ".-." : "R",
    "..." : "S",
    "-" : "T",
    "..-"  : "U",
    "...-" : "V",
    ".--" : "W",
    "-..-" : "X",
    "-.--" : "Y",
    "--.." : "Z",
    " ": " ",
     "" : ""}

morsebet = {
    "A":".-",
    "B":"-...",
    "C":"-.-.",
    "D":"-..",
    "E":".",
    "F":"..-.",
    "G":"--.",
    "H":"....",
    "I":"..",
    "J":".---",
    "K":"-.-",
    "L":".-..",
    "M":"--" ,
    "N":"-.",
    "O":"---",
    "P":".--.",
    "Q":"--.-",
    "R":".-.",
    "S":"...",
    "T":"-",
    "U":"..-",
    "V":"...-",
    "W":".--",
    "X":"-..-" ,
    "Y":"-.--" ,
    "Z":"--.." ,
    " ": " ",
     "" : ""}
result = ""
pygame.mixer.init()
longer = pygame.mixer.Sound("beep.mp3")
shorter = pygame.mixer.Sound("boper.mp3")

master = tk.Tk() #creates window which is called master for some reason

master.title("Morse code translator")


def eng_to_m():
    global output, result, sound, e1
    output.destroy()
    try:
        eng = e1.get().upper()
    except:
        eng = to_translate.upper()
    result = ""
    
    for i in eng:
        i = i.upper()
        if i == " ":
            what_add = "/ "
        elif i.isnumeric():
          messagebox.showinfo("Error", "NUMBER?¿?¿?¿!¡")
          break
        else:

            what_add = morsebet[i]
        result = result + " " + what_add


    output = tk.Label(master, text=result, wraplength=200, justify="left")#makes a labes that displays the output (morse code)
    output.grid(row=4, column=0, sticky=tk.W, pady=4)
    
    sound = tk.Button(master, text='Play sound', command=play_sound)# makes button to play the sound that the morse code does 
    sound.grid(row=5,column=1, sticky=tk.W, pady=4)
    

    e1 = tk.Entry(master)
    e1.grid(row=1, column=0)
    
def m_to_eng():
    global output, result, sound, e1
    output.destroy()
    try:
        sound.destroy()
    except:
        pass
    
    try:
        morse = e1.get()
    except:
        morse = to_translate
    result = ""
    
    letters = [""]
    dex = 0
    
    for i in morse:
        if i == "/":
            i = i+" "
            dex += 1
            letters.append("")
            letters[dex] = letters[dex] + " "
        elif i.isnumeric():
          messagebox.showinfo("Error", "NUMBER?¿?¿?¿!¡")
          break
        elif i == " ":
            dex += 1
            letters.append("")
        else:
            
            
            letters[dex] = letters[dex] + i

    print(letters)
    end = []

    
    for i in letters:
        new = alphabet.get(i)
        end.append(new)

    result = "".join(end)

    

    output = tk.Label(master, text=result, wraplength=200, justify="left")#makes a labes that displays the output (morse code)
    output.grid(row=4, column=0, sticky=tk.W, pady=4)

    e1 = tk.Entry(master)
    e1.grid(row=1, column=0)


        

def copy():
    pyperclip.copy(result.upper()) # coppies to clipboard

def paste():
    global e1, to_translate, pasted
    try:
        pasted.destroy()
    except:
        pass

    e1.destroy()
    pasted = tk.Label(master, text=pyperclip.paste(), wraplength=200, justify="left")#makes a labes that displays the output (morse code)
    pasted.grid(row=1, column=0, sticky=tk.W, pady=4)
    to_translate = pyperclip.paste()

def play_sound(): #plays the morse code sound
    global result, resolution
    
    if open_mouth != 0: 
        opening=open_mouth
    else: 
        opening="open.jpg"
    if closed_mouth != 0 :
        closed = closed_mouth
    else:
        closed = "close.jpg"

    try:
        master.geometry(resolution)
    except:
        messagebox.showinfo("Error", "Incorrect formating of resolution!")   
        result=0
        main()       


    
    for i in result:
        if i == ".":
            pygame.mixer.Sound.play(shorter)
            
            try:
                set_background(image=opening)
            except:
                messagebox.showinfo("Error", "No file found")
                break
            

            time.sleep(0.25)
            

        elif i == "-":
            pygame.mixer.Sound.play(longer)
            try:
                set_background(image=opening)
            except:
                messagebox.showinfo("Error", "No file found")
                break
            

            time.sleep(0.5)
        
        try:
            set_background(image=closed)
        except:
            messagebox.showinfo("Error", "No file found")
            break
        
        master.update()
        time.sleep(0.05)

    time.sleep(1)
    output.destroy()
    main()

def on_resize(event):
    # resize the background image to the size of label
    image = bgimg.resize((event.width, event.height))
    # update the image of the label
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)

def set_background(image):
    global bgimg, l, master
    bgimg = Image.open(image) # load the background image
    l = tk.Label(master)
    l.place(x=0, y=0, relwidth=1, relheight=1) # make label l to fit the parent window always
    l.bind('<Configure>', on_resize) # on_resize will be executed whenever label l is resized
    master.update()

def open_file(open_or_close):
    global open_mouth, closed_mouth, resolution
    if open_or_close == "open":
        try:
            open_output.destroy()
        except:
            pass
        
        open_mouth = fd.askopenfilename(title='select', filetypes=[("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")])
        open_output= tk.Label(settings_window, text=open_mouth, wraplength=200, justify="left")
        open_output.grid(row=0, column=1, sticky=tk.W, pady=4)
    elif open_or_close == "closed":
        try:
            closed_mouth.destroy()
        except:
            pass
        
        closed_mouth = fd.askopenfilename(title='select', filetypes=[("image", ".jpeg"), ("image", ".png"), ("image", ".jpg")])
        closed_output= tk.Label(settings_window, text=closed_mouth, wraplength=200, justify="left")
        closed_output.grid(row=1, column=1, sticky=tk.W, pady=4)
    
    elif open_or_close == "reset":
        open_mouth="open.jpg"
        closed_mouth="close.jpg"
        resolution = "300x500"

        try:
            open_output.destroy()
        except:
            pass
        try:
            closed_mouth.destroy()
        except:
            pass

def reseting():
  global open_mouth, closed_mouth
  open_mouth = 0
  closed_mouth = 0
  print(open_mouth)
  
def settings():
    global settings_window, ressa
    settings_window = tk.Toplevel(master)
    settings_window.title("Settings")
    settings_window.geometry("400x250")
    
    tk.Button(settings_window, text='Select image for open mouth', command=lambda: open_file("open")).grid(row=0, column=0, sticky=tk.W, pady=4)
    try:
        open_output= tk.Label(settings_window, text=open_mouth, wraplength=200, justify="left")
        open_output.grid(row=0, column=1, sticky=tk.W, pady=4)
    except: pass

    tk.Button(settings_window, text='Select image for closed mouth', command=lambda: open_file("closed")).grid(row=1, column=0, sticky=tk.W, pady=4)
    try:
        closed_output= tk.Label(settings_window, text=closed_mouth, wraplength=200, justify="left")
        closed_output.grid(row=1, column=1, sticky=tk.W, pady=4)
    except: pass

    tk.Label(settings_window, text="Image Resolution:", justify="left").grid(row=2,column=0, sticky=tk.W, pady=4)
    ressa = tk.Entry(settings_window, justify="left")
    ressa.grid(row=2, column=1, sticky=tk.E, pady=4, padx=0, rowspan=2)
    tk.Label(settings_window, text="(format resolution like : (X-axis)x(Y-axis)", justify="left", wraplength=200).grid(row=3,column=0, sticky=tk.W, pady=4)
    
    tk.Button(settings_window, text='Reset all settings', command=lambda: reseting()).grid(row=4, column=0, sticky=tk.W, pady=4)
    tk.Button(settings_window, text="Done", command=save_settings) .grid(row=4, column=1, sticky=tk.W, pady=4, padx=1)

def save_settings():
    global resolution
    resolution = ressa.get()
    if resolution == "":
        resolution = "300x500"
    settings_window.destroy()
    

def main():
    global output, e1, sound
    
    master.geometry("300x170")

    set_background(image="f0f0f0.png")
    
    
    e1 = tk.Entry(master)
    e1.grid(row=1, column=0)
    tk.Button(master, text='Paste from clipboard', command=paste).grid(row=1, column=1, sticky=tk.W, pady=4)


    tk.Button(master, text='To english', command=m_to_eng).grid(row=3, column=0, sticky=tk.W, pady=4) # button to run morse to english
    tk.Button(master, text='To morse code', command=eng_to_m).grid(row=3, column=1, sticky=tk.W, pady=4)# button to run english to morse

    output = tk.Label(master, text="")
    output.grid(row=4, column=0, sticky=tk.W, pady=4)
    output.destroy()

    tk.Button(master, text='Copy to clipboard', command=copy).grid(row=5, sticky=tk.W, pady=4)
    tk.Button(master, text='Settings', command=settings).grid(row=6, column=0, sticky=tk.W, pady=4)
    tk.Button(master, text="Exit", command=lambda: master.destroy()).grid(row=6, column=1, sticky=tk.W, pady=4)


main()
tk.mainloop()
