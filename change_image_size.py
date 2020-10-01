from PIL import Image

file_name = "circle_transparent.png"

image = Image.open('Pygame_Simulation\\assets\\{}'.format(file_name))
for i in range(100, 400, 50):
    new_image = image.resize((i, i))
    new_image.save('Pygame_Simulation\\assets\\{}_{}.png'.format(file_name.split('.')[0], i))