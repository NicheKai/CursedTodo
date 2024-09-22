import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import csv
import glob

list = []

def writetolist(listname):
    with open(listname, "w", newline="") as csvfile:
        csv_write = csv.writer(csvfile)
        for chore in list:
            csv_write.writerow(chore)
        csvfile.close

def readfromlist(listname):
    with open(listname, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row[1] == "True":
                tempbool = True
            else:
                tempbool = False

            test = [str(row[0]),(tempbool)]
            list.append(test)
        csvfile.close

def removechore(choreindex):
    list.pop(choreindex)

def createlist(listname):
    temp = (listname+".csv").strip(" ")
    with open(temp, "w", newline="") as csvfile:
        csvfile.close

    
def main(stdscr):
    x = True
    stdscr.nodelay(True)
    selected = 0
    #File select menu
    files = glob.glob("*.csv")

    while x == True: #Check for user inputs
        filelen = len(files)
        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "KEY_DOWN":
            selected += 1
        elif key == "x":
            x = False
        elif key == "KEY_UP":
            selected -= 1
        elif key == " " and selected != filelen:
            pickedlist = files[selected]
            x = False
        elif key == " ":
            inp = curses.newwin(1,50, selected+2,0)
            txtb = inp.subwin(1, 25, selected+2, 24)
            inp.addstr("Please input list name:")
            tb = curses.textpad.Textbox(txtb)
            inp.refresh()
            tb.edit()
            tbout = tb.gather()
            createlist(tbout)
            files = glob.glob("*.csv")

        if selected < 0: #Keep selection within the length of the list
            selected = 0
        elif selected >= filelen:
            selected = filelen

        stdscr.clear()
        stdscr.addstr(0, 0, "Lists", curses.A_UNDERLINE)
        for i in range(filelen):
            y = i+2
            stdscr.addstr(y, 0, (str(i+1)+")"))
            if i == selected and i < filelen:
                stdscr.addstr(y, 3, files[i], curses.A_BLINK)
            elif i < filelen:
                stdscr.addstr(y, 3, files[i])
        if selected == filelen:
            stdscr.addstr(y+1, 0, "Create a new list!", curses.A_BLINK)
        else:
            stdscr.addstr(y+1, 0, "Create a new list!")
        stdscr.refresh()

    #Load the Todolist selected
    readfromlist(pickedlist)
    #Todolist Menu
    selected = 0
    listlength = (len(list))
    stdscr.clear()
    stdscr.refresh()
    if listlength == 0:
        inp = curses.newwin(1,50, selected+2,0)
        txtb = inp.subwin(1, 25, selected+2, 23)
        inp.addstr("Please input new task: ")
        tb = curses.textpad.Textbox(txtb)
        inp.refresh()
        tb.edit()
        tbout = tb.gather()
        list.append([(tbout),(False)])
        listlength = (len(list))
        selected = selected+1
        writetolist(pickedlist)
    x = True
    while x == True: #Check for user inputs
        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "KEY_DOWN":
            selected += 1
        elif key == "x":
            x = False
        elif key == "d":
            del list[selected]
            writetolist(pickedlist)
        elif key == "KEY_UP":
            selected -= 1
        elif key == " " and selected != listlength:
            list[selected][1] = not list[selected][1]
            writetolist(pickedlist)
        elif key == " " and selected == listlength:
            inp = curses.newwin(1,50, selected+2,0)
            txtb = inp.subwin(1, 25, selected+2, 22)
            inp.addstr("Please input new task:")
            tb = curses.textpad.Textbox(txtb)
            inp.refresh()
            tb.edit()
            tbout = tb.gather()
            list.append([(tbout),(False)])
            listlength = (len(list))
            selected = selected+1
            writetolist(pickedlist)
        

        if selected < 0: #Keep selection within the length of the list
            selected = 0
        elif selected >= listlength:
            selected = listlength
        stdscr.clear()
        stdscr.addstr(0, 0, pickedlist, curses.A_UNDERLINE)
        for i in range(listlength):
            y = i+2
            stdscr.addstr(y, 0, (str(i+1)+")"))
            if i == selected and i < listlength:
                stdscr.addstr(y, 3, list[i][0], curses.A_BLINK)
            elif i < listlength:
                stdscr.addstr(y, 3, list[i][0])
            if list[i][1] == True:
                stdscr.addstr(y, 28, "[X]")
            else:
                stdscr.addstr(y, 28, "[ ]")
        if selected == listlength:
            stdscr.addstr(y+1, 0, "Add new item!", curses.A_BLINK)
        else:
            stdscr.addstr(y+1, 0, "Add new item!")
        stdscr.refresh()


wrapper(main)
