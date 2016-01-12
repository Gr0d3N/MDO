#import fbconsole
import datetime as dt
import time
import os
import sys
from hashlib import sha256
from peewee import *
import getpass
from Tkinter import Tk

# Update version list

def update_version():
    update_list = []
    print "I am sorry Mina I dont know what is that!"
    Q_new_input = raw_input("Do you want me to add this to my update verion \
TODO list to work on it later? \n")
    if "y" in Q_new_input.lower():
        new_input = raw_input("OK, then please describe it briefy here : \n")
        update_list.append(new_input)
        with open('Update List.txt', 'a') as out_file:
            for item in update_list:
                out_file.write("%s\n" % item)
        print "Todo update version list has been updated!"
    else:
        looping()

    looping()


# Clear Screen

def clear():
    os.system('clear')
    looping()


# Facebook

def facebook():
    
    fb1 = raw_input("What do ou wanna do with facebook? \n")
    if "status" in fb1.lower():
        verify = raw_input("do you want me to update your status? \n")
        if "y" in verify.lower():
            MyStatus = raw_input("What do you wanna say Mina? \n")
            update_status(MyStatus)
            print ""
            print "Status was updated to: " + MyStatus 
    else:
        update_version()

    looping()

def update_status(MyStatus):
    
    fbconsole.AUTH_SCOPE = ['publish_stream', 'publish_checkins']
    fbconsole.authenticate()

    status = fbconsole.post('/me/feed', {'message': MyStatus})


# Password master


def get_hexdigest(salt, plaintext):
    return sha256(salt + plaintext).hexdigest()

SECRET_KEY = ''

try:
    from dev_settings import *
except ImportError:
    pass

def make_password(plaintext, service):
    salt = get_hexdigest(SECRET_KEY, service)[:20]
    hsh = get_hexdigest(salt, plaintext)
    return ''.join((salt, hsh))

ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '0123456789!@#$%^&*()-_')

def password(plaintext, service, length=10, alphabet=ALPHABET):
    raw_hexdigest = make_password(plaintext, service)

    # Convert the hexdigest into decimal
    num = int(raw_hexdigest, 16)

    # What base will we convert `num` into?
    num_chars = len(alphabet)

    # Build up the new password one "digit" at a time,
    # up to a certain length
    chars = []
    while len(chars) < length:
        num, idx = divmod(num, num_chars)
        chars.append(alphabet[idx])

    return ''.join(chars)


db = SqliteDatabase('accounts.db')

class Service(Model):
    name = CharField()
    user_name = CharField()
    length = IntegerField(default=8)
    symbols = BooleanField(default=True)
    alphabet = CharField(default='')

    class Meta:
        database = db

    def get_alphabet(self):
        if self.alphabet:
            return self.alphabet
        alpha = ('abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                 '0123456789')
        if self.symbols:
            alpha += '!@#$%^&*()-_'
        return alpha

    def password(self, plaintext):
        print_password = password(plaintext, self.name, self.length, self.get_alphabet())
        print "Your password is:"
        print print_password

    def c_password(self, plaintext):
        c_password = password(plaintext, self.name, self.length, self.get_alphabet())
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(c_password)
        print "Password was copied to clipboard!"

    @classmethod
    def search(cls, q):
        return cls.select().where(cls.name ** ('%%%s%%' % q))

db.create_table(Service, True)


# New passwrord

def create_new_password(new_service_name, new_service_user_name, new_service_length, new_service_symbols, master_password):
    new_service_object = Service.create(name= new_service_name, user_name = new_service_user_name, length= new_service_length, symbols= new_service_symbols)
    new_service_object.password(master_password)
    looping()

# Print password

def print_password(requested_service_name, master_password):
    try:
        service_instance = Service.get(Service.name == requested_service_name)
        service_instance.password(master_password)
    except:
        print "No website or service with this name was found!"
        looping()
    looping()


# Copy password

def copy_password(requested_service_name, master_password):
    try:
        service_instance = Service.get(Service.name == requested_service_name)
        service_instance.c_password(master_password)
    except:
        print "No website or service with this name was found!"
        looping()
    looping()


# print user_name

def print_user_name(requested_service_name):
    try:
        service_instance = Service.get(Service.name == requested_service_name)
        user_name = service_instance.user_name
        print "Your username is: "
        print user_name
    except:
        print "No website or service with this name was found!"
        looping()
    looping()



# Looping again

def looping():
    
    my_input= raw_input("Let me know if you need anything else? \n")

    if "update version" in my_input.lower():
        update_version()
    elif "clear screen" in my_input.lower():
        clear()
    elif "facebook" in my_input.lower():
        facebook()
    elif "exit" in my_input.lower():
        sys.exit()
    elif "new password" in my_input.lower():
        new_service_name = raw_input("What is the website or the service name? \n")          
        new_service_user_name = raw_input("What is the user name? \n")
        new_service_length = int(raw_input("How many character you need your password to be? \n"))
        new_service_symbols = raw_input("Do you want to include symbols? \n")
        while ("yes" not in new_service_symbols.lower()) and ("no" not in new_service_symbols.lower()):
            new_service_symbols = raw_input("Answer can only be yes or no! Try again! \n")
        if new_service_symbols == "yes":
            new_service_symbols = True
        elif new_service_symbols == "no":
            new_service_symbols = False
        master_password = getpass.getpass("What is your master password? \n")
        create_new_password(new_service_name, new_service_user_name, new_service_length, new_service_symbols, master_password)
    elif "print password" in my_input.lower():
        requested_service_name = raw_input("What is the name of the website or the service? \n")
        master_password = getpass.getpass("What is your master password? \n")
        print_password(requested_service_name, master_password)
    elif "copy password" in my_input.lower():
        requested_service_name = raw_input("What is the name of the website or the service? \n")
        master_password = getpass.getpass("What is your master password? \n")
        copy_password(requested_service_name, master_password)
    elif "print username" in my_input.lower():
        requested_service_name = raw_input("what is the name of the website or the service? \n")
        print_user_name(requested_service_name)
    else:
        update_version()


# Welcome

my_input= raw_input("Hey Mina, how can I help you? \n")

if "update version" in my_input.lower():
    update_version()
elif "clear screen" in my_input.lower():
    clear()
elif "facebook" in my_input.lower():
    facebook()
elif "exit" in my_input.lower():
    sys.exit()
elif "new password" in my_input.lower():
    new_service_name = raw_input("What is the website or the service name? \n")          
    new_service_user_name = raw_input("What is the user name? \n")
    new_service_length = int(raw_input("How many character you need your password to be? \n"))
    new_service_symbols = raw_input("Do you want to include symbols? \n")
    while ("yes" not in new_service_symbols.lower()) and ("no" not in new_service_symbols.lower()):
        new_service_symbols = raw_input("Answer can only be yes or no! Try again! \n")
    if new_service_symbols == "yes":
        new_service_symbols = True
    elif new_service_symbols == "no":
        new_service_symbols = False
    master_password = getpass.getpass("What is your master password? \n")
    create_new_password(new_service_name, new_service_user_name, new_service_length, new_service_symbols, master_password)
elif "print password" in my_input.lower():
    requested_service_name = raw_input("What is the name of the website or the service? \n")
    master_password = getpass.getpass("What is your master password? \n")
    print_password(requested_service_name, master_password)
elif "copy password" in my_input.lower():
    requested_service_name = raw_input("What is the name of the website or the service? \n")
    master_password = getpass.getpass("What is your master password? \n")
    copy_password(requested_service_name, master_password)
elif "print username" in my_input.lower():
    requested_service_name = raw_input("what is the name of the website or the service? \n")
    print_user_name(requested_service_name)
else:
    update_version()        

