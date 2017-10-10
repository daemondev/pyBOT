import pandas as pd
import numpy as np
import json
import pymongo


cnx = pymongo.MongoClient()
db = cnx['pandas']
coll = db['data']

#https://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas
#https://stackoverflow.com/questions/24963062/a-better-way-to-load-mongodb-data-to-a-dataframe-using-pandas-and-pymongo
#https://stackoverflow.com/questions/20167194/insert-a-pandas-dataframe-into-mongodb-using-pymongo
#http://pbpython.com/excel-pandas-comp.html
#https://www.datacamp.com/community/tutorials/pandas-tutorial-dataframe-python
#http://xlsxwriter.readthedocs.io/working_with_pandas.html

#df = pd.read_excel("test.xlsx")
df = pd.read_excel("data.xlsx")
df.head()

def dataframeToMongo(collection, dataFrame):
    documents = json.loads(dataFrame.T.to_json()).values()
    #collection.insert_many(documents)
    collection.insert(documents)

def dataframeFromMongo(collection):
    return pd.DataFrame(list(collection.find()))

def dataframeFromMongoRecords(collection):
    return pd.DataFrame.from_records(collection.find())

def dataframeToExcel(filename, dataframe, sheetName = 'datos'):
    writer = pd.ExcelWriter(filename)
    dataframe.to_excel(writer, sheetName, index=False)
    writer.save()

def dataframeFromExcel(excelFileName, sheetName='Sheet1'):
    return pd.read_excel(excelFileName)

def dataframeJoin(*args):
    newDataFrame = pd.core.frame.DataFrame()
    for f in args:
        newDataFrame = newDataFrame.append(f)
    return newDataFrame

