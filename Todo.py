import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

list = [[("Wash the dishes"),(False)],[("Clean cups"), (False)],[("Mop floor"), (False)],[("Hang clothes"), (False)],[("Go shopping"), (False)],[("Walk Dog"), (False)]]
  
def main(stdscr):
    x = True
    stdscr.nodelay(True)
    selected = 0
    listlength = (len(list))
    stdscr.clear()

    while x == True: #Check for user inputs
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
        elif key == " " and selected != listlength:
            list[selected][1] = not list[selected][1]
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

        if selected < 0: #Keep selection within the length of the list
            selected = 0
        elif selected >= listlength:
            selected = listlength
        stdscr.clear()
        stdscr.addstr(0, 0, "Todo List", curses.A_UNDERLINE)
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
