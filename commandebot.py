# -*- coding: utf-8 -*-
"""
@author: Dylan Santos de Pinho, Cédric Pahud
"""
import shlex
import string

row = 9
board_player = [" "]*row**2
player = {"id":0,"board":board_player,"nb_boat":0}
# game = {"player1":player.copy,"player2":player.copy}
games = {"player1":player.copy(),"player2":player.copy(), "turn":0}

is_game_started = False
are_boats_placed = False

def help(data):
    return [data['d']['author']['id'],"Who needs help? I dont care"]
    
def start(data):
    global is_game_started
    print(data)
    if not is_game_started:
        games['player1']['id'] = data['d']['author']['id']            
        games['player2']['id'] = data['d']['mentions'][0]['id']  
        games["turn"] = games['player1']['id']
        is_game_started = True
        return [games['player1']['id'],"Game started!",games['player2']['id'],"It's time to d-d-d-d-duel!"]
         

#def board(data):
#   my_board(data)
#   adversary_board(data)

def my_board(data):
    if is_game_started:
        player = get_player(data)
        
        if player  == "try again":
            return [data['d']['author']['id'],"Mais t'es qui?"]
        
        board ="votre board\n__``` |" +  "|".join(letter for letter in string.ascii_uppercase[0:row]) + "|\n"
        for num in range(0,row,1):
            board += str(num+1) + "".join("|"+games[player]["board"][num*row+i] for i in range(0,row)) + "|\n"
        board += "```__"
        return [data['d']['author']['id'],board]
    else:
        return [data['d']['author']['id'],"Please start the game sale penguin"]

def fire(data):
    if are_boats_placed:
        if games["turn"] == data['d']['author']['id']:
            
            player = get_other_player(data)
            
            if player  == "try again":
                return [data['d']['author']['id'],"Mais t'es qui?"]
                 
            str = data['d']['content']
            case_coord = shlex.split(str, posix=False)[1].upper()
            case_impact = (ord(case_coord[1])-49)*9+ord(case_coord[0])-65
            if games[player]['board'][case_impact] == 'B':
                games[player]['board'][case_impact] = 'X'
            else:
                games[player]['board'][case_impact] = 'O'
            games["turn"] = games[player]['id']
            return adversary_board(data)
        else:
            return [data['d']['author']['id'],"It's not your turn.",get_other_player(data),"Your friend is waiting for you."]
    else:
        return [data['d']['author']['id'],"Please start the game and/or place your boats to fire"]
        
def put(data):
    global games
    global are_boats_placed
    if is_game_started:
        taille = 3
        player = get_player(data)
        
        if player  == "try again":
            return [data['d']['author']['id'],"Mais t'es qui?"]
        
        if games[player]['nb_boat'] == 5:
            return [data['d']['author']['id'],"All your boats are placed"]
        
        game_temp = games[player]['board'].copy()
        
        collision = False
        str = data['d']['content']
        case_coord = shlex.split(str, posix=False)[1].upper()
        position =  shlex.split(str, posix=False)[2].upper()
        case_posage = (ord(case_coord[1])-49)*9+ord(case_coord[0])-65
        temp = 0;
        for i in range(0,taille):
            if case_posage < row**2:
                if temp > case_posage%row:
                    collision = True                    
                temp = case_posage%row
                if game_temp[case_posage] == ' ':
                    game_temp[case_posage] = 'B'
                else:
                    collision = True
                
                if position=="H" :
                   case_posage += 1
                else :
                    case_posage += row 
                    
            else:
                collision = True
        
        if not collision:
            games[player]['board'] = game_temp.copy()  
            games[player]["nb_boat"] +=1 
            if games['player1']["nb_boat"]==5 and games['player2']["nb_boat"]==5:
                are_boats_placed = True
                return [games['player1'][id],"Your turn to fire",games['player2'],"Wait for the other player to fire."]
            return my_board(data)        
        else:
            return [data['d']['author']['id'],"The way is obstructed."]
    else:
        return [data['d']['author']['id'],"Please start the game..."]


def get_player(data):
    if games['player1']['id'] == data['d']['author']['id']:
        return 'player1'
    elif games['player2']['id'] == data['d']['author']['id']:
        return 'player2'
    else:
        return 'try again'
            

def get_other_player(data):
    if games['player1']['id'] == data['d']['author']['id']:
        return 'player2'
    elif games['player2']['id'] == data['d']['author']['id']:
        return 'player1'
    else:
        return 'try again'
            

def adversary_board(data):
    if is_game_started:
        player = get_other_player(data)
        
        if player  == "try again":
            return [data['d']['author']['id'],"Mais t'es qui?"]
        
        board ="board de l'adversaire\n__``` |" +  "|".join(letter for letter in string.ascii_uppercase[0:row]) + "|\n"
        for num in range(0,row,1):
            board += str(num+1) + "".join("|"+games[player]["board"][num*row+i] if not games[player]["board"][num*row+i] == 'B' else '| ' for i in range(0,row)) + "|\n"
        board += "```__"
        return [data['d']['author']['id'],board]
    else:
        return [data['d']['author']['id'],"Please start the game sale penguin"]

    