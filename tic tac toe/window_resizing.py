import pygame


def scale_up_to_ratio(smaller, larger, ratio):
    """
    method that takes the dimentions of 
    - smaller surface (pygame.Surface())
    - larger surface (pygame.Surface())
    - aspect ratio (w, h)
    and returns a surface resized to fill the larger
    pygame.Surface()
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


def resize_surfaces(scale, surf, outer_surf, ratio, x, y, offset):
    # temporatily scale down the outer_surf to use for scaling up
    # this will create a padding effect
    padded_outer_surf = pygame.transform.scale(outer_surf, (int(outer_surf.get_width() * scale), int(outer_surf.get_height() * scale)))
    surf = scale_up_to_ratio(surf, padded_outer_surf, (ratio))

    # coordinates of the center of the inner surface (surf)
    surf_pos = (int(outer_surf.get_width() * x), int(outer_surf.get_height() * y))

    # set these coordinates to rect, as surface.blit() accepts rects as destinations
    surf_rect = surf.get_rect()
    surf_rect.centerx, surf_rect.centery = surf_pos
 
    # calculate offset
    if offset != None:
        offset[0] += surf_rect.x
        offset[1] += surf_rect.y

    return surf, surf_rect, offset
