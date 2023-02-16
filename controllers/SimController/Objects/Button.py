import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size, colors="white on blue"):
        super().__init__()
        self.text = text
        self.colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        self.font = pygame.font.SysFont("freesansbold", size)
        self.text_render = self.font.render(text, 1, self.fg)
        self.image = self.text_render
        self.x, self.y, self.w, self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.position = position

        self.pressed = 1
        self.state = 0

        self.update()

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colors = "red on cyan"
        else:
            self.colors = "red on white"

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.state = not self.state
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.pressed = 1

        return self.state
