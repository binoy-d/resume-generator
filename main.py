from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab import platypus
from  reportlab.lib.styles import ParagraphStyle as PS
from reportlab.platypus import SimpleDocTemplate
import json
import sys

WIDTH, HEIGHT = letter
MARGIN = inch/2

'''
sets the theme lol
'''
def getTheme(theme:dict) -> dict:
    if theme["mode"] == "light":
        back = [int(i) for i in theme["light"].split(",")]
        front = [int(i) for i in theme["dark"].split(",")]
    else:
        back = [int(i) for i in theme["dark"].split(",")]
        front = [int(i) for i in theme["light"].split(",")]
    accent = [int(i) for i in theme["accent"].split(",")]
    return {"back":tuple(back), "front":tuple(front), "accent":tuple(accent)}


'''
loads info from json file
'''
def loadInfo(filename:str)->dict:
    with open(filename, "r") as fp:
        return json.load(fp)




'''
takes tuple of form (r, g, b)
where r, g, and b are between 0 and 255
and sets fill and stroke color

'''
def setColor(c:canvas.Canvas, color:tuple):
    r, g, b = color
    c.setFillColorRGB(r/255, g/255, b/255)
    c.setStrokeColorRGB(r/255, g/255, b/255)


'''
adds header with name, links, and contact info
returns bottom
'''
def header(c:canvas.Canvas, info:dict,theme:dict, top=HEIGHT-MARGIN )->float: 
    #smaller font, italic, red
    c.setFont("Helvetica-Oblique", 10)
    setColor(c, theme['accent'])

    #linkedin - left
    c.drawString(MARGIN, top, info["Info"]["linkedin"])
    c.linkURL("https://"+info["Info"]["linkedin"],(MARGIN, top,MARGIN+c.stringWidth(info["Info"]["linkedin"]),top+10))

    #github - right
    c.drawRightString(WIDTH-MARGIN, HEIGHT-MARGIN, info["Info"]["github"])
    c.linkURL("https://"+info["Info"]["github"],(WIDTH-MARGIN-c.stringWidth(info["Info"]["github"])-3, top,WIDTH-MARGIN,top+10))
    
    #name
    setColor(c, theme['front'])
    top-=inch/3
    c.setFont("Helvetica-Bold", 20)
    c.drawRightString(WIDTH/2-2,top, info["Info"]["name"][0]) #first
    setColor(c, theme['accent'])
    c.drawString(WIDTH/2+2, top, info["Info"]["name"][1]) #last

    x1 = WIDTH/2 - c.stringWidth(info["Info"]["name"][0])
    x2 = WIDTH/2 + c.stringWidth(info["Info"]["name"][1])
    c.linkURL("https://"+info["Info"]["site"],(x1,top,x2,top+20))

    #contact info - center below name
    top-=20 #size of name
    setColor(c, theme['front'])
    c.setFont("Helvetica", 10)
    contact = info["Info"]["email"]+" | "+info["Info"]["phone-number"]+" | "+info["Info"]["site"]
    c.drawCentredString(WIDTH/2,top,contact)

    #link site
    x2 = (WIDTH+c.stringWidth(contact))/2
    x1 = x2-c.stringWidth(info["Info"]["site"])
    c.linkURL("https://"+info["Info"]["site"],(x1,top,x2,top+10))

    #link email
    x1 = (WIDTH-c.stringWidth(contact))/2
    x2 = x1+c.stringWidth(info["Info"]["email"])
    c.linkURL("mailto:"+info["Info"]["email"],(x1,top,x2,top+10))

    #canvas.drawRightString(x, y, theme['front']), drawString(x, y, theme['front'])
    return top-inch/20

'''
add skills section, starting from top
returns bottom
'''
def skills(c:canvas.Canvas, info:dict, top:float, theme:dict)->float:
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    setColor(c, theme['accent'])
    
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Skills")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)
    
    #software development - black - bold
    top-=inch/6
    setColor(c, theme['front'])
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN+inch/4, top, "Software Development")

    
    #proficient
    top-=inch/6
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN+inch/2, top, "Proficient: ")
    skills = ", ".join(info["Skills"]["Software Development"]["Proficient"])
    c.drawRightString(WIDTH-MARGIN, top, skills)

    #familiar
    top-=inch/6
    c.drawString(MARGIN+inch/2, top, "Familiar: ")
    skills = ", ".join(info["Skills"]["Software Development"]["Familiar"])
    c.drawRightString(WIDTH-MARGIN, top, skills)

    #other - black - bold
    top-=inch/6
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN+inch/4, top, "Other")

    #other skills list - small
    c.setFont("Helvetica", 9)
    skills = ", ".join(info["Skills"]["Other"])
    c.drawRightString(WIDTH-MARGIN, top, skills)

    return top-inch/20 #the new bottom

'''
adds projects with name, descripton, link
returns new bottom
'''
def projects(c:canvas.Canvas, info:dict, top:float, theme:dict):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)

    setColor(c, theme['accent'])
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Projects")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)

    #each project
    top-=inch/6
    for project in info["Projects"]:
        #title
        setColor(c, theme['front'])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN+inch/4, top, project["name"])
          
        #link
        c.setFont("Helvetica-Oblique", 9)
        setColor(c, theme['accent'])
        c.drawRightString(WIDTH-MARGIN, top, project["link"])
        x1 = WIDTH-MARGIN-c.stringWidth(project["link"])
        x2 = WIDTH-MARGIN
        c.linkURL("https://"+project["link"], (x1, top, x2, top+9))



        #description
        c.setFont("Helvetica", 9)
        setColor(c, theme['front'])
        for line in project["description"]:
            top-=inch/6
            c.drawString(MARGIN+inch/3, top,"• "+line)
        top-=inch/6
    return top+inch/20

'''
adds experience with position, company, descripton, dates
returns new bottom
'''
def experience(c:canvas.Canvas, info:dict, top:float, theme:dict):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    setColor(c, theme['accent'])
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Experience")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)

    #each xp
    top-=inch/6
    for xp in info["Experience"]:
        #position
        setColor(c, theme['front'])
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN+inch/4, top, xp["position"]+" ")

        #dates
        c.drawRightString(WIDTH-MARGIN,top, xp["start"]+"-"+xp["end"])

        #company
        top-=inch/6
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN+inch/4, top,xp["company"])


        #location
        c.setFont("Helvetica-Oblique", 9)
        c.drawRightString(WIDTH-MARGIN,top, xp["location"])

        
        
        #description
        setColor(c, theme['front'])
        c.setFont("Helvetica", 9)
        for line in xp["description"]:
            top-=inch/6
            c.drawString(MARGIN+inch/3, top,"• "+line)
        top-=inch/6
    
    return top+inch/20 #pull back up a little


'''
adds education with university, major, gpa, expected grad 
returns new bottom
'''
def education(c:canvas.Canvas, info:dict, top:float, theme:dict):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    setColor(c, theme['accent'])
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Education")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)
    
    #university name - bold, black
    top-=inch/6
    setColor(c, theme['front'])
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
def certifications(c:canvas.Canvas, info:dict, top:float, theme:dict):
    #header - left - red - line below
    c.setFont("Helvetica-Bold", 12)
    setColor(c, theme['accent'])
    top-=MARGIN/4
    c.drawString(MARGIN, top, "Certifications")
    top-=inch/12
    c.line(MARGIN,top,WIDTH-MARGIN,top)
    
    
    
    setColor(c, theme['front'])
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



def background(c, theme):
    setColor(c, theme['back'])
    c.rect(-20,-20,WIDTH+40,HEIGHT+40,fill=1)



'''
using info from info dict, assembles and writes pdf
'''
def create_pdf(filename:str, info:dict, theme:dict)->None:
    c = canvas.Canvas(filename, pagesize = letter)
    background(c, theme)
    bottom = header(c, info, theme)    
    bottom = skills(c, info, bottom, theme)
    bottom = experience(c, info, bottom, theme)
    bottom = education(c, info, bottom, theme)
    bottom = projects(c, info, bottom, theme)
    bottom = certifications(c, info, bottom, theme)
    print(bottom)
    c.showPage()
    c.save()




def main():
    print(sys.argv)
    info = loadInfo("./info.json")
    if len(sys.argv)>=2:
        info["Theme"]["mode"] = sys.argv[1] #'light' or 'dark'

    theme = getTheme(info["Theme"])

   
    
    print("loaded info for ", info["Info"]["name"])
    create_pdf("./resume.pdf", info, theme)
    print("done")

if __name__ == '__main__':
    main()

