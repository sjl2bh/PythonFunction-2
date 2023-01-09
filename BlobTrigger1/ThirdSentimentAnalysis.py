
import matplotlib.pyplot as plt
from textblob import TextBlob  # conda install -c conda-forge textblob

from BlobTrigger1.NLPConfigFile import*

def Create_Sentiment_Analysis(data_clean):
    data_sentiment = data_clean  # variable "data" will be our corpus of type pandas.core.frame.DataFrame

    # Create quick lambda functions to find the polarity and subjectivity of each response
    pol = lambda x: TextBlob(x).sentiment.polarity
    sub = lambda x: TextBlob(x).sentiment.subjectivity

    data_sentiment['polarity'] = data_sentiment['RESPONSES'].apply(pol)
    data_sentiment['subjectivity'] = data_sentiment['RESPONSES'].apply(sub)

    fig3 = plt.figure()
    plt.rcParams['figure.figsize'] = [10, 8]

    for index, respondent in enumerate(data_sentiment.index):
        x = data_sentiment.polarity.loc[respondent]
        y = data_sentiment.subjectivity.loc[respondent]
        plt.scatter(x, y, color='blue')

    plt.title('Sentiment Analysis', fontsize=20)
    plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
    plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)
    if Show_Sentiment_Analysis_Plot_config_variable == 1:
        plt.savefig("BlobTrigger1\\Data_Holder_Folder\\SentimentAnalysis.png")
    

    return data_sentiment
    