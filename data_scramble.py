#########################################################################################
# Data Scramble Script
# Created By: David Hatchett
# Created on: 2025-12-10
#   This script created to mimic bad users inputs. A lot of the smaller functions that 
# do the acutal data manpluation came Orginially from Chatgtp. I'm sense made alterations
# of my own and I sturn the code together. We could maybe imporve this to seem more natural
# in the futher.
#    I chose to only edit .6 of the records as we need a good amount of correct works to
#work. I set the edits to .2 as we get results that are really werid otherwise.
#########################################################################################

import pandas as pd
import random
import string


NEIGHBORS = {
    'a': 'qswd', 'b': 'vghn', 'c': 'xdfv', 'd': 'serfcx', 'e': 'wsdr',
    'f': 'drtgvc', 'g': 'ftyhbv', 'h': 'gyujnb', 'i': 'ujko', 'j': 'huikmn',
    'k': 'jiolm', 'l': 'kop', 'm': 'njk', 'n': 'bhjm', 'o': 'iklp',
    'p': 'ol', 'q': 'wa', 'r': 'edft', 's': 'awedxz', 't': 'rfgy',
    'u': 'yhji', 'v': 'cfgb', 'w': 'qase', 'x': 'zsdc', 'y': 'tghu',
    'z': 'asx'
}   

def deletion(text:str, p=0.5) -> str:
    '''
    This randomlay deletes a char pase on the value of P. Primarly take 
    from a Chat GTP query and modified slightly for my use.
    
    :param text: Value you want to edit
    :type text: str
    :param p: probliity of deleting a car
    :return: edited string
    :rtype: str
    '''
    chars = list(str(text))
    return ''.join([c for c in chars if random.random() > p]) or text

def random_swap(text:str, p=0.05):
    '''
    Modified code from a chatgtp promet. minor changes to stay in line 
    with my sytle.
    this function will swap text based on the random value generated.
    will jump ahead two place if a swap occurs so as to not swap back.
    
    :param text: text value to have edited
    :type text: str
    :param p: change of swaping a value
    '''
    chars = list(str(text))
    i = 0
    while i < len(chars)-1:
        if random.random() < p:
            chars[i], chars[i+1] = chars[i+1], chars[i]
            i += 2
        else:
            i += 1
    return ''.join(chars)

def keyboard_error(text:str, swap_dict:dict[str,list[str]]=NEIGHBORS, p=0.05) -> str:
    '''
    Docstring for keyboard_error
    
    :param text: Description
    :type text: str
    :param swap_dict: Description
    :type swap_dict: dict[str, list[str]]
    :param p: Description
    '''
    out=list()
    for c in text:
        low = c.lower()
        if low in swap_dict and random.random() < p:
            rep = random.choice(swap_dict[low])
            out.append(rep.upper() if c.isupper() else rep)
        else:
            out.append(c)
    
    return ''.join(out)

def random_truncate(text:str, p=0.5)-> str:
    '''
    Docstring for random_truncate
    
    :param text: Description
    :type text: str
    :param p: Description
    :return: Description
    :rtype: str
    '''
    if random.random() < p and len(text) > 3:
        cut = random.randint(1,len(text)-2)
        return text[:cut]
    return text

def scramble_text(text:str):
    #Random Chace that the string is just left alone


    text = deletion(text, p=.2)
    text = random_swap(text, p=.2)
    text = keyboard_error(text, p=.2)
    text = random_truncate(text, p=.2)

    return text

def main() ->None:

    column_change = {
        'name':'label_name',
        'address':'label_address',
        'city':'label_city',
        'postalZip':'label_postalzip',
        'state':'label_state',
        'phone':'label_phone'
    }

    #Load data from csv and create 1000 copys of each record
    df = pd.read_csv('data/generated_data_20_names.csv')
    df.rename(columns=column_change, inplace=True)
    df = pd.concat([df] * 1000, ignore_index=True)


    df_to_edit = df.sample(frac=.6, replace=False)
    df = df.drop(df_to_edit.index)


    ## add data to the test field for the non edit recrds
    df['test_name'] = df['label_name']
    df['test_address'] = df['label_address']
    df['test_city'] = df['label_city']
    df['test_postalzip'] = df['label_postalzip']
    df['test_state'] = df['label_state']
    df['test_phone'] = df['label_phone']



    ## run the data through the scrambler for each coulumn
    ## insure we have some untoch records

    df_to_edit['test_name'] = df_to_edit['label_name'].apply(scramble_text)
    df_to_edit['test_address'] = df_to_edit['label_address'].apply(scramble_text)
    df_to_edit['test_city'] = df_to_edit['label_city'].apply(scramble_text)
    df_to_edit['test_postalzip'] = df_to_edit['label_postalzip'].apply(scramble_text)
    df_to_edit['test_state'] = df_to_edit['label_state'].apply(scramble_text)
    df_to_edit['test_phone'] = df_to_edit['label_phone'].apply(scramble_text)


    df = pd.concat([df,df_to_edit])

    ## select 80% of the records passed, I don't care if its reporduceable
    ## it may be best to create several test data sets.
    ## I might rerun to test preformace on completely unknow data
    df = df.sample(frac=.8, replace=False)



    #export scrabled data
    # df.to_excel('data/scarmble_data.xlsx')
    df.to_csv('data/scarmble_data_small.csv')

    

if __name__ == "__main__":
    main()