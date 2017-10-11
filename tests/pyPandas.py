import pandas as pd
import numpy as np
import json
import pymongo
from openpyxl import load_workbook # 2.4.0-a1
#from itertools import islice


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

def dfToMongo(collection, dataFrame):
    documents = json.loads(dataFrame.T.to_json()).values()
    return collection.insert_many(documents)
    #collection.insert(documents)

def dfInsertAndGetFromMongo(collection, dataframe):
    ids = dfToMongo(collection, dataframe)
    return dfGetFromMongoByIds(collection, ids)


def dfFromMongo(collection):
    return pd.DataFrame(list(collection.find()))

def dfFromMongoRecords(collection):
    return pd.DataFrame.from_records(collection.find())

def dfToExcel(filename, dataframe, sheetName = 'datos'):
    writer = pd.ExcelWriter(filename)
    dataframe.to_excel(writer, sheetName, index=False)
    writer.save()

def dfFromExcel(excelFileName, sheetName='Sheet1'):
    return pd.read_excel(excelFileName, index=False, na_values=[''])

def getSheetValues(excelFileName, sheetName="Sheet1"):
    wb = load_workbook(filename=excelFileName)
    sheet = wb[wb.get_sheet_names()[0]]
    return sheet.values


def dfFromExcelValues(excelFileName, sheetName='Sheet1'):
    """
    data = getSheetValues(excelFileName, sheetName)
    cols = next(data)[1:]
    data = list(data)
    idx = [r[0] for r in data]
    data = (islice(r, 1, None) for r in data)
    return pd.DataFrame(data, index=idx, columns=cols) #"""

    data = getSheetValues(excelFileName, sheetName)
    cols = next(data)
    data = list(data)
    return pd.DataFrame(data,columns=cols)

def dfJoin(*args):
    newDataFrame = pd.core.frame.DataFrame()
    for f in args:
        newDataFrame = newDataFrame.append(f, ignore_index=True) #concat([])
    return newDataFrame

def dfGetDuplicates(dataframe, *args):
    cols = []
    for c in args:
        cols.append(c)
    return dataframe[dataframe.duplicated(cols, keep=False)].sort_values(cols[0])

def dfGetFromMongoByIds(collection, ids):
    return pd.DataFrame(list(collection.find({'_id': {'$in': ids.inserted_ids}})))

dfa = dfFromExcel("a.xlsx")
dfb = dfFromExcel("b.xlsx")

dfc = dfJoin(dfa[['name','street','total']], dfb[['name','street','total']])
dfn = dfFromExcelValues('test.xlsx')
dfo = dfFromExcelValues('ontop.xlsx')
