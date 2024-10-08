# NOTE: all sql text should be in lowercase with only spaces as whitespace

import mysql.connector
from mysql.connector.errors import Error
import os

class text_color: 
   OPTION = '\033[95m'
   PROMPT = '\033[94m'
   OUTPUT = '\033[92m'
   TABLE = '\033[96m'
   INPUT = '\033[37m'
   END = '\x1b[0m'

changes_to_commit  = 0
changes = []

cnx = mysql.connector.connect(
        user='root',
        password='Am79qa@N8725',
        host='localhost',
        database='mnemonics');


# print the table

print_table_query = ('SELECT id, sound, timestamp FROM sounds')

#cursor.execute(print_table_query)

#for (mnemonic_id, sound) in cursor:
#    print(mnemonic_id, sound)

sound_search_query = ('SELECT id, sound, timestamp FROM sounds WHERE sound = %s');
mnemonic_search_query = ('SELECT id, sound_id, mnemonic, description, timestamp FROM mnemonics WHERE sound_id = %s');


def help_prompt():
    print(f'{text_color.OUTPUT}MENU:{text_color.END}')
    print(f'{text_color.OPTION}OPTIONS:\n\t-h or help (FOR HELP)\n\t-a (ADD MNEMONIC)\n\t'
            f'-e (EDIT MNEMONIC OR SOUND)\n\t-d (DELETE MNEMONIC OR SOUND)'
            f'\n\t-q (TO QUIT)\n\t-c (COMMIT CHANGES){text_color.END}')
    print(f'{text_color.PROMPT}Enter sound or mnemonic to SEARCH, or OPTION:{text_color.END}')

def add_help_prompt():
    print(f'{text_color.OUTPUT}ADDITION MODE:{text_color.END}')
    print(f'{text_color.OPTION}OPTIONS:\n\t-h or help (FOR HELP)\n\t-q (TO QUIT ADDING ENTRY){text_color.END}')
    print(f'{text_color.PROMPT}Enter [sound] | [mnemonic] | [description] to add to dictionary:{text_color.END}')

add_sound_query = ('INSERT INTO sounds (sound) VALUES (%s)');
add_mnemonic_query = ('INSERT INTO mnemonics (mnemonic, description, sound_id) VALUES (%s, %s, %s)');

def get_sound_id(sound):
    cursor = cnx.cursor()
    # check if there is a sound that resembles user input in lowercase
    cursor.execute(sound_search_query, [sound])
    
    sound_fetch = cursor.fetchall()
    sound_count = len(sound_fetch);
    
    if(sound_count < 1):
        print('Sound not found.')
        cursor.close()
        return -1
    
    sound_id = (sound_fetch[0])[0]
    cursor.close()
    #print(f'New sound created; id:{sound_id}.')
    return sound_id

# Returns true or false
def confirm():
    print(f'{text_color.PROMPT}Confirm? Y/n{text_color.END}')
    confirm = input(f'{text_color.INPUT}~:$ {text_color.END}')
    
    confirm = (confirm.strip()).lower()

    if confirm == 'y':
        return True
    else:
        return False


# If sound exists return id, if sound DNE create and return id
def add_sound(sound):
    sound = (sound.strip()).lower()
    sound_id = get_sound_id(sound);
    if (sound_id >= 0):
        #print(f"Sound already exists: {sound_id}")
        return

    # add the new sound
    cursor = cnx.cursor()
    cursor.execute(add_sound_query, [sound])
    cursor.close()

    #print(f"Added sound: {sound}")

# IF Mnemonic exists message "already exists", else CREATE and print entry
def add_mnemonic(sound, mnemonic, description):
    sound = (sound.strip()).lower()
    mnemonic = (mnemonic.strip())
    description = (description.strip())

    sound_id = get_sound_id(sound);
    if(sound_id < 0):
        print(f'{text_color.PROMPT}ERROR: Sound Does Not Exist.{text_color.END}')
        return

    cursor = cnx.cursor()
    
    try:
        cursor.execute(add_mnemonic_query, [mnemonic, description, sound_id])
    except mysql.connector.Error as err:
        print(str(Error(err.errno)))

    cursor.close()


def add():
    user_in_1 = input(f'{text_color.INPUT}~:$ {text_color.END}')
    
    if '-q' in user_in_1:
            os.system('clear')
            help_prompt()
            return
    
    split_in = user_in_1.split("|")
    
    if len(split_in) < 3:
        print(f'{text_color.PROMPT}Not enough arguments for definition.{text_color.END}')
        add();
        return;
    
    # process the strings
    for i in range(0, len(split_in)):
        split_in[i] = (split_in[i].strip())
        if i < 2 and split_in[i] == '':
            print(f'{text_color.PROMPT}INPUT ERROR: not enough arguments.{text_color.END}')
            add()
            return
        elif i > 2:
            print(f'{text_color.PROMPT}INPUT ERROR: too many arguments.{text_color.END}')
            add()
            return
        
        #print(f'split_in[{i}] = \"{split_in[i]}\"')

    print(f'{split_in[0]}\t|{split_in[1]}\t|{split_in[2]}\t') 

    if confirm():
        pass
        # add the code to input an entry

        [sound, mnemonic, mnemonic_desc] = split_in
        add_sound(sound)
        add_mnemonic(sound, mnemonic, mnemonic_desc)
        
        search(sound)

        input(f'{text_color.PROMPT}\nPress Enter to finish ADD:{text_color.END}')
        os.system('clear');
        help_prompt()
        return
    else:
        os.system('clear');
        add_help_prompt()
        add()
        return

# returns integer
def select_item():
    print(f'{text_color.PROMPT}Enter number of sound/mnemonic to edit:{text_color.END}')
    user_in = input(f'{text_color.INPUT}~:$ {text_color.END}')

    if user_in.isnumeric():
        return int(user_in)
    elif '-q' in user_in:
        return

# returns the sound_id, mnemonic_id of the selected mnemonic/sound
def search_select(search):
    search = (search.strip()).lower()
    cursor = cnx.cursor()
    # search for sound
    cursor.execute(sound_search_query, [search])

    sounds = cursor.fetchall()
    sound_count = len(sounds)

    cursor.close()
    if sound_count < 1:
        print(f'{text_color.OUTPUT}\"{sound}\" NOT found.{text_color.END}')
        return

    select_list = []
    
    print('')
    for [sound_id, sound, timestamp] in sounds:
        select_list.append([sound_id, None])
        print(f'{text_color.TABLE}[{len(select_list)}]| {sound}\t|{text_color.END}')

        mnemonic_cursor = cnx.cursor()
        mnemonic_cursor.execute(mnemonic_search_query,[sound_id])
        mnemonics = mnemonic_cursor.fetchall()
        mnemonic_count = len(mnemonics)
        for [mnemonic_id, sound_id, mnemonic, description, timestamp] in mnemonics:
            select_list.append([sound_id, mnemonic_id])
            print(f'{text_color.TABLE}[{len(select_list)}]\t\t| {mnemonic}\t| {description}{text_color.END}')

        mnemonic_cursor.close()
        print(f'{text_color.OUTPUT}\"{sound}\" found. It has {mnemonic_count} associated mnemonic(s).\n{text_color.END}')

    while True:
        selected = select_item()
        if not selected: 
            return
        elif selected > 0 and selected <= len(select_list):
            return select_list[selected-1]
        else:
            print(f'{text_color.OUTPUT}False argument.{text_color.END}')


def edit_help_prompt():
    os.system('clear');
    print(f'{text_color.OUTPUT}EDIT MODE:{text_color.END}')
    print(f'{text_color.OPTION}OPTIONS:\n\t-q (TO QUIT)\n\t-d [# NUMBER] (TO DELETE MNEMONIC WITH THAT NUMBER){text_color.END}')
    print(f'{text_color.PROMPT}Enter sound or mnemonic to SEARCH, or OPTION:{text_color.END}')

delete_mnemonic_prompt = ('DELETE FROM mnemonics WHERE sound_id = \'%s\' AND id = \'%s\';')

# same as edit but continuing with previous prompt
def edit_no_prompt(user_in):
    selected = search_select(user_in)
    if selected:
        print(selected)
        if selected[-1] == None:
            print('sound was selected')
        else:
            cursor = cnx.cursor()
            cursor.execute(delete_mnemonic_prompt, selected)
            cursor.close()
            print(f'{text_color.OUTPUT}Mnemonic Deleted.\n{text_color.END}')

    if not selected:
        os.system('clear');
        help_prompt()
    

    print(f'{text_color.PROMPT}Enter -c to continue Editing {user_in} or Enter to return:{text_color.END}')
    cont = input(f'{text_color.INPUT}~:$ {text_color.END}')
    if '-c' in cont:
        edit_no_prompt(user_in)
    else:
        os.system('clear');
        help_prompt()

# prompt search
# list w/ numbers to select
# confirm delete
def edit():
    edit_help_prompt()
    user_in = input(f'{text_color.INPUT}~:$ {text_color.END}')
    
    selected = search_select(user_in)
    if selected:
        print(selected)
        if selected[-1] == None:
            print('sound was selected')
        else:
            cursor = cnx.cursor()
            cursor.execute(delete_mnemonic_prompt, selected)
            cursor.close()
            print(f'{text_color.OUTPUT}Mnemonic Deleted.\n{text_color.END}')

    if not selected:
        os.system('clear');
        help_prompt()
    

    print(f'{text_color.PROMPT}Enter -c to continue Editing {user_in} or Enter to return:{text_color.END}')
    cont = input(f'{text_color.INPUT}~:$ {text_color.END}')
    if '-c' in cont:
        os.system('clear');
        edit_no_prompt(user_in)
    else:
        os.system('clear');
        help_prompt()



def search(sound):
    cursor = cnx.cursor()
    sound = (sound.strip()).lower()
    # check if there is a sound that resembles user input in lowercase
    cursor.execute(sound_search_query, [sound])
    
    fetchall = cursor.fetchall()
    sound_count = len(fetchall);
    
    if(sound_count < 1):
        print(f'{text_color.OUTPUT}\"{sound}\" NOT found.{text_color.END}')
        return

    sound_id, sound, timestamp = fetchall[0];
    
    # print(f'{text_color.TABLE}| {sound_id}\t| {sound}\t| {timestamp}{text_color.END}')
    print(f'{text_color.TABLE}|{sound}\t|{text_color.END}')
    cursor.close()

    mnemonic_cursor = cnx.cursor()
    mnemonic_cursor.execute(mnemonic_search_query,[sound_id])
    fetched_mnemonics = mnemonic_cursor.fetchall()
    mnemonic_count = len(fetched_mnemonics)

    for [mnemonic_id, foreign_sound_id, mnemonic, description, timestamp] in fetched_mnemonics:
        #print(f'{text_color.TABLE}\t| {mnemonic_id}\t| {foreign_sound_id}\t | {mnemonic}\t|{text_color.END}'
        #        f'{text_color.TABLE}\t{timestamp}\t| {description}{text_color.END}')
        print(f'{text_color.TABLE}\t| {mnemonic}\t| {description}{text_color.END}')

    print(f'{text_color.OUTPUT}\"{sound}\" found. It has {mnemonic_count} associated mnemonic(s).{text_color.END}')

    mnemonic_cursor.close()

# commit loop
def commit():
    print(f'{text_color.PROMPT}Commit changes to Database?{text_color.END}')
    if confirm():
        cnx.commit()
        print(f'{text_color.OUTPUT}Changes Commited.{text_color.END}')

def main():
    os.system('clear')
    help_prompt()
    while(True):            
        user_in = input(f'{text_color.INPUT}~:$ {text_color.END}')
        if '-qq' in user_in:
            os.system('clear')
            return
        elif '-q' in user_in:
            commited = commit()
            os.system('clear')
            return
        elif '-h' in user_in:
            help_prompt() 
        elif '-a' in user_in:
            os.system('clear');
            add_help_prompt()
            add()
            continue
        elif '-e' in user_in:
            edit()
        elif '-c' in user_in:
            commit()
        else:
            search(user_in)
        pass
main()

# how does this work:
# os.system('clear')
# print(Options: -q (QUIT) -a (ADD MNEMONIC) -e (EDIT MNEMONIC) -d (DELETE MNEMONIC OR SOUND)
# input('Enter search sound or mnemonic; or enter option:')
# is this the correct input (Y: yes / any other key : no)?
# if sound doesnt exist create sound
# if link mnemonic to sound

cnx.close()

