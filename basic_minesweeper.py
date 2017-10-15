import os
clear = lambda: os.system('cls')
import time


def rules():
    print '\n\n1.)Click on cells by entering their row followed by space followed by column'
    print '    For example, for selecting cell (1,2), enter "1 2"\n'
    print '2.)You may flag cells possibly containing bombs for reference\n'
    print '4.)To unflag a cell, click on it (figuratively, of course)\n'
    print '\nReady to have Fun?'
    raw_input()
    return 0;

def create_grid(level):
    #let grid be the answer/underlying grid
    #display_grid is displayed. A value of 0 means it has not been clicked yet

    if level==0:#beginner
        grid=[[' ' for i in range(10)] for j in range(10)]
        display_grid=[[0 for i in range(10)] for j in range(10)]
        noOfBombs=10
    elif level==1:#intermediate
        grid=[[' ' for i in range(16)] for j in range(16)]
        display_grid=[[0 for i in range(16)] for j in range(16)]
        noOfBombs=40
    elif level==2:
        grid=[[' ' for i in range(16)] for j in range(30)]
        display_grid=[[0 for i in range(16)] for j in range(30)]
        noOfBombs=99
    grid_dimensions=[i+1,j+1];
    return grid,noOfBombs,display_grid,grid_dimensions;

def fill_grid(noOfBombs,grid,grid_dimensions):
    grid=insert_bombs(noOfBombs,grid,grid_dimensions)
    #after inserting bombs, calculate the values for each cell
    for i in range(grid_dimensions[0]):
        for j in range(grid_dimensions[1]):
            if grid[i][j]!='B':
                count=0;
                for x in range(-1,2,1):
                    for y in range(-1,2,1):
                        if i+x>=0 and j+y>=0 and i+x<grid_dimensions[0] and j+y<grid_dimensions[1] and grid[i+x][j+y]=='B':
                            count+=1
                grid[i][j]=count
    return grid;



def insert_bombs(noOfBombs,grid,grid_dimensions):
    import random
    i=0
    while(i!=noOfBombs):
        x=random.randrange(0,grid_dimensions[0])
        y=random.randrange(0,grid_dimensions[1])
        if grid[x][y]!='B':
            #check if the space is available
            grid[x][y]='B'
            i+=1
    return grid;

def avalanche(grid,display_grid,grid_dimensions,i,j,count):

    #keep displaying the grid until the empty space is completely visible
    #I'm thinking, recursion for adjacent empty spaces?

    for x in range(-1,2,1):
        for y in range(-1,2,1):
            if i+x>=0 and j+y>=0 and i+x<grid_dimensions[0] and j+y<grid_dimensions[1]:#deals with edges
                if [i+x,y+j]!=[i,j] and grid[x+i][y+j]!='B' and display_grid[i+x][j+y]==0:
                    display_grid[i+x][j+y]=1
                    count+=1
                    if grid[i+x][j+y]==0:
                        grid,display_grid,grid_dimensions,i,j,count=avalanche(grid,display_grid,grid_dimensions,i+x,j+y,count);
                        i=i-x;
                        j=j-y;
                    #display(grid,display_grid,grid_dimensions);
    display_grid[i][j]=1;
    count+=1
    return grid,display_grid,grid_dimensions,i,j,count;



def display(grid,display_grid,grid_dimensions):
    clear()
    print '\n\t\t\t    |',
    for j in range(grid_dimensions[1]):
        if j<10:
            print '0'+str(j)+' ',
        else:
            print str(j)+' ',
    print ''
    print '\t\t\t',
    for j in range(grid_dimensions[1]*2+3):
        print '_',
    print '\n'
    for i in range(grid_dimensions[0]):
        if i<10:
            print '\t\t\t0'+str(i)+' |',
        else:
            print '\t\t\t'+str(i)+' |',
        for j in range(grid_dimensions[1]):
            if display_grid[i][j]==1:
                if grid[i][j]!='B':
                    print ' ',grid[i][j],
                else:
                    print '|B|',
            elif display_grid[i][j]==2:
                print '  X',
            else:
                print '  -',
        print '\n'
    return 0;

def revealCells(grid,display_grid,grid_dimensions,i,j,f):
    #this function means that if you click on any cell which has all of its
        #bombs flagged, its neighbouring cells will be revealed
    #the same effect can be found in real minesweeper games, by double clicking on a cell

    #unfortunately, if you have flagged a wrong cell and call this function, you will lose

    count=0

    for x in range(-1,2,1):
        for y in range(-1,2,1):
            if x+i>=0 and y+j>=0 and x+i<grid_dimensions[0] and y+j<grid_dimensions[1]:
                if display_grid[x+i][y+j]==2:
                    if grid[x+i][y+j]!='B':
                        print '\t\t\tOh No! You had flagged the wrong cell!\n'
                        terminate_game(grid,display_grid,grid_dimensions)
                    else:
                        count+=1
    if count==grid[i][j]:
        #if all bombs have been flagged, reveal all neighbouring cells
        if f==0:
            print '\t\t\tYou found the Easter Egg!'
            time.sleep(1)
        for x in range(-1,2,1):
            for y in range(-1,2,1):
                if x+i>=0 and y+j>=0 and x+i<grid_dimensions[0] and y+j<grid_dimensions[1]:
                    if display_grid[x+i][y+j]==0: #if it was not visible
                        display_grid[x+i][y+j]=1; #reveal it
                        if grid[i+x][j+y]==0: #check if it's a zero
                            grid,display_grid,grid_dimensions,x,y,count=avalanche(grid,display_grid,grid_dimensions,x+i,y+j,0)
    else:
        if f==0:
            print '\t\t\tCannot change a revealed cell!'
            time.sleep(1)
    return display_grid;


def check(grid,display_grid,grid_dimensions):
    #check for win
    for i in range(grid_dimensions[0]):
        for j in range(grid_dimensions[1]):
            if grid[i][j]!='B' and display_grid[i][j]!=1:
                return 1;
    display(grid,display_grid,grid_dimensions);
    print '\n\t\t\tYou Win!\n\n'

    #useless ending animation
    for i in range(grid_dimensions[0]):
        for j in range(grid_dimensions[1]):
            grid[i][j]='<'
            if j!=0:
                grid[i][j-1]=' '
            else:
                if i!=0:
                    grid[i-1][grid_dimensions[1]-1]='  '
            display_grid[i][j]=1
            display(grid,display_grid,grid_dimensions);
            print '\n\t\t\tYou Win!\n\n'
            time.sleep(0.2)
    exit();

def terminate_game(grid,display_grid,grid_dimensions):

    for i in range(grid_dimensions[0]):
        for j in range(grid_dimensions[1]):
            if grid[i][j]=='B':
                display_grid[i][j]=1
    display(grid,display_grid,grid_dimensions);
    print '\n\t\t\tYou hit a bomb!\n\n'
    exit()





def main():
    #yes I know this is not how it's done. I just couldn't remember what was usually used and didn't want to unindent the whole thing.
    clear()
    while(True):
        level=int(raw_input('Enter level:\n0->Beginner\n1->Intermediate\n'));
        if level in range(0,2):
            break
    rules();

    #level=0;
    bombCount=0;
    noOfCellsUnlocked=0
    f=0
    grid,noOfBombs,display_grid,grid_dimensions=create_grid(level);
    grid=fill_grid(noOfBombs,grid,grid_dimensions)

    while(True):

        display(grid,display_grid,grid_dimensions);
        print '\t\t\tBomb Count =',bombCount,'noOfCellsUnlocked = ',noOfCellsUnlocked,'\n'
        if bombCount>noOfBombs:
            print '\t\t\tYou found more bombs than I had planted.lol\n'

        x,y=map(int,raw_input('\t\t\tSelect a cell(x,y): ').split())
        flag=raw_input('\t\t\tClick or Flag? (c/f): ')
        if flag=='c':
        #if you choose to click
            if display_grid[x][y]==2:
                #check if it's a flag
                #if yes, reset the flag
                display_grid[x][y]=0
                bombCount-=1

            elif display_grid[x][y]==1:
                display_grid=revealCells(grid,display_grid,grid_dimensions,x,y,f)
                f=1
                noOfCellsUnlocked=0
                for i in range(grid_dimensions[0]):
                    noOfCellsUnlocked+=display_grid[i].count(1)
            elif grid[x][y]=='B':
                #if you hit a bomb
                terminate_game(grid,display_grid,grid_dimensions);
            else:
                #reveal the cell beneath
                display_grid[x][y]=1
                noOfCellsUnlocked+=1
                if grid[x][y]==0:
                    grid,display_grid,grid_dimensions,x,y,count=avalanche(grid,display_grid,grid_dimensions,x,y,0)
                    noOfCellsUnlocked=0
                    for i in range(grid_dimensions[0]):
                        noOfCellsUnlocked+=display_grid[i].count(1)

        if flag=='f':
            if display_grid[x][y]==1:
                print '\t\t\tCannot change a revealed cell!'
                time.sleep(1)
            else:
                display_grid[x][y]=2;
                bombCount+=1
        if noOfCellsUnlocked==(grid_dimensions[0])*(grid_dimensions[1])-noOfBombs:
            check(grid,display_grid,grid_dimensions)

main()

#This was fun
#Over and Out
