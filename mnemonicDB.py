# NOTE: all sql text should be in lowercase with only spaces as whitespace

import mysql.connector
import os

class text_color: 
   OPTION = '\033[95m'
   PROMPT = '\033[94m'
   OUTPUT = '\033[92m'
   TABLE = '\033[96m'
   INPUT = '\033[37m'
   END = '\x1b[0m'



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
            f'\n\t-q (TO QUIT){text_color.END}')
    print(f'{text_color.PROMPT}Enter sound or mnemonic to SEARCH, or OPTION:{text_color.END}')

def add_help_prompt():
    print(f'{text_color.OUTPUT}ADDITION MODE:{text_color.END}')
    print(f'{text_color.OPTION}OPTIONS:\n\t-h or help (FOR HELP)\n\t-q (TO QUIT ADDING ENTRY){text_color.END}')
    print(f'{text_color.PROMPT}Enter [sound] | [mnemonic] | [description] to add to dictionary:{text_color.END}')

add_sound_query = ('INSERT INTO sounds (sound) VALUES (%s)');
add_mnemonic_query = ('INSERT INTO mnemonics (mnemonic, description, sound_id) VALUES (%s, %s, %s)');

# If sound exists return id, if sound DNE create and return id
# RETURNS id of sound, or -1 if error
def add_sound():
    return -1;
    pass

# IF Mnemonic exists message "already exists", else CREATE and print entry
def add_mnemonic():
    pass


def add():
    user_in = input(f'{text_color.INPUT}~:$ {text_color.END}')
    
    if '-q' in user_in:
            os.system('clear')
            help_prompt()
            return
    
    split_in = user_in.split("|")
    
    if len(split_in) < 3:
        print(f'{text_color.PROMPT}Not enough arguments for definition.{text_color.END}')
        add();
        return;
    
    # process the strings
    for i in range(0, len(split_in)):
        split_in[i] = (split_in[i].strip()).lower()
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

    print(f'{text_color.PROMPT}Confirm? Y/n{text_color.END}')
    confirm = input(f'{text_color.INPUT}~:$ {text_color.END}')
    
    confirm = (confirm.strip()).lower()

    if confirm == 'y':
        pass
        # add the code to input an entry
        sound_id = add_sound(split_in[0])
        add_mnemonic(split_in[1], split_in[2], sound_id)

    else:
        os.system('clear');
        add_help_prompt()
        add()
        return


def main():
    os.system('clear')
    help_prompt()
    while(True):            
        user_in = input(f'{text_color.INPUT}~:$ {text_color.END}')
        if '-q' in user_in:
            return
        if '-h' in user_in:
            help_prompt() 
        if '-a' in user_in:
            os.system('clear');
            add_help_prompt()
            add()
        else:
            cursor = cnx.cursor()
            query_in = (user_in.strip()).lower()
            # check if there is a sound that resembles user input in lowercase
            cursor.execute(sound_search_query, [query_in])
            
            fetchall = cursor.fetchall()
            sound_count = len(fetchall);
            
            if(sound_count < 1):
               continue 

            sound_id, sound, timestamp = fetchall[0];
            
            print(f'{text_color.TABLE}| {sound_id}\t| {sound}\t| {timestamp}{text_color.END}')
            cursor.close()

            mnemonic_cursor = cnx.cursor()
            mnemonic_cursor.execute(mnemonic_search_query,[sound_id])
            fetched_mnemonics = mnemonic_cursor.fetchall()
            mnemonic_count = len(fetched_mnemonics)

            for [mnemonic_id, foreign_sound_id, mnemonic, description, timestamp] in fetched_mnemonics:
                print(f'{text_color.TABLE}\t| {mnemonic_id}\t| {foreign_sound_id}\t | {mnemonic}\t|{text_color.END}'
                        f'{text_color.TABLE}\t{timestamp}\t| {description}{text_color.END}')
            print(f'{text_color.OUTPUT}\"{sound}\" found. It has {mnemonic_count} associated mnemonic(s).{text_color.END}')
main()

# how does this work:
# os.system('clear')
# print(Options: -q (QUIT) -a (ADD MNEMONIC) -e (EDIT MNEMONIC) -d (DELETE MNEMONIC OR SOUND)
# input('Enter search sound or mnemonic; or enter option:')
# is this the correct input (Y: yes / any other key : no)?
# if sound doesnt exist create sound
# if link mnemonic to sound

cnx.close()

