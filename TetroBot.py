from copy import deepcopy #used to create copies of lists
import numpy as np
import tkinter, random
canvas=tkinter.Canvas(width=500,height=600)
canvas.pack()
colors = ['#cfcfcf','#FF971C','#0341AE','#72C838','#FF3213','#FFD500','#13F4EF','#800080']


clearedLines=0
canvas.create_text(415,130,font ='Bold 20',text='Lines Cleared:')
canvas.create_text(415,180, font ='Bold 20',text='0', tag = 'a')
def updateText():
    canvas.delete('a')
    canvas.create_text(415,180,font ='Bold 20', text=str(clearedLines), tag = 'a')


state = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def draw(state):
    for x in range(10):
        for y in range(20):
            colo='#cfcfcf'
            for i in range(len(colors)):
                if i==state[y][x]:
                    colo=colors[i]
            
            canvas.create_rectangle(30*x,30*y,30+30*x,30+30*y, fill = colo)
draw(state)



# O B G R Y T M
# 1 2 3 4 5 6 7
#orange, blue , green, red, yellow, turqoise, magenta

blocks=[[[1,1,1],
        [1,0,0]],

        [[2,2,2],
        [0,0,2]],

        [[0,3,3],
        [3,3,0]],

        [[4,4,0],
        [0,4,4]],

        [[5,5],
        [5,5]],

        [[6,6,6,6],
        ],
        
        [[7,7,7],
        [0,7,0]]]




#Is it possible to place the block on a certain position on the board
# X,Y are the coordinates of the playing field and the top left corner of the block is fit onto X,Y
def possibleMove(block, state, X, Y):
    for y in range(len(block)):
        for x in range(len(block[y])):
            if state[Y+y][X+x]!=0 and block[y][x]!=0:
                return 0
    return 1


# Finding lowest row to place a block in a column given by X, where the most left column of the block is in the X column
def findLowestY(block, state, X):
    for Y in range(0, len(state)-len(block)+1):
        if not possibleMove(block, state, X, Y):
            if Y==0:
                return(-1)
            return Y-1
    return len(state)-len(block)

#Evaluates the board state: the lower the better. Used to compare which moves are better or worse
def eval(state):
    #Calculates the perimeter
    perimeter = 0
    for x in range(len(state[0])):
        for y in range(len(state)):
            if y>1:
                if state[y][x]!=0 and state[y-1][x]==0:
                    perimeter+=1
            if y<len(state)-1:
                if state[y][x]!=0 and state[y+1][x]==0:
                    perimeter+=1
            if x>0:
                if state[y][x]!=0 and state[y][x-1]==0:
                    perimeter+=1
            if x<len(state[0])-1:
                if state[y][x]!=0 and state[y][x+1]==0:
                    perimeter+=1
    #Checks for holes
    holes = 0
    for x in range(len(state[0])):
        for y in range(len(state)-2):
            if state[y][x]!=0 and state[y+1][x]==0 and state[y+2][x]!=0:
                holes+=1

    # Checks for height
    height=0
    for x in range(len(state[0])):
        a=[state[y][x] for y in range(len(state))]
        if len([i for i, x in enumerate(a) if x])>0:
            height+=(len(state)-[i for i, x in enumerate(a) if x][0])**2


    return 2*perimeter+height+holes*20

#Add the block to the playing field to the position XX,YY fit to the top left square of the block
def stateAddBlock(State,block,XX,YY):
    State2=deepcopy(State)
    for y in range(len(block)):
        for x in range(len(block[y])):
            if block[y][x]!=0:
                State2[YY+y][XX+x]=block[y][x]
    return State2


    

def optimalBlock(state,block):
    mini=9999
    atX=9999
    
    optimalBlock=0
    Block=deepcopy(block)
    for i in range(4):
        Block=np.rot90(Block).tolist()
        for x in range(0, len(state[0])-len(Block[0])+1):
            b=eval(stateAddBlock(state, Block, x,findLowestY(Block, state, x)))
            if b < mini:
                mini = b
                atX=x
                optimalBlock = Block
    return atX,optimalBlock

def checkIfTetris():
    for y in range(len(state)):
        if (0 not in state[y]):
            return 1
    return 0
def findTetrisRow():
    y=len(state)-1
    while y>=0:
        
        if (0 not in state[y]):
            return y
        y-=1
    
        
def removeTetrisRow(state):
    global clearedLines
    clearedLines+=1
    updateText()
    State=deepcopy(state)
    i=findTetrisRow()
    while i>0:
        State[i]=deepcopy(State[i-1])
        i-=1
    State[0]=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return State
def CheckLost():
    if deepcopy(state[0])!=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        canvas.create_text(250,300,font='Bold 30', text='End of game!')
        return 1
    return 0

nextBlock = random.choice(blocks)
currentBlock=0
def click():
    global state, nextBlock, currentBlock
    currentBlock=nextBlock
    nextBlock = random.choice(blocks)
    state=stateAddBlock(state,optimalBlock(state,currentBlock)[1],optimalBlock(state,currentBlock)[0],findLowestY(optimalBlock(state,currentBlock)[1], state,optimalBlock(state,currentBlock)[0]) )
    draw(state)
    
    while(checkIfTetris()):
        state=removeTetrisRow(state)
    if not CheckLost():
        canvas.after(100,click)
click()
#canvas.bind('<Button-1>', click)
tkinter.mainloop()
