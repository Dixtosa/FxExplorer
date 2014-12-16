#! /usr/bin/python
# --encoding: utf-8

# Author:       Dixtosa
# Dependencies: sympy and wx

try:
	import wx
except:
	print "wxPython library is needed. Quitting..."
	quit()
app = wx.App()

from _Info import *
from math import *
try:
	import sympy
except:
	wx.MessageBox("The library sympy is not found! \n Some of the functions won't work")

import sys
###########################################################################################################
def formatFloat(number, pre = 1):
	return ("{:6."+str(pre)+"f}").format(number)

def INFINITY():
	return u"\u221E"
###########################################################################################################

class FxExplorerFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title,(0,0), wx.Size(1024, 768))
		self.SetWindowVariant(wx.WINDOW_VARIANT_NORMAL)
		self.p1 = wx.Panel(self,-1,(0,0),wx.Size(800,1000))
		self.p2 = wx.Panel(self,-1,(800,0),wx.Size(1000,1000))
		
		self.RED_FX = []
		self.BLUE_FX = []
		self.GREEN_FX = []
		
		self.GRAY_FX = []
		self.BLACK_FX = []
		self.BROWN_FX = []
		self.BLACK_FX = []
		
		self.CENTRE_X = 400
		self.CENTRE_Y = 400

		self.f10 = wx.Font(10,wx.FONTFAMILY_DEFAULT,wx.NORMAL,wx.NORMAL)
		
		self.setupObjects()
		self.setBindings()
		self.MenuBar()
		self.Maximize()
	def setBindings(self):
		self.p1.Bind(wx.EVT_PAINT, self.on_paint)
		self.p2.Bind(wx.EVT_BUTTON, self.default_,id = 77)
		self.p2.Bind(wx.EVT_BUTTON, self.OK_1,id = 1)
		self.p2.Bind(wx.EVT_BUTTON, self.OK_2,id = 2)
		self.p2.Bind(wx.EVT_BUTTON, self.OK_3,id = 3)
		self.p2.Bind(wx.EVT_BUTTON, self.Clear,id = 11)
		self.p2.Bind(wx.EVT_BUTTON, self.refresh,id = 12)
		self.p2.Bind(wx.EVT_BUTTON, self.Clear_1,id = 21)
		self.p2.Bind(wx.EVT_BUTTON, self.Clear_2,id = 22)
		self.p2.Bind(wx.EVT_BUTTON, self.Clear_3,id = 23)
		self.p2.Bind(wx.EVT_BUTTON, self.FX_EXPLORE_1,id = 31)
		self.p2.Bind(wx.EVT_BUTTON, self.FX_EXPLORE_2,id = 32)
		self.p2.Bind(wx.EVT_BUTTON, self.FX_EXPLORE_3,id = 33)
		#MOUSE EVENT BIND START#
		self.p1.Bind(wx.EVT_LEFT_DOWN, self.Down)
		self.p1.Bind(wx.EVT_LEFT_UP, self.Up)
		#MOUSE EVENT BIND END#

		self.p1.Bind(wx.EVT_MOTION, self.mousemotion)
		
		self.Bind(wx.EVT_MENU, self.exit, id = 56)
		self.Bind(wx.EVT_MENU, self.A_Programm, id = 57)
		self.Bind(wx.EVT_MENU, self.A_Programmers, id = 58)
		self.Bind(wx.EVT_MENU, self.usage, id = 59)
	def MenuBar(self):
		menu_bar = wx.MenuBar()
		menu_bar.SetWindowVariant(wx.WINDOW_VARIANT_LARGE)

		file_menu = wx.Menu()
		file_menu.Append(56, "Exit")
		menu_bar.Append(file_menu,"&File")

		about_menu = wx.Menu()
		about_menu.Append(57, u"About")
		about_menu.Append(58, u"About Programmers")
		about_menu.Append(59, u"პროგრამის გამოყენება")
		menu_bar.Append(about_menu,"&About")
		
		self.SetMenuBar(menu_bar)
	def setupObjects(self):
		self.txt_1 = wx.TextCtrl(self.p2,-1,"(x*x+3*x-9)/(2-x)",(0,1),wx.Size(150,20))
		self.txt_2 = wx.TextCtrl(self.p2,-1,"x*x",(0,101),wx.Size(150,20))
		self.txt_3 = wx.TextCtrl(self.p2,-1,"sin(x)*x",(0,201),wx.Size(150,20))
		self.txt_1.SetBackgroundColour("red")
		self.txt_1.SetForegroundColour("white")
		self.txt_2.SetBackgroundColour("blue")
		self.txt_2.SetForegroundColour("white")
		self.txt_3.SetBackgroundColour(wx.Colour(0,200,0))
		self.txt_3.SetForegroundColour("white")
		wx.Button(self.p2,1,"OK",(0,21),wx.Size(75,28))
		wx.Button(self.p2,2,"OK",(0,121),wx.Size(75,28))
		wx.Button(self.p2,3,"OK",(0,221),wx.Size(75,28))
		wx.Button(self.p2, 31, u"გამოიკვლიე \n ფუნქცია", (0,50 + 0),   wx.Size(150,50)).SetFont(self.f10)
		wx.Button(self.p2, 32, u"გამოიკვლიე \n ფუნქცია", (0,50 + 100), wx.Size(150,50)).SetFont(self.f10)
		wx.Button(self.p2, 33, u"გამოიკვლიე \n ფუნქცია", (0,50 + 200), wx.Size(150,50)).SetFont(self.f10)
		
		wx.Button(self.p2,11,"Clear All",(0,350),wx.Size(107,50))
		wx.Button(self.p2,12,"Refresh",(107,350),wx.Size(107,50))
		wx.Button(self.p2,21,"Clear",(75,21),wx.Size(75,28))
		wx.Button(self.p2,22,"Clear",(75,121),wx.Size(75,28))
		wx.Button(self.p2,23,"Clear",(75,221),wx.Size(75,28))
		
		self.p1.SetBackgroundColour("white")
		self.slider = wx.Slider(self.p2, -1,40 , 1, 400, (75,400), wx.Size(50,400), wx.SL_VERTICAL | wx.SL_LABELS)
		self.slider.Bind(wx.EVT_SLIDER, self.OnSlider)
		self.ZooM_Info = wx.StaticText(self.p2,-1, u"მასშტაბი: 1სმ = %s პიქსელი"%(self.slider.GetValue()),(50,300))
		self.ZooM_Info.SetFont(self.f10)
		wx.Button(self.p2,77,"Default",(40,425),wx.Size(50,50))

		self.MousePos = wx.StaticText(self.p2,wx.ID_ANY,"",(5,400))
	def exit(self,evt):
		self.Close()
	def usage(self,evt):
		frame_u = wx.Frame(self,-1, u"გამოყენება",(0,0),wx.Size(650,300))
		frame_u.Centre()
		panel_u = wx.Panel(frame_u,-1)
		wx.StaticText(panel_u,-1, "read usage.help")
		frame_u.Show()
	def mousemotion(self,evt):
		p1,p2 = evt.GetPosition()
		z = self.slider.GetValue()
		p1 -= self.CENTRE_X
		p2 -= self.CENTRE_Y
		p1 /= float(z)
		p2 /= float(z)
		self.MousePos.SetLabel(str(formatFloat(p1,2))+","+str(formatFloat(-p2,2)))
	def default_(self,event):
		self.dc.Clear()
		self.zoom = 40.0
		self.slider.SetValue(40)
		self.ZooM_Info.SetLabel(u"მასშტაბი: 1სმ = %s პიქსელი"%(self.slider.GetValue()))
		self.p1.Refresh()
	def Down(self,event):
		self.p1.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
		self.MOUSE_EVENT_LIST = []
		self.MOUSE_EVENT_LIST.append(event.GetPosition())
	def Up(self,event):
		self.p1.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
		self.MOUSE_EVENT_LIST.append(event.GetPosition())
		self.CENTRE_X_,self.CENTRE_Y_ = self.MOUSE_EVENT_LIST[1]-self.MOUSE_EVENT_LIST[0]
		self.CENTRE_X+= self.CENTRE_X_
		self.CENTRE_Y+= self.CENTRE_Y_
		self.p1.Refresh()
	def OnSlider(self, event):
		self.zoom = self.slider.GetValue()
		self.ZooM_Info.SetLabel(u"მასშტაბი: 1სმ = %s პიქსელი"%self.zoom)
		self.zoom = float(self.zoom)
		self.p1.Refresh()
	def update_drawings(self):
		sliderValue = float(self.slider.GetValue())

		drawOne = lambda Color, Function: self.daxazva(Function, Color, sliderValue, self.CENTRE_X, self.CENTRE_Y)
		drawList = lambda Color, List: [drawOne(Color, Function) for Function in List]

		drawList("RED", self.RED_FX)
		drawList("BLUE", self.BLUE_FX)
		drawList("GREEN", self.GREEN_FX)
		
		self.dc.SetPen(wx.Pen("BLACK"))
		for i in self.BLACK_FX:
			i *= self.slider.GetValue()
			self.dc.DrawLine(i+self.CENTRE_X, 0,i+self.CENTRE_X, 1000)

	def refresh(self,event):
		self.p1.Refresh()		
	def FX_EXPLORE_1(self,event):
		FX = self.txt_1.GetValue()
		self.explore("First",FX,self.ganasgvis_are(FX),self.Oy_Kveta(FX),self.warmoebuli(FX),self.dax_asi(FX))
	def FX_EXPLORE_2(self,event):
		FX = self.txt_2.GetValue()
		self.explore("Second",FX,self.ganasgvis_are(FX),self.Oy_Kveta(FX),self.warmoebuli(FX),self.dax_asi(FX))
	def FX_EXPLORE_3(self,event):
		FX = self.txt_3.GetValue()
		self.explore("Third",FX,self.ganasgvis_are(FX),self.Oy_Kveta(FX),self.warmoebuli(FX),self.dax_asi(FX))
	def ganasgvis_are(self,fx):
		fx = fx.replace("^","**")
		LIST = []
		x = -400
		while x<401:
			try:
				y = eval(fx)
			except ZeroDivisionError:
				LIST.append(x)
				print x,fx,"fxfx"
			except:
				pass
			x+= 1
		Str = "x ekutvnis "
		if len(LIST)>0:
			for C in LIST:
				c = str(C)
				if LIST.index(C)  ==0:
					Str+= "(-"+INFINITY()+";"+c+")"
				else:
					Str+= "U(" + str(LIST[LIST.index(C)-1])+";"+c+")"
			Str+= "U("+c+";+"+INFINITY()+")"
		else:
			Str+= "R-s"
		return Str,LIST
	def Oy_Kveta(self,fx):
		x = 0.0
		try:
			y = "(0.0,"+str(eval(fx))+")"
		except:
			y = "ar kvets Oy RerZs"
		return y
	def warmoebuli(self,fx):
		return sympy.diff(fx,"x")
		def K_limit(self,fx):
				y = ""
				try:
						y = sympy.limit(fx+"/x","x","oo")
				except sympy.PoleError:
						y = "SeuZlebelia gamoTvla"
				print y,"K_limit"
				return y
		def B_limit(self,fx):
				y = ""
				k = self.K_limit(fx)
				if k  =="oo" or k  =="ar aqvs" or k  =="SeuZlebelia gamoTvla":
						print "AR AQVS"
						return "AR AQVS"
				try:
						y = sympy.limit(fx+"-"+str(k)+"*x","x","oo")
						print fx+"-"+str(k)+"*x"
						print k
				except sympy.PoleError:
						y = "SeuZlebelia gamoTvla"
				except:
						y = ""
				print y,"B_limit"
				return y
		def dax_asi(self,fx):
			k = self.K_limit(fx)
			b = self.B_limit(fx)
			try:
				return "%d*x+%d"%(k,b)
			except:
				return u"არ აქვს :)"
		def mxebi(self,fx,xy):
				x0,y0 = float(xy[0]),float(xy[1])
				f_ = eval(str(self.warmoebuli(fx)).replace("x","x0"))
				y = str(f_)+"*(x-"+str(x0)+")+"+str(y0)
				return y
	def OK_1(self,event):
		Fx = self.txt_1.GetValue()
		if not (Fx in self.RED_FX):
			self.RED_FX.append(Fx)
		self.p1.Refresh()
	def OK_2(self,event):
		Fx = self.txt_2.GetValue()
		if not (Fx in self.BLUE_FX):
			self.BLUE_FX.append(Fx)
		self.p1.Refresh()
	def OK_3(self,event):
		Fx = self.txt_3.GetValue()
		if not (Fx in self.GREEN_FX):
			self.GREEN_FX.append(Fx)
		self.p1.Refresh()
	def Clear_1(self,event):
		self.clear_fx(self.RED_FX,self.CENTRE_X,self.CENTRE_Y)
		self.RED_FX = []
		self.p1.Refresh()
	def Clear_2(self,event):
		self.clear_fx(self.BLUE_FX,self.CENTRE_X,self.CENTRE_Y)
		self.BLUE_FX = []
		self.p1.Refresh()
	def Clear_3(self,event):
		self.clear_fx(self.GREEN_FX,self.CENTRE_X,self.CENTRE_Y)
		self.GREEN_FX = []
		self.p1.Refresh()
	def clear_fx(self,col_fx,centre_H,centre_V):
		for i in range(len(col_fx)):
			self.daxazva(col_fx[i],self.p1.GetBackgroundColour(),float(self.slider.GetValue()),centre_H,centre_V)
		self.lines(centre_H,centre_V)
	def Clear(self,event):
		self.dc.Clear()
		self.CENTRE_X = 400
		self.CENTRE_Y = 400
		self.lines(400,400)
		self.RED_FX = []
		self.BLUE_FX = []
		self.GREEN_FX = []
		self.GRAY_FX = []
		self.default_(event)
		self.p1.Refresh()
	def on_paint(self, event):
		#print "on_paint"
		self.dc = wx.PaintDC(self.p1)
		self.dc.SetBackground(wx.Brush('WHITE'))
		self.lines(self.CENTRE_X,self.CENTRE_Y)
		self.update_drawings()
		
	def lines(self,centre_X,centre_Y):
		self.dc.SetPen(wx.Pen('BLACK'))
		self.dc.DrawText("0",centre_X+1,centre_Y)
		self.xazebi(centre_X,centre_Y)
		self.ricxvebi(centre_X,centre_Y)
	def xazebi(self,centre_X,centre_Y):
		self.dc.DrawLine(0,centre_Y,800,centre_Y)
		self.dc.DrawLine(centre_X,800,centre_X,0)
	def ricxvebi(self,centre_X,centre_Y):
		zoom = 40.0/self.slider.GetValue()
		for i in range(20):
			#HORIZONTAL
			i_H = i-((centre_X-400)/40)
			self.dc.SetPen(wx.Pen('BLACK'))
			if not i_H  ==10:
				self.dc.DrawText(str(formatFloat(zoom*(i_H-10))),(centre_X-400)%40+i*40 - 15,centre_Y+3)
				self.dc.SetPen(wx.Pen('RED'))
				self.dc.DrawCircle((centre_X-400)%40+i*40,centre_Y,2)
		for k in range(20):
			k_V = k+((centre_Y-400)/40)
			self.dc.SetPen(wx.Pen('BLACK'))
			if not k_V  ==10:
				self.dc.DrawText(str(formatFloat(zoom*(k_V-10))),centre_X-3,(centre_Y-400)%40+800-k*40-13)
				self.dc.SetPen(wx.Pen('RED'))
				self.dc.DrawCircle(centre_X,(centre_Y-400)%40+800-k*40-5,2)
		i = -400
	def daxazva(self,string,color,zoom,centre_X,centre_Y):
		string = string.replace("^","**")
		string = string.lower()
		print centre_X,centre_Y
		self.dc.SetPen(wx.Pen(color))
		x = 0
		string = string.replace("x","x1")
		while x < 800:
			x1 = (x-centre_X)/zoom
			x2 = x1+1
			try:
				y1 = eval(string)*zoom
				y2 = eval(string.replace("x1","(x1+1/"+str(zoom)+")"))*zoom
			except:
				y1 = 0
				y2 = 0
				x += 1
				continue
			if (0 <= centre_Y-y1 <= 1000) or (0 <= centre_Y-y2 <= 1000):
				try:
					self.dc.DrawLine(x, centre_Y-y1,x+1, centre_Y-y2)
				except OverflowError:
					dial = wx.MessageDialog(None, ':|\n samwuxarod mogiwevs mxolod is grafiki naxo rac exlaa daxazuli,\n mets ver vxavaz cudi funqciaa Zalian :|\n: ))', 'Overflow Error', style = wx.ICON_ERROR | wx.OK)
					dial.ShowModal()
			x += 1
	def explore(self,Title,fx,gansagvris_are,gadakvetis_wertili,warmoebuli,dax_asi):
		self.fx__ = fx.replace("^","**")
		self.dax_asi__ = dax_asi
		fst = ["First","Second","Third"]
		Fx_E = wx.Frame(self,-1,"About %s Function"%(Title),(800,fst.index(Title)*100+95),wx.Size(500,300))
		p = wx.Panel(Fx_E,-1)
		wx.StaticText(p,-1,"1) D(x)= "+gansagvris_are[0],(0,0))
		
		wx.StaticText(p,-1,"2) OY Rerdzis gadakveTis wertilis koordinati: "+str(gadakvetis_wertili),(0,40))
		
		wx.StaticText(p,-1,"3) fuqnciis warmoebulia: y' = "+str(warmoebuli),(0,80))

		wx.StaticText(p,-1,"4) grafikis mxebi ",(0,120))
		self.XY = wx.TextCtrl(p,-1,"0,0",(90,115),wx.Size(60,20))
		self.coord = wx.StaticText(p,-1,"wertilshi",(150,120))
		wx.Button(p,1,"daxazva",(370,115),wx.Size(50,25)).Bind(wx.EVT_BUTTON,self.daxazva__mxebi)
		wx.Button(p,1,"yvelas waSla",(420,115),wx.Size(70,25)).Bind(wx.EVT_BUTTON,self.washla__mxebi)

		wx.StaticText(p,-1,"5) daxrili asimptota : "+(dax_asi),(0,160))
		if str(dax_asi.lower())  =="ar aqvs :)":
			dis = True
		else:
			dis = False
		b_d = wx.Button(p,wx.ID_ANY,"daxazva",(370,160),wx.Size(50,25))
		b_d.Bind(wx.EVT_BUTTON,self.daxazva_asi)
		b_d.Enable(not dis)
		b_w = wx.Button(p,wx.ID_ANY,"waSla",(420,160),wx.Size(70,25))
		b_w.Bind(wx.EVT_BUTTON,self.washla_asi)
		b_w.Enable(not dis)

		self.BLACK_FX_ = gansagvris_are[1]
		if self.BLACK_FX_  ==[]:
			are = "ar aqvs :)"
		elif len(self.BLACK_FX_)  ==1:
			are = "x udris "+str(self.BLACK_FX_[0])+" wertilshi"
		else:
			are = "x udris "+str(self.BLACK_FX_)+" wertilebshi"
		wx.StaticText(p,-1,"6) vertikaluri asimptota. "+are,(0,200))
		
		if are.lower()  =="ar aqvs :)":
			dis_are = True
		else:
			dis_are = False
		b_d_ver = wx.Button(p,1,"daxazva",(370,200),wx.Size(50,25))
		b_d_ver.Bind(wx.EVT_BUTTON,self.daxazva_asi_ver)
		b_d_ver.Enable(not dis_are)
		b_w_ver = wx.Button(p,1,"yvelas waSla",(420,200),wx.Size(70,25))
		b_w_ver.Bind(wx.EVT_BUTTON,self.washla_asi_ver)
		b_w_ver.Enable(not dis_are)
		
		Fx_E.Show()
	def daxazva_asi_ver(self,evt):
		self.dc.SetPen(wx.Pen("BLACK"))
		self.BLACK_FX = self.BLACK_FX_
		for i in self.BLACK_FX_:
			j = i*self.slider.GetValue()
			self.dc.DrawLine(j+self.CENTRE_X, 0,j+self.CENTRE_X, 1000)
		def daxazva_asi(self,evt):
			y = str(self.dax_asi__)
		self.daxazva(y,"BROWN",float(self.slider.GetValue()),self.CENTRE_X,self.CENTRE_Y)
		self.BROWN_FX.append(y)
	def daxazva__mxebi(self,evt):
		y = str(self.mxebi(self.fx__,self.XY.GetValue().split(",")))
		self.daxazva(y,"GRAY",40.0,400,400)
		self.GRAY_FX.append(y)
		self.coord.SetLabel("wertilshi, aris es funqcia:y = "+str(sympy.Derivative(y)))
	def washla__mxebi(self,e):
		self.GRAY_FX = []
		self.p1.Refresh()
	def washla_asi(self,e):
		self.BROWN_FX = []
		self.p1.Refresh()
	def washla_asi_ver(self,e):
		self.dc.SetPen(wx.Pen("WHITE"))
		self.BLACK_FX = []
		for i in self.BLACK_FX_:
			i *= self.slider.GetValue()
			self.dc.DrawLine(i+self.CENTRE_X, 0,i+self.CENTRE_X, 1000)
		self.update_drawings()
	def A_Programmers(self,event):
		import About
		About.ABOUT_PROGRAMMERS()
	def A_Programm(self, event):
		import About
		About.ABOUT_PROGRAMM()



frame = FxExplorerFrame(None, -1, Full_Name + " v" + Full_Version)
frame.Centre()
frame.Maximize()
frame.Show()
app.MainLoop()
