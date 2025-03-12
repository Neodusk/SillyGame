import pygame
import sys
import random
from character import Screen, Character

# Initialize pygame
pygame.init()

# todo: debug fix
debug = True
# Screen dimensions
# screen.width = 800
# screen.height = 600

window_screen = Screen(1920, 1080)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ARROW_COLOR = (0, 0, 0)  # Color for the arrows

# Character settings
# character.width = 112  # Frame width
# character.height = 128  # Frame height
# CHARACTER_SPEED = 5
# character.height = 128
# character.width = 112
# character_speed = 5


MOVE_LEFT = 0
MOVE_RIGHT = 0
MOVE_UP = 0
MOVE_DOWN = 0

# Create the screen
# screen = pygame.display.set_mode((screen.width, screen.height))
# pygame.display.set_caption("Silly Wittle Game")

# Load sprite sheet
sprite_sheet = pygame.image.load('./slimes/Green_Slime/Run.png')
area_grid = [
  ['area1', 'area2'],
  ['area3', 'area4']
]
# Define tilesets for different areas
tilesets = {
    'area1': './tileset/1 Tiles/FieldsTile_01.png',
    'area2': './tileset/1 Tiles/FieldsTile_02.png',
    'area3': './tileset/1 Tiles/FieldsTile_03.png',
    'area4': './tileset/1 Tiles/FieldsTile_04.png'
}

# Load initial tileset
# current_area = 'area1'
# tileset = pygame.image.load(tilesets[window_screen.current_area])
# tile_width, tile_height = tileset.get_size()

# Load house image and scale it
house_image = pygame.image.load('./tileset/2 Objects/7 House/3.png')
house_width, house_height = house_image.get_size()
scaled_house_width = house_width * 2  # Adjust the scaling factor as needed
scaled_house_height = house_height * 2  # Adjust the scaling factor as needed
house_image = pygame.transform.scale(house_image, (scaled_house_width, scaled_house_height))

# Create a mask for the house image
house_mask = pygame.mask.from_surface(house_image)

# Define house position (top right corner of area1)
house_x = window_screen.width - scaled_house_width  # Adjust the position as needed
house_y = 0  # Adjust the position as needed

rock_images = [pygame.image.load(f'./tileset/2 Objects/2 Stone/{i}.png') for i in range(1, 7)]
rock_width, rock_height = rock_images[0].get_size()
scaled_rock_width = rock_width * 4  # Adjust the scaling factor as needed
scaled_rock_height = rock_height * 4  # Adjust the scaling factor as needed


rock_positions = {
    'area1': [],
    'area2': [],
    'area3': [],
    'area4': []
}
rock_masks = {
    'area1': [],
    'area2': [],
    'area3': [],
    'area4': []
}

def initialize_rocks(wdw_screen: Screen, area, top: bool = False, bottom: bool = False, left: bool = False, right: bool = False):
    global rock_positions, rock_masks
    rock_positions[area] = []

    if area not in wdw_screen.collidable_positions:
        wdw_screen.collidable_positions[area] = []
    rock_masks[area] = []
    scaled_rock_width = rock_width * 4
    scaled_rock_height = rock_height * 4
    
    # Store positions and masks for rocks along the left border
    if left:
        for y in range(0, window_screen.height, scaled_rock_height):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, 0, y))
            wdw_screen.collidable_positions[area].append((rock_image, 0, y))
            rock_masks[area].append(pygame.mask.from_surface(rock_image))
    
    # Store positions and masks for rocks along the right border
    if right:
        for y in range(0, window_screen.height, scaled_rock_height):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, window_screen.width - scaled_rock_width, y))
            rock_masks[area].append(pygame.mask.from_surface(rock_image))
    
    # Store positions and masks for rocks along the top border
    if top:
        for x in range(0, window_screen.width, scaled_rock_width):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, x, 0))
            rock_positions[area].append((rock_image, x, 0))
            rock_masks[area].append(pygame.mask.from_surface(rock_image))
    
    # Store positions and masks for rocks along the bottom border
    if bottom:
        for x in range(0, window_screen.width, scaled_rock_width):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, x, window_screen.height - scaled_rock_height))
            rock_positions[area].append((rock_image, x, window_screen.height - scaled_rock_height))
            rock_masks[area].append(pygame.mask.from_surface(rock_image))

def draw_rocks(area, debug=False):
    for rock_image, rock_x, rock_y in rock_positions[area]:
        window_screen.screen.blit(rock_image, (rock_x, rock_y))
        rock_rect = pygame.Rect(rock_x, rock_y, rock_image.get_width(), rock_image.get_height())
        if debug:
          pygame.draw.rect(window_screen.screen, (255, 0, 0), rock_rect, 2)  # Red color with a thickness of 2

# Initialize rocks for area1
initialize_rocks(window_screen, 'area1', top=True, left=True)
initialize_rocks(window_screen, 'area2', top=True, right=True)
initialize_rocks(window_screen, 'area3', bottom=True, left=True)
initialize_rocks(window_screen, 'area4', bottom=True, right=True)

def check_collisions(character_rect: pygame.Rect, area):
    for rock_image, rock_x, rock_y in rock_positions[area]:
        rock_rect = pygame.Rect(rock_x, rock_y, rock_image.get_width(), rock_image.get_height())
        if character_rect.colliderect(rock_rect):
            return True
    return False

# def check_collisions(character_rect: pygame.Rect, area):
#     for rock_image, rock_x, rock_y in rock_positions[area]:
#         rock_rect = pygame.Rect(rock_x, rock_y, rock_image.get_width(), rock_image.get_height())
#         if character_rect.colliderect(rock_rect):
#             return True
#     return False

# def get_character_collision(character_x, character_y) -> pygame.Rect:
#     shift_amount = character.width // 2
#     character_rect = pygame.Rect(
#         character_x + (character.width - character.width * 3 // 4) // 2 - shift_amount, 
#         character_y + (character.height - character.height * 2 // 3) // 2, 
#         character.width * 3 // 4, 
#         character.height * 3 // 4
#     )
#     return character_rect

# def draw_character_with_collision(character_x, character_y):
#     # Draw the character
#     character_rect = get_character_collision(character_x, character_y)
#     pygame.draw.rect(window_screen, (0, 255, 0), character_rect, 2)  # Green color with a thickness of 2


# Function to extract frames from sprite sheet
def get_frames(sheet, num_columns, num_rows):
    frames = []
    sheet_width, sheet_height = sheet.get_size()
    frame_width = sheet_width // num_columns
    frame_height = sheet_height // num_rows
    print(f"Sprite sheet size: {sheet_width}x{sheet_height}")
    print(f"Frame size: {frame_width}x{frame_height}")
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            if x + frame_width <= sheet_width and y + frame_height <= sheet_height:
                frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
                frames.append(frame)
                print(f"Extracted frame at ({x}, {y}) with size {frame_width}x{frame_height}")
            else:
                print(f"Skipping frame at ({x}, {y}) - outside surface area")
    return frames


# Extract frames from sprite sheet
character_frames = get_frames(sprite_sheet, 7, 1)
frames = [character_frames[0], character_frames[1], character_frames[2], character_frames[1]]  # Keep frames 0, 1, 2, and 1

reversed_frames = [pygame.transform.flip(frame, True, False) for frame in frames]
# current_frame = 0
# frame_count = len(frames)

# Create masks for each frame
character_masks = [pygame.mask.from_surface(frame) for frame in frames]
reversed_character_masks = [pygame.mask.from_surface(frame) for frame in reversed_frames]

# Character starting position (below the house)
# character_x = house_x + scaled_house_width // 2 - character.width // 2
character_x = house_x + scaled_house_width // 2
character_y = house_y + scaled_house_height + 10  # Adjust the offset as needed
character = Character(
    position_x=character_x,
    position_y=character_y,
    frames=frames
)


# Load accessories
accessories = ['./accessories/1 Icons/Icon30_01.png', './accessories/1 Icons/Icon30_02.png', './accessories/1 Icons/Icon30_03.png']
current_accessory_index = 0
accessory_image = pygame.image.load(accessories[current_accessory_index])
accessory_width, accessory_height = accessory_image.get_size()
scaled_accessory_width = accessory_width * 2  # Adjust the scaling factor as needed
scaled_accessory_height = accessory_height * 2  # Adjust the scaling factor as needed
accessory_image = pygame.transform.scale(accessory_image, (scaled_accessory_width, scaled_accessory_height))

# Accessory position relative to the character
accessory_x_offset = (character.width - scaled_accessory_width) // 2
accessory_y_offset = character.height // 2
# Define arrow positions for accessories
arrow_width = 20
arrow_height = 40
left_arrow_x = window_screen.width // 2 - character.width // 2 - arrow_width - 10
left_arrow_y = window_screen.height // 2 - arrow_height // 2
right_arrow_x = window_screen.width // 2 + character.width // 2 + 10
right_arrow_y = window_screen.height // 2 - arrow_height // 2

# Define arrow points for accessories
left_arrow_points = [(left_arrow_x + arrow_width, left_arrow_y), (left_arrow_x, left_arrow_y + arrow_height // 2), (left_arrow_x + arrow_width, left_arrow_y + arrow_height)]
right_arrow_points = [(right_arrow_x, right_arrow_y), (right_arrow_x + arrow_width, right_arrow_y + arrow_height // 2), (right_arrow_x, right_arrow_y + arrow_height)]

# Define arrow positions for pets
pet_left_arrow_x = left_arrow_x
pet_left_arrow_y = left_arrow_y + arrow_height + 20
pet_right_arrow_x = right_arrow_x
pet_right_arrow_y = right_arrow_y + arrow_height + 20

# Define arrow points for pets
pet_left_arrow_points = [(pet_left_arrow_x + arrow_width, pet_left_arrow_y), (pet_left_arrow_x, pet_left_arrow_y + arrow_height // 2), (pet_left_arrow_x + arrow_width, pet_left_arrow_y + arrow_height)]
pet_right_arrow_points = [(pet_right_arrow_x, pet_right_arrow_y), (pet_right_arrow_x + arrow_width, pet_right_arrow_y + arrow_height // 2), (pet_right_arrow_x, pet_right_arrow_y + arrow_height)]

pets = ['./slime_pet/PNG/Slime1/Walk/Slime1_Walk_body.png', './slime_pet/PNG/Slime2/Walk/Slime2_Walk_body.png', './slime_pet/PNG/Slime3/Walk/Slime3_Walk_body.png']
pets_frames = [get_frames(pygame.image.load(pet), 8, 4) for pet in pets]
current_pet_index = 0
pet_frames = pets_frames[current_pet_index]
reversed_pet_frames = [pygame.transform.flip(frame, True, False) for frame in pet_frames]
pet_image = pet_frames[0]
pet_width, pet_height = pet_image.get_size()
hat_added = False
pet_added = False
scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))


def character_creation_screen():
    """Character creation screen"""
    creation_running = True
    global hat_added, pet_added, pet_frames, pet_image
    global current_accessory_index, accessory_image, accessory_x_offset, accessory_y_offset
    global current_pet_index, pet_image
    positions = window_screen.initialize_random_tilesets()
    while creation_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # it is best practice to use event.type to check for non-continuous pressing of keys
            # so things outside of movement etc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    creation_running = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # Change accessory with right arrow key
                    current_accessory_index = (current_accessory_index + 1) % len(accessories)
                    accessory_image = pygame.image.load(accessories[current_accessory_index])
                    accessory_width, accessory_height = accessory_image.get_size()
                    scaled_accessory_width = accessory_width * 2  # Adjust the scaling factor as needed
                    scaled_accessory_height = accessory_height * 2  # Adjust the scaling factor as needed
                    accessory_image = pygame.transform.scale(accessory_image, (scaled_accessory_width, scaled_accessory_height))
                    accessory_x_offset = (character.width - scaled_accessory_width) // 2
                    accessory_y_offset = character.height // 2
                    hat_added = True
                    # scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    # scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    # pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))

                    # pet_added = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  # Change accessory with left arrow key
                  current_accessory_index = (current_accessory_index - 1) % len(accessories)
                  accessory_image = pygame.image.load(accessories[current_accessory_index])
                  accessory_width, accessory_height = accessory_image.get_size()
                  scaled_accessory_width = accessory_width * 2  # Adjust the scaling factor as needed
                  scaled_accessory_height = accessory_height * 2  # Adjust the scaling factor as needed
                  accessory_image = pygame.transform.scale(accessory_image, (scaled_accessory_width, scaled_accessory_height))
                  accessory_x_offset = (character.width - scaled_accessory_width) // 2
                  accessory_y_offset = character.height // 2
                  hat_added = True
                  # pet_width, pet_height = pet_image.get_size()
                  # scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                  # scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Change pet with down arrow key
                    current_pet_index = (current_pet_index - 1) % len(pets)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Change pet with up arrow key
                    current_pet_index = (current_pet_index + 1) % len(pets)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (left_arrow_x <= mouse_x <= left_arrow_x + arrow_width and
                        left_arrow_y <= mouse_y <= left_arrow_y + arrow_height):
                    current_accessory_index = (current_accessory_index - 1) % len(accessories)
                    accessory_image = pygame.image.load(accessories[current_accessory_index])
                    accessory_width, accessory_height = accessory_image.get_size()
                    scaled_accessory_width = accessory_width * 2  # Adjust the scaling factor as needed
                    scaled_accessory_height = accessory_height * 2  # Adjust the scaling factor as needed
                    accessory_image = pygame.transform.scale(accessory_image, (scaled_accessory_width, scaled_accessory_height))
                    accessory_x_offset = (character.width - scaled_accessory_width) // 2
                    accessory_y_offset = character.height // 2
                    hat_added = True
                elif (right_arrow_x <= mouse_x <= right_arrow_x + arrow_width and
                        right_arrow_y <= mouse_y <= right_arrow_y + arrow_height):
                    current_accessory_index = (current_accessory_index + 1) % len(accessories)
                    accessory_image = pygame.image.load(accessories[current_accessory_index])
                    accessory_width, accessory_height = accessory_image.get_size()
                    scaled_accessory_width = accessory_width * 2  # Adjust the scaling factor as needed
                    scaled_accessory_height = accessory_height * 2  # Adjust the scaling factor as needed
                    accessory_image = pygame.transform.scale(accessory_image, (scaled_accessory_width, scaled_accessory_height))
                    accessory_x_offset = (character.width - scaled_accessory_width) // 2
                    accessory_y_offset = character.height // 2
                    hat_added = True
                elif (pet_left_arrow_x <= mouse_x <= pet_left_arrow_x + arrow_width and
                        pet_left_arrow_y <= mouse_y <= pet_left_arrow_y + arrow_height):
                    current_pet_index = (current_pet_index - 1) % len(pets)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
                    
                    
                elif (pet_right_arrow_x <= mouse_x <= pet_right_arrow_x + arrow_width and
                        pet_right_arrow_y <= mouse_y <= pet_right_arrow_y + arrow_height):
                    current_pet_index = (current_pet_index + 1) % len(pets)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
                else:
                    print("No arrow clicked")

        # tileset = pygame.image.load(tilesets[current_area])
        window_screen.draw_tilesets(positions)
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to start the game", True, BLACK)
        window_screen.screen.blit(text, (window_screen.width // 2 - text.get_width() // 2, 10))

        # Draw the accessory if added
        if hat_added:
            window_screen.screen.blit(accessory_image, (window_screen.width // 2 - character.width // 2 + accessory_x_offset, window_screen.height // 2 - character.height // 2 + accessory_y_offset))
        # Draw the pet if added
        if pet_added:
            window_screen.screen.blit(pet_image, (window_screen.width // 2 - character.width // 2 + accessory_x_offset, window_screen.height // 2 - character.height // 2 + accessory_y_offset + 50))
        # Draw the character
        window_screen.screen.blit(character.frames[0], (window_screen.width // 2 - character.width // 2, window_screen.height // 2 - character.height // 2))

        pygame.draw.polygon(window_screen.screen, ARROW_COLOR, left_arrow_points)
        pygame.draw.polygon(window_screen.screen, ARROW_COLOR, right_arrow_points)
        pygame.draw.polygon(window_screen.screen, ARROW_COLOR, pet_left_arrow_points)
        pygame.draw.polygon(window_screen.screen, ARROW_COLOR, pet_right_arrow_points)

        accessories_text = font.render("Accessories", True, BLACK)
        pets_text = font.render("Pets", True, BLACK)
        window_screen.screen.blit(accessories_text, (left_arrow_points[0][0] - accessories_text.get_width() - 20, left_arrow_points[0][1] - accessories_text.get_height() // 2))
        window_screen.screen.blit(pets_text, (pet_left_arrow_points[0][0] - pets_text.get_width() - 20, pet_left_arrow_points[0][1] - pets_text.get_height() // 2))


        pygame.display.flip()

# Show the character creation screen
character_creation_screen()

def get_movement(keys):
    global MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN
    MOVE_LEFT = keys[pygame.K_LEFT] or keys[pygame.K_a]
    MOVE_RIGHT = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    MOVE_UP = keys[pygame.K_UP] or keys[pygame.K_w]
    MOVE_DOWN = keys[pygame.K_DOWN] or keys[pygame.K_s]
    return MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN, MOVE_UP

# Main game loop
running = True
clock = pygame.time.Clock()
animation_counter = 0
animation_speed = 10  # Adjust this value to control the animation speed
moving_left = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Get the keys pressed
    keys = pygame.key.get_pressed()
    MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN, MOVE_UP = get_movement(keys)
    
    # Move the character
    moved = False
    new_character_x = character_x
    new_character_y = character_y
    # new_character_x = character.position_x
    # new_character_y = character.position_y

    # Select the correct mask for the current frame
    # if moving_left:
    #     character_mask = reversed_character_masks[character.current_frame]
    # else:
    #     character_mask = character_masks[character.current_frame]

    # Check for pixel-perfect collisions with the house
    # character.position_x = character_x
    # character.position_y = character_y
    character_x, character_y, moving_left, moved, animation_counter  = character.move(
        # character.position_x,
        # character.position_y,
        new_character_x,
        new_character_y,
        window_screen,
        MOVE_LEFT,
        MOVE_RIGHT,
        MOVE_UP,
        MOVE_DOWN
        # current_frame,
        # animation_counter
    )
    # window_screen.load_location(
    #   character
    # )
    character_x, character_y = window_screen.load_location(character, character_x, character_y)
    
    window_screen.fill_tileset(window_screen.tileset)

    # Draw the house in area1
    draw_rocks(window_screen.current_area, debug)
    if window_screen.current_area == 'area1':
        window_screen.screen.blit(house_image, (house_x, house_y))

    if debug:
    #   draw_character_with_collision(character_x, character_y)
      character.draw_collision(window_screen.screen)
    #   draw_character_with_collision(character_x, character_y)
    if hat_added:
        window_screen.screen.blit(accessory_image, (character.position_x - character.width // 2 + accessory_x_offset, character.position_y - character.height // 2 + accessory_y_offset))
    if pet_added:
        # screen.screen.blit(pet_image, (character.position_x - character.width // 2 + accessory_x_offset, character_y - character.height // 2 + accessory_y_offset + 50))
        window_screen.screen.blit(pet_frames[character.current_frame], (character.position_x - character.width // 2 + accessory_x_offset, character.position_y - character.height // 2 + accessory_y_offset + 50))
    # Draw the character
    if moving_left:
        window_screen.screen.blit(reversed_frames[character.current_frame], (character.position_x - character.width // 2, character.position_y - character.height // 2))
        if pet_added:
          window_screen.screen.blit(pet_frames[character.current_frame], (character.position_x - character.width // 2 + accessory_x_offset, character.position_y - character.height // 2 + accessory_y_offset + 50))
    else:
        window_screen.screen.blit(character.frames[character.current_frame], (character.position_x - character.width // 2, character.position_y - character.height // 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()