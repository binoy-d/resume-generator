from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

WIDTH, HEIGHT = A4
MARGIN = inch/2

ACCENT = (196/255, 34/255, 51/255)


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
returns bottom
'''
def header(c:canvas.Canvas, info:dict)->float:
    c.setFont("Helvetica-Bold", 20)
    #name
    c.drawCentredString(WIDTH/2,HEIGHT-inch, info["Info"]["name"])
    
    #smaller font
    c.setFont("Helvetica", 10)
    #linkedin - left
    c.drawString(MARGIN, HEIGHT-MARGIN, info["Info"]["linkedin"])
    #github - right
    c.drawRightString(WIDTH-MARGIN, HEIGHT-MARGIN, info["Info"]["github"])
    #contact info - center below name
    contact = info["Info"]["email"]+" | "+info["Info"]["phone-number"]+" | "+info["Info"]["site"]
    c.drawCentredString(WIDTH/2,HEIGHT-(inch*1.25),contact)
    #canvas.drawRightString(x, y, text), drawString(x, y, text)
    return HEIGHT-(inch*1.25)

'''
add skills section, starting from top
returns bottom
'''
def skills(c:canvas.Canvas, info:dict, top:float)->float:
    c.setFont("Helvetica-Bold", 12)
    #header - left - red - line below
    r, g, b = ACCENT
    c.setFillColorRGB(r, g, b)
    c.setStrokeColorRGB(r, g, b)
    c.drawString(MARGIN, top-MARGIN/4, "Skills")
    c.line(MARGIN,top-inch/6,WIDTH-MARGIN,top-inch/6)

    #software development - black - bold
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN+inch/4, top-inch/3, "Software Development")

    #proficient
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN+inch/2, top-inch/2, "Proficient: ")
    skills = ", ".join(info["Skills"]["Software Development"]["Proficient"])
    c.drawRightString(WIDTH-MARGIN, top-inch/2, skills)

    #familiar
    c.drawString(MARGIN+inch/2, top-inch/1.5, "Familiar: ")
    skills = ", ".join(info["Skills"]["Software Development"]["Familiar"])
    c.drawRightString(WIDTH-MARGIN, top-inch/1.5, skills)

    #other - black - bold
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN+inch/4, top-inch/1.2, "Other")

    #other skills list - small
    c.setFont("Helvetica", 9)
    skills = ", ".join(info["Skills"]["Other"])
    c.drawRightString(WIDTH-MARGIN, top-inch/1.2, skills)

    return top-inch/1.1 #the new bottom

'''
adds projects with name, descripton, link
returns new bottom
'''
def projects(c:canvas.Canvas, info:dict, top:float):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    r, g, b = ACCENT
    c.setFillColorRGB(r, g, b)
    c.setStrokeColorRGB(r, g, b)
    c.drawString(MARGIN, top-MARGIN/4, "Projects")
    c.line(MARGIN,top-inch/6,WIDTH-MARGIN,top-inch/6)
    top-=inch/3
    for project in info["Projects"]:
        #software development - black - bold
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 10)
        top-=inch/40
        c.drawString(MARGIN+inch/4, top, project["name"])
        c.setFont("Helvetica", 9)
        top-=inch/6
        for line in project["description"]:
            c.drawString(MARGIN+inch/3, top,"• "+line)
            top-=inch/6
    return top



'''
using info from info dict, assembles and writes pdf
'''
def create_pdf(filename:str, info:dict)->None:
    
    c = canvas.Canvas(filename, pagesize = A4)
    bottom = header(c, info)    
    bottom = skills(c, info, bottom)
    bottom = projects(c, info, bottom)
    
    
    c.showPage()
    c.save()

def main():
    info = loadInfo("./info.json")
    print("loaded info for ", info["Info"]["name"])
    create_pdf("./hello.pdf", info)

if __name__ == '__main__':
    main()


'''
c.line(0,0,0,1.7*inch)
'''