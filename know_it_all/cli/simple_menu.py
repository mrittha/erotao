__author__ = 'mrittha'

import know_it_all.cli.talker as talker


def ask_list(items):
    in_choice = True
    while in_choice:
        for i, v in enumerate(items):
            print(i, v)
        selection = talker.ask("What is your choice? (q to quit)")
        if selection.upper() == 'Q':
            return None
        selection = int(selection)
        if selection < 0 or selection >= len(items):
            talker.print_and_talk("That was not a valid selection.  Please select again.")
        else:
            return items[selection],selection


if __name__ == "__main__":
    selected = ask_list(['item 1', 'item 2', 'item 3'])
    if selected:
        talker.print_and_talk("You chose",selected)
