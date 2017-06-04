# -*- coding: utf-8 -*-
"""
@author: Dylan Santos de Pinho, Cédric Pahud
"""
import shlex
import string

row = 9
board_player = [" "]*row**2
numbers_of_boats = 1
player = {"id":0,"board":board_player,"nb_boat":0}
# game = {"player1":player.copy,"player2":player.copy}
games = {"player1":player.copy(),"player2":player.copy(), "turn":0}

is_game_started = False
are_boats_placed = False

def help(data):
    str_help = "```!help : to get all the commands\n"
    str_help += "!start @player : to start a game with a player\n"
    str_help += "!board @player : to get the boards, B = boats, O = miss, X = boat hitted\n"
    str_help += "!put position alignment : to put a boat in position(A1, A2,...) with the alignment (h/v).\n      ex: !put A1 h -> put a boat in A1 and B1\n          !put A1 v -> put a boat in A1 and A2 \n"
    str_help += "!fire position : to fire in position\n```"
    
    return [data['d']['author']['id'],str_help]
    
def start(data):
    global is_game_started
    global are_boats_placed
    global games
    if not is_game_started:
        are_boats_placed = False
        games = {"player1":player.copy(),"player2":player.copy(), "turn":0}
        games['player1']['id'] = data['d']['author']['id']            
        games['player2']['id'] = data['d']['mentions'][0]['id']  
        games["turn"] = games['player1']['id']
        is_game_started = True
        return [games['player1']['id'],"Game started!",games['player2']['id'],"It's time to d-d-d-d-duel!"]
         

def board(data):
    return [data['d']['author']['id'],my_board(data)[1] + " " + adversary_board(data)[1]]

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
        return [data['d']['author']['id'],"Please start the game"]

def my_board_but_not_for_me(data):
    if is_game_started:
        player = get_player(data)
        
        if player  == "try again":
            return [data['d']['author']['id'],"Mais t'es qui?"]
        
        board ="board de l'adversaire\n__``` |" +  "|".join(letter for letter in string.ascii_uppercase[0:row]) + "|\n"
        for num in range(0,row,1):
            board += str(num+1) + "".join("|"+games[player]["board"][num*row+i] for i in range(0,row)) + "|\n"
        board += "```__"
        return [data['d']['author']['id'],board]
    else:
        return [data['d']['author']['id'],"Please start the game"]

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
        return [data['d']['author']['id'],"Please start the game"]


def adversary_board_with_boat(data):
    if is_game_started:
        player = get_other_player(data)
        
        if player  == "try again":
            return [data['d']['author']['id'],"Mais t'es qui?"]
        
        board ="votre board\n__``` |" +  "|".join(letter for letter in string.ascii_uppercase[0:row]) + "|\n"
        for num in range(0,row,1):
            board += str(num+1) + "".join("|"+games[player]["board"][num*row+i] for i in range(0,row)) + "|\n"
        board += "```__"
        return [data['d']['author']['id'],board]
    else:
        return [data['d']['author']['id'],"Please start the game"]
    
def mon_adversary_board_with_boat(data):
    if is_game_started:
        player = get_other_player(data)
        
        if player  == "try again":
            return [data['d']['author']['id'],"Mais t'es qui?"]
        
        board ="board de l'adversaire\n__``` |" +  "|".join(letter for letter in string.ascii_uppercase[0:row]) + "|\n"
        for num in range(0,row,1):
            board += str(num+1) + "".join("|"+games[player]["board"][num*row+i] for i in range(0,row)) + "|\n"
        board += "```__"
        return [data['d']['author']['id'],board]
    else:
        return [data['d']['author']['id'],"Please start the game"]


def fire(data):
    if are_boats_placed:
        global is_game_started
        if games["turn"] == data['d']['author']['id']:
            player = get_other_player(data)
            
            if player  == "try again":
                return [data['d']['author']['id'],"Mais t'es qui?"]
                 
            str = data['d']['content']
            case_coord = shlex.split(str, posix=False)[1].upper()
            case_impact = (ord(case_coord[1])-49)*9+ord(case_coord[0])-65
            if games[player]['board'][case_impact] == 'B':
                games[player]['board'][case_impact] = 'X'
                games[player]["nb_boat"] -= 1
                if games[player]["nb_boat"] == 0 :
                    str1 = my_board(data)[1]+ mon_adversary_board_with_boat(data)[1] +"\nYou won the game"
                    str2 = adversary_board_with_boat(data)[1] + my_board_but_not_for_me(data)[1]+"\nYour lost the game."
                    is_game_started = False
                    return [data['d']['author']['id'],str1,games[get_other_player(data)]['id'],str2]
            elif games[player]['board'][case_impact] == ' ':
                games[player]['board'][case_impact] = 'O'
            else: 
                return [data['d']['author']['id'],"You already fired there."]
        
            games["turn"] = games[player]['id']
            return [data['d']['author']['id'],adversary_board(data)[1],games[get_other_player(data)]['id'],adversary_board_with_boat(data)[1]+"\nYour turn now."]
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
        
        if games[player]['nb_boat'] == numbers_of_boats*taille:
            return [data['d']['author']['id'],"All your boats are placed"]
        
        game_temp = games[player]['board'].copy()
        
        collision = False
        str = data['d']['content']
        if len(shlex.split(str, posix=False))!=3:
            return [data['d']['author']['id'],"Wrong syntax."]
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
            games[player]["nb_boat"] +=taille 
            if games['player1']["nb_boat"]==numbers_of_boats*taille and games['player2']["nb_boat"]==numbers_of_boats*taille:
                are_boats_placed = True
                return [games['player1']['id'],"Your turn to fire",games['player2']['id'],"Wait for the other player to fire."]
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
            


