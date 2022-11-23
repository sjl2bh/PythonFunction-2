#NOTES:
    #must create folder neamed Data_Holder_Folder in BlobTrigger1 directory to hold excel files
    #must create an excel file named FileyTheFile and save it in Data_Holder_Folder

import os

import logging

import azure.functions as func

from azure.storage.blob import BlobServiceClient, ContainerClient

import pandas as pd

import openpyxl


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    print("hello world")

    #I think I need to use BlobServiceClient.get_container_client
    STORAGEACCOUNTURL= "https://nlpproofofconcept.blob.core.windows.net"
    STORAGEACCOUNTKEY= "PoBJOICvm9I34RO5bzYum0+404s+CvpfJO+aQ54hgvkxHFrHZMSd7qEphkQqVZlaT3IIbK6RR0dZ+ASt0OWrNw=="
    LOCALFILENAME= "BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx"
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

    with open(file="BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx", mode="wb") as blob:
        stream = blob_client.download_blob()
        blob.write(stream.readall())
        blob.close()
