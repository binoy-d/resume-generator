from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import json


'''
loads info from json file
'''
def loadInfo(filename:str)->dict:
    with open(filename, "r") as fp:
        return json.load(fp)


def main():
    c = canvas.Canvas("./hello.pdf")
    c.drawString(2*cm, 22*cm, "Hello World!")
    c.showPage()
    c.save()
    print("wassup")

if __name__ == '__main__':
    info = loadInfo("./info.json")
    print(info["Info"]["name"])
    main()