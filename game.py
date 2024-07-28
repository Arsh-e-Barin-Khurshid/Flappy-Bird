import pygame as pg
import sys
import time
from random import randint

pg.init()

class Pipe:
    def __init__(self, scale_factor, move_speed):
        self.img_up = pg.transform.scale(pg.image.load("assets/pipeup.png").convert_alpha(), (52 * scale_factor, 320 * scale_factor))
        self.img_down = pg.transform.scale(pg.image.load("assets/pipedown.png").convert_alpha(), (52 * scale_factor, 320 * scale_factor))
        self.rect_up = self.img_up.get_rect()
        self.rect_down = self.img_down.get_rect()
        self.pipe_distance = 200
        self.rect_up.y = randint(250, 520)
        self.rect_up.x = 500
        self.rect_down.y = self.rect_up.y - self.pipe_distance - self.rect_up.height
        self.rect_down.x = 500
        self.move_speed = move_speed

    def drawpipe(self, win):
        win.blit(self.img_up, self.rect_up)
        win.blit(self.img_down, self.rect_down)

    def update(self, dt):
        self.rect_up.x -= int(self.move_speed * dt)
        self.rect_down.x -= int(self.move_speed * dt)

class Bird(pg.sprite.Sprite):
    def __init__(self, img_list, scale_factor):
        super().__init__()
        self.img_list = [pg.transform.scale(pg.image.load(img).convert_alpha(), (34 * scale_factor, 24 * scale_factor)) for img in img_list]
        self.image_index = 0
        self.image = self.img_list[self.image_index]
        self.rect = self.image.get_rect(center=(100, 100))
        self.y_velocity = 0
        self.gravity = 10
        self.flap_speed = 250
        self.anim_counter = 0
        self.update_on = False
        self.collision = False

    def update(self, dt):
        if self.update_on or self.collision:
            self.applyGravity(dt)
            self.playAnimation()

            if self.rect.y < 0 and self.flap_speed == 250:
                self.rect.y = 0
                self.flap_speed = 0
                self.y_velocity = 0
            elif self.rect.y >= 0 and self.flap_speed == 0:
                self.flap_speed = 250

    def applyGravity(self, dt):
        self.y_velocity += self.gravity * dt
        self.rect.y += self.y_velocity

    def flap(self, dt):
        self.y_velocity = -self.flap_speed * dt
        self.playAnimation()  # Trigger animation on flap

    def playAnimation(self):
        self.anim_counter += 1
        if self.anim_counter >= 5:
            self.image_index = (self.image_index + 1) % len(self.img_list)
            self.image = self.img_list[self.image_index]
            self.anim_counter = 0

    def resetposition(self):
        self.rect.center = (100, 100)
        self.y_velocity = 0
        self.anim_counter = 0

class Game:
    def __init__(self):
        # Setting window configuration
        self.width = 500
        self.height = 668
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250
        self.start_monitoring = False
        self.score = 0
        self.font = pg.font.Font("assets/font.ttf", 24)
        self.is_enter_pressed = False
        self.is_paused = True  # Initial game state
        self.game_over = False
        self.is_game_started = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.setUpBgAndGround()
        self.background_images = ["assets/bg1.png", "assets/bg2.png", "assets/bg3.png", "assets/bg4.png"]
        self.bird_images = [
            ["assets/bluebirdup.png", "assets/bluebirddown.png"],
            ["assets/brownbirdup.png", "assets/brownbirddown.png"],
            ["assets/yellowbirdup.png", "assets/yellowbirddown.png"],
            ["assets/greybirdup.png", "assets/greybirddown.png"]
        ]
        self.selected_background = None
        self.selected_bird_images = None

        self.showBackgroundSelectionMenu()

    def showBackgroundSelectionMenu(self):
        while True:
            self.win.fill((0, 0, 0))
            menu_text = self.font.render("Select Background:", True, (255, 255, 255))
            self.win.blit(menu_text, (self.width // 2 - menu_text.get_width() // 2, 50))

            for i, bg_path in enumerate(self.background_images):
                bg_img = pg.transform.scale(pg.image.load(bg_path).convert(), (200, 150))
                x = self.width // 2 - 100 + (i % 2) * 250 - 125
                y = (i // 2) * 200 + 150
                bg_rect = bg_img.get_rect(topleft=(x, y))
                self.win.blit(bg_img, bg_rect)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP:
                    for i, bg_path in enumerate(self.background_images):
                        bg_rect = pg.Rect(self.width // 2 - 100 + (i % 2) * 250 - 125, (i // 2) * 200 + 150, 200, 150)
                        if bg_rect.collidepoint(event.pos):
                            self.selected_background = bg_path
                            self.showBirdSelectionMenu()

    def showBirdSelectionMenu(self):
        while True:
            self.win.fill((0, 0, 0))
            menu_text = self.font.render("Select Bird:", True, (255, 255, 255))
            self.win.blit(menu_text, (self.width // 2 - menu_text.get_width() // 2, 50))

            for i, bird_paths in enumerate(self.bird_images):
                bird_img = pg.transform.scale(pg.image.load(bird_paths[0]).convert_alpha(), (68, 48))
                x = self.width // 2 - 100 + (i % 2) * 250 - 34
                y = 200 + (i // 2) * 100
                bird_rect = bird_img.get_rect(topleft=(x, y))
                self.win.blit(bird_img, bird_rect)

            pg.display.update()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONUP:
                    for i, bird_paths in enumerate(self.bird_images):
                        bird_rect = pg.Rect(self.width // 2 - 100 + (i % 2) * 250 - 34, 200 + (i // 2) * 100, 68, 48)
                        if bird_rect.collidepoint(event.pos):
                            self.selected_bird_images = bird_paths
                            self.bird = Bird(self.selected_bird_images, self.scale_factor)
                            self.bg_img = pg.transform.scale(pg.image.load(self.selected_background).convert(), (self.width, self.height))
                            self.gameloop()

    def gameloop(self):
        last_time = time.time()
        while True:
            # Calculating delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.is_paused = False  # Unpause the game
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                        self.is_game_started = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed and not self.game_over:
                        self.bird.flap(dt)

                if event.type == pg.MOUSEBUTTONUP:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def restartGame(self):
        self.score = 0
        self.is_enter_pressed = False
        self.is_game_started = False
        self.is_paused = True
        self.bird.resetposition()
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.bird.update_on = False
        self.game_over = False
        self.showBackgroundSelectionMenu()  # Show the background selection menu again

    def checkScore(self):
        if len(self.pipes) > 0:
            if (self.bird.rect.left > self.pipes[0].rect_down.left and self.bird.rect.right < self.pipes[0].rect_down.right and not self.start_monitoring):
                self.start_monitoring = True
            if self.bird.rect.left > self.pipes[0].rect_down.right and self.start_monitoring:
                self.start_monitoring = False
                self.score += 1

    def checkCollisions(self):
        if len(self.pipes) != 0:
            if self.bird.rect.colliderect(self.pipes[0].rect_down) or self.bird.rect.colliderect(self.pipes[0].rect_up):
                self.bird.collision = True  # Set the collision flag
                self.is_enter_pressed = False
                self.is_game_started = False

        if self.bird.rect.bottom > 568:
            self.bird.update_on = False
            self.bird.collision = False  # Stop bird updates
            self.is_enter_pressed = False
            self.is_game_started = False
            self.is_paused = True
            self.game_over = True

    def updateEverything(self, dt):
        if not self.is_paused:
            if self.is_enter_pressed and not self.game_over:
                # Move the ground
                self.ground1_rect.x -= int(self.move_speed * dt)
                self.ground2_rect.x -= int(self.move_speed * dt)

                # Reposition the ground if it goes off-screen
                if self.ground1_rect.right < 0:
                    self.ground1_rect.x = self.ground2_rect.right
                if self.ground2_rect.right < 0:
                    self.ground2_rect.x = self.ground1_rect.right

                # Generating pipes
                if self.pipe_generate_counter > 70:
                    self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                    self.pipe_generate_counter = 0

                self.pipe_generate_counter += 1

                # Moving the pipes
                for pipe in self.pipes:
                    pipe.update(dt)

                # Removing pipes if out of screen
                if len(self.pipes) != 0:
                    if self.pipes[0].rect_up.right < 0:
                        self.pipes.pop(0)

            # Moving the bird
            self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, 0))
        for pipe in self.pipes:
            pipe.drawpipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.win.blit(score_text, (10, 10))

        if self.game_over:
            score_restart = self.font.render(f"Restart", True, (0, 0, 0))
            self.restart_text_rect = score_restart.get_rect(center=(self.width // 2, 630))
            self.win.blit(score_restart, self.restart_text_rect)

    def setUpBgAndGround(self):
        self.ground1_img = pg.transform.scale(pg.image.load("assets/ground.png").convert(), (self.width, 100))
        self.ground2_img = pg.transform.scale(pg.image.load("assets/ground.png").convert(), (self.width, 100))

        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568

game = Game()
