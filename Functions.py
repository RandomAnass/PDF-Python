# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 04:58:35 2021

@author: anass
"""


from PyPDF2 import PdfFileReader , PdfFileWriter
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
import os

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
        return pdf_to_txt_ocr(file)
    else:
        return extract_from_pdf(file)

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

def image_orientation_for_ocr(image):

    gray = cv2.bitwise_not(image)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
    	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] 
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
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
    	flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE) 
    # draw the correction angle on the image so we can validate it
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))

    return rotated



def pdf_to_txt_ocr(pdfs):
    L=[]
    G=[]
    pages = convert_from_path(pdfs, 350)
    for page in pages:
        good=total=0
        image = np.array(page) 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        before_tresh= image_orientation_for_ocr(gray_image)
        threshold_img = cv2.threshold(before_tresh, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_data(threshold_img, output_type = Output.DICT, config=custom_config, lang='fra')
        L.append(mean(list(map(float,details['conf']))))
        
        for word, conf in zip(details['text'], map(float, details['conf'])):
            good += (conf > 75)
            total += 1
            G.append(good/total)
        parse_text = ""
        
        word_list = []
        
        last_word = ''
        for word in details['text']:
            if word!='':
                word_list.append(word)
                last_word = word
            if (last_word!='' and word == '') or (word==details['text'][-1]):
                parse_text+= ' '.join(word_list) +'\n'
                word_list = []
        #return mean(L),mean(G)
        return parse_text

    

def detect_doublon(text1,text2):
    "detection de doublons avec SequenceMatcher"
    if SequenceMatcher(None, text1, text2).ratio() > 0.85:
        return True
    return False




import camelot.io as camelot

def extract_table(file,options='xlsx',printing= True,the_password=None,the_pages='all',tables_list=None):
    # PDF file to extract tables from (from command-line)
    # extract all the tables in the PDF file
    if the_password:
        tables = camelot.read_pdf(file, password=the_password , pages=the_pages)
    else:
        tables = camelot.read_pdf(file, pages=the_pages)
    
    # print the first table as Pandas DataFrame
    name = os.path.splitext(file)[0]
    if printing :
        text=''
        text+="Summary :" +"\n"  
        text+="Total tables extracted: {}".format(tables.n) + "\n"
        for j in range(tables.n):
            text+="-------------------------------------------------------------------"+ "\n"
            text+="Details-table-{}".format(j+1) + "\n"
            text+=str(tables[j].parsing_report)+ "\n"
            text+="Full Table :"+ "\n"
            text+=str(tables[j].df)+ "\n"
        text+="-------------------------------------------------------------------" +'\n'
        text+= "The output is saved in : {} ".format(name)
    #options in [json, xlsx, html, markdown, sqlite] 
    #to_json, to_excel, to_html, to_markdown, to_sqlite, to_csv

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
    elif options=='compressed':
        tables.export("{}_tables.csv".format(name), f='csv', compress=True)
    if printing :
        return text


import tabula
import pandas as pd

def extract_table_tabula(file):
    """might be much faster , to test though"""
    # Read pdf into a list of DataFrame
    dfs = tabula.read_pdf(file, pages='all')
    
    # convert PDF into CSV
    # tabula.convert_into(file, "output.csv", output_format="csv", pages='all')
    
    df = pd.concat(dfs)
    #df.to_excel("languages.xlsx") 
    # convert all PDFs in a directory
    #tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')
   
    name = os.path.splitext(file)[0]  
    # We'll define an Excel writer object and the target file
    Excelwriter = pd.ExcelWriter("{}.xlsx".format(name),engine="xlsxwriter")
    name2 = Path(file).stem 
    #We now loop process the list of dataframes
    for i, df in enumerate (dfs):
        df.to_excel(Excelwriter, sheet_name="Sheet-{}-{}".format(name2,i+1),index=False)
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
    text =''
    for page_index in range(len(pdf_file)):
        # get the page itself
        page = pdf_file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            text+="[+] Found a total of {} images in page {}".format(len(image_list),page_index)
            text+="\n"
        else:
            text+="[!] No images found on page {}".format( page_index)
            text+="\n"
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
    return text
        

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
    #Overlaying Pages
    pages=[i-1 for i in pages]
    # opening watermark pdf file
    wmFileObj = open(wmFile, 'rb')
    pdfReaderwater = PyPDF2.PdfFileReader(wmFileObj) 

    # creating pdf File object of original pdf
    pdfFileObj = open(pdf, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    name = Path(pdf).stem 
    newFileName = os.path.dirname(pdf)+"/watermarked_" + name + ".pdf"
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


#pdfReader = PyPDF2.PdfFileReader(open('encrypted.pdf', 'rb'))
#pdfReader.isEncrypted
#pdfReader.decrypt('rosebud')


#encryption

def encrypt_PDF(file, password):
    pdf_in_file = open(file,'rb')  
    pdf= PdfFileReader(pdf_in_file)
    print(pdf.isEncrypted)
    output = PdfFileWriter()
    for i in range(pdf.numPages):
    	output.addPage(pdf.getPage(i))
    	output.encrypt(password)
    
    with open(Path(file).stem + "_encrypted" +".pdf", "wb") as outputStream:
        output.write(outputStream)
        
    pdf_in_file.close()
    

def decrypted_PDF(file, password):
    pdf_in_file = open(file,'rb')  
    pdf= PdfFileReader(pdf_in_file)
    print(pdf.isEncrypted)
    if pdf.isEncrypted :
        pdf.decrypt(password)
        output = PdfFileWriter()
        for i in range(pdf.numPages):
        	output.addPage(pdf.getPage(i))
    
        with open(Path(file).stem + "_decrypted" +".pdf", "wb") as outputStream:
            output.write(outputStream)
            
        pdf_in_file.close()
    else:
    # If file is not encrypted
        print("File already decrypted.")



###############################################################################


import img2pdf

# storing image path
img_path = "C:/Users/Admin/Desktop/GfG_images/do_nawab.png"

def image2pdf(img_path):
    image = Image.open(img_path)
    # converting into chunks using img2pdf
    pdf_bytes = img2pdf.convert(image.filename)
    # opening or creating pdf file
    name = Path(img_path).stem 
    file = open(name+ ".pdf", "wb")
    
    # writing pdf files with chunks
    file.write(pdf_bytes)
    # closing
    image.close()
    file.close()


#rom pdf2image import convert_from_path


# Store Pdf with convert_from_path function
def pdf_to_image(file,image_type):
    """we can add other options"""
    #convert_from_path( pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt="ppm", jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, single_file=False, output_file=uuid_generator(), poppler_path=None, grayscale=False, size=None, paths_only=False, hide_annotations=False,
    #image_type in ['ppm', 'jpeg', 'png', 'tiff']
    images = convert_from_path(file,fmt=image_type)
    name = Path(file).stem 
    for i in range(len(images)):
    	# Save pages as images in the pdf
    	images[i].save(name+ '-'+'page'+'-'+ str(i+1) +'.'+ image_type, image_type.upper())

# importing the modules
import pyttsx3

def pdf_to_audio(path,pages,saying=True,saving=True):
    pages=[i-1 for i in pages]
    name = Path(path).stem 
    # path of the PDF file
    pdf = open(path, 'rb')
    # creating a PdfFileReader object
    pdfReader = PdfFileReader(pdf)
    text=""
    for page in pages :
        from_page = pdfReader.getPage(page) 
        # extracting the text from the PDF
        text += from_page.extractText() 
    # reading the text
    pdf.close()
    speak = pyttsx3.init()
    if saving:
        speak.save_to_file(text , name+'.mp3')
    if saying :
        speak.say(text)

    speak.runAndWait()
    

from pdf2docx import Converter

pdf_file = '/path/to/sample.pdf'
docx_file = 'path/to/sample.docx'

def pdf_to_doc(pdf_file,password=None,starting=None,ending=None):
    # convert pdf to docx
    name = Path(pdf_file).stem 
    if password:
        cv = Converter(pdf_file, password)
    else:
        cv = Converter(pdf_file)
    if starting and ending : 
        cv.convert(name+'.docx', start=starting, end=ending)
    elif starting:
        cv.convert(name+'.docx', start=starting)
    elif ending:
        cv.convert(name+'.docx' , end=ending)
    else:
        cv.convert(name+'.docx')      # all pages by default
    #tom make it faster cv.convert(docx_file, multi_processing=True)
    cv.close()
        
import comtypes.client


def doc_to_pdf(in_file):
    wdFormatPDF = 17
    name = os.path.splitext(in_file)[0] 
    out_file = name+".pdf"
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()

# Import Module
from win32com import client

def excel_to_pdf2(file):
    "probably doesnt work in Linux"
    name = os.path.splitext(file)[0] 
    # Open Microsoft Excel
    excel = client.Dispatch("Excel.Application")
    
    # Read Excel File
    sheets = excel.Workbooks.Open(file)
    work_sheets = sheets.Worksheets[0]
    
    # Convert into PDF File
    work_sheets.ExportAsFixedFormat(0, name+'.pdf')


def excel_to_pdf(in_file):

    name = os.path.splitext(in_file)[0] 
    out_file = name+".pdf"
    excel = comtypes.client.CreateObject('Excel.Application')
    excel.Visible = False
    doc = excel.Workbooks.Open(in_file)
    doc.ExportAsFixedFormat(0, out_file, 1, 0)
    doc.Close()
    excel.Quit()

import pdftotree



def pdf_to_html(pdf_file):
    name = Path(pdf_file).stem +'.html' 
    pdftotree.parse(pdf_file, html_path=name, model_type=None, model_path=None, visualize=False)

import pdfkit
from urllib.parse import urlparse


def html_to_pdf(file_path,file_type):
    """not working for urls """
    #file_type in "url", "file", "text"
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    if file_type=="url":     
        domain = urlparse(file_path).netloc
        pdfkit.from_url(file_path, domain + '.pdf',configuration=config)
    elif file_type=="file":
        name = Path(file_path).stem +'.html' 
        pdfkit.from_file(file_path, name,configuration=config)
    # we may add folders too
    #    pdfkit.from_url(['google.com', 'yandex.ru', 'engadget.com'], 'out.pdf')
    #    pdfkit.from_file(['file1.html', 'file2.html'], 'out.pdf')
        

################################################################################

#encrypt_PDF(file, "joe*°122256")

#PDFsplit2(pdfs,[1])
