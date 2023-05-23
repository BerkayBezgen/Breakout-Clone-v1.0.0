import os

import pygame
pygame.font.init()


class Settings():  # Statische Klassen
    SCREENRECT = pygame.Rect(0, 0, 800, 600)
    FPS = 60
    PATHFILE = os.path.dirname(os.path.abspath(__file__))
    PATHIMG = os.path.join(PATHFILE, "images")
    PATHSOUND = os.path.join(PATHFILE, "sounds")

    @staticmethod
    def get_image_path(filename):
        return os.path.join(Settings.PATHIMG, filename)
    
    @staticmethod
    def get_sound_path(filename):
        return os.path.join(Settings.PATHSOUND, filename)

    FONT = pygame.font.SysFont("Arial", 25)
    


class Paddle(pygame.sprite.Sprite):

    def __init__(self, filename, x, y, colorkey=None):
        super().__init__()
        self.x = x
        self.y = y
        self.hearts = 3
        if colorkey is not None:
            self.image = pygame.image.load(Settings.get_image_path(filename))
            self.image.set_colorkey(colorkey)
        else:
            self.image = pygame.image.load(Settings.get_image_path(filename))
        self.image = pygame.transform.scale(self.image, (200,50))
        self.rect = self.image.get_rect()
        self.vel = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, colorkey=None):
        super().__init__()
        self.x = x
        self.y = y
        self.xv = 7.5
        self.yv = 7.5
        self.score = 0
        if colorkey is not None:
            self.image = pygame.image.load(Settings.get_image_path(filename)).convert()
            self.image.set_colorkey(colorkey)
        else:
            self.image = pygame.image.load(Settings.get_image_path(filename)).convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = [0, 0]
        self.game_over = False #Flag to track game over state

    def update(self, paddle, bricks):
        
        #Bewegung des Balles basierend auf der Geschwindigkeit
        self.rect.move_ip(self.xv, self.yv)

        # Überprüfüng ob der Ball mit dem Paddel kollidiert
        if self.rect.colliderect(paddle.rect):
            self.yv = -self.yv


        for brick in bricks:
            if brick.visible and self.rect.colliderect(brick.rect):
                self.yv = -self.yv
                brick.visible = False
                self.score += 5
                brick_destroyed_sound = pygame.mixer.Sound(Settings.get_sound_path("burst.mp3"))
                brick_destroyed_sound.play()


          

        
        
        # Überprüfüng ob der Ball den linken oder rechten Rand des Bildschirms erreicht
        if self.rect.left <= 0 or self.rect.right >= Settings.SCREENRECT.width:
            self.xv = -self.xv

        # Überprüfüng ob der Ball den oberen Bildschirmrand erreicht
        if self.rect.top <= 0:
            self.yv = -self.yv

       
        
        # Überprüfüng ob der Ball den unteren Bildschirmrand erreicht
        if self.rect.bottom > Settings.SCREENRECT.height:
            paddle.hearts -= 1
            loose_heart_sound = pygame.mixer.Sound(Settings.get_sound_path("burst.mp3"))
            loose_heart_sound.play()

            if paddle.hearts > 0:
                self.reset_position(paddle)
            else:
                self.game_over = True
 

    #  Setzt die Position des Balls und des Paddles zurück
    def reset_position(self, paddle):
        self.rect.topleft = (370, 300)
        paddle.rect.topleft = (300, 500)
        self.xv = 7
        self.yv = 7
            
            
    def draw(self, screen,paddle):
        screen.blit(self.image, self.rect)
        score_text = Settings.FONT.render(f"Score: {self.score}",True,(255, 255, 255))
        screen.blit(score_text,(10,10))
        lives_text = Settings.FONT.render(f"Lives: {paddle.hearts}",True,(255, 255, 255))
        screen.blit(lives_text, (Settings.SCREENRECT.width - 120, 10))
        if self.game_over:
            game_over_text = Settings.FONT.render("Game Over!", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=Settings.SCREENRECT.center)
            screen.blit(game_over_text, game_over_rect)
            
            

            

class Brick(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.xx = self.x + self.w
        self.yy = self.y + self.h
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, bricks):
        pygame.draw.rect(bricks, self.color, [self.x, self.y, self.w, self.h])


bricks = []
colors = [(255, 165, 0), (192, 192, 192), (255, 165, 0), (192, 192, 192), (255, 165, 0), (192, 192, 192), (255, 165, 0)]


def init():
    global bricks
    bricks = []
    for i in range(7):
        for j in range(10):
            bricks.append(Brick(10 + j * 79, 40 + i * 35, 70, 25, colors[i]))

 #Z.146 - 155: https://www.youtube.com/watch?v=DLptMaCxllI&list=PLxZI4CJBTZmDC7MqhzMi2RBRSYaxa2F7v&index=2

def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"  # Fensterkoordinaten
    pygame.init()  # Subsysteme starten

    screen = pygame.display.set_mode(Settings.SCREENRECT.size)  # Bildschirm/Fenster dimensionieren
    clock = pygame.time.Clock()  # Taktgeber
    pygame.display.set_caption("Breakout")

    background = pygame.image.load(Settings.get_image_path("background03.png")).convert()  # Bitmap laden und konvertieren
    background = pygame.transform.scale(background, Settings.SCREENRECT.size)  # Bitmap skalieren

    paddle = Paddle("paddle.png", 0, 0)
    ball = Ball("ball.png", 0, 0)
    paddle.rect.topleft = (300, 500)

    ball.rect.topleft = (370, 300)
    init()
    paddle_speed = 5
    game_over = False
    
    

    running = True  # Flagvariable
    while running:  # Hauptprogrammschleife

        clock.tick(Settings.FPS)  # Auf mind. 1/60s takten
        for event in pygame.event.get():  # Einlesen der Message-Queue
            if event.type == pygame.QUIT:  # Ist X angeklickt worden?
                running = False  # Toggle Flag
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_LEFT:
                    paddle.vel[0] = -paddle_speed
                elif event.key == pygame.K_RIGHT:
                    paddle.vel[0] = paddle_speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle.vel[0] = 0

            all_bricks_destroyed = all(not brick.visible for brick in bricks)
        if all_bricks_destroyed:
            # Display "You did it!" message
            message = Settings.FONT.render("Herzlichen Glückwunsch, Sie haben das Spiel erfolgreich beendet!", True, (255, 255, 255))
            message_rect = message.get_rect(center=Settings.SCREENRECT.center)
            screen.blit(message, message_rect)
            pygame.display.flip()  

            pygame.time.wait(5000)
            running = False  # 

        
        

        paddle.rect.move_ip(paddle.vel[0], paddle.vel[1])
        paddle.rect.clamp_ip(Settings.SCREENRECT)
        paddle.update()
        ball.update(paddle,bricks)

        if ball.game_over:
            game_over = True
        
        screen.blit(background, (0, 0))

        paddle.draw(screen)  # Hintergrund malen
        ball.draw(screen,paddle)
        

        for brick in bricks:
            if brick.visible:
                brick.draw(screen)


        if game_over:
            game_over_text = Settings.FONT.render("Game Over!", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect(center=Settings.SCREENRECT.center)
            screen.blit(game_over_text, game_over_rect)
            pygame.display.flip()  
            pygame.time.wait(3000)  
            break

        
        pygame.display.update()

    pygame.display.flip()  # Doublebuffer austauschen

    pygame.quit()  # Subssysteme stoppen


if __name__ == "__main__":
    main()