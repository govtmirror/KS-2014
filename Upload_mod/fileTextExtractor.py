#
# Copyright 2014 National MEdiation Board.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import zipfile, re
import pdf_miner_app_engine as pdf_miner
import xlrd
        
import logging


def to_unicode_or_bust(obj, encoding='utf-8'):

    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
          
    return obj

def extractTextFromFile(activeFile, activeFileName):
    """
    extract text from different types of files
    """
   
    extension = os.path.splitext(activeFileName)[1]
    logging.info(extension)
    
    if extension == ".docx":
        try:       
            # a docx file is a zip file so first unzip it
            docx = zipfile.ZipFile(activeFile)       
            
            # then read the file that has the actual text in  it
            content = docx.read('word/document.xml')
            
            # now replace all of the xml tags with nothing, we're left with just the text
            rawText = re.sub('<(.|\n)*?>','',content)         
          
            text_uni = to_unicode_or_bust(rawText)         
            #rawText = text_uni.encode('utf-8')
            
            return text_uni
        except:
            logging.info("An error occurred processing the file: %s" % activeFileName)
            return ""

    elif extension == ".pdf": 
        try:
            pdf = activeFile.read()      
            text = pdf_miner.pdf_to_text(pdf)
            text_uni = to_unicode_or_bust(text)
            #rawText = text_uni.encode('utf-8')
            return text_uni
        except:
            logging.info("An error occurred processing the file: %s" % activeFileName)
            return ""
 
    elif extension == ".xls" or extension == ".xlsx" :
        try:
            excelData = activeFile.read()       
            
            book = xlrd.open_workbook(file_contents=excelData)
 
            rawText = ""      
            for sheet in book.sheets():
                #iterate over all rows in spreadsheet 
                #note: the rows and columns are zero indexed
                #ie: resultStr = "Cell D30 is %s" % sh.cell_value(rowx=29, colx=3)  
                for rx in range(sheet.nrows):
                    #iterate over all columns in spreadsheet 
                    for col in range(0,sheet.ncols):      
                        cellVal = sheet.cell_value(rowx=rx, colx=col) or "" 
                        
                        #numeric integer values in Excel are actually stored as floats,
                        #i.e. 50 is stored as 50.0
                        #let's assume anything that comes back with a ".0" on the end is 
                        #an integer and strip off the ".0"
                        if isinstance(cellVal, float):
                            if cellVal.is_integer():
                                cellVal = int(cellVal)
 
                        rawText = rawText + " %s" % cellVal        
            
            return rawText
        except:
            logging.info("An error occurred processing the file: %s" % activeFileName)
            return "" 

    else:
        logging.info("Sorry, unhandled file type: %s.  Can't extract text." % extension)
    
    