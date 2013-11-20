import GameConstants


def Debug(*msgs):
    if GameConstants.DEBUG:
        message = '[Debug] '
        for msg in msgs:
            message += str(msg)
        print(message)

def ErrorMsg(*msgs):
    message = ''
    for msg in msgs:
        message += msg
    import tkinter
    import tkinter.messagebox
    tkinter.Tk().withdraw()
    tkinter.messagebox.showerror("Error!", message)
