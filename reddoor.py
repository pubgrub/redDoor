import copy
import os


# mode: 1 = Lösungen suchen, in results.txt schreiben
#       2 = results.txt lesen, versuchen auszudünnen
doSolve = 0
doAnalyze = 1


dotsX = [ 1, 1, 0, 3, 2, 2, 6, 1]
dotsY = [ 1 ,5, 2, 2, 3, 4, 5, 6]
dotsS = [ 2, 2, 2, 3, 1, 0, 1, 3]
#dotsS = [ 1, 1, 2, 1, 3, 0, 2, 3]


moveX = [ 1, 0, -1, 0]
moveY = [ 0, 1, 0, -1]

used = [[0 for i in range(7)] for j in range(7)]

startx = 0
starty = 6

endx1 = 0
endy1 = 0

endx2 = 6
endy2 = 6

n = 0
tests = 0
solutions = 0

def testSolution( u, px, py):
    global dotsX, dotsY
    # alle Punkte mitgenommen?
    for i in range( len( dotsX)):
        if( u[ dotsX[i]][dotsY[i]]) != 1:
            return 0
    # auch den einen zwischen den Kreuzungen??
    for i in range( len( px) -1):
        x = px[i]
        y = py[i]
        x1 = px[ i + 1]
        y1 = py[ i + 1]
        if( x == 2 and x1 == 2):
            if( (y == 4 and y1 == 3) or ( y == 3 and y1 == 4)):
                return 1;
        elif( x == 4 and x1 == 4):
            if( (y == 2 and y1 == 3) or ( y == 3 and y1 == 2)):
                return 1;
    return 0

def printSolution( px, py):
    global solutions
    global file

    lastX = px[0]
    lastY = py[0]

    # print( lastX)
    # print( lastY)
    # quit()

    grid  = [[" " for i in range(7 * 2)] for j in range(7 * 2)]
    for x in range(7):
        for y in range(7):
            grid[x * 2][y * 2] = "-"

    for y in  range(7 * 2):
        s = ""
        for x in range(7 * 2):
            s = s + grid[x][y]
        print( s)

    for i in range( len(px)):
        print( px[i], py[i])

    for p in range( 1, len( px)):
        if( lastX != px[p]):
            grid [lastX + px[p]] [py[p] * 2] = "O"
        else:
            grid[px[p] * 2][lastY + py[p]] = "O"
        grid[ px[p] * 2][py[p] * 2] = "O"
        lastX = px[p]
        lastY = py[p]

    for y in  range(7 * 2):
        s = ""
        for x in range(7 * 2):
            s = s + grid[x][y]
        print( s)
#    input("next...1111111")
    solutions = solutions + 1
    for i in range( len(px)):
        print( px[i], py[i], file = file)


def solve( x, y, used, pathX, pathY):
    global n, tests, solutions
    global endx1, endx2, endy1, endy2
    if( x == 3 and y == 3): # in der Mitte getroffen...
        return
    used[ x][ y] = 1
    used[ 6-x][ 6-y] = 1
    pathX.append( x)
    pathY.append( y)

    if( (x == endx1 and y == endy1) or ( x == endx2 and y == endy2)):
        tests = tests + 1
        result = testSolution( used, pathX, pathY)
        if( result):
            printSolution( pathX, pathY)
    for i in range(4):
        newX = x + moveX[ i]
        newY = y + moveY[ i]
        if( newX > 6 or newX < 0 or newY > 6 or newY < 0):
            # print( "Out of bounds: ", newX, newY)
            continue
        if( used[newX][newY] == 1):
            #  print("used: ", newX, newY)
            #  for i in range( 7):
            #  print( used[i])
            continue
        n = n + 1
        if( n % 1000 == 0):
            print( n, tests, solutions)
            # os.system('cls')
            # for py in range(7):
            #     s = ""
            #     for px in range(7):
            #         s = s + str(used[px][py])
            #     print( s)
        solve( newX, newY, copy.deepcopy(used), copy.deepcopy( pathX), copy.deepcopy( pathY))


def getNumber( o):
    s = ""
    for i in o:
        s = s +  str(i).strip()
    return s

def analyze():
    global dotsX
    global dotsY
    wfile = open("analyzed.txt", "w")
    pathX = []
    pathY = []
    dOrder = []
    dOrder1 = []
    dOrder2 = []
    dOrders = {}
    dotsSs = {}

    dOrders1 = {}
    dOrders2 = {}

    nTurns = 0
    lenPath = 0

    file = open( "results.txt", "r")

    x, y = [int(i) for i in next(file).split()] # erste Zeile
    pathX.append( x)
    pathY.append( y)


    for line in file:
        x, y = [int(i) for i in line.split()]
        if( x == 0 and y == 6):
            # neue Lösung
            for n in range(len( pathX)):
                print( pathX[n], pathY[n], file = wfile)
            print( dOrder, file = wfile)
            dotsSStr = ""
            dots1 = ""
            dots2 = ""
            for i in dOrder:
                if( dotsS[i]) != 0:
                    dotsSStr = dotsSStr + str(dotsS[ i]).strip()
            for i in dOrder1:
                if( dotsS[i]) != 0:
                    dots1 = dots1 + str(dotsS[ i]).strip()
            for i in dOrder2:
                if( dotsS[i]) != 0:
                    dots2 = dots2 + str(dotsS[ i]).strip()
            r = getNumber( dOrder)
            print( r, file = wfile)
            print( dotsSStr, file = wfile)
            if r in dOrders:
                dOrders[ r] = dOrders[ r] + 1
            else:
                dOrders[ r] = 1
            if( dots1 in dOrders1):
                dOrders1[dots1] = dOrders1[dots1] + 1
            else:
                dOrders1[dots1] = 1
            if( dots2 in dOrders2):
                dOrders2[dots2] = dOrders2[dots2] + 1
            else:
                dOrders2[dots2] = 1


            dotsSs[ r] = dotsSStr
            pathX = []
            pathY = []
            dOrder = []
            dOrder1 = []
            dOrder2 = []
            nTurns = 0
            lenPath = 0

        pathX.append( x)
        pathY.append( y)
        for d in range( len(dotsX)):
            if ( dotsX[d] == x and dotsY[d] == y) :
                dOrder1.append( d)
                dOrder.append( d)
                break
            if( dotsX[d] == 6 - x and dotsY[d] == 6 - y):
                dOrder2.append( d)
                dOrder.append( d)
                break
        # if( ( x == 2 and ( y == 4 or y == 3) ) or ( x == 4 and ( y == 2 or y == 3))):
        #     dOrder.append( )
    print( pathX, pathY, file = wfile)
    print( dOrder, file = wfile)

    for k in sorted(dotsSs, key=dotsSs.__getitem__):
        print(k, dOrders[k], dotsSs[ k])
    print()
    print("Schlange 1: ")
    print()
    for k in dOrders1:
        print( k, dOrders1[k])
    print()
    print("Schlange 2: ")
    print()
    for k in dOrders2:
        print( k, dOrders2[k])
    return 0

if doSolve:
    file = open( "results.txt", "w")
    pathX = []
    pathY = []
    solve( startx, starty, used, pathX, pathY)
    file.close()

if doAnalyze:
    analyze()
    quit()
