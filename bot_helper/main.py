import address_book as book
from commands import *
from termcolor import colored, cprint
from tabulate import tabulate
from datetime import date
from schema import help_table


def input_error(func):
    def inner(my_book, val):
        try:
            return_data = func(my_book, val)
        except IndexError:
            return_data = cprint("Give me name and phone please", 'red')
        except TypeError:
            return_data = cprint("Wrong command, try again", 'red')
        except KeyError:
            return_data = cprint("Wrong user, repeat please", 'red')
        except ValueError:
            return_data = cprint("Wrong number, repeat please", 'red')
        except book.WrongBirthday:
            return_data = cprint("Wrong birthday, repeat please", 'red')
        except book.ExistsPhone:
            return_data = cprint("Phone is exist", 'red')
        return return_data
    return inner

def handler_hello(my_book, _=None):
    return cprint("How can I help you?", 'green')

def handler_add(my_book, list_):
    my_book.exists_phone(list_[1])
    try:
        record = my_book.find(list_[0].capitalize())
    except:
        if len(list_) == 3:
            record = book.Record(list_[0].capitalize(), list_[2])
        else:
            record = book.Record(list_[0].capitalize())
        record.add_phone(list_[1])
        my_book.add_record(record)
    else:
        record.add_phone(list_[1])
        my_book.add_record(record)
    return cprint("Command successfully complete", 'green')

def handler_change(my_book, list_):
    my_book.exists_phone(list_[2])
    record = my_book.find(list_[0].capitalize())
    if record is not None:
        record.edit_phone(list_[1], list_[2])
    return cprint(f"Phone {list_[1]} from user {list_[0].capitalize()} successfully changed to phone {list_[2]}", 'green')

def handler_show_all(my_book, _=None):
    table_data = []

    headers = ["Name", "Phone", "Email", "Birthday"]
    table_data.append(headers)

    for record in my_book:
        name = record.name.value
        phones = ', '.join(p.value for p in record.phones)
        email = ''
        birthday = date.strftime(record.birthday.value, '%d.%m.%Y') if hasattr(record, "birthday") else ''
        table_data.append([name, phones, email, birthday])

    formatted_table = tabulate(table_data, headers="firstrow", tablefmt="pretty")

    return cprint(formatted_table, 'blue')

def handler_exit(my_book, _=None):
    return cprint("Good bye!", 'green')

def handler_find(my_book, list_):
    list_rec = my_book.finde_records(list_[0].capitalize())
    if len(list_rec) != 0:
        ret_book = book.AddressBook()
        for rec_ in list_rec:
            ret_book.add_record(rec_)
        return cprint(ret_book, 'yellow')
    else:
        return cprint("Contact not found", 'red')

def handler_delete_phone(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    record.remove_phone(list_[1])
    return cprint(f"Phone {list_[1]} of user {list_[0].capitalize()} successfully deleted", 'green')

def handler_delete_user(my_book, list_):
    my_book.delete(list_[0].capitalize())
    return cprint(f"User {list_[0].capitalize()} successfully deleted", 'green')

def handler_next_birthday(my_book, list_):
    record = my_book.find(list_[0].capitalize())
    days = record.days_to_birthday()
    return cprint(f"Next birthday for user {list_[0].capitalize()} after {days} days", 'blue')

def handler_help(my_book=None, _=None):
    formatted_table = tabulate(help_table, headers="firstrow", tablefmt="presto", numalign="center")

    return cprint(formatted_table, 'blue')

@input_error
def parser_command(my_book, command):
    list_command = command.split(" ")
    if list_command[0] in NAME_COMMANDS:
        any_command = NAME_COMMANDS[list_command[0]]
        ret_result = any_command(my_book, list_command[1:])
        return ret_result
    elif len(list_command) > 1 and list_command[0] + list_command[1] in NAME_COMMANDS:
        any_command = NAME_COMMANDS[list_command[0] + list_command[1]]
        ret_result = any_command(my_book, list_command[2:])
        return ret_result
    else:
        return cprint("Wrong command, try again", 'red')

def main():
    print(handler_help())
    file_name_j = "book_json.json"
    my_book_j = book.AddressBook()
    my_book = my_book_j.load_from_file_json(file_name_j)
    
    while True:
        user_input = get_command_suggestions("")
        ret_result = parser_command(my_book, user_input)
        
        if ret_result:
            print(ret_result)
            if ret_result == "Good bye!":
                my_book.save_to_file_json(file_name_j)
                exit()
                
if __name__ == "__main__":
    main()