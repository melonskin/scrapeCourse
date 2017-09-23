from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import os
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdfFile)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    return content

# for pdfFile in os.listdir(os.path.join(os.getcwd(),"Fall2016")):
#     outputString = readPDF(pdfFile)
#     with open(os.path.join(os.getcwd(),"Fall2016",os.path.basename(pdfFile),'.txt'), "w") as text_file:
#         text_file.write(outputString)
#     pdfFile.close()
#     break

pdfFile = urlopen("https://web-as.tamu.edu/gradereport/PDFReports/20161/grd20161EN.pdf")
outputString = readPDF(pdfFile)
# outputString[:1000]
with open('test.txt','w') as text_file:
    text_file.write(outputString)
# with open(os.path.join(os.getcwd(),"Fall2016",os.path.basename(pdfFile),'.txt'), "w") as text_file:
#       text_file.write(outputString)
pdfFile.close()