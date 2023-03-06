import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size, colors="white on blue", callback=None):
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
        self.callback = callback

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.colors = "red on cyan"
        else:
            self.colors = "red on white"

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.state = not self.state
                self.pressed = 0
                if self.callback:
                    self.callback()
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.pressed = 1

    def show(self, GUI):
        self.fg, self.bg = self.colors.split(" on ")
        pygame.draw.line(
            GUI.screen,
            (150, 150, 150),
            (self.x, self.y),
            (self.x + self.w, self.y),
            5,
        )
        pygame.draw.line(
            GUI.screen,
            (150, 150, 150),
            (self.x, self.y - 2),
            (self.x, self.y + self.h),
            5,
        )
        pygame.draw.line(
            GUI.screen,
            (50, 50, 50),
            (self.x, self.y + self.h),
            (self.x + self.w, self.y + self.h),
            5,
        )
        pygame.draw.line(
            GUI.screen,
            (50, 50, 50),
            (self.x + self.w, self.y + self.h),
            [self.x + self.w, self.y],
            5,
        )
        pygame.draw.rect(GUI.screen, self.bg, (self.x, self.y, self.w, self.h))
        GUI.screen.blit(self.text_render, self.position)

    def debug(self, GUI):
        return
