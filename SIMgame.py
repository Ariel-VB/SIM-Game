import tkinter as tk
from IPython.display import display
import ipywidgets as widgets
from ipywidgets import Layout

class SIMgame:
    
    global playerName
    global compName
    global playerTurn
    global compNumber
    global playerNumber
    global winnerFound
    global movesCount
    global winner
    global movesPlayed
    global currentBoard
    global infoTextList
    global resetting
    global twoPlayers
    
    movesPlayed = [[]for n in range(0,7)]
    
    for n in range(0,7):
        for m in range(0,7):
            movesPlayed[n].append(0)
    
    movesCount = 1
    compNumber = None
    playerNumber = None
    winner = 0
    winnerFound = False
    playerTurn = None
    compName = "AI"
    #infoText = []
    resetting = False
    twoPlayers = False
    
    def getComputerMove():
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentboard
        global infoTextList
        
        move = [None, None, None]
        startingDepth = movesCount
        currentBoardCopy = [[]for n in range(0,7)]
    
        for n in range(0,7):
            for m in range(0,7):
                currentBoardCopy[n].append(None)
                
        emptyPreviousMove = [None, None]
        emptyFirstMove = [None, None]
        
        #Part 1
        #Any move that is disjoint from first player's first move
        #For moves 1-3
        
        if (movesCount < 4):
            
            #Iterates through all moves
            for x in range(1,7):
                
                if playerTurn == True:
                    break
                    
                for y in range(x+1, 7):
                    
                    if playerTurn == True:
                        break
                        
                    #Check if move is disjoint
                    #If move has not been played
                    if movesPlayed[x][y] == 0:
                        
                        xDisjoint = True
                        yDisjoint = True
                        
                        #Check that no move is taken that includes x, if true at end of loop, continue to do the same for y
                        for y2 in range(1,7):
                            if movesPlayed[y2][x] != 0 or movesPlayed[x][y2] != 0:
                                xDisjoint = False
                                
                        #if xDisjoint is true at end of loop, continue to do the same for y
                        if xDisjoint == True:
                            for x2 in range(1,7):
                                if movesPlayed[y][x2] != 0 or movesPlayed[x2][y] == 0:
                                    yDisjoint == False
                                    
                        #If both x and y are disjointed, make this move and end turn
                        if xDisjoint == True and yDisjoint == True:
                            
                            #Choose x, y
                            movesPlayed[x][y] = compNumber
                            move[0] = x
                            move[1] = y
                            movesCount += 1
                            playerTurn = True
                            
                            SIMgame.add_text(f"Turn {movesCount-1}: {compName}'s move is {move[0]} {move[1]}.")
                            SIMgame.draw_line(move[0],move[1],"red")            
                            SIMgame.checkWinner()
                            
            #From here, there is no disjoint move available or one has been made
            
            #If none was found
            if playerTurn == False:
                print("No disjointed move.")
                
        
        #Part 2 - Smart Heuristic for moves 4 through 6 (<7)
        elif movesCount < 7:
            
            move  = SIMgame.smartHeuristic()
            
            #Play chosen move
            movesPlayed[move[0]][move[1]] = compNumber
            movesCount += 1
            playerTurn = True
            
            SIMgame.add_text(f"Turn {movesCount-1}: {compName}'s move is {move[0]} {move[1]}.")
            SIMgame.draw_line(move[0],move[1],"red")            
            SIMgame.checkWinner()
            
        
        #If 15th move (last move), just choose the last available move
        elif movesCount == 15:
            
            validMove = False
            
            for x in range(1,7):
                if validMove == False:
                    
                    for y in range(x+1, 7):
                        if validMove == False:
                            
                            if movesPlayed[x][y] == 0:
                                
                                movesPlayed[x][y] = compNumber
                                validMove = True
                                movesCount += 1
                                playerTurn = True
                                
                                SIMgame.add_text(f"Turn {movesCount-1}: {compName}'s move is {x} {y}.")
                                SIMgame.draw_line(x,y,"red")            
                                SIMgame.checkWinner()
                                
                                
        #Otherwise minimax
        else:
            
            #Copy current board first
            for i in range(0, 7):
                for j in range(0,7):
                    currentBoardCopy[i][j] = movesPlayed[i][j]
                    
            move = SIMgame.minimax(True, startingDepth, currentBoardCopy, emptyPreviousMove, emptyFirstMove)
            
            #If there is no path that guarantees minimax a win, and the best score it can do is -1:
            #Use the smart heuristic method instead, to avoid minimax giving up early since
            #it is equally likely to choose a move that loses immediately and a move that loses later in the game
            if move[2] == -1:
                
                move = SIMgame.smartHeuristic()
                
            #Minimax will return 0,0 if it has no available moves left without losing
            #So if it returns 0, play the first available move
            if move[0] != 0:
                movesPlayed[move[0]][move[1]] = compNumber
                movesCount += 1
                playerTurn = True
                
                SIMgame.add_text(f"Turn {movesCount-1}: {compName}'s move is {move[0]} {move[1]}.")
                SIMgame.draw_line(move[0],move[1],"red")            
                SIMgame.checkWinner()
                
            #If it does return 0, play the first available move and lose (greedy)
            else:
                validMove = False
                
                for x in range(1,7):
                    if validMove == False:
                        
                        for y in range(x+1, 7):
                            if validMove == False:
                                
                                if movesPlayed[x][y] == 0:
                                    movesPlayed[x][y] = compNumber
                                    validMove = True
                                    movesCount += 1
                                    playerTurn = True
                                    
                                    SIMgame.add_text(f"Turn {movesCount-1}: {compName}'s move is {x} {y}.")
                                    SIMgame.draw_line(x,y,"red")            
                                    SIMgame.checkWinner()
       
    
    #SMART HEURISTIC FUNCTION
    #Will assign moves positive and negative points based on quality, then select the best one
    #Points are assigned in 2 index of move[]
    def smartHeuristic():
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentboard
        global infoTextList
        
        move = [None, None, None]
        
        move[2] = -10000
        
        #Iterates through all moves
        for x in range(1,7):
            for y in range(x+1, 7):
                score = -10000
                
                #Legal move check
                #Score becomes 0 if move is legal
                if movesPlayed[x][y] == 0:
                    score = score + 10000
                    
                
                #Loss check (AI-AI-AI)
                #Check all y2 values for the current x (row)
                for y2 in range(x+1, 7):
                    
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x][y2] == compNumber:
                        if movesPlayed[y][y2] == compNumber or movesPlayed[y2][y] == compNumber:
                            score = score - 100
                
                #Check all x2 values for the current y (column)
                for x2 in range(y-1, 0, -1):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x2][y] == playerNumber:
                        if movesPlayed[x][x2] == playerNumber or movesPlayed[x2][x] == playerNumber:
                            score = score - 100
                            
                #Closing Player Triangle Check
                #AI-Player-Player Triangle
                #Check all y2 values for the current x (row)
                for y2 in range(x+1, 7):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x][y2] == playerNumber:
                        if movesPlayed[y][y2] == playerNumber or movesPlayed[y2][y] == playerNumber:
                            score = score - 10
                
                #Check all x2 values for the current y (column)
                for x2 in range(y-1, 0, -1):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x2][y] == playerNumber:
                        if movesPlayed[x][x2] == playerNumber or movesPlayed[x2][x] == playerNumber:
                            score = score - 10
                            
                
                #Partial Triangle Check (Player check first)
                #AI-AI-Player (checking for 1 AI and 1 Player move)
                #Check all y2 values for the current x (row)
                for y2 in range(x+1, 7):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x][y2] == playerNumber:
                        if movesPlayed[y][y2] == compNumber or movesPlayed[y2][y] == compNumber:
                            score = score + 5
                            
                #Check all x2 values for the current y (column)
                for x2 in range(y-1, 0, -1):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x2][y] == playerNumber:
                        if movesPlayed[x][x2] == compNumber or movesPlayed[x2][x] == compNumber:
                            score = score + 5
                            
                #Partial Triangle Check (AI check first)
                #AI-AI-Player (checking for 1 AI and 1 Player move)
                #Check all y2 values for the current x (row)
                for y2 in range(x+1, 7):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x][y2] == compNumber:
                        if movesPlayed[y][y2] == playerNumber or movesPlayed[y2][y] == playerNumber:
                            score = score + 5
                            
                #Check all x2 values for the current y (column)
                for x2 in range(y-1, 0, -1):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x2][y] == compNumber:
                        if movesPlayed[x][x2] == playerNumber or movesPlayed[x2][x] == playerNumber:
                            score = score + 5
                            
                #AI-AI Connection
                #Check all y2 values for the current x (row)
                for y2 in range(x+1, 7):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x][y2] == compNumber:
                        if movesPlayed[y][y2] == 0 or movesPlayed[y2][y] == 0:
                            score = score - 5
                            
                #Check all x2 values for the current y (column)
                for x2 in range(y-1, 0, -1):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x2][y] == compNumber:
                        if movesPlayed[x][x2] == 0 or movesPlayed[x2][x] == 0:
                            score = score - 5
                            
                #Player-AI Connection
                #Check all y2 values for the current x (row)
                for y2 in range(x+1, 7):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x][y2] == playerNumber:
                        if movesPlayed[y][y2] == 0 or movesPlayed[y2][y] == 0:
                            score = score + 1
                            
                #Check all x2 values for the current y (column)
                for x2 in range(y-1, 0, -1):
                    #Check any moves with matching x or y, to see if their other coordinate matches
                    if movesPlayed[x2][y] == playerNumber:
                        if movesPlayed[x][x2] == 0 or movesPlayed[x2][x] == 0:
                            score = score + 1
                            
                #Finally, if move score is better than the stored score, replace stored move
                if score > move[2]:
                    move[0] = x
                    move[1] = y
                    move[2] = score
                    
        return move
    
    
    #MINIMAX FUNCTION
    def minimax (maximizingPlayer, depth, currentBoard, previousMove, firstMove):
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentboard
        global infoTextList
        
        #Index 0 is move x, index 1 is move y, index 2 is score (0, 1, -1))
        output = [None, None, None]
        
        #Generate all possible moves
        possibleMoves = [[None, None] for n in range(0, (16-depth))]
        index = 0
        
        for x in range(1, 7):
            for y in range(x+1, 7):
                #If move is possible and has not been made, add to the array of possible moves
                if currentBoard[x][y] == 0:
                    possibleMoves[index][0] = x
                    possibleMoves[index][1] = y
                    index += 1
                    
        #Setting first move to be passed down to all child nodes - only happens on SECOND call
        if depth == movesCount + 1:
            firstMove[0] = previousMove[0]
            firstMove[1] = previousMove[1]
            
        #If it is the maximizing player's turn, return the minimax resulting in the highest score:
        if maximizingPlayer == True:
            currentMax = [None, None, None]
            #NOTE - if returned score is -999, that means that there were no more nodes to test
            currentMax[0] = 0
            currentMax[1] = 0
            currentMax[2] = -999
            #Lower than all scores, will ensure that score is set to next highest encountered
            
            #Iterates through all valid moves
            for x in range(0, index):
                
                #Update board for new move
                updatedBoard = [[]for n in range(0,7)]
    
                for n in range(0,7):
                    for m in range(0,7):
                        updatedBoard[n].append(None)
                        
                #Copy currentBoard first
                for i in range(0,7):
                    for j in range(0,7):
                        updatedBoard[i][j] = currentBoard[i][j]
                        
                #Now add new move
                updatedBoard[possibleMoves[x][0]][possibleMoves[x][1]] = compNumber
                
                #If leaf node:
                #If move will result in a win or loss (using score function), check against current max
                if SIMgame.countTriangles(updatedBoard) == -1 or SIMgame.countTriangles(updatedBoard) == 1:
                    #If score is more than currentMax, reassign this move and score to currentMax
                    if SIMgame.countTriangles(updatedBoard) > currentMax[2]:
                        currentMax[0] = possibleMoves[x][0]
                        currentMax[1] = possibleMoves[x][1]
                        currentMax[2] = SIMgame.countTriangles(updatedBoard)
                        
                #If a move does not result in a win or loss (not a leaf node),
                #NEED TO RUN MINIMAX AGAIN, and check if minimax result is better than currentMax
                if SIMgame.countTriangles(updatedBoard) == 0:
                    
                    minimaxResult = [None, None, None]
                    
                    minimaxResult = SIMgame.minimax(False, depth + 1, updatedBoard, possibleMoves[x], firstMove)
                    
                    #Checking if the result is better than currentMax, setting new currentMax if it is
                    if minimaxResult[2] > currentMax[2]:
                        
                        currentMax[0] = possibleMoves[x][0]
                        currentMax[1] = possibleMoves[x][1]
                        currentMax[2] = minimaxResult[2]
                        
                    
            #If there were no options to test, error check
            if currentMax[2] == -999:
                print("Error")
                
            #Return score of currentMax with firstMove move
            output[0] = currentMax[0]
            output[1] = currentMax[1]
            output[2] = currentMax[2]
            return output
        
        
        #If it is the minimizing player's turn:
        if maximizingPlayer == False:
            currentMin = [None, None, None]
            currentMin[0] = 0
            currentMin[1] = 0
            currentMin[2] = 999
            #Higher than all scores, will ensure that score is set to next lowest encountered
            
            #Iterates through all valid moves
            for x in range(0, index):
                
                #Update board for new move
                updatedBoard = [[]for n in range(0,7)]
    
                for n in range(0,7):
                    for m in range(0,7):
                        updatedBoard[n].append(None)
                        
                #Copy currentBoard first
                for i in range(0,7):
                    for j in range(0,7):
                        updatedBoard[i][j] = currentBoard[i][j]
                        
                #Now add new move
                updatedBoard[possibleMoves[x][0]][possibleMoves[x][1]] = playerNumber
                
                #If leaf node:
                #If move will result in a win or loss (using score function), check against current min
                if SIMgame.countTriangles(updatedBoard) == -1 or SIMgame.countTriangles(updatedBoard) == 1:
                    # If score is less than currentMin, reassign this move and score to currentMin
                    if SIMgame.countTriangles(updatedBoard) < currentMin[2]:
                        currentMin[0] = possibleMoves[x][0]
                        currentMin[1] = possibleMoves[x][1]
                        currentMin[2] = SIMgame.countTriangles(updatedBoard)
                        
                #If a move does not result in a win or loss (not a leaf node),
                #NEED TO RUN MINIMAX AGAIN, and check if minimax result is less than currentMin
                if SIMgame.countTriangles(updatedBoard) == 0:
                    
                    minimaxResult = SIMgame.minimax(True, depth + 1, updatedBoard, possibleMoves[x], firstMove)
                    
                    #Checking if the result is less than currentMin, setting new currentMin if it is
                    if minimaxResult[2] < currentMin[2]:
                        currentMin[0] = possibleMoves[x][0]
                        currentMin[1] = possibleMoves[x][1]
                        currentMin[2] = minimaxResult[2]
                    
                    
            #If there were no options to test, error check
            if currentMin[2] == 999:
                print("Error")
                
            #Return score of currentMin with firstMove move
            output[0] = currentMin[0]
            output[1] = currentMin[1]
            output[2] = currentMin[2]
            return output
        
        return None
    
    
    #SCORING FUNCTION
    def countTriangles(currentBoard):
        
        score = 0
        
        redBlue = [0, 0, 0]
        
        for x in range(1,7):
            for y in range(x+1, 7):
                for z in range(y+1, 7):
                    
                    if currentBoard[x][y] == 1 and currentBoard[x][z] == 1 and currentBoard[y][z] == 1:
                        redBlue[1] += 1
                        
                    if currentBoard[x][y] == 2 and currentBoard[x][z] == 2 and currentBoard[y][z] == 2:
                        redBlue[2] += 1
                        
        if compNumber == 1:
            
            if redBlue[1] > 0:
                score = -1
                
            if redBlue[2] > 0:
                score = 1
                
        if compNumber == 2:
            
            if redBlue[1] > 0:
                score = 1
                
            if redBlue[2] > 0:
                score = -1
        
        return score
    
    
    def getPlayerMove():
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentBoard
        global infoTextList
        
        global root
        global canvas
        global button_first
        global button_second
        
        global e1Label
        global e2Label
        global e1
        global e2
        global entryButton
        global enteredMove
        
        global twoPlayers
        
        e1Label.place(relx = .55, rely = .85)
        e2Label.place(relx = .5, rely = .92)
        e1.place(relx = .70, rely = .85)
        e2.place(relx = .70, rely = .92)
        entryButton.place(relx = .70, rely = .75)
        
                
    def getPlayerMove2():
        
        global movesPlayed
        global playerNumber
        global movesCount
        global playerTurn
        global enteredMove
        global infoTextList
        
        global twoPlayers
        
        validCheck = False
        #Checking for invalid input:
        if enteredMove[0] == 1 or enteredMove[0] == 2 or enteredMove[0] == 3 or enteredMove[0] == 4 or enteredMove[0] == 5 or enteredMove[0] == 6:
            if enteredMove[1] == 1 or enteredMove[1] == 2 or enteredMove[1] == 3 or enteredMove[1] == 4 or enteredMove[1] == 5 or enteredMove[1] == 6:
                if enteredMove[0] != enteredMove[1]:
                    validCheck = True
        
        if validCheck == False:
            SIMgame.add_text("Please enter a valid move.")
            
        elif validCheck == True:
        
            validMove = False       

            if enteredMove[0]<enteredMove[1]:            
                x = enteredMove[0]
                y = enteredMove[1]

            else:
                x = enteredMove[1]
                y = enteredMove[0]        


            if winner == 1 or winner == 2:
                SIMgame.add_text("The game is over!")

            elif x > 0 and x <= 6 and y > 0 and y <= 6 and x < y and movesPlayed[x][y] == 0:
                
                #For versus AI:
                if twoPlayers == False:
                    validMove = True
                    movesPlayed[x][y] = playerNumber
                    movesCount += 1
                    playerTurn = False

                    SIMgame.add_text(f"Turn {movesCount-1}: You moved {x} {y}.")
                    SIMgame.draw_line(x,y,"blue")
                    SIMgame.checkWinner()
                    
                #For versus another player:
                if twoPlayers == True:
                    validMove = True
                    
                    #If movesCount is odd, it is playerNumber's turn
                    if movesCount%2 != 0:
                        movesPlayed[x][y] = playerNumber
                        playerTurn = True
                        movesCount += 1
                        
                        SIMgame.add_text(f"Turn {movesCount-1}: Blue moved {x} {y}.")
                        SIMgame.draw_line(x,y,"blue")
                        SIMgame.checkWinner()
                        
                    #If movesCount is even, it is compNumber's turn
                    elif movesCount%2 == 0:
                        movesPlayed[x][y] = compNumber
                        playerTurn = True
                        movesCount += 1
                        
                        SIMgame.add_text(f"Turn {movesCount-1}: Red moved {x} {y}.")
                        SIMgame.draw_line(x,y,"red")
                        SIMgame.checkWinner()


            else:
                SIMgame.add_text("Illegal move: try again")
                
                
    def checkWinner():
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentboard
        global infoTextList
        global twoPlayers
        
        redBlue = [0, 0, 0]
        
        for x in range(1,7):
            for y in range(x+1, 7):
                for z in range(y+1, 7):
                    
                    if movesPlayed[x][y] == 1 and movesPlayed[x][z] == 1 and movesPlayed[y][z] == 1:
                        redBlue[1] += 1
                        
                        SIMgame.draw_line(x,y,"win2")
                        SIMgame.draw_line(y,z,"win2")
                        SIMgame.draw_line(z,x,"win2")
                        
                    if movesPlayed[x][y] == 2 and movesPlayed[x][z] == 2 and movesPlayed[y][z] == 2:
                        redBlue[2] += 1
                        
                        SIMgame.draw_line(x,y,"win1")
                        SIMgame.draw_line(y,z,"win1")
                        SIMgame.draw_line(z,x,"win1")
                        
        if redBlue[1] > 0:
            winnerFound = True
            winner = 2
            
        if redBlue[2] > 0:
            winnerFound = True
            winner = 1
            
        if winnerFound:
            
            if twoPlayers == False:
                if winner == playerNumber:
                    SIMgame.add_text("You won!")
                    SIMgame.ask_reset()
                if winner == compNumber:
                    SIMgame.add_text("You lost!")
                    SIMgame.ask_reset()
                    
            elif twoPlayers == True:
                if winner == playerNumber:
                    SIMgame.add_text("Blue wins!")
                    SIMgame.ask_reset()
                if winner == compNumber:
                    SIMgame.add_text("Red wins!")
                    SIMgame.ask_reset()
                
        else:
            if playerTurn == True:
                SIMgame.getPlayerMove()
            if playerTurn == False:
                SIMgame.getComputerMove()
    
    def draw_line(x, y, color):
        
        global canvas
        global playerNumber
        global compNumber
        
        if color == "blue":
            htmlcolor = "#3582ff"
        if color == "red":
            htmlcolor = "#ff5454"
            
        if color == "win1":
            #Draw losing RED triangle
            if playerNumber == 1:
                htmlcolor = "#ffb2b2"
            #Draw losing BLUE triangle
            if compNumber == 1:
                htmlcolor = "#b2cfff"
            
        if color == "win2":
            #Draw losing BLUE triangle
            if playerNumber == 1:
                htmlcolor = "#b2cfff"
            #Draw losing RED triangle
            if compNumber == 1:
                htmlcolor = "#ffb2b2"
            
        if x == 1: 
            x1 = 125
            y1 = 70
        if x == 2: 
            x1 = 275
            y1 = 70
        if x == 3: 
            x1 = 350
            y1 = 200
        if x == 4: 
            x1 = 275
            y1 = 330
        if x == 5: 
            x1 = 125
            y1 = 330
        if x == 6: 
            x1 = 50
            y1 = 200
            
        if y == 1: 
            x2 = 125
            y2 = 70
        if y == 2: 
            x2 = 275
            y2 = 70
        if y == 3: 
            x2 = 350
            y2 = 200
        if y == 4: 
            x2 = 275
            y2 = 330
        if y == 5: 
            x2 = 125
            y2 = 330
        if y == 6: 
            x2 = 50
            y2 = 200    
        
        if color == "red" or color == "blue":
            line = canvas.create_line(x1, y1, x2, y2, fill=htmlcolor, width=3)
            canvas.tag_lower(line)
        
        if color == "win1" or color == "win2":
            line = canvas.create_line(x1, y1, x2, y2, fill=htmlcolor, width=5)
     
    def add_text(text):
        global infoTextList

        #Adds the new text to the scroll box and scrolls to the bottom
        infoTextList.insert(tk.END, text)
        infoTextList.see("end")
        
    
    #When the game ends, displays a button to play again:
    def ask_reset():
        
        global resetting
        
        #Variable to tell main() if the game is starting for the first time or resetting:
        resetting = True
        
        #Clears the move entry spaces/button:
        e1.place_forget()
        e2.place_forget()
        e1Label.place_forget()
        e2Label.place_forget()
        entryButton.place_forget()  
        
        #Button to restart game:
        #On-click function:
        def restart():
            
            #Remove the button
            restartButton.place_forget() 
            
            #Resets game:
            SIMgame.reset_game()
        
        restartButton = tk.Button(root, text='Play Again', command=restart)
            
        restartButton.place(relx = .70, rely = .75)
    
    #Clears the canvas and restarts the game:
    def reset_game():
        
        #Clears the canvas so that main() can reset the game:
        canvas.delete("all")
        
        SIMgame.main()
        
        
            
    def main():
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentBoard
        global infoTextList
        
        global root
        global canvas
        global button_first
        global button_second
        global button_ai
        global button_human
        
        global e1Label
        global e2Label
        global e1
        global e2
        global entryButton
        global entered_move
        
        global resetting
        global twoPlayers
        
        playerName = "Player"
        
        
        #Resetting variables
        movesPlayed = [[]for n in range(0,7)]
    
        for n in range(0,7):
            for m in range(0,7):
                movesPlayed[n].append(0)

        movesCount = 1
        compNumber = None
        playerNumber = None
        winner = 0
        winnerFound = False
        playerTurn = None
        compName = "AI"
        #infoText = []
        
        
        #TKINTER SETUP:
        
        #Only do this the first time, not if the game is being reset:
        if resetting == False:
            root = tk.Tk()
            root.title("SIM Game")
            
            #Prevents resizing the window:
            root.resizable(width=False, height=False)

            canvas_width = 400
            canvas_height = 600

            canvas = tk.Canvas(root, 
                   width=canvas_width,
                   height=canvas_height)

            canvas.pack()
            
            #Setting up scrolling text:
            scrollbar = tk.Scrollbar(root)
            #scrollbar.place(relx=0.5, rely=1.0, anchor='sw')
            infoTextList = tk.Listbox(root, yscrollcommand = scrollbar.set, width = 28, height = 12)

            infoTextList.place(relx=0.01, rely=0.99, anchor='sw')
            scrollbar.place(in_=infoTextList, relx=1.0, relheight=1.0, bordermode="outside")
            scrollbar.config(command = infoTextList.yview)

        r = 7
        
        x1 = 125
        y1 = 70
        
        x2 = 275
        y2 = 70
        
        x3 = 350
        y3 = 200
        
        x4 = 275
        y4 = 330
        
        x5 = 125
        y5 = 330

        x6 = 50
        y6 = 200

        canvas.create_oval(x1-r,y1-r,x1+r,y1+r, fill = "#000000")
        canvas.create_oval(x2-r,y2-r,x2+r,y2+r, fill = "#000000")
        canvas.create_oval(x3-r,y3-r,x3+r,y3+r, fill = "#000000")
        canvas.create_oval(x4-r,y4-r,x4+r,y4+r, fill = "#000000")
        canvas.create_oval(x5-r,y5-r,x5+r,y5+r, fill = "#000000")
        canvas.create_oval(x6-r,y6-r,x6+r,y6+r, fill = "#000000")
        
        label1 = tk.Label(root, text="1")
        label2 = tk.Label(root, text="2")
        label3 = tk.Label(root, text="3")
        label4 = tk.Label(root, text="4")
        label5 = tk.Label(root, text="5")
        label6 = tk.Label(root, text="6")
        
        label1.place(x=x1-20, y=y1-30)
        label2.place(x=x2+10, y=y2-30)
        label3.place(x=x3+25, y=y3-10)
        label4.place(x=x4+10, y=y4+15)
        label5.place(x=x5-20, y=y5+15)
        label6.place(x=x6-35, y=y6-10)        
        
        SIMgame.add_text("Welcome to the game!")
        
        #Option to play with two human players:
        SIMgame.add_text("Who will you play against?")

        
        def pick_ai():
            global playerTurn
            global button_ai
            global button_human
            global infoTextList
            global twoPlayers
            
            twoPlayers = False
            
            SIMgame.add_text("You will play against the AI.")
            button_ai.place_forget()
            button_human.place_forget()
            SIMgame.main_choice()
            
        def pick_human():
            global playerTurn
            global button_ai
            global button_human
            global infoTextList
            global twoPlayers
            
            twoPlayers = True
            
            playerTurn = True
            SIMgame.add_text("Player 1 will be blue.")
            SIMgame.add_text("Player 2 will be red.")
            button_ai.place_forget()
            button_human.place_forget()
            SIMgame.main2()
            
        if resetting == False:

            button_ai = tk.Button(root, text='Play AI', width=15, command=pick_ai)
            button_human = tk.Button(root, text='Play Human', width=15, command=pick_human)
            
        button_ai.place(relx = .70, rely = .85)
        button_human.place(relx = .70, rely = .92)
        
        #Defining play first/second buttons for when they are used
        def pick_first():
            global playerTurn
            global button_first
            global button_second
            global infoTextList

            playerTurn = True
            SIMgame.add_text("It's your turn!")
            button_first.place_forget()
            button_second.place_forget()
            SIMgame.main2()

        def pick_second():
            global playerTurn
            global button_first
            global button_second
            global infoTextList

            playerTurn = False
            SIMgame.add_text("It's the computer's turn.")
            button_first.place_forget()
            button_second.place_forget()
            SIMgame.main2()

        if resetting == False:

            button_first = tk.Button(root, text='Play First', width=15, command=pick_first)
            button_second = tk.Button(root, text='Play Second', width=15, command=pick_second)
            
        e1Label = tk.Label(root, text="First point", justify=tk.LEFT)
        e2Label = tk.Label(root, text="Second point", justify=tk.LEFT)
        e1Label.place(relx = .55, rely = .85)
        e2Label.place(relx = .5, rely = .92)

        e1 = tk.Entry(root)
        e2 = tk.Entry(root)
        e1.place(relx = .70, rely = .85)
        e2.place(relx = .70, rely = .92)

        def enter_move():
            global enteredMove
            enteredMove = []

            try:
                enteredMove.append(int(e1.get()))
            except:
                enteredMove.append("Error")

            try:
                enteredMove.append(int(e2.get()))
            except:
                enteredMove.append("Error")

            SIMgame.getPlayerMove2()

        if resetting == False:            
            entryButton = tk.Button(root, text='Enter move', command=enter_move)

        entryButton.place(relx = .70, rely = .75)

        e1Label.place_forget()
        e2Label.place_forget()
        e1.place_forget()
        e2.place_forget()
        entryButton.place_forget()            
        
        if resetting == False:
            tk.mainloop()
            
        resetting = False
        
        
    def main_choice():

        global button_first
        global button_second

        SIMgame.add_text("Will you play first or second?")

        button_first.place(relx = .70, rely = .85)
        button_second.place(relx = .70, rely = .92)
        
        
    def main2():
        
        global playerName
        global compName
        global playerTurn
        global compNumber
        global playerNumber
        global winnerFound
        global movesCount
        global winner
        global movesPlayed
        global currentBoard
        global infoTextList
        
        global root
        global canvas
        global button_first
        global button_second
        
        global e1Label
        global e2Label
        global e1
        global e2
        global entryButton
        

        if playerTurn == True:
            compNumber = 2
            playerNumber = 1
            
        else:
            compNumber = 1
            playerNumber = 2
            SIMgame.getComputerMove()
            
        if winnerFound == False and movesCount <= 15:
            
            if playerTurn == True:
                SIMgame.add_text("Input your next move.")
                SIMgame.getPlayerMove()
                SIMgame.checkWinner()
            else:
                SIMgame.getComputerMove()
                SIMgame.checkWinner()

            
#Run game:            
SIMgame.main()