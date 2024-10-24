from colorama import Fore, Back, Style
from functools import wraps


# constants for print results colors (success or error)
# for full book display color
# and full commands menu

COLOR_DONE = Fore.GREEN
COLOR_ERROR = Fore.RED
COLOR_MENU = Fore.WHITE
COLOR_BOOK = Fore.BLUE
COMMANDS_MENU = f"""
Welcome! Assistant bot's commands menu:
 add <name> <number> \t\t# to add new single contact to phone book
 change <name> <new_number> \t# to change contact's number
 phone <name> \t\t\t# show contact's phone number by its name (if exist)
 all\t\t\t\t# show all contacts in the book
 exit | close \t\t\t# exit from assistant
"""


# action results printed with their colors
# after each command COMMANDS_MENU will be displayed
#
# changes: arguments no more counts in main function
# replaced by INPUT_ERROR decorator which covers all the errors for
# ADD_CONTACT, CHANGE_CONTACT and SHOW_PHONE functions
# added one non standart exception: AlreadyExistsError to prevent
# overwriting data in ADD_CONTACT function
#
# PARSE_INPUT function was already implemented in the task, just copied
#
# ADD_CONTACT function adds record to book (returns string)
#
# CHANGE_CONTACT function changes record if it exists (returns string)
#
# SHOW_PHONE function return contact's number if exists (returns string)
#
# ALL action displays all book


class AlreadyExistsError(Exception):
    pass


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            match func.__name__:
                case "add_contact":
                    return f"{COLOR_ERROR}Give me name and phone please"
                case "change_contact":
                    return f"{COLOR_ERROR}Give me name and it's new phone please"

        except KeyError:
            match func.__name__:
                case "change_contact":
                    return f'{COLOR_ERROR}Contact WAS NOT found. Nothing to change. Use "add" command to create one'
                case "show_phone":
                    return f'{COLOR_ERROR}Contact WAS NOT found. Please use "add" command to create one'

        except IndexError:
            match func.__name__:
                case "show_phone":
                    return f"{COLOR_ERROR}Give me name to search"

        except AlreadyExistsError:
            return f'{COLOR_ERROR}Contact WAS NOT added. Already exists. Please use "change" command for edit'

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts: dict) -> str:
    name, phone = args
    if contacts.get(name) == None:
        contacts[name] = phone
        return f'{COLOR_DONE}Contact "{name}" with number {phone} added'
    else:
        raise AlreadyExistsError


@input_error
def change_contact(args, contacts: dict) -> str:
    name, phone_new = args
    phone_old = contacts[name]
    contacts[name] = phone_new
    return f'{COLOR_DONE}Phone number for "{name}" was changed from "{phone_old}" to "{phone_new}"'


@input_error
def show_phone(args, contacts: dict) -> str:
    name = args[0]
    return f'{COLOR_DONE}Phone number found. Name: "{name}", phone: {contacts[name]}'


def main():

    contacts = {}

    while True:
        print(f"{COLOR_MENU}{COMMANDS_MENU}")
        user_input = input(f"Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(f"{COLOR_MENU}Good bye!")
            break

        elif command == "add":
            print("\n" + add_contact(args, contacts))

        elif command == "change":
            print("\n" + change_contact(args, contacts))

        elif command == "phone":
            print("\n" + show_phone(args, contacts))

        elif command == "all":
            print(
                f'\n{COLOR_BOOK}Full address book [numbers in base: {len(contacts)}]\n{"Name":^12}{"phone":^12}'
            )
            for k, v in contacts.items():
                print(f"{k:^12}{v:^12}")

        else:
            print(f"\n{COLOR_ERROR}Invalid command")


if __name__ == "__main__":
    main()
