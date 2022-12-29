

import pandas as pd
from wordcloud import WordCloud  # Will need to install using   conda install -c conda-forge wordcloud
import matplotlib.pyplot as plt
from BlobTrigger1.NLPConfigFile import*

def Create_Exploratory_Data_Analysis(data_dtm, data_clean):
    data = data_dtm  # variable "data" will be our document term matrix of type pandas.core.frame.DataFrame

    ############THESE VARIABLES NEED ATTENTION BEFORE EVERY RUN
    Topics = ['CTC', 'Levy']  # should probably move this to the top
    Acronyms_And_Meaningful_Words = ['ctc', 'child', 'credit',
                                    'levy']  # these elements are used when creating the variables data_IRS_Acronyms_and_Meaningful_Words, data_IRS_Categorized
    fig1 = plt.figure()
    # define parameters of wordcloud popup
    wc = WordCloud(background_color="white", colormap="Dark2",
                max_font_size=150, random_state=42)
    # read column of data_clean RESPONSES to a string variable called text_for_word_cloud
    text_for_word_cloud = data_clean["RESPONSES"]
    # generate a wordcloud based on the text string of all responses
    wc.generate(str(text_for_word_cloud))
    # show the wordcloud using matplotlib
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    if Show_Word_Cloud_Plot_config_variable == 1:
        plt.savefig("BlobTrigger1\\Data_Holder_Folder\\WordCloud.png")

    data_transposed = data.transpose()  # transposed version of document term matrix
    
    fig2 = plt.figure()
    # Let's isolate just these words
    ######## POTENTIAL ERROR HERE: if excel book doesn't contain one of the words in Acronymns_And_Meaningful_Words, you get an error during transposing
    data_IRS_Acronyms_and_Meaningful_Words = data_transposed.transpose()[
        Acronyms_And_Meaningful_Words]  # need more words here from someone with experience at IRS, should probably make this a list at the top of file
    data_IRS_Categorized = pd.concat([
                                        data_IRS_Acronyms_and_Meaningful_Words.ctc + data_IRS_Acronyms_and_Meaningful_Words.child + data_IRS_Acronyms_and_Meaningful_Words.credit,
                                        data_IRS_Acronyms_and_Meaningful_Words.levy],
                                    axis=1)  #########These are hard coded topics
    data_IRS_Categorized.columns = Topics

    # create barplot of topics based on count of topics in data_IRS_Categorized
    Counts_Of_Times_Mentioned = []
    for i in range(len(Topics)):
        Counts_Of_Times_Mentioned.append(data_IRS_Categorized[Topics[i]].sum())

    # Topics is the list of topics shown in the data_IRS_Categorized pandas dataframe, Counts_Of_Times_Mentioned is a list of the sums of each topic mentioned in the same order as Topics
    plt.bar(Topics, Counts_Of_Times_Mentioned)
    plt.title('Topic vs. Count of Times Mentioned')
    plt.xlabel('Topic')
    plt.ylabel('Count of Times Mentioned')
    if Show_Bar_Plot_config_variable == 1:
        plt.savefig("BlobTrigger1\\Data_Holder_Folder\\BarPlot.png")
    return 

