# noinspection PyBroadException

import operator
import subprocess
import sys
import webbrowser

try:
    import cv2
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'opencv-python'])
finally:
    import cv2
import glob
import os
import shutil
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.ttk import *
from configparser import ConfigParser
from send2trash import send2trash

try:
    from PIL import Image, ImageTk, GifImagePlugin
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pillow'])
finally:
    from PIL import Image, ImageTk, GifImagePlugin
import pathlib

os.chdir(pathlib.Path(__file__).parent.absolute())
if os.path.isfile('./config.ini'):
    config_object = ConfigParser()
    config_object.read("config.ini")
    mmvselect = config_object["Display_gif_warning"]
    smvselect = config_object["Suppression_method"]
    umvselect = config_object["Update_method"]
    wmvselect = config_object["Weight_display_methd"]
    mmv = mmvselect["select"]
    smv = smvselect["select"]
    umv = umvselect["select"]
    wmv = wmvselect["select"]
    if mmvselect["boolean"] == "True":
        GifWarningSt = True
    elif mmvselect["boolean"] == "Falce" or mmvselect["boolean"] == "()":
        GifWarningSt = False
    cfgpathdefault = config_object["Pathcfg"]
    if cfgpathdefault["default_maine"] == "NON":
        defaultpath = ""
    else:
        defaultpath = cfgpathdefault["default_maine"]
    if cfgpathdefault["default_create"] == "NON":
        folder_creation_path = ""
    else:
        folder_creation_path = cfgpathdefault["default_create"]
else:
    line1 = "[Pathcfg]\ndefault_maine = NON\ndefault_create = NON\n\n[Display_gif_warning]\nboolean = True\n"
    line2 = "select = 1\n\n[Suppression_method]\nselect = 1\n\n[Update_method]\nselect = 1\n\n[Weight_display"
    line3 = "_methd]\nselect = 1"
    with open('config.ini', 'w+') as out:
        out.writelines([line1, line2, line3])
    mmv = 1
    smv = 1
    umv = 1
    wmv = 1
    GifWarningSt = True
    defaultpath = ""
    folder_creation_path = ""

actual_version = '[beta] 3.8.2'

pixels_x, pixels_y, x, scm, ind, bk, focus = 0, 0, 0, 0, 0, 0, 0
ds = 1
infile, img, ButtonNext, ButtonBack, ButtonDelete, ButtonMove1, ButtonMove2, lb1, lb2, lb3, lb4, lb5, lb6, lb7, lb8 = \
    "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x "
global_state = True
gif_animation = True
file = []
ButtonLoad, lb3state = "x", "x"
previous_focus = "x"
wdm = 1
focus_go = True

# ---------------------------- | SETTINGS | ------------------------
int(mmv)
int(smv)
int(umv)
int(wmv)
if umv == "2" or umv == 1:
    if not os.path.isdir('./Download'):
        os.mkdir("./Download")
    import urllib.request

    url = "https://raw.githubusercontent.com/overline090/MediaFileter/master/ver.inf"
    headers = urllib.request.urlretrieve(url, filename="./Download/ver.inf")
    verinfonew = open("./Download/ver.inf")
    verinfordnew = verinfonew.readline(12)
    if verinfordnew != actual_version:
        print("ok")
        verinfonew.close()
        new_ver = True
        if umv == "2":
            url_update = "https://raw.githubusercontent.com/overline090/MediaFileter/master/update/update.ini"
            urllib.request.urlretrieve(url_update, filename="./Download/update.inf")
            update_ini = ConfigParser()
            update_ini.read("./Download/update.inf")
            update_info = update_ini["Update_info"]
            update_link = update_ini["Update_link"]
            link_amount = update_info["link_amount"]
            maine_name = update_info["maine_name"]
            int(link_amount)
            os.chdir('./Download')
            for link in link_amount:
                if not link == 0:
                    update_url = update_link[str("url") + link]
                    urllib.request.urlretrieve(update_url, filename=maine_name)
            for x in glob.iglob('*.*', recursive=True):
                print(x)
                shutil.move(x, '../'+x)
            os.chdir("../")
            exec(open(maine_name).read())
            #shutil.rmtree("./Download")
            exit()
    else:
        verinfonew.close()
        shutil.rmtree("./Download")
        new_ver = False
if umv == 2:
    umv = 3
if umv == 3:
    pass


def value_on_off(boolvar):
    if boolvar:
        return "ON"
    else:
        return "OFF"


class maine:
    def __init__(self, master):
        global x
        global focus, defaultpath, GifWarningSt
        myvar = IntVar()
        myvar.set(mmv)
        supprmethodvar = IntVar()
        supprmethodvar.set(smv)
        updatemethodevar = IntVar()
        updatemethodevar.set(umv)
        wheightdisplaymethod = IntVar()
        wheightdisplaymethod.set(wmv)

        def image():
            global infile, lb8, gif_animation, pixels_tot, image_r, extension, pixels_x, GifWarningSt, pixels_y,\
                x, img, ds, f1t, f2t, f2t, f3t, f4t, f5t, f6t, f7t, f8t, f9t, ButtonNext, ButtonBack, ButtonDelete,\
                ButtonMove1, ButtonMove2, lb1, lb2, lb3, lb4, lb5, lb6, lb7, lb8, lb3state, nip, global_state, lberror,\
                ind, bk, wdm
            lberror = ttk.Label(root, text="ERROR use keyboard arrow")
            lberror.place(anchor="center", x=960, y=540)
            if ds == 0:
                img.destroy()
                try:
                    ButtonMove1.destroy()
                    ButtonMove2.destroy()
                    ButtonBack.destroy()
                    ButtonNext.destroy()
                    ButtonDelete.destroy()
                except:
                    pass
                try:
                    lb1.destroy()
                except:
                    pass
                lb3.destroy()
                lb4.destroy()
                lb6.destroy()
                lb7.destroy()
                lb3state.destroy()
                try:
                    lb8.destroy()
                except:
                    pass
            if x == len(file):
                x = 0
            if x == -len(file):
                x = 0
            zoom = 0.5

            try:
                load = Image.open(file[x])
            except:
                load = "ERROR"
            if len(file) == 0:
                load = "FINISH"
            if load != "FINISH" and load != "ERROR":
                pixels_x, pixels_y = tuple([int(zoom * x) for x in load.size])
                pixels_tot = pixels_x * pixels_y
                image_r = math.sqrt((pixels_x ** 2) + (pixels_y ** 2))
                if pixels_x < 860:
                    pixels_x = pixels_x * 2
                    pixels_y = pixels_y * 2
                if pixels_y < 490:
                    pixels_x = pixels_x * 2
                    pixels_y = pixels_y * 2
                if pixels_x > 1800:
                    pixels_x = pixels_x // 2
                    pixels_y = pixels_y // 2
                if pixels_y > 980:
                    pixels_x = pixels_x // 2
                    pixels_y = pixels_y // 2
                if pixels_x > 1920:
                    pixels_x = pixels_x // 3
                    pixels_y = pixels_y // 3
                if pixels_y > 1080:
                    pixels_x = pixels_x // 3
                    pixels_y = pixels_y // 3
                extension = os.path.splitext(file[x])[1][1:]
            self.master = master
            self.master.geometry("1920x1080")
            self.frame = ttk.Frame(self.master)
            mvt = "move to "
            f1txt = str(mvt) + f1t
            f2txt = str(mvt) + f2t
            if global_state:
                ButtonBack = ttk.Button(root, text="back", command=back_f)
                ButtonBack.place(x=0, y=1080 - 55, width=70, height=55)
                ButtonNext = ttk.Button(root, text="next", command=next_f)
                ButtonNext.place(anchor="ne", x=1920, y=1080 - 55, width=70, height=55)
                ButtonDelete = ttk.Button(root, text="delet file", command=delete)
                ButtonDelete.place(x=70, y=1080 - 55, width=70, height=55)
                ButtonMove1 = ttk.Button(root, text=f1txt, command=move1)
                ButtonMove1.place(x=0, y=1080 - 110, height=55)
                ButtonMove2 = ttk.Button(root, text=f2txt, command=move2)
                ButtonMove2.place(anchor="ne", x=1920, y=1080 - 110, height=55)
            if load != "FINISH" and load != "ERROR":
                lb1 = ttk.Label(root, text=file[x])
                lb1.pack()
            NumberOfInList: int = len(file)
            strNumberOfInList: str = str(NumberOfInList)
            lb3text = str("amount of remaining images: ") + strNumberOfInList
            lb3 = ttk.Label(root, text=lb3text)
            lb3.place(x=0, y=0)
            lb3state = ttk.Progressbar(root, orient="horizontal",
                                       length=100, mode="determinate")
            lb3state.place(x=0, y=22)
            if load != "FINISH" and load != "ERROR":
                lb3state["maximum"] = nip
                lb3state["value"] = nip - NumberOfInList
            else:
                lb3state["maximum"] = 100
                lb3state["value"] = 100
            if load != "FINISH":
                try:
                    nipp = 100 * float(nip - NumberOfInList) / float(nip)
                    nippr = ("{0:.2f}".format(nipp))
                except:
                    nippr = 0
            else:
                nippr = 100.0
            lb3pertext = str(nippr) + "%"
            lb3percent = ttk.Label(root, text=lb3pertext)
            lb3percent.place(x=110, y=22)
            ActualPosition = str(x + 1)
            lb4text = str("actual image in list: ") + ActualPosition
            lb4 = ttk.Label(root, text=lb4text)
            lb4.place(x=0, y=44)
            if load != "FINISH" and load != "ERROR":
                pixels_totstr = str(pixels_tot)
                lb6text = str("total pixels: ") + pixels_totstr
            else:
                lb6text = ""
            lb6 = ttk.Label(root, text=lb6text)
            lb6.place(anchor="ne", x=1920, y=0)
            if load != "FINISH" and load != "ERROR":
                image_r = ("{:.0f}p".format(image_r))
                lb7text = str("resolution: ") + str(image_r)
            else:
                lb7text = ""
            lb7 = ttk.Label(root, text=lb7text)
            lb7.place(anchor="ne", x=1920, y=22)
            if load != "FINISH" and load != "ERROR":
                sizebyte = os.stat(file[x]).st_size
                if wdm == 1:
                    def convert_bytesIES(num):
                        """
                        this function will convert bytes to MB.... GB... etc
                        """
                        for unit in ['bytes', 'Ko', 'Mo', 'Go', 'To']:
                            if num < 1000.0:
                                return f'{num}{unit}' if unit == 'bytes' else f'{num:.2f}{unit}'
                            num /= 1000.0

                    lb8text = convert_bytesIES(sizebyte)
                else:
                    def convert_bytes(num):
                        """
                        this function will convert bytes to MB.... GB... etc
                        """
                        for unit in ['bytes', 'Ko', 'Mo', 'Go', 'To']:
                            if num < 1024.0:
                                return f'{num}{unit}' if unit == 'bytes' else f'{num:.2f}{unit}'
                            num /= 1024.0

                    lb8text = convert_bytes(sizebyte)
            else:
                lb8text = ""
            lb8 = ttk.Label(root, text=lb8text)
            lb8.place(anchor="ne", x=1920, y=44)

            ds = 0
            # --------------------------------------------------------------------------------------------- probleme /!/
            if not gif_animation:
                extension = "DISABLED"
            if load != "FINISH" and load != "ERROR":
                if extension == "gif":
                    gif = file[x]
                    imageObject = load
                    imgframe = imageObject.n_frames
                    frames = []

                    def gifinit(gif_init):
                        frames.append(PhotoImage(file=gif, format='gif -index %i' % gif_init))
                        gif_init += 1
                        if gif_init == imgframe:
                            frame_update(0)
                        img.after(0, gif_init, gif_init)

                    def frame_update(update_ind):
                        update_ind += 1
                        if update_ind == imgframe:
                            update_ind = 0
                        img.configure(image=frames[update_ind])
                        img.after(50, frame_update, update_ind)

                    imgtext = "amount of frame: " + str(imgframe)
                    img = Label(root, text=imgtext, compound=TOP)
                    img.place(anchor="center", x=960, y=540)
                    img.after(0, gifinit(0), 0)
                else:
                    render = ImageTk.PhotoImage(load.resize((pixels_x, pixels_y)))
                    img = ttk.Label(image=render)
                    img.image = render
                    img.place(anchor="center", x=960, y=540)
            else:
                if load == "FINISH":
                    img = ttk.Label(text=load)
                    img.place(anchor="center", x=960, y=540, width=230, height=50)
                elif load == "ERROR":
                    img = ttk.Label(text="ERROR: " + str(file[x]))
                    img.place(anchor="center", x=960, y=540, width=230, height=50)

            # ----------------------------------------------------------- probleme /!/   inf: unbreak loop curing change
            def key_pressed(event):
                global x, global_state
                key = event.keysym
                if key == "Left":
                    if x > 0:
                        x = x - 1
                    image()
                if key == "Right":
                    if x < nip - 1:
                        x = x + 1
                    else:
                        x = x
                    image()
                if key == "Up":
                    x = NumberOfInList - 1
                    image()
                if key == "Down":
                    x = 0
                    image()
                if key == "1":
                    if f1t != "":
                        new = str(f1t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "2":
                    if f2t != "":
                        new = str(f2t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "3":
                    if f3t != "":
                        new = str(f3t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "4":
                    if f4t != "":
                        new = str(f4t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "5":
                    if f5t != "":
                        new = str(f5t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "6":
                    if f6t != "":
                        new = str(f6t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "7":
                    if f7t != "":
                        new = str(f7t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "8":
                    if f8t != "":
                        new = str(f8t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "9":
                    if f3t != "":
                        new = str(f9t) + "/" + (file[x])
                        shutil.move(file[x], new)
                        file.remove(file[x])
                        if x == len(file):
                            x -= 1
                        else:
                            x = x
                        image()
                if key == "Return":
                    if supprmethodvar == 1:
                        os.remove(file[x])
                    else:
                        send2trash(file[x])
                    file.remove(file[x])
                    if x == len(file):
                        x -= 1
                    else:
                        x = x
                    image()
                if key == "F5":
                    pa2f()
                if key == "Delete":
                    global_state = operator.not_(global_state)
                    image()

            root.bind("<Key>", key_pressed)

        def back_f():
            global x
            x = x - 1
            image()

        def next_f():
            global x
            x = x + 1
            image()

        def delete():
            global x
            if supprmethodvar == 1:
                os.remove(file[x])
            else:
                send2trash(file[x])
            file.remove(file[x])
            x = x
            image()

        def move1():
            global x
            if f1t != "":
                new = str(f1t) + "/" + (file[x])
                shutil.move(file[x], new)
                file.remove(file[x])
                x = x
                image()

        def move2():
            global x
            if f2t != "":
                new = str(f2t) + "/" + (file[x])
                shutil.move(file[x], new)
                file.remove(file[x])
                x = x
                image()

        def pa2f():
            global nip, x
            file.clear()
            for in_file in glob.glob('*.jpeg'):
                file.append(in_file)
            for in_file in glob.glob('*.jpg'):
                file.append(in_file)
            for in_file in glob.glob('*.tiff'):
                file.append(in_file)
            for in_file in glob.glob('*.bmp'):
                file.append(in_file)
            for in_file in glob.glob('*.png'):
                file.append(in_file)
            for in_file in glob.glob('*.webp'):
                file.append(in_file)
            for in_file in glob.glob('*.svg'):
                file.append(in_file)
            for in_file in glob.glob('*.gif'):
                file.append(in_file)
            file.sort()
            nip = len(file)
            x = 0
            image()

        def pa2():
            global f1, f2, f3, f4, f5, f6, f7, f8, f9, lb6, ButtonLoad, nip, infile, pixels_x, pixels_y, focus
            if gfc.state() == ():
                gif_scan = False
            else:
                gif_scan = True
            gfc.destroy()
            x = -1
            lbmaine.destroy()
            butnext.destroy()
            folderselect.destroy()
            localget = localp.get()
            if localget != "":
                os.chdir(localget)
            else:
                os.chdir(pathlib.Path(__file__).parent.absolute())
            localp.destroy()
            pre_folder = next(os.walk("./"))[1]
            for infile in glob.glob('*.jpeg'):
                file.append(infile)
            for infile in glob.glob('*.jpg'):
                file.append(infile)
            for infile in glob.glob('*.tiff'):
                file.append(infile)
            for infile in glob.glob('*.bmp'):
                file.append(infile)
            for infile in glob.glob('*.png'):
                file.append(infile)
            for infile in glob.glob('*.webp'):
                file.append(infile)
            for infile in glob.glob('*.svg'):
                file.append(infile)
            if gif_scan:
                for infile in glob.glob('*.gif'):
                    file.append(infile)
            file.sort()
            self.master = master
            self.master.geometry("250x300")
            self.frame = ttk.Frame(self.master)
            nip = len(file)
            nil = str(nip)
            lb6text = str("amount of image: ") + nil
            lb6 = ttk.Label(root, text=lb6text)
            lb6.pack()
            ButtonLoad = ttk.Button(root, text="load", command=fpi)
            ButtonLoad.pack()
            f1 = Entry(root, takefocus=0)
            f1.pack()
            f2 = Entry(root, takefocus=0)
            f2.pack()
            f3 = Entry(root, takefocus=0)
            f3.pack()
            f4 = Entry(root, takefocus=0)
            f4.pack()
            f5 = Entry(root, takefocus=0)
            f5.pack()
            f6 = Entry(root, takefocus=0)
            f6.pack()
            f7 = Entry(root, takefocus=0)
            f7.pack()
            f8 = Entry(root, takefocus=0)
            f8.pack()
            f9 = Entry(root, takefocus=0)
            f9.pack()
            possiblefocus = [f1, f2, f3, f4, f5, f6, f7, f8, f9]
            possiblefocus_get = [".!entry2", ".!entry3", ".!entry4", ".!entry5", ".!entry6", ".!entry7", ".!entry8",
                                 ".!entry9", ".!entry10"]
            ttk.Entry.focus(possiblefocus[focus])

            def key_pressedMaine2(event):
                global focus, x, previous_focus
                key = event.keysym
                focus = possiblefocus_get.index(str(root.focus_get()))
                if key == "Up":
                    if focus != 0:
                        focus -= 1
                    ttk.Entry.focus(possiblefocus[focus])
                if key == "Down":
                    if focus != 8:
                        focus += 1
                    ttk.Entry.focus(possiblefocus[focus])
                if key == "Left":
                    if previous_focus != focus:
                        x = -1
                    if x > 0:
                        x -= 1
                        possiblefocus[focus].delete(first=0, last=100)
                        possiblefocus[focus].insert(0, pre_folder[x])
                        previous_focus = focus
                if key == "Right":
                    if previous_focus != focus:
                        x = -1
                    if x < len(pre_folder) - 1:
                        x += 1
                        possiblefocus[focus].delete(first=0, last=100)
                        possiblefocus[focus].insert(0, pre_folder[x])
                        previous_focus = focus
                if key == "Return":
                    fpi()

            root.bind("<Key>", key_pressedMaine2)

        def folder_path_def(insert):
            global focus_go
            focus_go = False
            folder_path = filedialog.askdirectory()
            insert.delete(0, END)
            insert.insert(0, folder_path)
            focus_go = True

        def fpi():
            global f1t, f2t, f3t, f4t, f5t, f6t, f7t, f8t, f9t
            global f1, f2, f3, f4, f5, f6, f7, f8, f9, lb6, ButtonLoad, x, folder_creation_path
            x = 0
            f1t = f1.get()
            f2t = f2.get()
            f3t = f3.get()
            f4t = f4.get()
            f5t = f5.get()
            f6t = f6.get()
            f7t = f7.get()
            f8t = f8.get()
            f9t = f9.get()
            if folder_creation_path != "":
                os.chdir(folder_creation_path)
            if f1t != "":
                if not os.path.isdir(f1t):
                    os.mkdir(f1t)
            if f2t != "":
                if not os.path.isdir(f2t):
                    os.mkdir(f2t)
            if f3t != "":
                if not os.path.isdir(f3t):
                    os.mkdir(f3t)
            if f4t != "":
                if not os.path.isdir(f4t):
                    os.mkdir(f4t)
            if f5t != "":
                if not os.path.isdir(f5t):
                    os.mkdir(f5t)
            if f6t != "":
                if not os.path.isdir(f6t):
                    os.mkdir(f6t)
            if f7t != "":
                if not os.path.isdir(f7t):
                    os.mkdir(f7t)
            if f8t != "":
                if not os.path.isdir(f8t):
                    os.mkdir(f8t)
            if f9t != "":
                if not os.path.isdir(f9t):
                    os.mkdir(f9t)
            ButtonLoad.destroy()
            f1.destroy()
            f2.destroy()
            f3.destroy()
            f4.destroy()
            f5.destroy()
            f6.destroy()
            f7.destroy()
            f8.destroy()
            f9.destroy()
            lb6.destroy()
            settings.destroy()
            image()

        self.master = master
        self.master.geometry("300x300")
        lbmaine = ttk.Label(root, text="type the folder containing the images or fil empty (default)")
        lbmaine.pack()
        localp = Entry(root, takefocus=0, width='50')
        localp.pack()

        def gfcmessage():
            if gfc.state() == ('active', 'focus', 'selected', 'hover'):
                msgwindow = Toplevel(master)
                msgwindow.title("warning")
                msgwindow.iconbitmap('src/attention.ico')
                msgwindow.geometry("300x100")

                def focuskeep():
                    msgwindow.focus_force()
                    msgwindow.after(1, focuskeep)

                gfc.state(['!selected'])

                def gfcaprove():
                    global gif_animation
                    gif_animation = True
                    gfc.state(['selected'])
                    root.focus()
                    msgwindow.destroy()

                def gfcunaprove():
                    root.focus()
                    msgwindow.destroy()

                def gfcdisablegifanim():
                    global gif_animation
                    gif_animation = False
                    root.focus()
                    gfc.state(['selected'])
                    msgwindow.destroy()

                Label(msgwindow,
                      text="ACTIVATING GIF CAN CAUSE LAG OR CRASH \n           ar you sur you want to continue?",
                      foreground="red", font="Arial 10").pack()
                Button(msgwindow, text="no", command=gfcunaprove).place(anchor="sw", x=0, y=100)
                Button(msgwindow, text="disable gif animation", command=gfcdisablegifanim).place(anchor="s", x=150,
                                                                                                 y=100)
                Button(msgwindow, text="yes", command=gfcaprove).place(anchor="se", x=300, y=100)

                def key_pressedMaine3(event):
                    key = event.keysym
                    if key == "Return":
                        gfcaprove()
                    if key == "BackSpace":
                        gfcunaprove()

                msgwindow.bind("<Key>", key_pressedMaine3)
                msgwindow.after(1, focuskeep)

        def settings_page():
            global GifWarningSt, defaultpathmmv, folder_creation_path, defaultpath
            settingwindow = Toplevel(master)
            settingwindow.title("setting")
            settingwindow.iconbitmap('src/Pelfusion-Long-Shadow-Media-Settings.ico')
            settingwindow.geometry("300x500")
            settingwindow.focus_force()
            gfc.state(['disabled'])
            folderselect.state(['disabled'])
            butnext.state(['disabled'])
            localp.state(['disabled'])
            settings.state(['disabled'])
            try:
                lbnewver.state(['disabled'])
            except:
                pass

            def focuskeepsetting_page():
                supprmethodvar.set(supprmethodvar.get())
                updatemethodevar.set(updatemethodevar.get())
                if focus_go:
                    settingwindow.focus_force()
                settingwindow.after(1, focuskeepsetting_page)

            Label(settingwindow, text="Display gif warning message").grid(row=0, column=0, sticky="W")

            def on_closing():
                global wdm
                gfc.state(['!disabled'])
                folderselect.state(['!disabled'])
                butnext.state(['!disabled'])
                localp.state(['!disabled'])
                settings.state(['!disabled'])
                try:
                    lbnewver.state(['!disabled'])
                except:
                    pass
                global defaultpath
                defaultpath = defaultpathentry.get()
                if not GifWarningSt:
                    mmvselect["boolean"] = "False"
                    if myvar.get() == 1:
                        global gif_animation
                        gif_animation = True
                        gfc.state(['selected'])
                        gfc.state(['disabled'])
                    elif myvar.get() == 2:
                        gfc.state(['!selected'])
                        gfc.state(['disabled'])
                    elif myvar.get() == 3:
                        gif_animation = False
                        gfc.state(['selected'])
                        gfc.state(['disabled'])
                else:
                    mmvselect["boolean"] = "True"
                if defaultpathentry.get() != "":
                    localp.delete(0, END)
                    localp.insert(0, defaultpathentry.get())
                    cfgpathdefault["default_maine"] = defaultpathentry.get()
                if FolderCreationPath.get() != "":
                    global folder_creation_path
                    folder_creation_path = FolderCreationPath.get()
                    cfgpathdefault["default_create"] = FolderCreationPath.get()
                wdm = wheightdisplaymethod.get()

                mmvselect["select"] = str(myvar.get())
                smvselect["select"] = str(supprmethodvar.get())
                umvselect["select"] = str(updatemethodevar.get())
                wmvselect["select"] = str(wheightdisplaymethod.get())

                with open('config.ini', 'w') as conf:
                    config_object.write(conf)

                settingwindow.destroy()

            settingwindow.protocol("WM_DELETE_WINDOW", on_closing)

            def GifWarningCommand():
                global GifWarningSt
                GifWarningSt = not GifWarningSt
                GifWarning.configure(text=value_on_off(GifWarningSt))
                if GifWarningSt:
                    GifMethod1.state(['disabled'])
                    GifMethod2.state(['disabled'])
                    GifMethod3.state(['disabled'])
                else:
                    GifMethod1.state(['!disabled'])
                    GifMethod2.state(['!disabled'])
                    GifMethod3.state(['!disabled'])
                    myvar.set(myvar.get())

            GifWarningText = value_on_off(GifWarningSt)
            GifWarning = Button(settingwindow, text=GifWarningText, command=GifWarningCommand)
            GifWarning.grid(row=0, column=1, sticky="W")

            GifMethod1 = ttk.Radiobutton(settingwindow, text="always on", variable=myvar, value=1)
            GifMethod1.grid(row=1, column=0, sticky="W")
            GifMethod2 = ttk.Radiobutton(settingwindow, text="always off", variable=myvar, value=2)
            GifMethod2.grid(row=2, column=0, sticky="W")
            GifMethod3 = ttk.Radiobutton(settingwindow, text="not animated", variable=myvar, value=3)
            GifMethod3.grid(row=3, column=0, sticky="W")

            if GifWarningSt:
                GifMethod1.state(['disabled'])
                GifMethod2.state(['disabled'])
                GifMethod3.state(['disabled'])
            else:
                GifMethod1.state(['!disabled'])
                GifMethod2.state(['!disabled'])
                GifMethod3.state(['!disabled'])

            Label(settingwindow, text="default path (fill empty for none):").grid(row=4, column=0, sticky="W")
            defaultpathentry = ttk.Entry(settingwindow, takefocus=0, width='30')
            defaultpathentry.grid(row=5, column=0, sticky="W")
            Button(settingwindow, text="select folder", command=lambda: folder_path_def(insert=defaultpathentry)) \
                .grid(row=5, column=1, sticky="W")
            Label(settingwindow, text="path where the folder will be created\n (fill empty for default):") \
                .grid(row=6, column=0, sticky="W")
            FolderCreationPath = Entry(settingwindow, takefocus=0, width='30')
            FolderCreationPath.grid(row=7, column=0, sticky="W")
            Button(settingwindow, text="select folder", command=lambda: folder_path_def(insert=FolderCreationPath)) \
                .grid(row=7, column=1, sticky="W")
            Label(settingwindow, text="suppression method:").grid(row=8, column=0, sticky="W")
            SupprMethod1 = ttk.Radiobutton(settingwindow, text="instant delete", variable=supprmethodvar, value=1)
            SupprMethod1.grid(row=9, column=0, sticky="W")
            SupprMethod2 = ttk.Radiobutton(settingwindow, text="move to trash", variable=supprmethodvar, value=2)
            SupprMethod2.grid(row=10, column=0, sticky="W")
            Label(settingwindow, text="update method").grid(row=11, column=0, sticky="W")
            UpdateMhetode1 = Radiobutton(settingwindow, text="check for update", variable=updatemethodevar, value=1)
            UpdateMhetode1.grid(row=12, column=0, sticky="W")
            UpdateMhetode2 = Radiobutton(settingwindow, text="auto update", variable=updatemethodevar, value=2)
            UpdateMhetode2.grid(row=13, column=0, sticky="W")
            UpdateMhetode3 = Radiobutton(settingwindow, text="do not check for update", variable=updatemethodevar,
                                         value=3)
            UpdateMhetode3.grid(row=14, column=0, sticky="W")
            Label(settingwindow, text="file weight display method").grid(row=15, column=0, sticky="W")
            wheightdisplaym1 = Radiobutton(settingwindow, text="standard IEC", variable=wheightdisplaymethod, value=1)
            wheightdisplaym1.grid(row=16, column=0, sticky="W")
            wheightdisplaym2 = Radiobutton(settingwindow, text="notation before 1998 (used by windows)",
                                           variable=wheightdisplaymethod, value=2)
            wheightdisplaym2.grid(row=17, column=0, sticky="W")
            defaultpathentry.insert(0, defaultpath)
            FolderCreationPath.insert(0, folder_creation_path)

            settingwindow.after(1, focuskeepsetting_page)

        # -----------------------------------------------------------------------maine page
        gfc = Checkbutton(root, text='enable gif', command=gfcmessage)
        gfc.pack()
        gfc.state(['!alternate'])
        folderselect = ttk.Button(root, text="selct flolder", command=lambda: folder_path_def(insert=localp))
        folderselect.pack()
        ttk.Entry.focus(localp)
        butnext = ttk.Button(root, text="next", command=pa2)
        butnext.pack()
        os.chdir(pathlib.Path(__file__).parent.absolute())
        settingimg = Image.open('src/Settings-icon.png')
        self.settingicon = ImageTk.PhotoImage(settingimg)
        global defaultpath
        if defaultpath != "":
            localp.delete(0, END)
            localp.insert(0, defaultpath)

        if umv == "1":
            if new_ver:
                def webopen():
                    webbrowser.open_new_tab('https://github.com/overline090/MediaFileter')

                lbnewver = Button(root, text="new version detected: " + str(verinfordnew), command=webopen)
                lbnewver.pack(side=BOTTOM)
                settings = Button(root, text="settings", image=self.settingicon, compound=LEFT,
                                  padding="-100,-100,-100,-100", command=settings_page)
                settings.pack(side=BOTTOM)
            else:
                settings = Button(root, text="settings", image=self.settingicon, compound=LEFT,
                                  padding="-100,-100,-100,-100", command=settings_page)
                settings.pack(side=BOTTOM)
                pass
        else:
            settings = Button(root, text="settings", image=self.settingicon, compound=LEFT,
                              padding="-100,-100,-100,-100", command=settings_page)
            settings.pack(side=BOTTOM)

        if not GifWarningSt:
            if myvar.get() == 1:
                global gif_animation
                gif_animation = True
                gfc.state(['selected'])
                gfc.state(['disabled'])
            elif myvar.get() == 2:
                gfc.state(['!selected'])
                gfc.state(['disabled'])
            elif myvar.get() == 3:
                gif_animation = False
                gfc.state(['selected'])
                gfc.state(['disabled'])

        def key_pressedMaine(event):
            key = event.keysym
            if key == "Return":
                pa2()
            if key == "Control_R":
                folder_path_def(localp)

        root.bind("<Key>", key_pressedMaine)


root = Tk()
app = maine(root)
root.attributes("-fullscreen", False)
root.bind("<Tab>", lambda event: root.attributes("-fullscreen",
                                                 not root.attributes("-fullscreen")))
root.bind("<twosuperior>", lambda event: root.wm_iconify())
root.bind("<Escape>", lambda event: root.destroy())
root.title("media hopper")
root.mainloop()
