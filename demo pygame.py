import pygame
from pygame.locals import *
import time
import sys
from random import randint
from copy import deepcopy
import threading

def judge(table,turn):
    value=0
    #横
    for i in range(len(table)):
        l=0
        rightPos=0
        for j in range(len(table[i])):
            if table[i][j]==turn :
                if l==0:#judge if it's the first
                    if j!=0 and not table[i][j-1]:#judge if the last one is space
                        rightPos+=1
                l+=1
                if l>=4:
                    return(9999999999999)
            if table[i][j]!=turn:
                if l!=0:
                    if not table[i][j]:#judge if the next one is space
                        rightPos+=1
                    if l>=3 and rightPos==2:
                        return(100000)
                    if rightPos!=0:
                        value+=min(int(10*10**(l+rightPos-1)),100000)
                    l=0
                    rightPos=0
            if j==len(table[i])-1:
                if l>=3 and rightPos==2:
                        return(100000)
                if l!=0:
                    if rightPos!=0:
                        value+=min(int(10*10**(l+rightPos-1)),100000)
                    l=0
                    rightPos=0
                
    for j in range(len(table[0])):
        l=0
        rightPos=0
        for i in range(len(table)):
            if table[i][j]==turn :
                if l==0:
                    if i!=0 and not table[i-1][j]:
                        rightPos+=1
                l+=1
                if l>=4:
                    return(9999999999999)
            if l!=0 and table[i][j]!=turn:
                if not table[i][j]:
                    rightPos+=1
                if l>=3 and rightPos==2:
                        return(100000)
                if rightPos!=0:
                    value+=min(int(10*10**(l+rightPos-1)),100000)
                l=0
                rightPos=0
            if i==len(table)-1:
                if l>=3 and rightPos==2:
                        return(100000)
                if l!=0:
                    if rightPos!=0:
                        value+=min(int(10*10**(l+rightPos-1)),100000)
                    l=0
                    rightPos=0
    diago=[]
    for i in range(len(table)):
        diago.append([])
        j=0
        while i+j<len(table) and j<len(table[0]):
            diago[-1].append(table[i+j][j])
            j+=1
    for i in range(1,len(table[0])):
        diago.append([])
        j=0
        while j<len(table) and i+j<len(table[0]):
            diago[-1].append(table[j][i+j])
            #print(j,i+j)
            j+=1
    for i in range(len(table)):
        diago.append([])
        j=0
        while 0<=i-j<len(table) and j<len(table[0]):
            diago[-1].append(table[i-j][j])
            j+=1
    
    for i in range(1,len(table[0])):
        diago.append([])
        j=0
        while 0<=len(table)-j-1<len(table) and 0<=i+j<len(table[0]):
            diago[-1].append(table[len(table)-j-1][i+j])
            j+=1
    for i in range(len(diago)):
        l=0
        rightPos=0
        for j in range(len(diago[i])):
            if diago[i][j]==turn :
                if l==0:
                    if j!=0 and not diago[i][j-1]:
                        rightPos+=1
                l+=1
                if l>=4:
                    return(9999999999999)
            if diago[i][j]!=turn:
                if l!=0:
                    if not diago[i][j]:
                        rightPos+=1
                    if l>=3 and rightPos==2:
                        return(100000)
                    if l>=4:
                        return(9999999999999)
                    if rightPos!=0:
                        value+=min(int(10*10**(l+rightPos-1)),100000)
                    l=0
                    rightPos=0
            if j==len(diago[i])-1:
                if l!=0:
                    if l>=3 and rightPos==2:
                        return(100000)
                    if l>=4:
                        return(9999999999999)
                    if rightPos!=0:
                        value+=min(int(10*10**(l+rightPos-1)),100000)
                    l=0
                    rightPos=0
    
    return(value)


"""def put(table,turn,j):
    for i in range(len(table)-1,-1,-1):
        #print(table[i][j])
        if table[i][j]==0:
            l=deepcopy(table)
            l[i][j]=turn
            #print(l)
            #input()
            return(l)
    return None"""

def dfs(table,turn,maxB,n,j,nb):

    if n!=m:
        bln=False
        for i in range(len(table)-1,-1,-1):
            if table[i][j]==0:
                table[i][j]=3-turn
                bln=True
                
                x,y=i,j
                break
        if not bln : #Have changed nothing
            return None
    log.write("       "*(m-n)+"第{:}重".format(m-n)+" 第{:}子".format(j+1)+"\r\n")
    for i in table:
        log.write("       "*(m-n)+str(i)+"\r\n")
    log.write("\r\n")
    #input()
    if n!=m and str(table)+str(nb-1) in dic:
        log.write("       "*(m-n)+"曾出现!"+"\r\n")
        log.write("       "*(m-n)+"分数:"+str(dic[str(table)+str(nb-1)])+"\r\n")
        return(dic[str(table)+str(nb-1)])
    
    scoreC=judge(table,ai)
    scoreP=judge(table,3-ai)
    log.write("       "*(m-n)+"玩家分数:"+str(scoreP)+"\r\n")
    log.write("       "*(m-n)+"电脑分数:"+str(scoreC)+"\r\n")
    v=scoreC-scoreP
    if nb==42:
        dic.update({str(table)+str(nb):v})
        return(v)
    

    if n!=m:
        if scoreC>=9999999999999 and not(maxB) and (m-n)==1:
            table[x][y]=0
            return(scoreC*100)
        if scoreC>=9999999999999:
            table[x][y]=0
            return(scoreC)
        if scoreP>=9999999999999 and maxB and (m-n)==2:
            table[x][y]=0
            return(-scoreP)
        if scoreP>=9999999999999:
            table[x][y]=0
            return(-scoreP)
   
    if int(n)<=0 and nb<20:
        dic.update({str(table)+str(nb):v})
        table[x][y]=0
        return(v)#Recursive termination
    
    if int(n)<=-1 and nb<27:
        dic.update({str(table)+str(nb):v})
        table[x][y]=0
        return(v)#Recursive termination
    if int(n)<=-2 and nb<34:
        dic.update({str(table)+str(nb):v})
        table[x][y]=0
        return(v)#Recursive termination
    if int(n)<=-3 and nb<=41:
        dic.update({str(table)+str(nb):v})
        table[x][y]=0
        return(v)#Recursive termination
    max_min=(-1)**maxB*999999999999999999999999
    ind=0

    if maxB:
        for i in range(len(table[0])):
            v=dfs(table,3-turn,not maxB,n-1,i,nb+1)
            if v==None:continue
            if v>max_min:
                max_min=v
                ind=i
        if n==m:
            return(ind)
        else:
            dic.update({str(table)+str(nb):v})
            table[x][y]=0
            return(max_min)
                
    else :
        #print()
        for i in range(len(table[0])):
            v=dfs(table,3-turn,not maxB,n-1,i,nb+1)
            if v==None:continue
            if v<max_min:
                max_min=v
                ind=i
        if n==m:
            return(ind)
        else:
            dic.update({str(table)+str(nb):v})
            table[x][y]=0
            return(max_min)
        
dic={}
pygame.mixer.init()
pygame.mixer.music.load('demo.mid')
channel = pygame.mixer.find_channel()
sound = pygame.mixer.Sound('fall.ogg')
pygame.mixer.music.play(-1)
m=4#floors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
PINK = (249, 57, 255)
LIGHT_BLUE = (54, 207, 241)
white_rect = pygame.Rect(0, 0, 824, 549)
pygame.init()
windowSurface = pygame.display.set_mode((824, 549))
font = pygame.font.Font("FreeSans.ttf", 50)
win_text = font.render("You've won", True, BLACK)
pygame.display.set_caption('Connect 4')
yellowPiece = pygame.image.load("yellowPiece.png")
bluePiece = pygame.image.load("bluePiece.png")
board = pygame.image.load("board.png")
highLight = pygame.image.load("highLignt.png")
board = pygame.transform.scale(board, (824, 549))
highLight = pygame.transform.scale(highLight, (101, 549))
l_piece=90
yellowPiece = pygame.transform.scale(yellowPiece, (l_piece, l_piece))
bluePiece = pygame.transform.scale(bluePiece, (l_piece, l_piece))
wait=False
log=open("log.log","w")
table=[[0 for j in range(13)] for i in range(12)]

tableT=list(zip(*table))
tableStr=["" for i in range(7)]

threads=[]
turn=1
ai=randint(1,2)

log.write("电脑棋子:"+str(ai)+"\r\n")
first=True
nb=0
while 1:


    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(windowSurface, WHITE, white_rect)#White paper

    x_left=60
    col=((mouse_pos[0]-x_left)//101)#index
    x_hl=x_left+col*101
    
    if ai==turn:
        
        if not(wait):
            if first:
                col=3
            else:
                col=dfs([table[i][3:10] for i in range(3,9)],ai,True,m,-1,nb+1)
            #print(col)
            log.write("一步:"+"\r\n")
            if 0 in tableT[col+3][3:9]:
                x_falling=x_left+col*101
                col_falling=col
                turn_falling=turn
                wait=True
                y_shouldBe=(4-len(tableStr[col_falling]))*(l_piece-14)+114
                y_falling=0
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            if not(wait) and 0 in tableT[col+3][3:9] and -1<col<7:
                x_falling=x_hl
                col_falling=col
                turn_falling=turn
                wait=True
                y_shouldBe=(4-len(tableStr[col_falling]))*(l_piece-14)+114
                y_falling=0
    if wait: #When it's falling
        y_falling+=4+2*m
        if turn_falling==1: windowSurface.blit(yellowPiece, (x_left+97+(col_falling-1)*104,y_falling))
        if turn_falling==2: windowSurface.blit(bluePiece, (x_left+97+(col_falling-1)*104,y_falling))
    #Have fallen
    if wait and y_shouldBe-y_falling<=3:
        channel.play(sound) 
        first=False
        wait=False
        y_falling=y_shouldBe
        tableStr[col_falling]+=str(turn)
        tableT=list(zip(*table))    
        line=len(tableStr[col_falling])
        tableT[col_falling+3]=[0]*3+[0]*(6-line)+list(tableStr[col_falling])[::-1]+[0]*3
        tableT[col_falling+3]=list(map(int,tableT[col_falling+3]))
        table=list(map(list,list(zip(*tableT))))
        cor=[-3,-2,-1,+1,+2,+3] 
        diagsP=[[(cor[i+j],cor[i+j]) for j in range(3)]+[(0,0)] for i in range(4)]
        win = False
        if True in [len(list(set([table[13-line-4+diagsP[i][j][0]][col_falling+3+diagsP[i][j][1]] for j in range(4)])))==1 for i in range(4)]:
            win = True
        cor=[-3,-2,-1,+1,+2,+3]
        diagsP=[[(cor[i+j],-cor[i+j]) for j in range(3)]+[(0,0)] for i in range(4)]
        if True in [len(list(set([table[13-line-4+diagsP[i][j][0]][col_falling+3+diagsP[i][j][1]] for j in range(4)])))==1 for i in range(4)]:
            win = True
        win = judge([table[i][3:10] for i in range(3,9)],turn)==9999999999999 or judge([table[i][3:10] for i in range(3,9)],turn)==9999999999999 #win or str(turn)*4 in "".join(list(map(str,table[13-line-4]))) or str(turn)*4 in "".join(list(map(str,tableT[col_falling+3])))      

        nb+=1
        if win:
            for i in range(3,10):
                for j in range(3,11):
                    if table[i][j]==1:
                        windowSurface.blit(yellowPiece, (x_left+97+(j-4)*104,(i-4)*(l_piece-14)+114))
                    if table[i][j]==2:
                        windowSurface.blit(bluePiece, (x_left+97+(j-4)*104,(i-4)*(l_piece-14)+114))
            windowSurface.blit(board, (0,0))
            if ai==turn:win_text = font.render("You have lost!", True, BLACK)
            else :win_text = font.render("Player win!", True, BLACK)
            windowSurface.blit(win_text, (10, 20))
            pygame.display.update()
            time.sleep(3000)
            pygame.quit()
            sys.exit()
        if list(map(len,tableStr))==[6]*7:
            for i in range(3,10):
                for j in range(3,11):
                    if table[i][j]==1:
                        windowSurface.blit(yellowPiece, (x_left+97+(j-4)*104,(i-4)*(l_piece-14)+114))
                    if table[i][j]==2:
                        windowSurface.blit(bluePiece, (x_left+97+(j-4)*104,(i-4)*(l_piece-14)+114))

            windowSurface.blit(board, (0,0))
            win_text = font.render("No winnner!", True, BLACK)
            windowSurface.blit(win_text, (10, 20))
            pygame.display.update()
            time.sleep(3000)
            pygame.quit()
        turn=3-turn
    if -1<col<7:    
        windowSurface.blit(highLight, (x_hl,0))

    for i in range(3,10):
        for j in range(3,11):
            if table[i][j]==1:
                windowSurface.blit(yellowPiece, (x_left+97+(j-4)*104,(i-4)*(l_piece-14)+114))
            if table[i][j]==2:
                windowSurface.blit(bluePiece, (x_left+97+(j-4)*104,(i-4)*(l_piece-14)+114))
    windowSurface.blit(board, (0,0))
    if turn==1: windowSurface.blit(yellowPiece, (750,0))
    if turn==2: windowSurface.blit(bluePiece, (750,0))
    pygame.display.update()


            
    
    
        
