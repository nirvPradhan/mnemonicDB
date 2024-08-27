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

print_table_query = ('SELECT id, sound FROM sounds')

#cursor.execute(print_table_query)

#for (mnemonic_id, sound) in cursor:
#    print(mnemonic_id, sound)

sound_search_query = ('SELECT id, sound FROM sounds WHERE sound = %s');


def help_prompt():
    print(f'{text_color.OPTION}OPTIONS:\n\t-h or help (FOR HELP)\n\t-a (ADD MNEMONIC)\n\t'
            f'-e (EDIT MNEMONIC OR SOUND)\n\t-d (DELETE MNEMONIC OR SOUND){text_color.END}')
    print(f'{text_color.PROMPT}Enter sound or mnemonic to SEARCH, or OPTION:{text_color.END}')


add_sound_query = ('SELECT id, sound FROM sounds WHERE sound = %s');
add_mnemonic_query = ('SELECT id, sound FROM sounds WHERE sound = %s');

def add():
    while True:
        
        print(f'{text_color.PROMPT}Enter [sound] | [mnemonic] | [description] to add to dictionary:{text_color.END}')
        user_in = input(f'{text_color.INPUT}~:$ {text_color.END}')
        
        if '-q' in user_in:
                os.system('clear')
                help_prompt()
                return
        
        split_in = user_in.split("|")
        
        if len(split_in) < 3:
            print(f'{text_color.PROMPT}Not enough arguments for definition.{text_color.END}')
            continue
        
        # process the strings
        for sp in split_in:
            sp = (sp.strip()).lower()

        print(f'{split_in[0]}\t|{split_in[1]}\t|{split_in[2]}\t') 
        confirm = input(f'{text_color.INPUT}~:$ {text_color.END}')
        print(f'{text_color.PROMPT}Confirm? Y/n{text_color.END}')
        confirm = (confirm.strip()).lower()

        if confirm == 'y':
            pass
        else:
            continue


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
            add()
        else:
            cursor = cnx.cursor()
            query_in = (user_in.strip()).lower()
            # check if there is a sound that resembles user input in lowercase
            cursor.execute(sound_search_query, [query_in])
            
            #for (mnemonic_id, sound) in cursor:

            # dunno why but can only get accurate rowcount after fetchall
            fetched = cursor.fetchall()
            rowcount = cursor.rowcount
            for [mnemonic_id, sound] in fetched:
                print(f'{text_color.TABLE}| {mnemonic_id}\t| sound\t{text_color.END}')

            print(f'{text_color.OUTPUT}{rowcount} instances found.{text_color.END}')
            cursor.close()
main()

# how does this work:
# os.system('clear')
# print(Options: -q (QUIT) -a (ADD MNEMONIC) -e (EDIT MNEMONIC) -d (DELETE MNEMONIC OR SOUND)
# input('Enter search sound or mnemonic; or enter option:')
# is this the correct input (Y: yes / any other key : no)?
# if sound doesnt exist create sound
# if link mnemonic to sound

cnx.close()

