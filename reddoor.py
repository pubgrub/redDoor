import copy
import os


# mode: 1 = Lösungen suchen, in results.txt schreiben
#       2 = results.txt lesen, versuchen auszudünnen
doSolve = 0
doAnalyze = 1


dotsX = [ 1, 1, 0, 3, 2, 2, 6, 1]
dotsY = [ 1 ,5, 2, 2, 3, 4, 5, 6]
dotsSize = [ "2", "2", "2", "3", "1", "0", "1", "3"]
dotsColor = [ "1", "1", "2", "1", "3", "0", "2", "3"]


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

def printSolution( px, py, f):
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
        print( s, file = f)

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
        print( s, file = f)
    #   input("next...1111111")
    solutions = solutions + 1
    for i in range( len(px)):
        print( px[i], py[i], file = f)


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

    solution = 0


    pathX = []
    pathY = []

    dots_OrderString = ""
    dots1_OrderString = ""
    dots2_OrderString = ""

    dots_SizeString = ""
    dots1_SizeString = ""
    dots2_SizeString = ""

    dots_ColorString = ""
    dots1_ColorString = ""
    dots2_ColorString = ""


    pathXList = []
    pathYList = []

    dots_OrderStringList = []
    dots1_OrderStringList = []
    dots2_OrderStringList = []

    dots_SizeStringList = []
    dots1_SizeStringList = []
    dots2_SizeStringList = []

    dots_ColorStringList = []
    dots1_ColorStringList = []
    dots2_ColorStringList = []

    dots_OrderDict = {}
    dots_SizeDict = {}
    dots_ColorDict = {}


    nTurn = 0
    dir = 0
    lenPath = 0

    nTurnList = []
    lenPathList = []

    file = open( "results.txt", "r")

    # Erste Zeile manuell holen, löst keine Analyse aus
    x, y = [int(i) for i in next(file).split()] # erste Zeile
    pathX.append( x)
    pathY.append( y)

    for line in file:
        x, y = [int(i) for i in line.split()]

        if( not ( x == 0 and y == 6)):
            # neuen Punkt merken
            pathX.append( x)
            pathY.append( y)

            # Länge des Pfades erhöhen
            lenPath += 1

            # auf Richtungsänderung überprüfen
            akt_dir = x - pathX[ -2] + ( y - pathY[ -2]) * 2
            if( dir != akt_dir):
                nTurn += 1
                dir = akt_dir

            # Aktuellen Punkt auf Dot überprüfen und wenn ja in Listen schreiben
            for d in range( len(dotsX)):
                dotsSizeID = dotsSize[ d]
                dotsColorID = dotsColor[ d]
                if( dotsSizeID != "0"):
                    if ( dotsX[d] == x and dotsY[d] == y) :
                        dots_OrderString += str( d).strip()
                        dots_SizeString += dotsSizeID
                        dots_ColorString += dotsColorID

                        dots1_OrderString += str( d).strip()
                        dots1_SizeString += dotsSizeID
                        dots1_ColorString += dotsColorID
                        break
                    if( dotsX[d] == 6 - x and dotsY[d] == 6 - y):
                        dots_OrderString += str( d).strip()
                        dots_SizeString += dotsSizeID
                        dots_ColorString += dotsColorID

                        dots2_OrderString += str( d).strip()
                        dots2_SizeString += dotsSizeID
                        dots2_ColorString += dotsColorID
                        break

        else:
            # neue Lösung


            # Pfad und Strings in Arrays schreiben
            pathXList.append( pathX)
            pathYList.append( pathY)

            dots_OrderStringList.append( dots_OrderString)
            dots1_OrderStringList.append( dots1_OrderString)
            dots2_OrderStringList.append( dots2_OrderString)

            dots_SizeStringList.append( dots_SizeString)
            dots1_SizeStringList.append( dots1_SizeString)
            dots2_SizeStringList.append( dots2_SizeString)

            dots_ColorStringList.append( dots_ColorString)
            dots1_ColorStringList.append( dots1_ColorString)
            dots2_ColorStringList.append( dots2_ColorString)

            nTurnList.append( nTurn)
            lenPathList.append( lenPath)

            dots_OrderDict[ dots_OrderString] = dots_OrderDict.get( dots_OrderString, 0) + 1
            dots_SizeDict[ dots_SizeString] = dots_SizeDict.get( dots_SizeString, 0) + 1
            dots_ColorDict[ dots_ColorString] = dots_ColorDict.get( dots_ColorString, 0) + 1


            # Variablen resetten
            pathX = [ x]
            pathY = [ y]
            nTurn = 0
            dir = 0
            lenPath = 0

            dots_OrderString = ""
            dots1_OrderString = ""
            dots2_OrderString = ""


            dots_SizeString = ""
            dots1_SizeString = ""
            dots2_SizeString = ""

            dots_ColorString = ""
            dots1_ColorString = ""
            dots2_ColorString = ""

            solution += 1

    file.close()

    wfile = open("analyzed.txt", "w")
    for i in range( len( pathXList)):
        print( "Solution: " + str( i), file = wfile)
        print( pathXList[ i], pathYList[ i], file = wfile)
        print( "Pathlength: ", lenPathList[ i], file = wfile)
        print( "Dots Order: ", dots_OrderStringList[ i], file=wfile)
        print( "Size Order: ", dots_SizeStringList[ i], file = wfile)
        print( "Color Order: ", dots_ColorStringList[ i], file = wfile)
        print( "Turns: ", nTurnList[ i], file = wfile)
        printSolution( pathXList[ i], pathYList[ i], wfile)
    wfile.close()

#    for k in sorted(nTurnList, key=dotsSs.__getitem__):
#        print(k, dots_SizeOrders[k], dotsSs[ k])

    max_turns = 0
    max_len = 0
    max_turnLen = 0

    for i in range( len(pathXList)):
        max_turns = max( max_turns, nTurnList[ i])
        max_len = max( max_len, lenPathList[ i])
        max_turnLen = (max( max_turnLen, nTurnList[ i] + lenPathList[ i]))
    print( "Anzahl Schritte:")
    for i in range( len(pathXList)):
        if lenPathList[ i] == max_len:
            print( i, dots_SizeDict[ dots_SizeStringList[ i]])
    print( "Anzahl Turns:")
    for i in range( len(pathXList)):
        if nTurnList[ i] == max_turns:
            print( i, dots_SizeDict[ dots_SizeStringList[ i]])
    print( "Kombiniert:")
    for i in range( len(pathXList)):
        if nTurnList[ i] + lenPathList[ i] == max_turnLen - 2:
            print( i, dots_SizeDict[ dots_SizeStringList[ i]])



    print( max_turns)
    print( max_len)
    return

if doSolve:
    file = open( "results.txt", "w")
    pathX = []
    pathY = []
    solve( startx, starty, used, pathX, pathY)
    file.close()

if doAnalyze:
    analyze()
    quit()
