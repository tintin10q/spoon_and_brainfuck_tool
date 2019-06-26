import re
import threading
from tkinter import filedialog
from tkinter import *
import sys
import io
# Brainfuck Interpreter
# Copyright 2011 Sebastian Kaspari
#
# Usage: ./bf.py [FILE]

import sys
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()

def evaluate(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": sys.stdout.write(chr(cells[cellptr]))
    if command == ",": cells[cellptr] = ord(getch())
      
    codeptr += 1


def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap


def main():
  if len(sys.argv) == 2: execute(sys.argv[1])
  else: print("Usage:", sys.argv[0], "filename")


def remove_spaces_and_newlines(spoon):
    """Code without spaces and new lines"""
    spoon = spoon.replace(" ","").replace("\n","")
    return spoon

def regex_spoon(spoon):
    """Returns regex object of spoon"""
    regex = r"(1)|(000)|(010)|(011)|(00100)|(0011)|(001010)|(0010110)"
    matches = re.finditer(regex, spoon)
    return matches


def get_split_up_spoon(matches):
    """Split up spoon code"""
    split_up_spoon = ""
    for match in matches:
        group = match.group()
        split_up_spoon += "{} ".format(group)
    return split_up_spoon


def translate_to_brain_fuck(matches):
    """Turns the spoon code into brainfuck code"""

    brainfuck_code = ""
    brainfuck_lib = {
        "1": "+",
        "000": "-",
        "010": ">",
        "011": "<",
        "00100": "[",
        "0011": "]",
        "001010": ".",
        "0010110": ","
    }
    for match in matches:
        group = match.group()
        brainfuck_code += "{} ".format(brainfuck_lib[group])

    return brainfuck_code

def execute_brainfuck(brainfuck_code):
    """Tries to execute brainfuck code"""
    return evaluate(brainfuck_code)

def exit_gui():
    root.quit()




def insert(string_input,text, newline=True, error=False,scroll=True):  # to get text to output field
    string_input = str(string_input)
    if error == True:
        text.insert(END, "** ")
        text.insert(END, string_input.upper())
        text.insert(END, " **")
    if error == False:
        text.insert(END, string_input)
    if newline == True:
        text.insert(END, "\n")
    if scroll:
        text.see(END)
    return

def open_file():
    threading.Thread(target=open_file_tread).start()
    return

def open_file_tread():

    filename = filedialog.askopenfilename(initialdir="/", title="Select file with spoon code",
                                          filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
    spoon = open(filename,"r+").read()
    threading.Thread(target=translate_all,args=(spoon,)).start()
    return

def start_translation_from_button():
    spoon = split_up_spoon_message.get("1.0",END)
    threading.Thread(target=translate_all, args=(spoon,)).start()

def translate_all(spoon):
    clear_text()
    spoon = remove_spaces_and_newlines(spoon)

    insert(spoon,spoon_import_message)

    matches = regex_spoon(spoon)
    matches2 = regex_spoon(spoon)

    split_up_spoon = get_split_up_spoon(matches)
    insert(split_up_spoon,split_up_spoon_message)

    brainfuck_text = translate_to_brain_fuck(matches2)

    insert(brainfuck_text,brainfuck_message)

    # Start bs
    old_stdout = sys.stdout  # Memorize the default stdout stream
    sys.stdout = buffer = io.StringIO()

    evaluate(brainfuck_text)

    sys.stdout = old_stdout  # Put the old stream back in place

    whatWasPrinted = buffer.getvalue()  # Return a str containing the entire contents of the buffer.

    executed_brainfuck_code = whatWasPrinted
    insert(executed_brainfuck_code, execute_brainfuck_message)



def run_brain_fuck():
    threading.Thread(target=run_brain_fuck_tread).start()

def run_brain_fuck_tread():
    execute_brainfuck_message.delete("1.0",END)
    brainfuck_code_from_text = brainfuck_message.get("1.0",END)


    old_stdout = sys.stdout  # Memorize the default stdout stream
    sys.stdout = buffer = io.StringIO()

    evaluate(brainfuck_code_from_text)

    sys.stdout = old_stdout  # Put the old stream back in place

    whatWasPrinted = buffer.getvalue()  # Return a str containing the entire contents of the buffer.

    executed_brainfuck_code = whatWasPrinted
    insert(executed_brainfuck_code,execute_brainfuck_message)






background_color = "#23272A"
button_background = "#395a72"
outline_color= "#2C2F33"
fg_color = "white"

root = Tk()
root.title("Spoon helper by Quinten")
root.config(bg=background_color)


Button(text="Click to open file",command=open_file,bg=button_background,fg=fg_color,font="Helvetica 10",pady=10).pack()

# Code to add widgets will go here...
Label(root,text="Imported spoon",relief="groove",bg=button_background,fg=fg_color,font="Helvetica 10").pack()
spoon_import_message = Text(root,relief=SUNKEN,height=7,background="#2C2F33",fg="white",font="Helvetica 11")
spoon_import_message.pack()

Button(text='Run spoon code from ↓',command=start_translation_from_button,bg=button_background,fg=fg_color,font="Helvetica 10",pady=10).pack()

Label(root,text="Split up spoon",relief=GROOVE,bg=button_background,fg=fg_color,font="Helvetica 10").pack()


split_up_spoon_message = Text(root,relief=SUNKEN,height=7,background="#2C2F33",fg="white",font="Helvetica 11")

split_up_spoon_message.pack()
Button(text='Run brainfuck code from ↓',command=run_brain_fuck,bg=button_background,fg=fg_color,font="Helvetica 10",pady=10).pack()
Label(root,text="Brainfuck translation",relief=GROOVE,bg=button_background,fg=fg_color,font="Helvetica 10").pack()
brainfuck_message = Text(root,relief=SUNKEN,height=7,background="#2C2F33",fg="white",font="Helvetica 11")

brainfuck_message.pack()

Label(root,text="Executed brainfuck",relief=GROOVE,bg=button_background,fg=fg_color,font="Helvetica 10").pack()
execute_brainfuck_message = Text(root,relief=SUNKEN,height=7,background="#2C2F33",fg="white",font="Helvetica 11")
execute_brainfuck_message.pack()

stopButton = Button(root, text="Exit", command=exit_gui, width=20, bg=background_color, fg=fg_color,
                    font="Helvetica 10")
stopButton.pack()

def insert_all(message):
    clear_text()
    for i in (spoon_import_message,split_up_spoon_message,brainfuck_message,execute_brainfuck_message):
        insert(message,i)

def clear_text():
    for i in (spoon_import_message,split_up_spoon_message,brainfuck_message,execute_brainfuck_message):
        i.delete('1.0', END)

insert_all("Import file to start")


root.mainloop()