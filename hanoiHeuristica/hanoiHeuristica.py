from ast import While
from asyncio.windows_events import NULL
from collections import deque
from copy import copy, deepcopy
import functools
from pickle import NONE
from turtle import *
import turtle
import time

#CLASE NODO QUE REPRESENTA CADA ESTADO DEL PROBLEMA
#LAS TRES TORRES SE REPRESENTAN CON PILAS DE NUMEROS DE ENTEROS
#EL DISCO MAS PEQUENO SE REPRESENTA CON UN 1, Y EL N-ESIMO DISCO SE REPRESENTA CON N
class Nodo:     #seLf, costo, nodo Padre, pila1,pila2,pila3
    def __init__(self,c,n,t1,t2,t3):
        self.costo=c        #CANTIDAD DE MOVIMIENTOS PARA LLEGAR A ESTE NODO PARTICULAR, COSTO DEL PADRE +1
        self.padre=n        #NODO PADRE
        self.torreA=t1      #POR CONVENCION, SIEMPRE SE EMPIEZA DESDE LA TORRE A
        self.torreB=t2
        self.torreC=t3
    #FUNCION PARA IMPRIMIR UN ESTADO (LOS DISCOS DE CADA TORRE)    
    def imprimir(self):
        print(self.torreA)
        print(self.torreB)
        print(self.torreC)
        

#FUNCION OBJETIVO, BASTA CON VER QUE LA TORRE A, DONDE SE PONEN TODOS LOS DISCOS AL INICIO, ESTE VACIA
#LUEGO COMPORBAR QUE TODOS LOS DISCOS ESTEN EN ALGUNA DE LAS OTRAS DOS TORRES
def funObjectivo(n,numDiscos):
    return ( (len(n.torreA)==0) & ( (len(n.torreB)==numDiscos) | (len(n.torreC)==numDiscos)) )

#FUNCION SUCESRES, PARA CADA TORRE SE COMPRUEBA SI ES POSIBLE MOVER SU CIMA ACTUAL A ALGUNA DE LAS OTRAS DOS TORRES
def funSucesores(n):
   sucesores=[]   
#COMPROBAR MOVIMIENTO DESDE LA TORRE A, HACIA B Y C
   if(len(n.torreA)>0):
        x=n.torreA[-1]
        if(len(n.torreB)==0 or x<n.torreB[-1]):
            copia=deepcopy(n)   #SE GENERA COPIA DEL NODO DEL QUE ESTAMOS GENERANDO LOS  
            copia.padre=n       
            copia.costo=n.costo+1   #SE CALCULA EL COSTO
            copia.torreB.append(copia.torreA.pop())     #SE MUEVE EL DISCO
            sucesores.append(copia)
        if(len(n.torreC)==0 or x<n.torreC[-1]):
            copia=deepcopy(n)
            copia.padre=n
            copia.costo=n.costo+1
            copia.torreC.append(copia.torreA.pop())
            sucesores.append(copia)    
#COMPROBAR MOVIMIENTO DESDE LA TORRE B, HACIA A Y C
   if(len(n.torreB)>0):
        x=n.torreB[-1]
        if(len(n.torreA)==0 or x<n.torreA[-1]):
            copia=deepcopy(n)
            copia.padre=n
            copia.costo=n.costo+1
            copia.torreA.append(copia.torreB.pop())
            sucesores.append(copia)
        if(len(n.torreC)==0 or x<n.torreC[-1]):
            copia=deepcopy(n)
            copia.padre=n
            copia.costo=n.costo+1
            copia.torreC.append(copia.torreB.pop())
            sucesores.append(copia)                
#COMPROBAR MOVIMIENTO DESDE LA TORRE C, HACIA A Y B
   if(len(n.torreC)>0):
        x=n.torreC[-1]
        if(len(n.torreA)==0 or x<n.torreA[-1]):           
            copia=deepcopy(n)
            copia.padre=n
            copia.costo=n.costo+1
            copia.torreA.append(copia.torreC.pop())
            sucesores.append(copia)
        if(len(n.torreB)==0 or x<n.torreB[-1]):
            copia=deepcopy(n)
            copia.padre=n
            copia.costo=n.costo+1
            copia.torreB.append(copia.torreC.pop())
            sucesores.append(copia)                 
   return sucesores


#FUNCION PARA COMPARAR SI DOS ESTADOS SON IGUALES (SUS TORRES SON IDENTICAS)
def comNodos(n1,n2):
    flag=True
    if(len(n1.torreA)==len(n2.torreA) and len(n1.torreB)==len(n2.torreB) and len(n1.torreC)==len(n2.torreC)):
       for i in range (0,len(n1.torreA)):
           if(n1.torreA[i]!=n2.torreA[i]):
               flag=False
       for i in range (0,len(n1.torreB)):
           if(n1.torreB[i]!=n2.torreB[i]):
               flag=False
       for i in range (0,len(n1.torreC)):
           if(n1.torreC[i]!=n2.torreC[i]):
               flag=False
    else:
        flag=False
    return flag



#FUNCION HEURISTICA F(N)=H(N)+G(N)
#DONDE G(N) ES EL COSTO ACUMULADO, Y H(N) ES EL COSTO RESTANTE HASTA EL OBJETIVO
def funHeuristica(n):
    distObj=0   #DISTANCIA HASTA EL OBJETIVO G(N)
    paso=0      #SIGUIENTE DISCO POR ACOMODAR
    flag=True
    #DISATANCIA HASTA EL OBJETIVO (REPRESENTADA POR LA CANTIDAD DE DISCOS CONSECUTIVOS EN LA PRIMERA TORRE)
    for i in range (0,len(n.torreA)):
        if(n.torreA[i]==discos-i and flag):
            distObj+=n.torreA[i]      
            paso=n.torreA[i]    #OBTENER EL DISCO ACTUAL CON EL QUE SE "TRABAJA"
        else:
            flag=False
    
    distObj=2**distObj           
    #c=(2**discos)-(2**(paso-1))    ##ESTO ES PEOR (NO PONER)!!!

    ##COMPROBAR SI EN ALGUNA OTRA TORRE SE HA RESUELTO EL ANTERIOR CASO, Y DE SER ASI USARLO PARA MEJORAR EL PESO DEL ESTADO
    paso=paso-1
    parametro=1     #SUMA DE DISCOS QUE HAN SIDO COLOCADOS CONSECUTIVAMENTE DE FORMA "CORRECTA"
    flag=True
    if(len(n.torreB)>0 and (n.torreB[0]==paso)):
        for i in range (0,len(n.torreB)):
            if(n.torreB[i]==paso-i and flag):
                parametro+=n.torreB[i]
            else:
                flag=False
        
    if(len(n.torreC)>0 and n.torreC[0]==paso):
        for i in range (0,len(n.torreC)):
            if(n.torreC[i]==paso-i and flag):
                parametro+=n.torreC[i]
            else:
                flag=False    
    #EL PARAMETRO FUNCIONA COMO CONTRAPESO DEL COSTO EN SI
    return float((n.costo/parametro)+distObj)

#IMPLEMENTACION A*
def AEstrella(numDiscos):
    
    stack = deque()
    for x in reversed(range(discos)):
        stack.append(x+1)
    raiz=Nodo(0,NULL,stack,deque(),deque())
    raiz.imprimir()
    
    Lista=[raiz]    #LISTA=FRONTERA
    visitados=[]    #LISTA DE ESTADOS YA VISITADOS
    revisado=Lista[0]

    while len(Lista)>0:
        if(funObjectivo(revisado,discos)):
            #print("ENCONTRADO")
            return revisado
        else:
            visitados.append(Lista.pop(0))
            for x in funSucesores(revisado):
                flag=True
                for y in visitados:
                    if(comNodos(x,y)):
                        flag=False
                if(flag):
                    Lista.append(x)
            #ORDENAR
            Lista.sort(key=funHeuristica)
            
            if(revisado.costo>0 and revisado.costo%100==0):
                for x in visitados:
                    if(x.costo<(revisado.costo**0.5)):
                        visitados.remove(x)
            """             #VER LISTA CONFORME AVANZA EL ALGORITMO
            print("***********************************LISTA ACTUAL*******************************************")
            for x in Lista:
                print("COSTO RAIZ: ",x.costo)
                print("COSTO TOTAL: ",funHeuristica(x))
                x.imprimir()
            input()
            print(len(Lista))
            """
            revisado=Lista[0]    
            print("COSTO REVISADO ACTUAL:",revisado.costo)
    print("SIN SOLUCION")
    return NULL



###################################FUCNIONES GRAFICAS
def linea(x1,y1,x2,y2):
    turtle.up()
    turtle.goto(x1,y1)
    turtle.down()
    turtle.goto(x2,y2)

def rectangulo(x,y,size):
    t1.up()
    t1.goto(x,y)
    t1.down()
    t1.fillcolor('blue') 
    t1.begin_fill()
    t1.forward(size)
    t1.left(90)
    t1.forward(30)    
    t1.left(90)
    t1.forward(size)
    t1.left(90)
    t1.forward(30)
    t1.left(90)
    t1.end_fill()
    
def dibPostes():
    linea(200,100,500,100)    
    linea(600,100,900,100)
    linea(1000,100,1300,100)
    
    linea(350,100,350,400)
    linea(750,100,750,400)
    linea(1150,100,1150,400)

def dibEstado(n):
    y=100
    for d in n.torreA:
        rectangulo(350-(d*25),y,d*50)
        y+=30
    y=100
    for d in n.torreB:
        rectangulo(750-(d*25),y,d*50)
        y+=30   
    y=100
    for d in n.torreC:
        rectangulo(1150-(d*25),y,d*50)
        y+=30
    turtle.update()
    time.sleep(3)
    t1.clear()

############################################FUCNIONES GRAFICAS FIN


##INCIO ALGORITMO

print("POR FAVOR INTRODUZCA LA CANTIDAD DE DISCOS:")
discos=input()
discos=int(discos)
solucion = deque()
#APLICAR ALGORITMO
resultado=AEstrella(discos)
#COMPROBAR E IMPRIMIR SOLUCION
if(resultado is None):
    print("ERROR")
else:
    t1=turtle.Turtle()
    turtle.tracer(0,0)
    turtle.setworldcoordinates(0,0,1400,1400)
    turtle.title("TORRES DE HANOI")
    #DIB POSTES
    dibPostes()
    
    while resultado.padre!=NULL:
        solucion.append(resultado)
        resultado=resultado.padre
    solucion.append(resultado)
    print("\n\nSOLUCION: ")
    resultado=solucion.pop()
    while len(solucion)>0:
        print()
        resultado.imprimir()
        dibEstado(resultado)
        resultado=solucion.pop()
    print()
    resultado.imprimir()
    dibEstado(resultado)
    turtle.done()


        



