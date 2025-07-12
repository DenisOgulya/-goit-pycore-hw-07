from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass
    
    
class Phone(Field):
    def __init__(self, phone):
        if(len(phone) == 10):
            super().__init__(phone)
        #HERE SHOULD BE ERROR
        
class Birthday(Field):
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних
            pattern = r"\d{2}.\d{2}.\d{4}"
            if re.fullmatch(pattern, value):
                # та перетворіть рядок на об'єкт datetime
                self.value = datetime.strptime(value, "%d.%m.%Y")
                super().__init__(self.value)
                
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
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, bithday: {self.birthday.value}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        self.data.pop(name)

    def get_upcoming_birthdays(self):
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


def main():
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("13.08.1978")

    
    
    name = john_record.name.value

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    

    john = book.find('John')
    john.edit_phone("1234567890", "1112223333")

    found_phone = john.find_phone("5555555555")
    john.remove_phone("5555555555")

    # Видалення запису Jane
    book.delete("Jane")
    
    
    # Виведення всіх записів у книзі
    for record in book.get_upcoming_birthdays():
        print(record)
    
if __name__ == "__main__":
    main()   