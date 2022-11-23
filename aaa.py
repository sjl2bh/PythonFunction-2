import os

import logging

from azure.storage.blob import BlobServiceClient, ContainerClient

import pandas as pd

import openpyxl


#I think I need to use BlobServiceClient.get_container_client
STORAGEACCOUNTURL= "https://nlpproofofconcept.blob.core.windows.net"
STORAGEACCOUNTKEY= "PoBJOICvm9I34RO5bzYum0+404s+CvpfJO+aQ54hgvkxHFrHZMSd7qEphkQqVZlaT3IIbK6RR0dZ+ASt0OWrNw=="
LOCALFILENAME= "BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx"
CONTAINERNAME= "nlpinputs"
BLOBNAME= "TESTFILEFORAZURE.xlsx"

    #download from blob
blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
container_client = blob_service_client_instance.get_container_client(container= "nlpinputs") 
blob_client = container_client.get_blob_client(BLOBNAME)
   # with open(LOCALFILENAME, "wb") as CurrentBlob:
    #     blob_data = blob_client_instance.download_blob()
    #     blob_data.readinto(CurrentBlob)
    #     print(blob_data)
    #     print("THIS IS blob_data TYPE: " + str(type(CurrentBlob)))     

with open(file="BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx", mode="wb") as blob:
    stream = blob_client.download_blob()
    blob.write(stream.readall())
    blob.close()
