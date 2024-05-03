import pygame
import random


# Defining window width and height
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
pygame.font.init()
GREEN_BG = (173, 214, 68)
WHITE = (255, 255, 255)
score = 0
FPS = 60

class Snake:
    SPEED = 20
    SNAKE_SKIN = (93, 125, 245)
    SNAKE_HEAD = (157, 224, 232)
    WIDTH = 20
    HEIGHT = 20
    # define array to keep track of coordinates of each body part of snake
    bodyPos = []



    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
        # Have snake initially start with 3 body parts
        self.bodyPos.append([self.posX, self.posY])
        self.bodyPos.append([self.posX - 20, self.posY])
        self.bodyPos.append([self.posX - 40, self.posY])

class Apple:
   eaten = False

   def __init__(self, posX, posY):
       self.posX = posX
       self.posY = posY
       


def get_random_pos(min, max):
    value = random.randint(min, max)
    while value % 20 != 0:
        value = random.randint(min, max)
    return value

def update_remaining_pos():
    # remove last element
    snake.bodyPos.pop()

def snake_grow():
    # check last two x values and y values of snakeBody (last two elements)
    # if the x values are not the same aka they are changing then
    if snake.bodyPos[len(snake.bodyPos) - 1][0] != snake.bodyPos[len(snake.bodyPos) - 2][0]:
         snake.bodyPos.append([snake.bodyPos[len(snake.bodyPos) - 1][0] - 20, snake.bodyPos[len(snake.bodyPos) - 1][1]])
    # otherwise, if the y values are not the same  then
    elif snake.bodyPos[len(snake.bodyPos) - 1][1] != snake.bodyPos[len(snake.bodyPos) - 2][1]:
         snake.bodyPos.append([snake.bodyPos[len(snake.bodyPos) - 1][0], snake.bodyPos[len(snake.bodyPos) - 1][1] - 20])


def draw_snake():
        for i in range(len(snake.bodyPos)):
            # if snake head
            if i == 0:
                pygame.draw.rect(WIN, snake.SNAKE_HEAD, pygame.Rect(snake.bodyPos[i][0], snake.bodyPos[i][1], snake.HEIGHT, snake.WIDTH))
            else:
                pygame.draw.rect(WIN, snake.SNAKE_SKIN, pygame.Rect(snake.bodyPos[i][0], snake.bodyPos[i][1], snake.HEIGHT, snake.WIDTH))
                
                
def draw_apple():
    pygame.draw.rect(WIN, (250, 0, 0), pygame.Rect(current_apple.posX, current_apple.posY, 20, 20))

def show_score():
    # Setting up score
    font = pygame.font.Font(None, 36)  
    text = font.render("Score: %d" % (score), True, WHITE)  
    text_rect = text.get_rect()  
    text_rect.topright = (WIDTH - 10, 10)  
    WIN.blit(text, text_rect)  


def draw_window():
    # Set green background
    WIN.fill(GREEN_BG)
    # Draw grid
    draw_grid()
    # show score
    show_score()
    # Draw snake
    draw_snake()
    # Draw apple
    draw_apple()


    pygame.display.update()

def draw_grid():
    blockSize = 20 #Set the size of the grid block
    for x in range(0, WIDTH, blockSize):
        for y in range(0, HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(WIN, (150, 150, 150), rect, 1)

def is_at_edge():
    if snake.posY >= 480 or snake.posY <= 1 or snake.posX >= 480 or snake.posX <= 1:
        return True
    else:
        return False
    
def generate_apple():
    global current_apple
    apple_created = False
    same_pos = 0

    while apple_created == False:
        # generate new apple coordinates
        current_apple = Apple(get_random_pos(60, 460), get_random_pos(60, 460))
        # check if apple coordinates match snake.bodyPos coordinates
        # iterate through each snake body position
        for i in range(0, len(snake.bodyPos)):
            # if snake body position is equal to apple position
            if snake.bodyPos[i][0] == current_apple.posX and snake.bodyPos[i][1] == current_apple.posY:
                same_pos += 1
        
        # if there are no body coordinates that are the same as apple coordinates then stop the loop
        if same_pos == 0:
            apple_created = True
        else:
            # reset same_pos to 0
            same_pos = 0



    
def check_apple_eaten():
    global current_apple
    global score
    # check if position X and Y of snake head is the same as current_apple's position
    if snake.bodyPos[0][0] == current_apple.posX and snake.bodyPos[0][1] == current_apple.posY:
        # if so, create a new apple that doesn't spawn in the same coordinates as snake's body
        generate_apple()
        # make snake body longer
        snake_grow()
        # increase score
        score += 1

def check_body_hit():
    # check if snake head is equal to any of the positions in snake body
    for i in range(1, len(snake.bodyPos)):
        if snake.bodyPos[i][0] == snake.bodyPos[0][0] and snake.bodyPos[i][1] == snake.bodyPos[0][1]:
            return True
    return False

# Create Snake object
snake = Snake(get_random_pos(60, 460), get_random_pos(60, 460))
# Create Apple object
current_apple = Apple(get_random_pos(60, 460), get_random_pos(60, 460))

def main():
    clock = pygame.time.Clock()
    run = True
    moves_right = False
    moves_down = False
    moves_left = False
    moves_up = False



    while run:
        # Run the while loop 60 times per second
        clock.tick(FPS)
        for event in pygame.event.get():
            #if the user quits the game, then the loop should stop
            if event.type == pygame.QUIT:
                run = False
        
            # Check key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    moves_right = True
                    moves_down = False
                    moves_left = False
                    moves_up = False
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    moves_down = True 
                    moves_right = False
                    moves_left = False
                    moves_up = False
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    moves_left = True
                    moves_right = False
                    moves_up = False
                    moves_down = False
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    moves_up = True
                    moves_down = False
                    moves_left = False
                    moves_right = False
        
        # Manage user movement based on key presses
        if moves_right:
            pygame.time.delay(280)
            snake.posX += snake.SPEED 
            snake.bodyPos.insert(0, [snake.posX, snake.posY])
            update_remaining_pos()  
        elif moves_left:
            pygame.time.delay(280)
            snake.posX -= snake.SPEED 
            snake.bodyPos.insert(0, [snake.posX, snake.posY])
            update_remaining_pos() 
        elif moves_down:
            pygame.time.delay(280)
            snake.posY += snake.SPEED 
            snake.bodyPos.insert(0, [snake.posX, snake.posY])
            update_remaining_pos() 

        elif moves_up:
            pygame.time.delay(280)
            snake.posY -= snake.SPEED 
            snake.bodyPos.insert(0, [snake.posX, snake.posY])
            update_remaining_pos() 


        # check if snake has eaten apple
        check_apple_eaten()

        # check if snake head collided with body
        if check_body_hit():
            run = False

        # check if snake head reaches edge coordinates
        if is_at_edge():
            run = False

        draw_window()

    pygame.quit()

# Ensure that only the main.py file is called or executed
if __name__ == '__main__':
    main()