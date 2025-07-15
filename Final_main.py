from collections import UserDict
import re
from datetime import datetime, timedelta
from decorators import input_error

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
    
    
class Phone(Field):
    def __init__(self, phone):
             # Залишаємо лише цифри
            clean_phone = ''.join(filter(str.isdigit, phone))
            if len(clean_phone) != 10:
                raise ValueError("Invalid phone format: use 10-digit number")
            super().__init__(clean_phone)

        
class Birthday(Field):
    def __init__(self, value):          
    # Додайте перевірку коректності даних
            pattern = r"\d{2}.\d{2}.\d{4}"
            if not re.fullmatch(pattern, value):
                raise ValueError("Invalid date format. Use DD.MM.YYYY")
            try:
                # та перетворіть рядок на об'єкт datetime
                data_obj = datetime.strptime(value, "%d.%m.%Y")
                super().__init__(data_obj)
            except ValueError:
                raise ValueError("Invalid date format. Use DD.MM.YYYY")    

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None    

    def add_phone(self, phone):       
        self.phones.append(Phone(phone)) # реалізація класу

    def add_birthday(self, birthday_data):
        self.birthday = Birthday(birthday_data)
    
        
    def remove_phone(self, phone):
        new_phone_list = []
        for el in self.phones:
            if el.value != phone:
                new_phone_list.append(el)
        self.phones = new_phone_list
    
    def find_phone(self, phone_for_find):
         
        for phone in self.phones:
            if phone.value == phone_for_find:
                return phone.value
    
    def edit_phone(self, current_phone, new_phone):
        
        for phone in self.phones:
            if phone.value == current_phone:
                phone.value =  new_phone 
            
    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "not set"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {birthday_str}"
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        message = "contact added"
        return message
        
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        self.data.pop(name)

    def birthdays(self):
        next_week_birthdays = []
        today = datetime.today().date()
        end_of_week = today + timedelta(days=7)
        
        for key, value in self.data.items():
            
            # birthday = datetime.strptime(value.birthday.value, "%Y.%m.%d").date()
            birthday_this_year = value.birthday.value.replace(year=today.year).date()

        # If birthday already passed this year, assume it's next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= end_of_week:
                # user_copy = value
           
            
            # If the birthday is on Saturday (5), move it to Monday
                if birthday_this_year.weekday() == 5:
                    birthday_this_year += timedelta(days=2)
                elif birthday_this_year.weekday() == 6:  # Sunday → Monday
                    birthday_this_year += timedelta(days=1)

                # user_copy["birthday"] = birthday_this_year.strftime("%Y-%m-%d")
                
                next_week_birthdays.append(value)
            

        return next_week_birthdays
    
# Show birthday according to name

    def show_birthday(self, name_for_find):
        for key, value in self.data.items():
            if key == name_for_find:
                return value.birthday.value


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contacts(args, book: AddressBook):
     name, phone, *_ = args
     record = book.find(name)
     message = "Contact updated."
     if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
     if phone:
        record.add_phone(phone)
     return message

@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if not record:
        return ("There is no contact with such name")
    else:
        phones = '; '.join(phone.value for phone in record.phones)
        return(phones)

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        return("There is no Contact with such name!")
    else:
        record.edit_phone(old_phone, new_phone)
        return("Number was changed")

@input_error
def add_birthday(args, book):
    name, birthday_data, *_ = args
    record = book.find(name)
    if not record:
        return("There is no Contact with such name!")
    else:
        record.add_birthday(birthday_data)
        return ("Contact was updated")

@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if not record:
        return("There is no Contact with such name!")
    else:
        return record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "Birthday not set"
    
@input_error
def show_birthdays(args, book): 
      for key, record in book.data.items():
        return record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "Birthday not set"     

@input_error
def all_contacts(book):
    for key, record in book.data.items():
        return record

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contacts(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print (show_phone(args, book))

        elif command == "all":
            print(all_contacts(book))
            

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(show_birthdays(args, book))

        else:
            print("Invalid command.")
            
            
if __name__ == "__main__":
    main()   
