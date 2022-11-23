#NOTES:
    #must create folder neamed Data_Holder_Folder in BlobTrigger1 directory to hold excel files
    #must create an excel file named FileyTheFile and save it in Data_Holder_Folder

import os

import logging

import azure.functions as func

from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient

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
    nlpinputs_Storage=os.environ["nlpinputsStorage"]

    service_client = BlobServiceClient.from_connection_string(conn_str=nlpinputs_Storage)
    container_client = service_client.get_container_client(container=CONTAINERNAME) 
    blob_client = container_client.get_blob_client(BLOBNAME)
   

    with open(file="BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx", mode="wb") as blob:
        stream = blob_client.download_blob()
        blob.write(stream.readall())
        blob.close()

    
    # dataframe_blobdata = pd.ExcelFile("BlobTrigger1\\Data_Holder_Folder\\FileyTheFile.xlsx")
    # file_name = open(LOCALFILENAME,'r', encoding='utf-8')
    # print(type(file_name))
    # print(file_name)
    # xl_workbook = pd.ExcelFile(file_name)
    # input_df = xl_workbook.parse("DataSheet")  # Parse the sheet into a dataframe
    # print(input_df)    
    # #t2=time.time()
    # #print(("It takes %s seconds to download "+BLOBNAME) % (t2 - t1))