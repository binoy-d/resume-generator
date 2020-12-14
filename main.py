from reportlab.pdfgen import canvas
from reportlab.lib.units import cm






def main():
    c = canvas.Canvas("./hello.pdf")
    c.drawString(2*cm, 22*cm, "Hello World!")
    c.showPage()
    c.save()
    print("wassup")

if __name__ == '__main__':
    main()