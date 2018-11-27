import sys
sys.path.append("game/")
import wrapped_flappy_bird as game

game_state = game.GameState()
# instantiate
while True:

    do = [1, 0]
    image, reward, terminal = game_state.frame_step(do, manual=True)

