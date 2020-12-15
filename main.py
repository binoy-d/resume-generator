from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

WIDTH, HEIGHT = A4
MARGIN = inch/2
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
    c.setFont("Helvetica-Bold", 20)
    #name
    c.drawCentredString(WIDTH/2,HEIGHT-inch, info["Info"]["name"])
    
    #smaller font
    c.setFont("Helvetica", 10)
    #linkedin - left
    c.drawString(MARGIN, HEIGHT-inch/1.5, info["Info"]["linkedin"])
    #github - right
    c.drawRightString(WIDTH-MARGIN, HEIGHT-MARGIN, info["Info"]["github"])
    #contact info - center below name
    contact = info["Info"]["email"]+" | "+info["Info"]["phone-number"]+" | "+info["Info"]["site"]
    c.drawCentredString(WIDTH/2,HEIGHT-(inch*1.25),contact)
    #canvas.drawRightString(x, y, text), drawString(x, y, text)
    
'''
add skills section, starting from top
'''
def skills(c:canvas.Canvas, info:dict, top:float):
    c.setFont("Helvetica-Bold", 12)
    #header - left - red - line below
    c.setFillColorRGB(196/255, 34/255, 51/255)
    c.drawString(MARGIN, top-inch/4, "Skills")


'''
using info from info dict, assembles and writes pdf
'''
def create_pdf(filename:str, info:dict)->None:
    
    c = canvas.Canvas(filename, pagesize = A4)
    header(c, info)    
    skills(c, info, HEIGHT-(inch*1.25))

    c.showPage()
    c.save()

def main():
    info = loadInfo("./info.json")
    print("loaded info for ", info["Info"]["name"])
    create_pdf("./hello.pdf", info)

if __name__ == '__main__':
    main()


'''
c.setStrokeColorRGB(0.2,0.5,0.3)
c.setFillColorRGB(1,0,1)
# draw some lines
c.line(0,0,0,1.7*inch)
'''