from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

WIDTH, HEIGHT = letter
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
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Projects")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)

    #each project
    top-=inch/6
    for project in info["Projects"]:
        #project name
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN+inch/4, top, project["name"])
        c.setFont("Helvetica", 9)
        
        #description
        for line in project["description"]:
            top-=inch/6
            c.drawString(MARGIN+inch/3, top,"• "+line)
        top-=inch/6
    return top+inch/20

'''
adds experience with position, company, descripton, dates
returns new bottom
'''
def experience(c:canvas.Canvas, info:dict, top:float):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    r, g, b = ACCENT
    c.setFillColorRGB(r, g, b)
    c.setStrokeColorRGB(r, g, b)
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Experience")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)

    #each project
    top-=inch/6
    for xp in info["Experience"]:
        #project name
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN+inch/4, top, xp["position"])
        c.setFont("Helvetica", 9)
        
        #description
        for line in xp["description"]:
            top-=inch/6
            c.drawString(MARGIN+inch/3, top,"• "+line)
        top-=inch/6
    return top+inch/20


'''
adds education with university, major, gpa, expected grad 
returns new bottom
'''
def education(c:canvas.Canvas, info:dict, top:float):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    r, g, b = ACCENT
    c.setFillColorRGB(r, g, b)
    c.setStrokeColorRGB(r, g, b)
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Education")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)
    
    #university name - bold, black
    top-=inch/6
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN+inch/4, top, info["Education"]["school"])
    
    #expected grad - bold
    c.drawRightString(WIDTH-MARGIN, top, "Expected Graduation: "+info["Education"]["graduation"])

    #major, gpa - small
    c.setFont("Helvetica", 9)
    top-=inch/6
    c.drawString(MARGIN+inch/3, top, info["Education"]["degree"]+" | "+info["Education"]["gpa"])
    
    return top-inch/12




'''
adds certifications with certifier, list of certs 
returns new bottom
'''
def certifications(c:canvas.Canvas, info:dict, top:float):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    r, g, b = ACCENT
    c.setFillColorRGB(r, g, b)
    c.setStrokeColorRGB(r, g, b)
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Certifications")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)
    
    
    
    c.setFillColorRGB(0, 0, 0)
    for cert in info["Certifications"]:
        #certifier - bold, black
        top-=inch/6
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN+inch/4, top, cert["certifier"])

        #list of certs - small
        c.setFont("Helvetica", 9)
        certs = ', '.join(cert["certifications"])
        c.drawRightString(WIDTH-MARGIN, top, certs)

    return top-inch/12




'''
using info from info dict, assembles and writes pdf
'''
def create_pdf(filename:str, info:dict)->None:
    
    c = canvas.Canvas(filename, pagesize = letter)
    bottom = header(c, info)    
    bottom = skills(c, info, bottom)
    bottom = experience(c, info, bottom)
    bottom = education(c, info, bottom)
    bottom = projects(c, info, bottom)
    bottom = certifications(c, info, bottom)
    print(bottom)
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