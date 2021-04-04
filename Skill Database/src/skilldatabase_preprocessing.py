import pandas as pd
import os

def list_remove_duplicates(l):
    """Removes duplicates from list elements whilst preserving element order

    Input
        list with string elements

    Return 
        list without duplicates, preserved order

    """
    return list(dict.fromkeys(l))

def list_string_manual_correction(x):
    """Traverse a list of strings and correct entries manually
    Can be applied to pandas Series object
    
    Input
        x: list with keywords to manually correct
        
    Return
        list: manually corrected list
    
    
    """
    
    print("Correct strings manually. \n\
    \t1. Go forward with ENTER \n\
    \t2. Go backwards by typing the backwardsstep number.\n\
    \tGo to next topic current topic by typing 'exit'")
    
    i = 0
    while i < len(x):
        correction = input("{}\t {} >>>".format(i, x[i]))

        ## navigate in integer steps
        # when integer specified, change index 
        if correction.isnumeric():
            i -= int(correction)
            
        elif correction == 'exit':
            i = len(x)
            
        elif len(correction) > 0 and correction != 'exit':
            x[i] = correction
            i += 1

        # if nothing specified go 1 step forward 
        else:
            i += 1
            
    return x




# from sys import version
# from os import getcwd
# print(version)
# print(getcwd())

# get all files in [folder] starting with [string]
## TODO: SPECIFY PATH OF FILLED QUESTIONNAIRES
path = './../Steckbriefe/Ausgefüllt' 
string_file_names = 'IASA Graduate Profile Questionnaire'
files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and string_file_names in i]

print("Loaded files from {}\n{}".format(path,"="*40))
print (*files, sep='\n')

# read in all excel files, drop remarks, transpose
df_list = [pd.read_excel(os.path.join(path, f) , header=1, index_col=0).drop(columns='Remarks').T for f in files]
df = pd.concat(df_list)
df.index = df.loc[:,'First Name'] + ' ' + df.loc[:,'Last Name']


### transforms sheets into dataframes
## subset Skills and Knowledge
# determine indices
idx_skills = df.columns.get_loc("Skills")
idx_knowledge = df.columns.get_loc("Knowledge")
idx_end = df.columns.get_loc('Your personal introduction (please answer each of the following questions in 1-2 sentences)')

# subset skill and knowledge with indices
df_skills = df.iloc[:, idx_skills+1:idx_knowledge]
df_knowledge = df.iloc[:, idx_knowledge+1:idx_end]
df_subset = pd.concat([df_skills,df_knowledge], axis=1)

# retrieve all answers seperated by comma
ds_skills_knowledge = df_subset.apply(lambda s: s.str.cat(sep=', ').split(", ")).T
df_skills_knowledge = pd.DataFrame(ds_skills_knowledge, columns=['raw'])

# manually correct entries
df_skills_knowledge['corrected'] = df_skills_knowledge.raw.apply(list_string_manual_correction)

# remove duplicates (while maintaining order)
df_skills_knowledge['no_duplicates'] = df_skills_knowledge.corrected.apply(list_remove_duplicates)

# convert list objects to strings 
for col in df_skills_knowledge.columns:
    df_skills_knowledge[col] = df_skills_knowledge.loc[:,col].apply(lambda x: ', '.join(x))

# export as xlsx
df_skills_knowledge.to_excel(os.path.join(path,'cleaned_profiles.xlsx') , index = False)
