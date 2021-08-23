# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 04:58:35 2021

@author: anass
"""


from PyPDF2 import PdfFileReader
import fitz
import csv
import cv2    
import numpy as np
import pytesseract
from statistics import mean
from pytesseract import Output
from pdf2image import convert_from_path
from difflib import SequenceMatcher
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pdf_path=r"C:\Users\anass\Programmation\PDF\p4.pdf"


def get_info(pdf_path): 
    pdf = PdfFileReader(pdf_path)
    
    pages =pdf.getNumPages()
    infos = pdf.documentInfo   
    author = infos.author
    creator = infos.creator
    producer = infos.producer
    subject = infos.subject
    title = infos.title
    
    return [pages, author, creator, producer, subject, title]


def extract_text(file, limit_perc=0.25):
    text_perc = get_text_percentage(file)
    if text_perc < limit_perc:
        return extract_from_pdf(file)
    else:
        return pdf_to_txt_ocr(file)

def get_text_percentage(file):
    """
    If the returned percentage of text is very low, the document is a scanned PDF
    """
    total_page_area = 0.0
    total_text_area = 0.0

    doc = fitz.open(file)

    for page_num, page in enumerate(doc):
        total_page_area += abs(page.rect)
        for b in page.getTextBlocks():
            if b[6] == 0:
                r = fitz.Rect(b[:4])  # rectangle where block text appears
                total_text_area += abs(r)
    return total_text_area / total_page_area 



def extract_from_pdf(file):
    text = ""
    doc = fitz.open(file)
    for page in doc:
        text += page.getText("Layout")
    text = text.replace('�', '')
    return text

def image_orientation_for_ocr(threshold_img):

    # threshold the image, setting all foreground pixels to

    thresh = threshold_img
    
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
    	angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
    	angle = -angle
        
    # rotate the image to deskew it
    (h, w) = thresh.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(thresh, M, (w, h),
    	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # show the output image
    # print("[INFO] angle: {:.3f}".format(angle))
    return rotated


def pdf_to_txt_ocr(pdfs,txt_path):
    L=[]
    G=[]
    pages = convert_from_path(pdfs, 350)
    for page in pages:
        good=total=0
        image = np.array(page) 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        last_image = image_orientation_for_ocr(threshold_img)
        custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_data(last_image, output_type = Output.DICT, config=custom_config, lang='fra')
        L.append(mean(list(map(float,details['conf']))))
        
        for word, conf in zip(details['text'], map(float, details['conf'])):
            good += (conf > 75)
            total += 1
            G.append(good/total)
        parse_text = []
        
        word_list = []
        
        last_word = ''
        for word in details['text']:
            if word!='':
                word_list.append(word)
                last_word = word
            if (last_word!='' and word == '') or (word==details['text'][-1]):
                parse_text.append(word_list)
                word_list = []
        with open(txt_path,  'a', newline="") as file:
                  csv.writer(file, delimiter=" ").writerows(parse_text)
            
    return mean(L),mean(G)

def detect_doublon(text1,text2):
    "detection de doublons avec SequenceMatcher"
    if SequenceMatcher(None, text1, text2).ratio() > 0.85:
        return True
    return False




import camelot.io as camelot

def extract_table(file,options='xlsx',printing= True,the_password=None,the_pages='all',to_compress=True,tables_list=None,all_in_csv=False):
    # PDF file to extract tables from (from command-line)
    # extract all the tables in the PDF file
    if the_password:
        tables = camelot.read_pdf(file, password=the_password , pages=the_pages)
    else:
        tables = camelot.read_pdf(file, pages=the_pages)
    
    # print the first table as Pandas DataFrame
    if printing :
        print("## Summary ########################################################")  
        print("Total tables extracted:", tables.n)
        for j in range(tables.n):
            print("-------------------------------------------------------------------")
            print("Details-table-{}".format(j+1) )
            print(tables[j].parsing_report)
            print("-- Full Table -----------------------------------------------------")
            print(tables[j].df)
        print("###################################################################")
    name = Path(file).stem 
    #options in [json, xlsx, html, markdown, sqlite] 
    #to_json, to_excel, to_html, to_markdown, to_sqlite, to_csv

    if all_in_csv :
        tables.export("{}.csv".format(name), f='csv', compress=to_compress)
    else :
        if tables_list:
            tables_list = [k-1 for k in tables_list]
        else:
            tables_list = range(tables.n)
            #we can use dictionnaries here
        if options == 'xlsx' :
            for j in tables_list: tables[j].to_excel("{}-{}.{}".format(name,j+1,options))
        elif options=='csv':
            for j in tables_list: tables[j].to_csv("{}-{}.{}".format(name,j+1,options))
        elif options=='markdown':
            for j in tables_list: tables[j].to_markdown("{}-{}.{}".format(name,j+1,options))
        elif options=='sqlite':
            for j in tables_list: tables[j].to_sqlite("{}-{}.{}".format(name,j+1,options))
        elif options=='json':
            for j in tables_list: tables[j].to_json("{}-{}.{}".format(name,j+1,options))
        elif options=='html':
            for j in tables_list: tables[j].to_html("{}-{}.{}".format(name,j+1,options))
              

import tabula
import pandas as pd

def extract_table_tabula(file):
    """might be much faster , to test though"""
    # Read pdf into a list of DataFrame
    dfs = tabula.read_pdf(file, pages='all')
    
    # convert PDF into CSV
    tabula.convert_into(file, "output.csv", output_format="csv", pages='all')
    
    df = pd.concat(dfs)
    df.to_excel("languages.xlsx") 
    # convert all PDFs in a directory
    #tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')
   
    name = Path(file).stem 
    # We'll define an Excel writer object and the target file
    Excelwriter = pd.ExcelWriter("{}.xlsx".format(name),engine="xlsxwriter")
    
    #We now loop process the list of dataframes
    for i, df in enumerate (dfs):
        df.to_excel(Excelwriter, sheet_name="Sheet-{}-{}".format(name,i+1),index=False)
    #And finally save the file
    Excelwriter.save()

import pikepdf # pip3 install pikepdf
   
def extract_links(file):
    # PdfFileReader
    pdf_file = pikepdf.Pdf.open(file)
    urls = []

    # iterate over PDF pages
    for page in pdf_file.pages:
        if page.get("/Annots") :
            for annots in page.get("/Annots"):
                if annots.get("/A"):
                    uri = annots.get("/A").get("/URI")
                    if uri is not None:
                        #print("[+] URL Found:", uri)
                        urls.append(str(uri))
            
    return urls


#############################method2----using Regex
import re

def extract_links_regex(text):
    # a regular expression of URLs
    url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\n]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
    urls = []
    # extract all urls using the regular expression
    for match in re.finditer(url_regex, text):
        url = match.group()
        print("[+] URL Found:", url)
        urls.append(url)
    return urls

###################################################

from pikepdf import Pdf, PdfImage

def extract_images_pike(file):
   """many errors, should be tested"""
   example = Pdf.open(file)
   for i,page in enumerate(example.pages) :
       rawimage = page.images['/Im0']
       pdfimage = PdfImage(rawimage)
       pdfimage.extract_to(fileprefix='image-{}'.format(i))
       



##################################################
import io
from PIL import Image
def extract_images(file):
    pdf_file = fitz.open(file)    
    # iterate over PDF pages
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            # save it to local disk
            image.save(open(f"image{page_index+1}_{image_index}.{image_ext}", "wb"))
        

###############################################################################
# importing required modules

import PyPDF2
 
 

def PDFmerge(pdfs, output):

    # creating pdf file merger object pdf merger class
    pdfMerger = PyPDF2.PdfFileMerger()
    # appending pdfs one by one
    for pdf in pdfs:
        pdfMerger.append(pdf)
    # writing combined pdf to output pdf file
    with open(output, 'wb') as f:
        pdfMerger.write(f)
 
 
def PDFsplit(pdf, splits):

    # creating input pdf file object
    name = Path(pdf).stem 
    splits=[i-1 for i in splits]
    pdfFileObj = open(pdf, 'rb')
    # creating pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # starting index of first slice
    start = 0
    # starting index of last slice
    end = splits[0]

    for i in range(len(splits)+1):
        # creating pdf writer object for (i+1)th split
        pdfWriter = PyPDF2.PdfFileWriter()
        # output pdf file name
        outputpdf = name+ str(start+1)+"-"+str(end) + '.pdf'
        # adding pages to pdf writer object
        for page in range(start,end):
            pdfWriter.addPage(pdfReader.getPage(page))
        # writing split pdf pages to pdf file
        with open(outputpdf, "wb") as f:
            pdfWriter.write(f)
        # interchanging page split start position for next split
        start = end
        try:
            # setting split end position for next split
            end = splits[i+1]
        except IndexError:
            # setting split end position for last split
            end = pdfReader.numPages
    # closing the input pdf file object

    pdfFileObj.close()

def PDFsplit2(pdf, pages): 
    """We need to verify the index"""
    pages=[i-1 for i in pages]
    # splits is the list of pages positions (starting from 1)
    name = Path(pdf).stem 
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    if set(pages).issubset(set(range(pdfReader.getNumPages()))):
        pdfWriter = PyPDF2.PdfFileWriter()
        # output pdf file name
        outputpdf = name+ "-split" + '.pdf'
        # adding pages to pdf writer object
        for page in pages:
            pdfWriter.addPage(pdfReader.getPage(page))
        # writing split pdf pages to pdf file
        with open(outputpdf, "wb") as f:
            pdfWriter.write(f)
        pdfFileObj.close()
    else :
        #we might change here
        pdfFileObj.close()
        raise IndexError()
                
####################################################################
#water_mark

def add_watermark(wmFile, pdf,pages):
    """takes water mark pdf, we can add the option of image but we will have to deal with the positionning"""
    pages=[i-1 for i in pages]
    # opening watermark pdf file
    wmFileObj = open(wmFile, 'rb')
    pdfReaderwater = PyPDF2.PdfFileReader(wmFileObj) 

    # creating pdf File object of original pdf
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
    name = Path(pdf).stem 
    newFileName = "watermarked_" + name + ".pdf"
    pdfWriter = PyPDF2.PdfFileWriter()
    
    for page in range(pdfReader.numPages):
        pageObj= pdfReader.getPage(page)
        if page in pages :
        # creating watermarked page object
            pageObj.mergePage(pdfReaderwater.getPage(0))
            pdfWriter.addPage(pageObj)
        else :
            pdfWriter.addPage(pageObj)
     
    newFile = open(newFileName, 'wb')
    pdfWriter.write(newFile)

    # closing the watermark pdf file object
    wmFileObj.close()
    pdfFileObj.close()
    newFile.close()
 

###############################################################################

###############################################################################
file = r"C:\Users\anass\Programmation\PDF\p2.pdf"   
#extract_table(file)

extract_images_pike(file)



