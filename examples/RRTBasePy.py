from cgitb import grey
import random
import math
from tracemalloc import start
from unittest.mock import seal
from cv2 import fastNlMeansDenoising
import pygame
import sys
sys.path.insert(0, '/home/murilo/Documentos/fbot-vss-python/src/')
import FIRALib


class RRTMap:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        self.start = start
        self.goal = goal
        self.MapDimensions = MapDimensions
        self.Maph, self.Mapw = self.MapDimensions

        self.MapWindowsName = "VSS - RRT path planning"
        pygame.display.set_caption(self.MapWindowsName) #nome da janela
        self.map = pygame.display.set_mode(( self.Mapw, self.Maph)) # dimensões do campo
        self.map.fill(( 255, 255, 255))
        self.nodeRad = 2
        self.nodeThinckness=0
        self.edgeThinckness = 1

        self.obstacles = []
        self.obsdim = obsdim
        self.obsNumber = obsnum

        self.borda1= (0,0)
        self.borda11= (0,15)

        #Cores
        self.grey = (70, 70, 70)
        self.blue = (0, 0, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.white = (255, 255, 225)
        self.black = (0,0,0)

    def drawMap(self, obstacles):
        pygame.draw.circle(self.map, self.blue, self.start, self.nodeRad+25,0)
        pygame.draw.circle(self.map, self.green,self.goal,self.nodeRad+10,0)

        
        self.drawObs(obstacles)

    def drawPath(self, path):
        for node in path:
            pygame.draw.circle(self.map, self.red, node, self.nodeRad+3,0)


    def drawObs(self, obstacles):
        obstaclesList = obstacles.copy()
        while (len(obstaclesList)>0):
            obstacle = obstaclesList.pop(0)
            #print(obstacle)
            #pygame.draw.circle(self.map, self.black,(obstacle[0],obstacle[1]),self.nodeRad+25,0)
            pygame.draw.rect(self.map, self.black, obstacle)


class RRTGraph:
    def __init__(self, start, goal, MapDimensions, obsdim, obsnum):
        (x,y) = start
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.maph, self.mapw = MapDimensions
        self.x=[]
        self.y=[]
        self.parent=[]

        #inicializando a árvore
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        # Obstaculos
        self.osbtacles = []
        self.obsDim = obsdim
        self.obsNum = obsnum

        # caminho

        self.goalstate = None
        self.path = []


    #def import_position(self):
    #    uppercornerx = int(random.uniform(0,self.mapw - self.obsDim))#posição do obstaculo
    #    uppercornery = int(random.uniform(0,self.maph - self.obsDim))

    #    return (uppercornerx, uppercornery)
    
    def makeobs(self):
        obs = []

        for i in range(0, self.obsNum):
            blue_0 = FIRALib.blue_car(0)
            blue_1 = FIRALib.blue_car(1)
            blue_2 = FIRALib.blue_car(2)
            yellow_1 = FIRALib.yellow_car(1)
            yellow_2 = FIRALib.yellow_car(2)
            blue_0 = (-75 + 428+(blue_0[0]/2)*1000,-75 + 305 - (blue_0[1]/2)*1000,)
            blue_1 = (-75 + 428+(blue_1[0]/2)*1000, -75 + 305 - (blue_1[1]/2)*1000,self.obsDim, self.obsDim)
            blue_2 = (-75 + 428+(blue_2[0]/2)*1000, -75 + 305 - (blue_2[1]/2)*1000,self.obsDim, self.obsDim)
            yellow_1 = (-75 + 428+(yellow_1[0]/2)*1000, -75 + 305 - (yellow_1[1]/2)*1000,self.obsDim, self.obsDim)
            yellow_2 = (-75 + 428+(yellow_2[0]/2)*1000, -75 + 305 - (yellow_2[1]/2)*1000,self.obsDim, self.obsDim)
            rectang = None
            startgoalcol = True
            borda1 = (0, 0, 50, 203)
            borda2 = (0, 406, 50, 610)
            borda3 = (806, 0, 50, 203)
            borda4 = (806, 406, 50, 610)
            while startgoalcol:
                #upper = self.makeRandomRect()
                rectang = pygame.Rect(blue_0,(self.obsDim, self.obsDim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol = True
                else:
                    startgoalcol = False
            obs.append(rectang)
            obs.append(blue_1)
            obs.append(blue_2)
            obs.append(yellow_1)
            obs.append(yellow_2)
            obs.append(borda3)
            obs.append(borda4)
            obs.append(borda1)
            obs.append(borda2)

        self.obstacles = obs.copy()
        return obs

    def add_node(self, n, x, y):
        self.x.insert(n,x)   #pega os valores de X e Y e coloca nas listas
        self.y.append(y)     #Correspondentes

        

    def remove_node(self,n):
        self.x.pop(n)   #Removes as valores X e Y
        self.y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child,parent) #Adiciona pai e filho a lista

    def remove_edge(self,n):    
        self.parent.pop(n)  #Remove o Filho

    def number_of_nodes(self):
        return len(self.x)

    def distance(self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        px = (float(x1)-float(x2))**2
        py = (float(y1)-float(y2))**2  #calcula as distancias dos pontos
        return (px+py)**(0.5)

    def sample_envir(self):
        x = int(random.uniform(0,self.mapw)) #gera amostras aleatoria no mapa
        y = int(random.uniform(0,self.maph))
        return x,y

    def nearest(self,n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(0,n):
            if self.distance(i, n)<dmin:
                dmin = self.distance(i, n)
                nnear=i
        return nnear

    def isFree(self):
        n = self.number_of_nodes()-1
        (x,y) = (self.x[n],self.y[n])
        obs = self.obstacles.copy()         #tentar enteder melhor depois
        while len(obs)>0:                   #os nós não ocuparem o mesmo lugar que os obstaculos

            rectang = obs.pop(0)
            rectang = pygame.Rect(rectang)
            if rectang.collidepoint(x,y):
                self.remove_node(n)
                return False
        return True

    def crossObstacle(self,x1,x2,y1,y2):
        obs = self.obstacles.copy()
        while(len(obs)>0):
            rectang=obs.pop(0)              #Tentar entender melhor depois
            for i in range(0,101):
                u=i/100
                x= x1*u + x2*(1-u)
                y=y1*u + y2*(1-u)
                #rectang = obs.pop(0)
                rectang = pygame.Rect(rectang)
                if rectang.collidepoint(x,y):
                    return True
        return False

    def connect(self,n1,n2):
        (x1,y1)=(self.x[n1],self.y[n1])
        (x2,y2)=(self.x[n2],self.y[n2])
        if self.crossObstacle(x1,x2,y1,y2):
            self.remove_node(n2)            #faz a conexão dos nós
            return
        else:
            self.add_edge(n1,n2)
            return True

    def step(self, nnear, nrand, dmax=35):
        d = self.distance(nnear, nrand)
        if d>dmax:
            u= dmax/d
            (xnear, ynear) = (self.x[nnear],self.y[nnear])
            (xrand,yrand) = (self.x[nrand],self.y[nrand])
            (px,py) = (xrand - xnear, yrand-ynear)
            theta = math.atan2(py,px)
            (x,y)=(int(xnear + dmax * math.cos(theta)), int(ynear + dmax * math.sin(theta)))
            self.remove_node(nrand)
            if abs(x-self.goal[0])<dmax and abs(y - self.goal[1])<dmax:
                self.add_node(nrand, self.goal[0], self.goal[1])
                self.goalstate =  nrand
                self.goalFlag = True
            else:
                self.add_node(nrand,x,y)

    def path_to_goal(self):
        if self.goalFlag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while (newpos != 0):
                self.path.append(newpos)
                newpos=self.parent[newpos]
            self.path.append(0)
        return self.goalFlag

    def getPathCoords(self):
        pathCoords=[]
        for node in self.path:
            x, y =(self.x[node], self.y[node])
            pathCoords.append((x,y))
        return pathCoords


    def bias(self, ngoal):
        n = self.number_of_nodes()
        self.add_node(n,ngoal[0],ngoal[1])
        nnear = self.nearest(n)
        self.step(nnear, n)
        self.connect(nnear,n)
        return self.x,self.y,self.parent

    def expand(self):
        n = self.number_of_nodes()
        x,y = self.sample_envir()
        self.add_node(n,x,y)
        if self.isFree():
            xnearest = self.nearest(n)
            self.step(xnearest,n)
            self.connect(xnearest,n)
        return self.x,self.y,self.parent

    def cost(self):
        pass







    
