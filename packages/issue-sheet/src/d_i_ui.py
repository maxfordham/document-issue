# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 14:00:22 2018

@author: j.gunstone

:synopsis: Some simply user interface widgets to just make life a little easier.
            Often return the result.

.. note::
    Careful consideration when using these as where they are being run
    from can affect how they work...

"""

import tkinter
from tkinter import filedialog, Tk, messagebox, scrolledtext, INSERT, StringVar
from tkinter import OptionMenu, Button, mainloop, Label, LEFT, Entry, W
from PIL.ImageTk import PhotoImage
from PIL import Image, ImageTk
from constants import mf_modules_dir, FPTH_ICON


MFFONTLARGE = ("Calibri", 32) #Large Calibri Font
MFFONTSMALL = ("Calibri", 12) #Small Calibru Font

class MFTk(tkinter.Tk):
    '''Tk window with MF styling'''
    
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.config(bg = "white")
        self.iconbitmap(default=FPTH_ICON)

class MFButton(tkinter.Button):
    '''Tk Button with MF styling'''
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Button.__init__(self, master=master, cnf=cnf, **kw)
        self.config(bg="black", fg="white", font=MFFONTSMALL)

class MFLabelFrame(tkinter.LabelFrame):
    '''Tk Label Frame with MF styling'''
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.LabelFrame.__init__(self, master=master, cnf=cnf, **kw)
        self.config(bg = "white", font=MFFONTSMALL)
        
class MFCheckButton(tkinter.Checkbutton):
    '''Tk Label Frame with MF styling'''
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Checkbutton.__init__(self, master=master, cnf=cnf, **kw)
        self.config(bg = "white", font=MFFONTSMALL)
        
class MFLabel(tkinter.Label):
    '''Tk Label with MF styling'''
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Label.__init__(self, master=master, cnf=cnf, **kw)
        self.config(bg="white", font=MFFONTSMALL)
        
class MFLabelBlack(tkinter.Label):
    '''Tk Label with Black MF styling'''
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Label.__init__(self, master=master, cnf=cnf, **kw)
        self.config(bg="black", fg="white", font=MFFONTSMALL)
        
class MFHeader(tkinter.Label):
    '''Tk header with MF styling large font white text on black background'''
    def __init__(self, master=None, cnf={}, **kw):
        tkinter.Label.__init__(self, master=master, cnf=cnf, **kw)
        #img = tkinter.PhotoImage(file = str(os.path.dirname(mf_modules.__file__))+'\\'+'res\\MF_O_250px.gif')
        self.config(bg="black", fg="white", font=MFFONTLARGE)

class MFOptionMenu(tkinter.OptionMenu):
    '''Tk OptionMenu with MF styling'''
    def __init__(self, master, variable, value, *values, **kwargs):
        tkinter.OptionMenu.__init__(self, master, variable, value, *values, **kwargs)
        self.config(bg = "black", fg="white", font=MFFONTSMALL)


def start_hidden_root():
    ''' starts the Tk session with hiding the main window'''
    root = Tk()
    root.iconbitmap(default=FPTH_ICON)
    root.withdraw()

def start_root(title="MF"):
    ''' starts the Tk session without hiding the main window'''
    root = Tk()
    root.title(title)
    root.iconbitmap(default=FPTH_ICON)
    return root

def show_editable_text(text):
    ''' shows lots of text as scrollable text - useful for copying and pasting'''
    window = start_root(title="Ctrl+C to Copy; Ctrl+V to Paste")
    edit_area = scrolledtext.ScrolledText(master=window, width=50, height=10)
    edit_area.insert(INSERT, text)
    edit_area.pack()
    window.mainloop()

def getfilename(filetypes=(("All","*.*"))):
    ''' get filename from explorer and return'''
    start_hidden_root()
    infile = filedialog.askopenfilename(multiple=False)
    return infile

def getsavefilename(extension=None, initialfile=""):
    ''' get filename from explorer and return'''
    start_hidden_root()
    infile = filedialog.asksaveasfilename(defaultextension=extension, initialfile=initialfile)
    return infile

def getfoldername(initialdir=None):
    ''' get folder name from explorer and return'''
    start_hidden_root()
    infile = filedialog.askdirectory(initialdir=initialdir)
    return infile

def info_messagebox(message="Done", title="Done"):
    ''' show info OK type box '''
    start_hidden_root()
    messagebox.showinfo(title, message)

def warning_messagebox(message="Warning", title="Warning"):
    ''' display warning'''
    start_hidden_root()
    messagebox.showwarning(title, message)

def yesno_messagebox(message="Yes or No", title="Option", yesaction=None, noaction=None):
    ''' display yes no question'''
    start_hidden_root()
    if messagebox.askyesno(title, message):
        yesaction()
    else:
        noaction()

def okcancel_messagebox(message="OK or Cancel", title="Option", okaction=None, cancelaction=None):
    ''' display OK cancel question'''
    start_hidden_root()
    if messagebox.askokcancel(title, message):
        okaction()
    else:
        cancelaction()


def tkinter_choice(choices, default_val):
    '''
    define list of possible choices and a default value and
    this function create a dropdown list of the user defined
    options with a default_val pre-selected.

    .. todo:: Better do this!

    :param       choices (list): list of possible choices to choose from
    :param   default_val(?): item from the list to set as default

    :returns: choice(?): user defines variable "choice" with their selction from the dropdown menu
    '''

    def ok():
        '''function when ok is clicked'''
        global choice
        choice = var.get()
        print("choice is:", choice)
        master.destroy()
        master.quit()
        return choice

    master = start_root(title="Choices")
    master.minsize(250, 100)
    var = StringVar(master)
    var.set(default_val) # initial value
    option = OptionMenu(master, var, *choices)
    option.pack()

    button = Button(master, text="OK", command=ok)
    button.pack()
    mainloop()
    return choice

#from tkinter import *
def tkinter_label(explanation, gif_pth=None):
    '''
    flash a label box that tells the user some information. press
    ok to close.

    Args:
        explanatation (str): message to teh user
        gif_pth (dir): show image in message box
            (only GIF and PPM/PGM file types available)
    Returns:
        message box with "explanation" and "gif_pth".

    '''
    #root = Tk()
    root = start_root()
    if gif_pth != None:
        logo = PhotoImage(file=gif_pth) #https://www.python-course.eu/tkinter_labels.php
        w1 = Label(root, image=logo).pack(side="right")
    else:
        #w1 = Label(root).pack(side="right")
        print('')
    explanation = explanation
    w2 = Label(root,
               justify=LEFT,
               padx=10,
               text=explanation).pack(side="left")

    button = Button(root, text='Ok', width=25, command=root.destroy)
    button.pack()
    root.mainloop()



#from tkinter import *
#from tkinter import filedialog
def tkinter_filedialog():
    '''
    prompts user to select folder
    '''
    return getfoldername()

    #root = Tk()
    #root.filename = filedialog.askdirectory(title="Select folder")
    #root.destroy()
    #root.quit()
    #return root.filename

#from tkinter import *

def tkinter_show_img(imageFile):
    '''
    # use a Tkinter label as a panel/frame with a background image
    # note that Tkinter only reads gif and ppm images
    # use the Python Image Library (PIL) for other image formats
    # free from [url]http://www.pythonware.com/products/pil/index.htm[/url]
    # give Tkinter a namespace to avoid conflicts with PIL
    # (they both have a class named Image)

    Args:
       imageFile (dir): img dir

    Example:
        imageFile =
        tkinter_show_img(imageFile)

    '''

    #root = Tk()
    #root.title('background image')
    root = start_root(title='background image')

    # pick an image file you have .bmp  .jpg  .gif.  .png
    # load the file and covert it to a Tkinter image object
    image1 = ImageTk.PhotoImage(Image.open(imageFile))

    # get the image size
    w = image1.width()
    h = image1.height()

    # position coordinates of root 'upper left corner'
    x = 20
    y = 0

    # make the root window the size of the image
    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # root has no image argument, so use a label as a panel
    panel1 = Label(root, image=image1)
    panel1.pack(side='top', fill='both', expand='yes')

    # put a button on the image panel to test it
    button2 = Button(panel1, text='close', command=root.destroy)
    button2.pack(side='top')

    # save the panel's image from 'garbage collection'
    panel1.image = image1

    # start the event loop
    root.mainloop()


#from tkinter import *
def tkinter_user_input(title, options):
    '''
    user input menu. creates dict of user responses from
    list of questions.

    Args:
        title (str): to describe what information is being input
        options (list): a list of fields (keys) that the user needs
            to complete.

    Returns:
        dictionary (dict): dict with users inputs to the corresponding
            questions.

    Example:
        title="Input:\n reference floor (str, e.g. '01')\n\
            list of duplicate floors (list, e.g. ['02','03'])"
        options=["reference floor","list of duplicate floors"]
        tkinter_user_input(title,options)
    '''
    def show_entry_fields():
        #dictionary = dict(zip(options, vals))
        global dictionary
        v = []
        for val in vals:
            v.append(val.get())
        dictionary = dict(zip(options, v))
        return master.destroy()

    def ignore():
        #dictionary = dict(zip(options, vals))
        global dictionary
        v = []
        for val in vals:
            v.append(None)
        dictionary = dict(zip(options, v))
        return master.destroy()

    master = start_root()
    Label(master, text=title).grid(row=0, sticky=W)

    vals = []
    for n in range(0, len(options)):
        Label(master, text=options[n]).grid(row=n+1, sticky=W)
        vals.append('vals'+str(n))
    n = 0
    for n in range(0, len(vals)):
        vals[n] = Entry(master)
        vals[n].grid(row=n+1, column=1)

    Button(master, text='ignore and continue', command=ignore).grid(row=3,
                                                                    column=0,
                                                                    sticky=W,
                                                                    pady=4)
    Button(master, text='save my inputs', command=show_entry_fields).grid(row=3,
                                                                          column=1,
                                                                          sticky=W, pady=4)
    #Button(master, image=icon)
    mainloop()
    return dictionary
