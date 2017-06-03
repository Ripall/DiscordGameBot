# -*- coding: utf-8 -*-
"""
@author: Dylan Santos de Pinho, Cédric Pahud
"""

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
        
def adversary_board_with_boat(data):
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