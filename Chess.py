# -*- coding: latin-1 -*-
import pygame,sys
from pygame.locals import *
import math 


class Button:
	def __init__(self,x,y,w,h,image,image1):
		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.image=image
		self.image1=image1
		
	def contains(self,a,b):
		if (a>=self.x and a<=self.x+self.w) and (b>self.y and b<=self.y+self.h):
			return True
			
		else:
			return False
			
	def draw(self,screen):
		button= pygame.image.load(self.image).convert_alpha()
		screen.blit(button,(self.x,self.y))
		pygame.display.flip()
		
	def  click(self,screen,event):			
		if event.type==5 and self.contains(event.pos[0],event.pos[1]):
			button= pygame.image.load(self.image1).convert_alpha() #pour changer le contraste du bouton lors du click
			screen.blit(button,(self.x,self.y))
			pygame.display.flip()
		if event.type==6 :
			self.draw(screen)
			if self.contains(event.pos[0],event.pos[1]):
				return True
			else:
				return False	
		
		
class Piece:
	def __init__(self,x,y,color,image,name,symbol):
		self.piece_x=x #prend des valeurs de 0 à 7 
		self.piece_y=y #prend des valeurs de 0 à 7 
		self.color=color # 0=noir,1=blanc,4=vide
		self.image=image
		self.name=name
		self.symbol=symbol #icone pour l'historique
	def nature(self):
		return True
	def valide(self,xf,yf,board):
		if xf<0 or xf >=8  or yf>=8 or yf<0 : 
			return False
		elif board.matrix[yf][xf].nature():
			if board.matrix[yf][xf].color==self.color:
					return False	
			else:
					return True
		else:
			return True
	
		
class Vide(Piece):	
	def __init__(self):
		self.color=4
		self.image="vide.png"
		self.name="vide"
	def nature(self):
		return False
	def permission(self):
		return False
	
class Cheval(Piece):
	
	def permission(self,xf,yf,board):
		return self.valide(xf,yf,board) and \
			 (( (abs(self.piece_x-xf))==2 and (abs(self.piece_y-yf))==1 ) or (abs(self.piece_y-yf))==2 and (abs(self.piece_x-xf))==1)
			
	
class Tour(Piece):
	def permission(self,xf,yf,board):
		if xf-self.piece_x==0  or yf-self.piece_y==0:
			if self.obstacle(xf,yf,board) and self.valide(xf,yf,board):
				return True
			else:
				return False
		else:
				return False
	def  obstacle(self,xf,yf,board): #retourne vrai s'il n'y a pas un obstacle
		test=True
		if yf==self.piece_y:
			if (xf-self.piece_x)>=2:
				for i in range(self.piece_x+1,xf):
					if board.matrix[yf][i].nature():
						test=False
						break
			if (xf-self.piece_x)<=-2:
				for i in range(self.piece_x-1,xf,-1):
					if board.matrix[yf][i].nature():
						test=False
						break			
		if xf==self.piece_x:
			if (yf-self.piece_y)>=2:
				for i in range(self.piece_y+1,yf):
					if board.matrix[i][xf].nature():
						test=False
						break
		
			if (yf-self.piece_y)<=-2:
				for i in range(self.piece_y-1,yf,-1):
					if board.matrix[i][xf].nature():
						test=False
						break				
		return test
	
class Roi(Piece):
	
	def permission(self,xf,yf,board):		
		if self.valide(xf,yf,board):
				if abs(xf-self.piece_x)<=1 and abs(yf-self.piece_y)<=1 :
					
					return True
					
				else :
					return False
								
		else:
			return False	
		
			
			
	
class Fou(Piece):
	def permission(self,xf,yf,board):
		
		if abs(xf-self.piece_x)==abs(yf-self.piece_y)  :
			if self.valide(xf,yf,board) and self.obstacle1(xf,yf,board):
				return True
			else:
				return False	
		return False		
	def obstacle1(self,xf,yf,board):
		

		if (xf-self.piece_x)>0 and 	(yf-self.piece_y)>0:
			px=1
			py=1
		elif (xf-self.piece_x)>0 and 	(yf-self.piece_y)<0:
			px=1
			py=-1
		elif (xf-self.piece_x)<0 and 	(yf-self.piece_y)<0:
			px=-1
			py=-1		
		elif (xf-self.piece_x)<0 and 	(yf-self.piece_y)>0:
			px=-1
			py=1
		i=self.piece_x+px
		j=self.piece_y+py
		courant=board.matrix[j][i]

		if courant.nature() and  i-xf!=0:
				return False		
			
		while  not courant.nature() and  i-xf!=0:
			i=i+px
			j=j+py
			courant=board.matrix[j][i]
			if courant.nature() and i-xf!=0:
				return False
						
		return True 
class Pion(Tour):
	def permission(self,xf,yf,board):
		if self.color==0: #"0=noir"
			if (xf-self.piece_x)==0 and ((yf-self.piece_y)==1 or  (yf-self.piece_y)==2 and self.piece_y==1 and self.obstacle(xf,yf,board)) :
				if not board.piece(xf,yf).nature() and self.valide(xf,yf,board):
					return True
				else:
					return False
			elif abs(xf-self.piece_x)==abs(yf-self.piece_y)==1 and self.valide(xf,yf,board) and (yf-self.piece_y)>=0 :
					if board.piece(xf,yf).nature() :
						return True		
					else:
						return False
				
			else:
				return False
		if self.color==1: #"1=blanc"
			if (xf-self.piece_x)==0 and ((yf-self.piece_y)==-1 or  (yf-self.piece_y)==-2 and self.piece_y==6 and self.obstacle(xf,yf,board)) :
				if not board.piece(xf,yf).nature() and self.valide(xf,yf,board):
					return True
				else:
					return False
			elif abs(xf-self.piece_x)==abs(yf-self.piece_y)==1 and self.valide(xf,yf,board) and (yf-self.piece_y)<=0 :
					if board.piece(xf,yf).nature() and board.piece(xf,yf).color==0: 
						return True		
					else:
						return False
			else:
				return False
class Dame(Fou,Tour):
	def permission(self,xf,yf,board):
		if xf-self.piece_x==0  or yf-self.piece_y==0:
			if self.obstacle(xf,yf,board) and self.valide(xf,yf,board):
				return True
			else :
				return False
				
		elif abs(xf-self.piece_x)==abs(yf-self.piece_y) and self.obstacle1(xf,yf,board) and self.valide(xf,yf,board) :
			return True			
		else:
			return False				

class Board:
	def __init__(self):
		self.fond="chessboard.jpg"
		self.matrix=[]
		self.historic=[]
		self.dim=74
		self.roque0=True #True tant que le roi et la tour noirs ne sont pas déplacés
		self.roque1=True #True tant que le roi et la tour blancs ne sont pas déplacés
		self.roi1_x=4 # roi noir
		self.roi1_y=0 # roi noir
		self.roi2_x=4 # roi blanc
		self.roi2_y=7 # roi blanc
		self.a1=9 #position de la marque verte suivant x de la case de départ 
		self.b1=9 #position de la marque verte suivant y de la case de départ
		self.a2=9 #position de la marque verte suivant x de la case d'arrivée
		self.b2=9 #position de la marque verte suivant y de la case d'arrivée
	
	
		
		
		tour11=Tour(0,0,0,"tour0.png","tour01","stour0.png")
		cheval11=Cheval(1,0,0,"cheval0.png","cheval01","scheval0.png")
		fou11=Fou(2,0,0,"fou0.png","fou01","sfou0.png")
		roi1=Roi(4,0,0,"roi0.png","roi0","sroi0.png")
		dame1=Dame(3,0,0,"dame0.png","dame0","sdame0.png")
		fou12=Fou(5,0,0,"fou0.png","fou02","sfou0.png")
		cheval12=Cheval(6,0,0,"cheval0.png","cheval02","scheval0.png")
		tour12=Tour(7,0,0,"tour0.png","tour02","stour0.png")
		pion11=Pion(0,1,0,"pion0.png","pion01","spion0.png")
		pion12=Pion(1,1,0,"pion0.png","pion02","spion0.png")
		pion13=Pion(2,1,0,"pion0.png","pion03","spion0.png")
		pion14=Pion(3,1,0,"pion0.png","pion04","spion0.png")
		pion15=Pion(4,1,0,"pion0.png","pion05","spion0.png")
		pion16=Pion(5,1,0,"pion0.png","pion06","spion0.png")
		pion17=Pion(6,1,0,"pion0.png","pion07","spion0.png")
		pion18=Pion(7,1,0,"pion0.png","pion08","spion0.png")
		
		
		tour21=Tour(0,7,1,"tour1.png","tour11","stour1.png")
		cheval21=Cheval(1,7,1,"cheval1.png","cheval11","scheval1.png")
		fou21=Fou(2,7,1,"fou1.png","fou11","sfou1.png")
		roi2=Roi(4,7,1,"roi1.png","roi1","sroi1.png")
		dame2=Dame(3,7,1,"dame1.png","dame1","sdame1.png")
		fou22=Fou(5,7,1,"fou1.png","fou12","sfou1.png")
		cheval22=Cheval(6,7,1,"cheval1.png","cheval12","scheval1.png")
		tour22=Tour(7,7,1,"tour1.png","tour12","stour1.png")
		pion21=Pion(0,6,1,"pion1.png","pion11","spion1.png")
		pion22=Pion(1,6,1,"pion1.png","pion12","spion1.png")
		pion23=Pion(2,6,1,"pion1.png","pion13","spion1.png")
		pion24=Pion(3,6,1,"pion1.png","pion14","spion1.png")
		pion25=Pion(4,6,1,"pion1.png","pion15","spion1.png")
		pion26=Pion(5,6,1,"pion1.png","pion16","spion1.png")
		pion27=Pion(6,6,1,"pion1.png","pion17","spion1.png")
		pion28=Pion(7,6,1,"pion1.png","pion18","spion1.png")
		vide=Vide()
		
		for i in range (8):
			
			if i==0:
				self.matrix.append([tour11,cheval11,fou11,dame1,roi1,fou12,cheval12,tour12])
			elif i==1:
				self.matrix.append([pion11,pion12,pion13,pion14,pion15,pion16,pion17,pion18])
			elif i>1 and i<6:
				self.matrix.append( [vide]*8) #"objet vide"
			elif i==6:
				self.matrix.append([pion21,pion22,pion23,pion24,pion25,pion26,pion27,pion28])
			elif i==7:
				self.matrix.append([tour21,cheval21,fou21,dame2,roi2,fou22,cheval22,tour22])
	
	def move(self,x0,y0,xf,yf,chekmate_son,eat_son):
		vide=Vide()
		x1=self.roi1_x
		y1=self.roi1_y
		x2=self.roi2_x
		y2=self.roi2_y
		a1=self.a1
		b1=self.b1
		a2=self.a2
		b2=self.b2
		test=True
			
		
		if self.piece(x0,y0).name=="roi0":
				self.roi1_x=xf
				self.roi1_y=yf
		elif self.piece(x0,y0).name=="roi1":
				self.roi2_x=xf
				self.roi2_y=yf
				
		if self.roque0 and (self.piece(x0,y0).name=="tour02" or self.piece(x0,y0).name=="roi0"):
				self.roque0=False
		elif  self.roque1 and (self.piece(x0,y0).name=="tour12" or self.piece(x0,y0).name=="roi1"):
				self.roque1=False	
		objet=self.piece(xf,yf)
		self.matrix[yf][xf]=self.matrix[y0][x0]
		self.matrix[y0][x0]=vide
		self.matrix[yf][xf].piece_x=xf
		self.matrix[yf][xf].piece_y=yf
		self.a1=x0
		self.b1=y0
		self.a2=xf
		self.b2=yf
			
		if self.kech()==1 and  self.piece(xf,yf).color==0 or self.kech()==0 and  self.piece(xf,yf).color==1:
				chekmate_son.play()
		else: 
			if objet.nature():
				eat_son.play()
				
			
		if self.kech()==1 and  self.piece(xf,yf).color==1 :
				test=False
				self.matrix[y0][x0]=self.matrix[yf][xf]
				self.matrix[yf][xf]=objet
				self.matrix[y0][x0].piece_x=x0
				self.matrix[y0][x0].piece_y=y0
				self.matrix[yf][xf].piece_x=xf
				self.matrix[yf][xf].piece_y=yf
				self.roi2_x=x2
				self.roi2_y=y2
				self.a1=a1
				self.b1=b1
				self.a2=a2
				self.b2=b2
				
				
		elif self.kech()==0 and  self.piece(xf,yf).color==0:
				test=False
				self.matrix[y0][x0]=self.piece(xf,yf)
				self.matrix[yf][xf]=objet
				self.matrix[y0][x0].piece_x=x0
				self.matrix[y0][x0].piece_y=y0
				self.matrix[yf][xf].piece_x=xf
				self.matrix[yf][xf].piece_y=yf
				self.roi1_x=x1
				self.roi1_y=y1
				self.a1=a1
				self.b1=b1
				self.a2=a2
				self.b2=b2
		else:
				self.historic.append([x0,y0,self.matrix[yf][xf],xf,yf,objet,a1,b1,a2,b2,x1,y1,x2,y2])
				if self.matrix[yf][xf].symbol=="spion0.png" and self.matrix[yf][xf].piece_y==7:
					self.matrix[yf][xf]=Dame(xf,yf,0,"dame0.png","dame0","sdame0.png")
				if self.matrix[yf][xf].symbol=="spion1.png" and self.matrix[yf][xf].piece_y==0:
					self.matrix[yf][xf]=Dame(xf,yf,1,"dame1.png","dame1","sdame1.png")	
		return test
		
	def move_piece(self,x0,y0,xf,yf,chekmate_son,eat_son):
		test=False
		test1=False
		if self.piece(x0,y0).permission(xf,yf,self):
			test1=self.move(x0,y0,xf,yf,chekmate_son,eat_son)
			test=True
		elif 	self.roque(x0,y0,xf,yf)==0:
			test1=self.move(x0,y0,xf,yf,chekmate_son,eat_son)
			self.historic.append(["roque0"])
			self.move(7,0,5,0,chekmate_son,eat_son)
			test=True
		elif 	self.roque(x0,y0,xf,yf)==1:
			test1=self.move(x0,y0,xf,yf,chekmate_son,eat_son)
			self.historic.append(["roque1"])
			self.move(7,7,5,7,chekmate_son,eat_son)
			test=True	
		return test and test1
		
	def roque(self,x0,y0,xf,yf): # retourne 0 si le roque noir est fait , retourne 1 si le roque blanc est fait et retourne 4 sinon
		if self.piece(x0,y0).name=="roi0" and self.roque0 and not self.test(5,0) and not self.test(6,0) and xf==6 and yf==0:
			self.roi1_x=6
			self.roi1_y=0
			if self.kech()==0:
				self.roi1_x=x0
				self.roi1_y=y0
				return 4
				
			else:	
				return 0 
		elif self.piece(x0,y0).name=="roi1" and self.roque1 and not self.test(5,7) and not self.test(6,7) and xf==6 and yf==7:
			self.roi2_x=6
			self.roi2_y=7
			if self.kech()==1:
				self.roi2_x=x0
				self.roi2_y=y0
				return 4
			else:	
				return 1
		else:
			return 4


			
	def undo(self):
		if self.historic!=[]: 
			temp=self.historic[len(self.historic)-1]
			self.historic.remove(temp)
			
			self.matrix[temp[1]][temp[0]]=temp[2]
			self.matrix[temp[1]][temp[0]].piece_x=temp[0]
			self.matrix[temp[1]][temp[0]].piece_y=temp[1]
			self.matrix[temp[4]][temp[3]]=temp[5]
			self.matrix[temp[4]][temp[3]].piece_x=temp[3]
			self.matrix[temp[4]][temp[3]].piece_y=temp[4]
			
			self.a1=temp[6]
			self.b1=temp[7]
			self.a2=temp[8]
			self.b2=temp[9]
			self.roi1_x=temp[10]
			self.roi1_y=temp[11]
			self.roi2_x=temp[12]
			self.roi2_y=temp[13]	
			if self.historic!=[]:
				temp=self.historic[len(self.historic)-1]
				if temp[0]=="roque0":
					self.historic.remove(temp)
					self.roque0=True
					self.undo()
				if temp[0]=="roque1":
					self.historic.remove(temp)
					self.roque1=True
					self.undo()
	def test(self,x0,y0):
			return self.piece(x0,y0).nature()
				
	def kech(self):
				
		for i in range(8):
			for j in range(8):
				
				if self.matrix[i][j].color==1:
					if self.matrix[i][j].permission(self.roi1_x,self.roi1_y,self):
						
						return 0
						
				if self.matrix[i][j].color==0:
					if self.matrix[i][j].permission(self.roi2_x,self.roi2_y,self):
						
						return 1	
		return 4
		
		

		
	
	def chekmate(self):
		color=self.kech()
		
		vide=Vide()
		test=True
		if color!=4:
				
				for x0 in range(8):
					for y0 in range(8):
						if self.matrix[y0][x0].color==color:
							for xf in range(8):
								for yf in range(8):
									x1=self.roi1_x
									y1=self.roi1_y
									x2=self.roi2_x
									y2=self.roi2_y
									if self.piece(x0,y0).permission(xf,yf,self) :
										if x0==self.roi1_x and y0==self.roi1_y:
											self.roi1_x=xf
											self.roi1_y=yf
										if x0==self.roi2_x and y0==self.roi2_y:
											self.roi2_x=xf
											self.roi2_y=yf
										objet=self.piece(xf,yf)
										self.matrix[yf][xf]=self.matrix[y0][x0]
										self.matrix[y0][x0]=vide
										self.matrix[yf][xf].piece_x=xf
										self.matrix[yf][xf].piece_y=yf
										if self.kech()==4 :
											test=False
										self.matrix[y0][x0]=self.matrix[yf][xf]
										self.matrix[yf][xf]=objet
										self.matrix[y0][x0].piece_x=x0
										self.matrix[y0][x0].piece_y=y0
										self.matrix[yf][xf].piece_x=xf
										self.matrix[yf][xf].piece_y=yf
										self.roi2_x=x2
										self.roi2_y=y2
										self.roi1_x=x1
										self.roi1_y=y1
										if not test:
											return test
				return True		
		return False
					
	
	def piece(self,x0,y0):
		
		return self.matrix[y0][x0]
			
	

class Board_Painter(Board):
	
	def draw(self,fenetre):
		fond = pygame.image.load(self.fond).convert()
		chekmate=pygame.image.load("chekmate.png").convert()
		green=pygame.image.load("green.png").convert()
		fenetre.blit(fond, (0,0))
		
		fenetre.blit(green, (self.a1*self.dim+27, self.b1*self.dim+26))	
		fenetre.blit(green, (self.a2*self.dim+27, self.b2*self.dim+26))
		
		if self.kech()==0:
			fenetre.blit(chekmate, (self.roi1_x*self.dim+27, self.roi1_y*self.dim+26))
		if self.kech()==1:
			fenetre.blit(chekmate, (self.roi2_x*self.dim+27, self.roi2_y*self.dim+26))	
		for i in range(8):
			for j in range(8):
				
				if self.matrix[i][j].nature()  :
					
					image_piece= pygame.image.load(self.matrix[i][j].image).convert_alpha()
					fenetre.blit(image_piece, (self.matrix[i][j].piece_x*self.dim+27, self.matrix[i][j].piece_y*self.dim+26))		
		if self.chekmate():
			fond = pygame.image.load("chekmatelogo.png").convert_alpha()
			fenetre.blit(fond, (-30,200))
					
		pygame.display.flip()	
	def draw_motion(self,fenetre,x0,y0,x,y):
		fond = pygame.image.load(self.fond).convert()
		chekmate=pygame.image.load("chekmate.png").convert()
		green=pygame.image.load("green.png").convert()
		fenetre.blit(fond, (0,0))
		
		fenetre.blit(green, (self.a1*self.dim+27, self.b1*self.dim+26))	
		fenetre.blit(green, (self.a2*self.dim+27, self.b2*self.dim+26))
		
		if self.kech()==0:
			fenetre.blit(chekmate, (self.roi1_x*self.dim+27, self.roi1_y*self.dim+26))
		if self.kech()==1:
			fenetre.blit(chekmate, (self.roi2_x*self.dim+27, self.roi2_y*self.dim+26))	
			
			
		for i in range(8):
			for j in range(8):
				if self.matrix[i][j].nature():
				
					if self.matrix[i][j] is not self.piece(x0,y0)	:
						
						image_piece= pygame.image.load(self.matrix[i][j].image).convert_alpha()
						fenetre.blit(image_piece, (self.matrix[i][j].piece_x*self.dim+27, self.matrix[i][j].piece_y*self.dim+26))
						
		image_piece= pygame.image.load(self.piece(x0,y0).image).convert_alpha()	
				
		fenetre.blit(image_piece,(x-self.dim/2,y-self.dim/2))
		pygame.display.flip()	
	def historic_draw(self,screen):
		list=["A","B","C","D","E","F","G","H"]
		cadre_historique=pygame.image.load("cadre_historique.png").convert()
		screen.blit(cadre_historique, (660, 152))
		myfont = pygame.font.SysFont("boardway", 25,bold=True)
		label = myfont.render("HISTORY", 100, (255,255,255))
		screen.blit(label, (725, 180))
		i=0
		while i<=9 and i<=(len(self.historic)-1) and self.historic!=[]:
			if len(self.historic)>10:
				temp=self.historic[len(self.historic)-10+i]
			else:
				temp=self.historic[i]
			i=i+1		
			if temp[0]!="roque0" and temp[0]!="roque1":
				symbol_piece= pygame.image.load(temp[2].symbol).convert_alpha()
				screen.blit(symbol_piece, (690, 170+i*32))
				label = myfont.render(str(temp[0]+1)+list[temp[1]]+"----->"+str(temp[3]+1)+list[temp[4]], 1, (3,34,76))
				screen.blit(label, (725, 170+i*32))
			else :		
				label = myfont.render("ROQUE", 100, (0,0,0))
				screen.blit(label, (725, 170+i*32))
		pygame.display.flip()			
class Chess:
	def __init__(self):
		pygame.init()
		self.color=1
		self.draw_historic=False
		self.fenetre = pygame.display.set_mode((860, 640))
		pygame.display.set_caption('Checkmate ')
		self.deplacement_son = pygame.mixer.Sound("deplacement_son.wav")
		self.chekmate_son=pygame.mixer.Sound("buddy.wav")
		self.erreur_son=pygame.mixer.Sound("erreur.wav")
		self.eat_son=pygame.mixer.Sound("eat.wav")
		self.fond = pygame.image.load("fond.jpg").convert()
		self.undo=Button(690,10,120,38,"undo.png","undo1.png")
		self.historic=Button(690,110,120,38,"historic.png","historic1.png")
		self.replay=Button(690,60,120,38,"replay.png","replay1.png")
		self.board=None
	def set_board(self,board):
		self.board=board
	def piece_move(self,a,b):
		click=True
		while click:
			for event1 in pygame.event.get():
				if (event1.type==4 ):
					self.board.draw_motion(self.fenetre,a,b,event1.pos[0],event1.pos[1])
					self.option_draw()
												
				if(event1.type==6):
					
					x=(event1.pos[0]-27)/self.board.dim
					y=(event1.pos[1]-26)/self.board.dim
					if self.board.move_piece(a,b,x,y,self.chekmate_son,self.eat_son) :
						if  a!=x or b!=y:	
							if self.color==0:
								self.color=1
							else:
								self.color=0
							self.deplacement_son.play()
					else:
						if  a!=x or b!=y:
							self.erreur_son.play()
							
					self.board.draw(self.fenetre)
					self.option_draw()
					
					click=False
					
	def piece_select(self,event):
		if event.type==5 and event.pos[0]<=(self.board.dim*8+27) and  event.pos[1]<=(self.board.dim*8+26):
			a=(event.pos[0]-27)/self.board.dim
			b=(event.pos[1]-26)/self.board.dim
			if self.board.test(a,b)  and self.color==self.board.piece(a,b).color:
				self.piece_move(a,b)
	def option_draw(self):
		self.undo.draw(self.fenetre)
		self.replay.draw(self.fenetre)
		self.historic.draw(self.fenetre)
		if self.draw_historic:
			self.board.historic_draw(self.fenetre)	
				
		pygame.display.flip()
	def run(self):
		self.board.draw(self.fenetre)
		self.option_draw()
		
		while True:
			for event in pygame.event.get():		
				if event.type == QUIT:
					self.quit()
				elif self.undo.click(self.fenetre,event) and self.board.historic!=[]: #pour eviter le changement de couleur au debut de la partie
						self.board.undo()
						self.board.draw(self.fenetre)
						self.option_draw()
						if self.color==0:
							self.color=1
						else:
							self.color=0
				elif self.replay.click(self.fenetre,event):
					self.color=1
					self.set_board(Board_Painter())
					self.run()	
				elif self.historic.click(self.fenetre,event):
					if self.draw_historic:
						self.draw_historic=False
					else:
						self.draw_historic=True
					self.fenetre.blit(self.fond, (0,0))	
					self.board.draw(self.fenetre)
					self.option_draw()						
				else:
					self.piece_select(event)
			
			
			
	def newgame(self):
		self.fenetre.blit(self.fond, (0,0))
		button=Button(230,400,481,124,"newgame.png","newgame1.png")
		button.draw(self.fenetre)
		while True:
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit()
				if button.click(self.fenetre,event):
					self.run()
					
	def quit(self):
		pygame.quit()
		exit()
		
def abs(x):
	return math.sqrt(x**2)			

chess=Chess()

chess.set_board(Board_Painter())
chess.newgame()
						
			
	
