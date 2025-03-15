import pygame
import sys
import random
from creation_screen import character_creation_screen
from assets import get_frames
from game_objects import Screen, Character

# Initialize pygame
pygame.init()

window_screen = Screen(1920, 1080)


MOVE_LEFT = 0
MOVE_RIGHT = 0
MOVE_UP = 0
MOVE_DOWN = 0


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


rock_positions = {
    'area1': [],
    'area2': [],
    'area3': [],
    'area4': []
}


# TODO: We need to get the actual range of positions of the rocks somehow
def combine_rock_tiles(rock_positions, width, height):
    """Combine rock tiles into a single surface"""
    combined_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for rock_image, rock_x, rock_y in rock_positions:
        combined_surface.blit(rock_image, (rock_x, rock_y))
    return combined_surface

def initialize_rocks(wdw_screen: Screen, area, top: bool = False, bottom: bool = False, left: bool = False, right: bool = False):
    """Set up the rocks for the given area"""
    rock_images = [pygame.image.load(f'./tileset/2 Objects/2 Stone/{i}.png') for i in range(1, 7)]
    rock_width, rock_height = rock_images[0].get_size()
    global rock_positions
    rock_positions[area] = []

    if area not in wdw_screen.collidable_positions:
        wdw_screen.collidable_positions[area] = []
    scaled_rock_width = rock_width * 4
    scaled_rock_height = rock_height * 4
    
     # Store positions and masks for rocks along the left border
    if left:
        for y in range(0, window_screen.height, scaled_rock_height):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, 0, y))
            wdw_screen.collidable_positions[area].append((rock_image, 0, y))
    
    # Store positions and masks for rocks along the right border
    if right:
        for y in range(0, window_screen.height, scaled_rock_height):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, window_screen.width - scaled_rock_width, y))
            wdw_screen.collidable_positions[area].append((rock_image, window_screen.width - scaled_rock_width, y))
    # Store positions and masks for rocks along the top border
    if top:
        for x in range(0, window_screen.width, scaled_rock_width):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, x, 0))
            wdw_screen.collidable_positions[area].append((rock_image, x, 0))
    # Store positions and masks for rocks along the bottom border
    if bottom:
        for x in range(0, window_screen.width, scaled_rock_width):
            rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
            rock_positions[area].append((rock_image, x, window_screen.height - scaled_rock_height))
            wdw_screen.collidable_positions[area].append((rock_image, x, window_screen.height - scaled_rock_height))

    # Combine rock tiles into a single surface
    combined_surface = combine_rock_tiles(rock_positions[area], window_screen.width, window_screen.height)
    combined_mask = pygame.mask.from_surface(combined_surface)
    wdw_screen.collidable_positions[area] = [(combined_surface, 0, 0, combined_mask)]
    
    # # Store positions and masks for rocks along the left border
    # if left:
    #     for y in range(0, window_screen.height, scaled_rock_height):
    #         rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
    #         rock_positions[area].append((rock_image, 0, y))
    #         wdw_screen.collidable_positions[area].append((rock_image, 0, y))
    
    # # Store positions and masks for rocks along the right border
    # if right:
    #     for y in range(0, window_screen.height, scaled_rock_height):
    #         rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
    #         rock_positions[area].append((rock_image, window_screen.width - scaled_rock_width, y))
    #         wdw_screen.collidable_positions[area].append((rock_image, window_screen.width - scaled_rock_width, y))
    # # Store positions and masks for rocks along the top border
    # if top:
    #     for x in range(0, window_screen.width, scaled_rock_width):
    #         rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
    #         rock_positions[area].append((rock_image, x, 0))
    #         wdw_screen.collidable_positions[area].append((rock_image, x, 0))
    # # Store positions and masks for rocks along the bottom border
    # if bottom:
    #     for x in range(0, window_screen.width, scaled_rock_width):
    #         rock_image = pygame.transform.scale(random.choice(rock_images), (scaled_rock_width, scaled_rock_height))
    #         rock_positions[area].append((rock_image, x, window_screen.height - scaled_rock_height))
    #         wdw_screen.collidable_positions[area].append((rock_image, x, window_screen.height - scaled_rock_height))

def draw_rocks(area: str):
    """Draw the rocks on the screen"""
    for rock_image, rock_x, rock_y in rock_positions[area]:
        window_screen.screen.blit(rock_image, (rock_x, rock_y))

# Initialize rocks for area1
initialize_rocks(window_screen, 'area1', top=True, left=True)
initialize_rocks(window_screen, 'area2', top=True, right=True)
initialize_rocks(window_screen, 'area3', bottom=True, left=True)
initialize_rocks(window_screen, 'area4', bottom=True, right=True)


sprite_sheet = pygame.image.load('./slimes/Green_Slime/Run.png')
# Extract frames from sprite sheet
character_frames = get_frames(sprite_sheet, 7, 1)
frames = [character_frames[0], character_frames[1], character_frames[2], character_frames[1]]  # Keep frames 0, 1, 2, and 1
character_x = house_x + scaled_house_width // 2
character_y = house_y + scaled_house_height + 10  # Adjust the offset as needed
character = Character(
    position_x=character_x,
    position_y=character_y,
    frames=frames
)


# Show the character creation screen
character_creation_screen(character, window_screen)

def get_movement(keys):
    """Get movement directions based on key presses."""
    global MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN
    MOVE_LEFT = keys[pygame.K_LEFT] or keys[pygame.K_a]
    MOVE_RIGHT = keys[pygame.K_RIGHT] or keys[pygame.K_d]
    MOVE_UP = keys[pygame.K_UP] or keys[pygame.K_w]
    MOVE_DOWN = keys[pygame.K_DOWN] or keys[pygame.K_s]
    return MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN, MOVE_UP

# Main game loop
GAME_RUNNING = True
clock = pygame.time.Clock()
while GAME_RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_RUNNING = False
    # Get the keys pressed
    keys = pygame.key.get_pressed()
    MOVE_LEFT, MOVE_RIGHT, MOVE_DOWN, MOVE_UP = get_movement(keys)

    # Move the character
    new_character_x = character_x
    new_character_y = character_y

    character.move(
        new_character_x,
        new_character_y,
        window_screen,
        MOVE_LEFT,
        MOVE_RIGHT,
        MOVE_UP,
        MOVE_DOWN
    )
    character_x, character_y = window_screen.load_location(character)

    window_screen.fill_tileset(window_screen.tileset)

    # Draw the house in area1
    draw_rocks(window_screen.current_area)
    if window_screen.current_area == 'area1':
        window_screen.screen.blit(house_image, (house_x, house_y))

    if character.get_accessory():
        window_screen.screen.blit(
            character.get_accessory().image,
            (character.position_x - character.width // 2 + character.get_accessory().position_x, character.position_y - character.height // 2 + character.get_accessory().position_y)
        )
    if character.get_pet():
        window_screen.screen.blit(
            character.get_pet().frames[character.current_frame],
            (character.position_x - character.width // 2 + character.get_accessory().position_x, character.position_y - character.height // 2 + character.get_accessory().position_y + 50)
        )
        
    window_screen.screen.blit(
        character.frames[character.current_frame],
        (character.position_x - character.width // 2, character.position_y - character.height // 2)
    )

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
sys.exit()