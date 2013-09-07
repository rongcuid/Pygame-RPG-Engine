import GameConstants


def Debug(*msgs):
    if GameConstants.DEBUG:
        print("[Debug] ", end="")
        for msg in msgs:
            print(msg, end="")
        print()
