bottom = self.rect.bottom
            left = self.rect.left
            self.image = pygame.transform.scale(self.image,(30,40))
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.left = left