from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
import json
#https://www.reportlab.com/docs/reportlab-userguide.pdf

'''
loads info from json file
'''
def loadInfo(filename:str)->dict:
    with open(filename, "r") as fp:
        return json.load(fp)



'''
adds header with name, links, and contact info
'''
def header(c:canvas.Canvas, info:dict):
    width, height = A4
    c.drawString(width/2,height-inch, info["Info"]["name"])


'''
using info from info dict, assembles and writes pdf
'''
def create_pdf(filename:str, info:dict)->None:
    
    c = canvas.Canvas(filename, pagesize = A4)
    header(c, info)    
    c.showPage()
    c.save()

def main():
    info = loadInfo("./info.json")
    print("loaded info for ", info["Info"]["name"])
    create_pdf("./hello.pdf", info)

if __name__ == '__main__':
    main()