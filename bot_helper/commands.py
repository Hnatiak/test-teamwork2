from prompt_toolkit import prompt
from termcolor import colored, cprint
from prompt_toolkit.completion import WordCompleter
from main import handler_help, handler_hello, handler_add, handler_change, handler_show_all, handler_exit, handler_find, handler_delete_phone, handler_delete_user, handler_next_birthday

import address_book as book

NAME_COMMANDS = {
    "help": handler_help,
    "hello": handler_hello,
    "add": handler_add,
    "change": handler_change,
    "show-all": handler_show_all,
    "goodbye": handler_exit,
    "close": handler_exit,
    "exit": handler_exit,
    "find": handler_find,
    "delete-telephone": handler_delete_phone,
    "delete-user": handler_delete_user,
    "next-birthday": handler_next_birthday
}

# def get_command_suggestions(prefix):
    # suggestions = [cmd for cmd in NAME_COMMANDS.keys() if prefix.lower() in cmd.lower()]
    # formatted_suggestions = "\n".join(f"{' ' * 60}| {cmd} |" for cmd in suggestions)
    # user_input = prompt(f"Please enter your command: ", completer=WordCompleter(suggestions, ignore_case=True))
    # return user_input.lower()


def get_command_suggestions(prefix):
    try:
        suggestions = [cmd for cmd in NAME_COMMANDS.keys() if prefix.lower() in cmd.lower()]
        formatted_suggestions = "\n".join(f"{' ' * 60}| {cmd} |" for cmd in suggestions)
        user_input = prompt(f"Please enter your command: ", completer=WordCompleter(suggestions, ignore_case=True))
        return user_input.lower()
    except KeyboardInterrupt:
        print("\nCommand input interrupted. Exiting...")
        exit()