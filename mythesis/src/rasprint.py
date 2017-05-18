from escpos import *

def raspout(essid="wifiname",username="joshua.w",password="matriux"):
	#Epson = escpos.Escpos(0x0416,0x5011,0)
	Epson = printer.Usb(0x0416,0x5011,0)
	Epson.text("ESSID: %s\nusername: %s\npassword: %s"
                % (essid,username,password))
	#Epson.image("logo.gif")
	Epson.barcode
	Epson.barcode('\n1324354657687','EAN13',64,2,'','')
	Epson.cut()

if __name__ == '__main__':
	raspout()
