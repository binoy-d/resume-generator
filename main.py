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
    c.setFont("Helvetica-Bold", 20)
    #name
    c.drawCentredString(width/2,height-inch, info["Info"]["name"])
    
    #smaller font
    c.setFont("Helvetica", 10)
    #linkedin - left
    c.drawString(inch/2, height-inch/2, info["Info"]["linkedin"])

    #github - right
    c.drawRightString(width-inch/2, height-inch/2, info["Info"]["github"])

    #canvas.drawRightString(x, y, text), drawString(x, y, text)
    


'''
using info from info dict, assembles and writes pdf
'''
def create_pdf(filename:str, info:dict)->None:
    
    c = canvas.Canvas(filename, pagesize = A4)
    c.setFont("Helvetica", 14)

    '''
    c.setStrokeColorRGB(0.2,0.5,0.3)
    c.setFillColorRGB(1,0,1)
    # draw some lines
    c.line(0,0,0,1.7*inch)
    '''
    header(c, info)    
    c.showPage()
    c.save()

def main():
    info = loadInfo("./info.json")
    print("loaded info for ", info["Info"]["name"])
    create_pdf("./hello.pdf", info)

if __name__ == '__main__':
    main()