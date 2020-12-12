import pygame
import constants as con

def fit_aspect_ratio(start, ratio, end):
    """
    resisze start to be as large as posible
    with the given aspect ratio
    without overflowing over end
    """

    end_size = list(end.get_size())

    i = 0
    # run loop until max size is found
    while True:     

        # scale up start by multiples of the aspect ratio
        i += 1
        size = [ratio[0] * i, ratio[1] * i]

        # if bigger than end
        if size[0] >= end_size[0] or size[1] >= end_size[1]:

            # revert last scale up
            size = [size[0] - ratio[0] * con.WINDOW_PADDING, size[1] - ratio[1] * con.WINDOW_PADDING]      
            # scale start to the now found max size    
            resized = pygame.transform.scale(start, size)
            return resized

def center_surfaces(inner, outer):
    """
    Position top left corner of inner 
    so that inner is in the center of outer
    """

    inner_size = inner.get_size()
    outer_size = outer.get_size()

    center_x = (outer_size[0] - inner_size[0] ) / 2   
    center_y = (outer_size[1] - inner_size[1] ) / 2

    return [center_x, center_y]