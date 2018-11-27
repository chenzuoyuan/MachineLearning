import sys
sys.path.append("game/")
import cv2
import wrapped_flappy_bird as game

game_state = game.GameState()
# instantiate
do = [0, 1]
image, reward, terminal = game_state.frame_step(do)
# input moves, return the result
print image.shape, reward, terminal
# print the size of image, reward and the value of terminal

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
# RGB transfer to BGR
cv2.imshow('image', image)
# display the picture
cv2.waitKey(0)

