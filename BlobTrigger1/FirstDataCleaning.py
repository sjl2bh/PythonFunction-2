
import pandas as pd

import openpyxl

import re

import string


from BlobTrigger1.NLPConfigFile import*
from BlobTrigger1.ListsOfWordsToBeCleaned import*


file_name = "BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx"
xl_workbook = pd.ExcelFile(file_name) # Load the excel workbook
input_df = xl_workbook.parse("DataSheet")  # Parse the sheet into a dataframe
print(input_df)


################BEGIN DATA CLEANING################################
List_Of_Respondent_IDs = input_df.iloc[:, 0].tolist()  # Cast column A into a python list, will skip row 1
List_Of_Responses = input_df.iloc[:, 1].tolist()  # Cast column B into a python list, will skip row 1

# Check if data came in correctly
# for i in List_Of_Respondent_IDs:
#     print(List_Of_Respondent_IDs)
#
# for i in List_Of_Responses:
#     print(List_Of_Responses)
# print(len(List_Of_Respondent_IDs))
# print(len(List_Of_Responses))
# print(List_Of_Respondent_IDs[0])

# Changing lists to dictionary using zip() ID; response
Dictionary_Of_Data = dict(zip(List_Of_Respondent_IDs, List_Of_Responses))
# print ("Resultant dictionary is : " +  str(res))

# Puts Dictionary into pandas dataframe
data_df = pd.DataFrame.from_dict([Dictionary_Of_Data]).transpose()
data_df.columns = ['RESPONSES']

#data_df = data_df.sort_index() ##################Commented this out cause I think it is unnecessary

# Check for first 5 lines of dataframe
# print(data_df.head())
# print(data_df.dtypes)

########################################################
# TEXT CLEANING
# Apply a first round of cleaning (must always be done)
def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = str(text)
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
#    text = re.sub('\w*\d\w*', '', text)
    return text
round1 = lambda x: clean_text_round1(x)
# Cleans the text with round one regular expressions
data_clean = pd.DataFrame(data_df.RESPONSES.apply(round1))

# print(data_clean)

# Apply a second round of cleaning (must always be done)
def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = str(text)
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text
round2 = lambda x: clean_text_round2(x)
data_clean = pd.DataFrame(data_clean.RESPONSES.apply(round2))

################## Optional text cleaning
def remove_words_from_comments(text):
    '''If a comment contains a word specified by a list/set of list
    in the parameters, the word is removed and the rest of the comment
    is kept'''
    text = str(text)
    for Word_To_Be_Removed in range(0, len(Full_List_Of_Words_To_Be_Removed_From_Comment)):
        text = re.sub(Full_List_Of_Words_To_Be_Removed_From_Comment[Word_To_Be_Removed],'',text)
    return text
Remove_Words = lambda x: remove_words_from_comments(x)
data_clean = pd.DataFrame(data_clean.RESPONSES.apply(Remove_Words))

def remove_comments_containing_filtered_words(text):
    '''If a comment contains a word specified by a list/set of list
    in the parameters, the word is removed and the rest of the comment
    is kept'''
    text = str(text)
    for Word_To_Remove_Comment_By in range(0, len(Full_List_Of_Words_To_Remove_Comments_By)):
        if Full_List_Of_Words_To_Remove_Comments_By[Word_To_Remove_Comment_By] in text:
            text = ""
    return text
Remove_Comments = lambda x: remove_comments_containing_filtered_words(x)
data_clean = pd.DataFrame(data_clean.RESPONSES.apply(Remove_Comments))



def remove_comments_containing_nan(text):
    '''THIS MUST BE AT THE END OF TEXT CLEANING. If a comment is just "nan" in the pandas dataframe (often happens in text cleaning), then it will be replaced with a blank space so that the
    topic modelling is not affected by the nonsense word "nan"'''
    text = str(text)
    if text == "nan":
            text = ""
    return text
Remove_nan_Comments = lambda x: remove_comments_containing_nan(x)
data_clean = pd.DataFrame(data_clean.RESPONSES.apply(Remove_nan_Comments))
#print(data_clean)
#########THIS LINE COMPLETES THE FINAL CORPUS

print("First Data Cleaning Happened")