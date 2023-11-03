import tkinter as tk
from PIL import Image,ImageTk
import random

root=tk.Tk()
L1=[(i,j) for i in range(10,200,21) for j in range(110,170,21)]
L2=[(i,j) for i in range(10,200,21) for j in range(300,340,21)]
L3=[(i,j) for i in range(250,500,21) for j in range(180,243,21)]
L4=[(i,j) for i in range(570,620,21) for j in range(244,288,21)]

R=L1+L2+L3+L4

L_inv=[(i,40) for i in range(20,630 ,27)]

class Invader(tk.Canvas):
    

    ######Initialisation des paramètres 
    def __init__(self):
        super().__init__(width=640,height=480,background='black',highlightthickness=0)
        self.MOVE_INCREMENT=5
        self.valeur=True
        self.direction="Right"
        self.laser_position=(0,0)
        self.is_dead=False
        
        self.invader_position=(320,10)
        self.mystery_position=(620,10)
        self.ship_position=(320,460)
        self.L=[str(i) for i in range(20,630 ,27)]
        self.load_assets()
        self.bind_all("<Key>",self.on_key_press)
        #self.bind_all("<KeyRelease-space>",self.on_key_release)
        self.after(1000,self.alpha)
        
        self.create_objects()
        self.perform_actions1()
        


    ###### loading Assets and creating images


        
    def load_assets(self):
        self.invader_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//invader.gif")
        self.invader_body=ImageTk.PhotoImage(self.invader_image)
        
        self.ship_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//spaceship.gif")
        self.ship_body=ImageTk.PhotoImage(self.ship_image)
        
        self.wall_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//wall.png")
        self.wall_body=ImageTk.PhotoImage(self.wall_image)
        
        self.laser_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//laser.png")
        self.laser_body=ImageTk.PhotoImage(self.laser_image)
        
        self.explosion_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//explosionblue.png")
        self.explosion_body=ImageTk.PhotoImage(self.explosion_image)
        
        self.laser_inv_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//laser2.png")
        self.laser_inv_body=ImageTk.PhotoImage(self.laser_inv_image)
        
        self.mystery_image=Image.open("D://pg python//pygame trial//Tkinter//Space invaders tk//mystery1.png")
        self.mystery_body=ImageTk.PhotoImage(self.mystery_image)
        
        
    def create_objects(self):
        self.create_image(*self.invader_position,image=self.invader_body, tag='invader')
        self.create_image(*self.ship_position, image=self.ship_body,tag='ship')
        for (i,j) in R:
            self.create_image(i,j,image=self.wall_body,tag='wall')
        for (i,j) in L_inv :
            self.create_image(i,j,image=self.invader_body,tag=str(i))
         
        
            
        
      ######invader
        
      
        
      
    def move_invader(self):
        x=self.invader_position[0]
        y=self.invader_position[1]
        if x==640:
            self.MOVE_INCREMENT=-5
        if x==0:
            self.MOVE_INCREMENT=5            
        x=x+self.MOVE_INCREMENT
        y=self.invader_position[1]
        self.invader_position=(x,y)
        self.coords('invader',(x,y))
    
    
    
    
    ###### spaceship
    
    
    
    def move_ship(self):
        
        x_pos=self.ship_position[0]
        y_pos=self.ship_position[1]
        if self.ship_position[0]==25 :
           if self.direction=='Right':
                x_pos=x_pos+5
           if self.direction=='Up':
                y_pos=y_pos-5
           if self.direction=="Down":
                y_pos=y_pos+5
           if self.direction=='Left':
                self.direction="Right"
                
        elif self.ship_position[0]==625:
               if self.direction=='Left':
                    x_pos=x_pos-5
               if self.direction=='Right':
                     self.direction="Left"
               if self.direction=='Up':
                    y_pos=y_pos-5
               if self.direction=="Down":
                    y_pos=y_pos+5
                    
        elif self.ship_position[1]==465:
                  if self.direction=='Left':
                       x_pos=x_pos-5
                  if self.direction=='Right':
                      x_pos=x_pos+5
                  if self.direction=='Up':
                       y_pos=y_pos-5
                  if self.direction=="Down":
                       self.direction='Up'
        
        else:
            if self.direction=='Left':
                 x_pos=x_pos-5
            if self.direction=='Right':
                x_pos=x_pos+5
            if self.direction=='Up':
                 y_pos=y_pos-5
            if self.direction=="Down":
                 y_pos=y_pos+5
     
               
        self.ship_position=(x_pos,y_pos)
        self.coords('ship',self.ship_position)
    
    
    def on_key_press(self,event):
        new_order=event.keysym
        all_directions=["Right","Up","Left","Down"]
        if new_order in all_directions:
            self.direction=new_order
        
    
    ######## Laser
    
    def create_laser(self):
        self.laser_position=self.ship_position
        self.create_image(*self.laser_position,image=self.laser_body,tag='laser')
    
    def move_laser(self):
      if self.valeur==True:
        if self.find_withtag("ship"):
            if self.find_withtag("laser"):
                self.move("laser",0,-25)
                y_laser=self.coords("laser")
                if y_laser[1] <0:
                    self.valeur=False
                    self.delete("laser")
            else:
                self.create_laser()
                
    def perform_actions1(self):
        self.move_invader()
        self.move_ship()
        self.move_laser()
        self.invader_dead()
        self.update_laser2()
        self.move_mystery()
        self.ship_hit()
        self.after(10, self.perform_actions1)
        print(self.find_withtag("laser"))
     
    def on_key_release(self,e):
         self.valeur=True


    def alpha(self):
        self.bind_all("<KeyRelease-space>",self.on_key_release)
        
    #####EXPLOSION ET DESTRUCTION DE BLOCS ET ENNEMIS 
      
    def invader_dead(self):
        if(  self.find_withtag("laser") and self.find_withtag('invader')):
            self.x_laser,self.y_laser=self.coords("laser")
            self.x_invader,self.y_invader=self.coords('invader')
        
            if (self.x_laser>=self.x_invader-9 and self.x_laser<=self.x_invader+22 and self.y_laser<=self.y_invader+17):
                self.last=[self.x_invader,self.y_invader]
                self.delete("invader")
                self.is_dead=True
                self.create_explosion()
                self.after(400,self.delete_explosion)
     
        
    def create_explosion(self):
         self.explosion_position=(self.last[0],self.last[1])
         self.create_image(*self.explosion_position,image=self.explosion_body,tag='explosion')
         
    def delete_explosion(self):
        self.delete("explosion")
        
        
   #####Laser invader
    def create_laser2(self):
        
        if self.L:
            a=random.randint(0,len(self.L)-1)
            self.laser_inv_position=self.coords(self.L[a])
            if self.find_withtag(self.L[a]):
                self.create_image(self.laser_inv_position[0],40,image=self.laser_inv_body,tag='laser2')
            
            
    def update_laser2(self):
        
        if self.find_withtag("laser2"):
            self.move("laser2",0,10)
            y_laser2=  self.coords("laser2")
            if y_laser2[1]>470:
                self.delete("laser2")
        else:
            self.create_laser2()
        
    
    def create_mystery(self):
        if len(self.find_withtag("invader"))==0:
            self.create_image(*self.mystery_position,image=self.mystery_body,tag='mystery')
            
            
    def move_mystery(self):
        if len(self.find_withtag("mystery"))==0:
            self.create_mystery()
        if self.find_withtag("mystery"):
            (x,y)=self.coords("mystery")
            if x>=640:
                 self.MOVE_INCREMENT=-5
            if x<=0:
                self.MOVE_INCREMENT=+5 
            self.move('mystery',self.MOVE_INCREMENT,0)
       
    def ship_hit(self):
        if self.find_withtag("ship") and self.find_withtag("laser2"):
            (x1,y1)=self.coords("ship")
            (x2,y2)=self.coords("laser2")
            if (x2>=x1-1 and x2<=x1+37 and y2+15>=y1):
                self.last_ship_pos=[x1,y1]
                self.delete("ship")
                self.create_explosion2()
                self.delete("laser")
                self.after(400,self.delete_explosion)
                
                
            
    def create_explosion2(self):
       self.explosion_position=(self.last_ship_pos[0],self.last_ship_pos[1])
       self.create_image(*self.explosion_position,image=self.explosion_body,tag='explosion')
       
root.title("Invader with Tkinter")
root.resizable(False,False) 
board=Invader()
board.pack()

root.mainloop()