import pygame
import os
import cv2

def click_handler(x, y):
    if y < 600:
        spriteAdder(x, y)
    else:
        pass

def map_obj_del(x, y):
    x = (x//40)*40
    y = (y//40)*40

    for objects in map_objects:
        if objects[1] == x and objects[2] == y:
            map_objects.remove(objects)

def rot_sprite(x, y):
    x = (x//40)*40
    y = (y//40)*40
    
    for objects in map_objects:
        if objects[1] == x and objects[2] == y:
            objects[0] = pygame.transform.rotate(objects[0], 90)

def spriteAdder(x, y):
    x = (x//40)*40
    y = (y//40)*40

    map_objects.append([tilesImg[selected_sprite], x, y])

def save_file(surface):
    path = os.getcwd()
    path = path.split('\\')
    path = path[:len(path)-1]
    new_path = ''
    for p in path:
        new_path += p+'/'
    new_path += '/Output'
    os.chdir(new_path)

    data = os.listdir()
    if data:
        x = data[len(data)-1:]
        x = x[0].split('.')[0]
        file = str(int(x)+1)+'.png'
    else:
        file = '0.png'
    pygame.image.save(surface,file)
    
    img = cv2.imread(file)
    crop_img = img[:600, :600]
    os.remove(file)
    cv2.imwrite(file, crop_img)
    
os.chdir('Images')
tiles = os.listdir()
tilesImg = [pygame.image.load(img) for img in tiles]
width = 600
height = 600 + (int((len(tiles)/15)+1)*40)
selected_sprite = 0

map_objects = []

surface = pygame.display.set_mode((width, height))

loop = True
saveFile = False

while loop == True:
    surface.fill((0, 0, 0))
    for i, tileImg in enumerate(tilesImg):
        surface.blit(tileImg, (0+(i*40),600))

    for objects in map_objects:
        surface.blit(objects[0], (objects[1], objects[2]))
    if saveFile == False:  
        pygame.draw.rect(surface, (255, 0, 0), (0+(selected_sprite*40), 600, 40, 40), 5)        

    pygame.display.update()

    if saveFile == True:
        save_file(surface)
        loop = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                x, y = pygame.mouse.get_pos()
                rot_sprite(x, y)
            if event.key == pygame.K_LEFT:
                if selected_sprite > 0:
                    selected_sprite -= 1
            if event.key == pygame.K_RIGHT:
                if selected_sprite < len(tilesImg)-1:
                    selected_sprite += 1
            if event.key == pygame.K_s:
                saveFile = True
                
    x, y = pygame.mouse.get_pos()
    leftClick, _, rightClick = pygame.mouse.get_pressed()    
    if leftClick:
        click_handler(x, y)
    if rightClick:
        map_obj_del(x, y)

pygame.quit()
quit()
