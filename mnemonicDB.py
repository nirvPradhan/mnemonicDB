# NOTE: all sql text should be in lowercase with only spaces as whitespace

import mysql.connector
import os

class text_color: 
   OPTION = '\033[95m'
   PROMPT = '\033[94m'
   OUTPUT = '\033[92m'
   TABLE = '\033[96m'
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


def main():
    os.system('clear')
    help_prompt()
    while(True):
                
        user_in = input('~:$ ')
        
        if '-q' in user_in:
            return
        if '-h' in user_in:
            help_prompt() 
        else:
            cursor = cnx.cursor()
            query_in = (user_in.strip()).lower()
            # check if there is a sound that resembles user input in lowercase
            cursor.execute(sound_search_query, [query_in])
            
            #for (mnemonic_id, sound) in cursor:
            #    print(f'{text_color.TABLE}| {mnemonic_id}\t| sound\t{text_color.END}')

            # dunno why but can only get accurate rowcount after fetchall
            fetched = cursor.fetchall()
            rowcount = cursor.rowcount
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

