import sys
sys.path.append("game/")
import cv2
import wrapped_flappy_bird as game

game_state = game.GameState()

init = [1, 0]
# define the initial movement
im, _, _ = game_state.frame_step(init)
# input the movement, get the image
bird = cv2.imread('assets/sprites/redbird-midflap.png')
# read the picture of bird
pipe = cv2.imread('assets/sprites/pipe-green.png')
# read the picture of pipe
pipe = pipe[:50,:,:]
# cut the picture of pipe

def matchTemplate(im, template, mode=cv2.TM_CCOEFF):
    '''
    input:
        im: original image, hope we can find a similar area that matches the template
        template: the template
        mode: match algorithm, we use the correlation match algorithm(cv2.TM_CCOEFF)
    output:
        four angle values that original image match the template
    '''
    res = cv2.matchTemplate(im, template, cv2.TM_CCOEFF)
    # match algorithm of template, return a value matrix
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # find the minimum, the maximum values and their locations of the value matrix
    if max_val > 1e7:
    # 1e7 is a man-made value from experience, and it'll be used when matching pipe
        left, top = max_loc
        # because we choiced TM_CCOEFF algorithm, the result of maximum is what we need
        right, bottom = left + template.shape[1], top + template.shape[0]
        # convert to the location of right and bottom
        return left, top, right, bottom
    return None

find_pipe = False
while True:

    action = [0, 1]

    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    # transfer RGB to BGR

    bird_left, bird_top, bird_right, bird_bottom = matchTemplate(im, bird)
    cv2.rectangle(im, (bird_left, bird_top), (bird_right, bird_bottom), 255, 2)
    # find bird

    if find_pipe:
        # if we find pipe, then get the location of bird and pipe, if the left side of bird goes through the right side of pipe, then find next pipe
        im = im[:,:pipe_right,:]
        pipe_left, pipe_top, pipe_right, pipe_bottom = matchTemplate(im, pipe)

        action = [0, 1] if pipe_top < bird_bottom + 10 else [1, 0]
        # if the distance between bird's bottom and pipe's top, then up, or do nothing

        if bird_left > pipe_right:
            find_pipe = False

    else:
        result = matchTemplate(im, pipe)
        # find pipe
        if result:
            # if the result if matchTemplate is not None, then we think it we have found the pipe
            pipe_left, pipe_top, pipe_right, pipe_bottom = result

            action = [0, 1] if pipe_top < bird_bottom + 10 else [1, 0]
        # if the distance between bird's bottom and pipe's top, then up, or do nothing

            find_pipe = True

    if find_pipe:
        cv2.rectangle(im, (pipe_left, pipe_top), (pipe_right, pipe_bottom), 0, 2)
        # visualize the pipe
    cv2.imshow('im', im)
    # visualize the image
    cv2.waitKey(1)

    im, _, t = game_state.frame_step(action)
    # get next image
    if t:
    # if game over, then display the last image
        cv2.waitKey(0)
        break
