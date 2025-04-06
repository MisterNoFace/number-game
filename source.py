import pygame,sys,numpy,os,time
from random import randint
pygame.init()

screen=pygame.display.set_mode((600,600))
pygame.display.set_caption("")
font=pygame.font.Font("font.ttf",120)
correct_order=numpy.array([
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,'']
])
def shuffle_matrix(m):
    for x,block in enumerate(m):
        for y,i in enumerate(block):
            randX,randY=randint(0,3),randint(0,3)
            aux=m[x][y]
            m[x][y]=m[randX][randY] 
            m[randX][randY]=aux
    return m
items=shuffle_matrix(correct_order.copy())

arrow=[pygame.image.load('images/'+i) for i in os.listdir('images')]  
arrowframe=0
arrowW,arrowH=arrow[0].get_width(),arrow[0].get_height()

pos=(0,0)
rect_size=150
pad=20
moves={
    'right':False,
    'left':False,
    'down':False,
    'up':False,
}
while True:
    screen.fill((160,224,242))
    arrowframe+=0.2
    if arrowframe>=len(arrow):
        arrowframe=0
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if numpy.array_equal(items,correct_order):
                if event.key==pygame.K_SPACE:
                    items=shuffle_matrix(items)     
            else:
                x=pos[0]
                y=pos[1]
                if event.key==pygame.K_RIGHT and moves['right']:
                    x=pos[0]
                    y=pos[1]-1
                elif event.key==pygame.K_LEFT and moves['left']:
                    x=pos[0]
                    y=pos[1]+1
                elif event.key==pygame.K_DOWN and moves['down']:
                    x=pos[0]-1
                    y=pos[1]
                elif event.key==pygame.K_UP and moves['up']:
                    x=pos[0]+1
                    y=pos[1]
                items[pos[0]][pos[1]]=items[x][y]
                items[x][y]=''
            

    for x,block in enumerate(items):
        for y,i in enumerate(block):
            if i!='':
                img=font.render(str(i),False,(255,255,255))
                rect=pygame.Rect(y*rect_size,x*rect_size,rect_size,rect_size)
                visible_rect=pygame.Rect(rect.x+pad/2,rect.y+pad/2,rect.width-pad,rect.height-pad)
                pygame.draw.rect(screen,(50,200,100),visible_rect)
                screen.blit(img,(rect.x+(rect.width/2-img.get_width()/2),rect.y+(rect.height/2-img.get_height()/2)))
            else:
                pos=(x,y)
       
    if pos[1]>0:
        moves['right']=True
    else:
        moves['right']=False
    if pos[1]<3:
        moves['left']=True
    else:
        moves['left']=False
    if pos[0]>0:
        moves['down']=True
    else:
        moves['down']=False
    if pos[0]<3:
        moves['up']=True
    else:
        moves['up']=False

    if moves['right']:
        screen.blit(pygame.transform.rotate(arrow[int(arrowframe)],180),(pos[1]*rect_size,pos[0]*rect_size+(rect_size/2-arrowH/2)))
    if moves['left']:
        screen.blit(pygame.transform.rotate(arrow[int(arrowframe)],0),(pos[1]*rect_size+(rect_size-arrowW),pos[0]*rect_size+(rect_size/2-arrowH/2)))
    if moves['up']:
        screen.blit(pygame.transform.rotate(arrow[int(arrowframe)],270),(pos[1]*rect_size+(rect_size/2-arrowW/2),pos[0]*rect_size+(rect_size-arrowH)))
    if moves['down']:
        screen.blit(pygame.transform.rotate(arrow[int(arrowframe)],90),(pos[1]*rect_size+(rect_size/2-arrowW/2),pos[0]*rect_size))


    if numpy.array_equal(items,correct_order):
        finaltext='you completed it!'+'\npress SPAZIO\nto restart'
        img=font.render(finaltext,False,(255,255,255))
        s=pygame.display.get_window_size()
        r=pygame.Surface((s[0],s[1]))
        r.fill((0,0,0))
        r.set_alpha(200)
        screen.blit(r,(0,0))
        screen.blit(img,(s[0]/2-img.get_width()/2,s[1]/2-img.get_height()/2))

    pygame.display.update()
    pygame.time.Clock().tick(60)