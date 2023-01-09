#NOTES:
    #must create folder neamed Data_Holder_Folder in BlobTrigger1 directory to hold excel files
    #must create an excel file named TemporaryDataFile.xlsx and save it in Data_Holder_Folder

import os

import logging

import azure.functions as func

from azure.storage.blob import BlobServiceClient, ContainerClient

import pandas as pd

import openpyxl

import re

import string

from BlobTrigger1.NLPConfigFile import*
from BlobTrigger1.ListsOfWordsToBeCleaned import*
from BlobTrigger1.FirstDataCleaning import Create_Data_Clean
from BlobTrigger1.SecondExploratoryDataAnalysis import Create_Exploratory_Data_Analysis
from BlobTrigger1.ThirdSentimentAnalysis import Create_Sentiment_Analysis
from BlobTrigger1.FourthTopicModeling import Create_Topic_Modeling

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    print("hello world")

    #I think I need to use BlobServiceClient.get_container_client
    STORAGEACCOUNTURL= "https://nlpproofofconcept.blob.core.windows.net"
    STORAGEACCOUNTKEY= "PoBJOICvm9I34RO5bzYum0+404s+CvpfJO+aQ54hgvkxHFrHZMSd7qEphkQqVZlaT3IIbK6RR0dZ+ASt0OWrNw=="
    LOCALFILENAME= "BlobTrigger1\\Data_Holder_Folder\\TemporaryDataFile.xlsx"
    CONTAINERNAME= "nlpinputs"
    def DefineBlobName(StringTheBlobName):
        tempList = StringTheBlobName.split('/',1)
        print(tempList[1])
        return(tempList[1])
    BLOBNAME= DefineBlobName(myblob.name)

    #download from blob
    blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
    container_client = blob_service_client_instance.get_container_client(container= "nlpinputs") 
    blob_client = container_client.get_blob_client(BLOBNAME)
   

    with open(file="BlobTrigger1\\Data_Holder_Folder\\TemporaryDataFile.xlsx", mode="wb") as blob:
        stream = blob_client.download_blob()
        blob.write(stream.readall())
        blob.close()


    data_clean, data_dtm, input_df = Create_Data_Clean()
    print("SHOULD ONLY PRINT ONCE")
    print(data_clean)


    Create_Exploratory_Data_Analysis(data_dtm, data_clean)

    data_sentiment = Create_Sentiment_Analysis(data_clean)

    Create_Topic_Modeling(input_df, data_clean, data_sentiment)


    ####START UPLOADING FILES TO OUTPUTS CONTAINER

    CONTAINERNAME2= "outputs"
    FILES = os.listdir ('BlobTrigger1\\Data_Holder_Folder')
    

    blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
    
    #can force creation if this container client does not exist
    container_client = blob_service_client_instance.get_container_client(container= "outputs") 
    for file in FILES:
        upload_file_path = 'BlobTrigger1\\Data_Holder_Folder\\' + file
        blob_client = container_client.get_blob_client(file)
        with open(file=upload_file_path, mode="rb") as data:
            blob_client.upload_blob(data, overwrite=True)