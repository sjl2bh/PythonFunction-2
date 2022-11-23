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
    blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, BLOBNAME, snapshot=None)
    # with open(LOCALFILENAME, "wb") as CurrentBlob:
    #     blob_data = blob_client_instance.download_blob()
    #     blob_data.readinto(CurrentBlob)
    #     print(blob_data)
    #     print("THIS IS blob_data TYPE: " + str(type(CurrentBlob)))
        
    container_client = blob_service_client_instance.get_container_client(container= "nlpinputs") 
    
    st = container_client.download_blob(BLOBNAME).download_to_stream()
    download_file = open(file="BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx", mode="wb+") 
    download_file.write(container_client.download_blob(BLOBNAME).readall())
    download_file.close()
    
    # dataframe_blobdata = pd.ExcelFile("BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx")
    # file_name = open(LOCALFILENAME,'r', encoding='utf-8')
    # print(type(file_name))
    # print(file_name)
    # xl_workbook = pd.ExcelFile(file_name)
    # input_df = xl_workbook.parse("DataSheet")  # Parse the sheet into a dataframe
    # print(input_df)    
    # #t2=time.time()
    # #print(("It takes %s seconds to download "+BLOBNAME) % (t2 - t1))