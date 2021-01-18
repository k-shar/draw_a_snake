import pygame

def scale_up_to_ratio(smaller, larger, ratio):
    """
    method that takes the dimentions of 
    - smaller surface (pygame.Surface())
    - larger surface (pygame.Surface())
    - aspect ratio (w, h)
    and returns the dimentions of 
    - the new resized "smaller" window (x, y)
    """

    maximum_size = list(larger.get_size())
    i = 0
    while True:
        i += 1
        # create a dummy list to hold the size
        test_size = [ratio[0] * i, ratio[1] * i]

        # if size is too big to fit in larger
        if test_size[0] > maximum_size[0] or test_size[1] > maximum_size[1]:

            # rollback last attempted scale up
            test_size = [test_size[0] - ratio[0], test_size[1] - ratio[1]]

            # scale smaller surface to new dimentions
            resized = pygame.transform.scale(smaller, test_size)
            return resized

def center_surfaces(inner, outer):
    """
    return coordinates for where
    the top left corner of inner
    needs to be so inner looks 
    horizontaly and vertically centered to outer
    """

    inner_size = inner.get_size()
    outer_size = outer.get_size()

    center_x = (outer_size[0] - inner_size[0]) / 2
    center_y = (outer_size[1] - inner_size[1]) / 2

    return [center_x, center_y]
