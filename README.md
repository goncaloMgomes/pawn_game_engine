# pawn_game_engine

This is an engine for the pawn game.

The pawn game is like chess but only with pawns, same rules apply, one player wins when one of theirs pawns arrives at the row on the other side of the board or if the adversary is out of moves.

The engine can be used on the terminal by running the command: 

```bash
python3 pawn_engine.py
```

Or like an API by importing the pawn_engine.py file.
```python
set_human_colour(colour)  #"white" makes the human play with the white pieces and the engine with the black pieces
                          #"black" is the other way around
```
```python
set_starting_player(player) #defines who starts playing, options: "computer" or "human"
```
```python
print_board_position() #prints the piece's positions on the board
```
```python
init_board() #initializes the board with the pieces on the starting positions
```
```python
print_board() #prints the board in the current state
```
```python
legal_move = do_move(src_label,dst_label) #plays human move, for that give the source label and the destiny label
                                          #returns True if the moveis valid False otherwise
```

```python
#for the engine move one can do:
do_cmove(get_cmove()) #plays the engine move
#or
move = get_cmove() #get the engine move
do_cmove(move) #plays the engine move
```
```python
winner = is_game_over(get_cmove())  #check if the game is over, winner == 0 if the game is not over
                                    #winner == engine_colour if the engine won
                                    #winner == human_colour if the human won the game
```

