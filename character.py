"""Class for character objects"""
import pygame
import random

class Screen:
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.area_grid = [
            ['area1', 'area2'],
            ['area3', 'area4']
        ]
        self.tilesets = {
            'area1': './tileset/1 Tiles/FieldsTile_01.png',
            'area2': './tileset/1 Tiles/FieldsTile_02.png',
            'area3': './tileset/1 Tiles/FieldsTile_03.png',
            'area4': './tileset/1 Tiles/FieldsTile_04.png'
        }
        self.collidable_positions = {
            'area1': [],
            'area2': [],
            'area3': [],
            'area4': []
        }
        self.current_area = "area1"
        self.tileset = pygame.image.load(self.tilesets[self.current_area])
        self.tile_width, self.tile_height = self.tileset.get_size()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Silly Wittle Game")

    def load_tileset(self, tileset):
        """Load the tileset"""
        if not tileset:
            print(f"No tileset provided, defaulting to {self.tileset}")
            tileset = self.tileset
        self.tileset = pygame.image.load(tileset)
        self.tile_width, self.tile_height = self.tileset.get_size()

    def fill_tileset(self, tileset):
        """Fill the screen with the given tileset"""
        tile_width, tile_height = self.tileset.get_size()
        for y in range(0, self.height, tile_height):
            for x in range(0, self.width, tile_width):
                self.screen.blit(tileset, (x, y))

    def add_to_area_grid(self, area):
        """Add an area to the grid"""
        self.area_grid.append(area)
    
    def replace_area_grid(self, area):
        """Replace the area grid with a new grid"""
        self.area_grid = area

    def set_current_area(self, row, column):
        """Set the current area""" 
        self.current_area = self.area_grid[row][column]
    
    def find_area_coordinates(self, area = None):
        """Find the coordinates of the area in the grid"""
        if area is None:
            area = self.current_area
        for row_index, row in enumerate(self.area_grid):
            if area in row:
                return row_index, row.index(area)
        return None, None

    def load_current_area(self):
        """Load the Screen with the current area"""
        self.tileset = pygame.image.load(self.tilesets[self.current_area])
        # print(f"Loading {self.current_area} tileset")
        self.tile_width, self.tile_height = self.tileset.get_size()

    def load_location(self, character: "Character", character_x, character_y):
        """Load the location of the character on the screen"""
        # Check if the character has reached the edge of the current area
        # character_x = character.position_x
        # character_y = character.position_y
        character_height = character.height
        row, col = self.find_area_coordinates()
        if row is None or col is None:
            raise ValueError("Area not found in the grid")

        # Check if the character has reached the edge of the current area
        if character_x < 0:
            col -= 1
            if col < 0:
                col = len(self.area_grid[0]) - 1
            character_x = self.width - character.width
        elif character_x > self.width - character.width:
            col += 1
            if col >= len(self.area_grid[0]):
                col = 0
            character_x = 0
        elif character_y < 0:
            row -= 1
            if row < 0:
                row = len(self.area_grid) - 1
            character_y = self.height - character_height
        elif character_y > self.height - character_height:
            row += 1
            if row >= len(self.area_grid):
                row = 0
            character_y = 0
        self.set_current_area(row, col)
        self.load_current_area()
        return character_x, character_y

    def initialize_random_tilesets(self, tilesets = None):
        """Initialize random tilesets"""
        if not tilesets:
            tilesets = self.tilesets
        # todo: tileset load shouldnt be static
        sample_tileset = pygame.image.load(tilesets["area1"])
        tile_width, tile_height = sample_tileset.get_size()
        positions = []
        for y in range(0, self.height, tile_height):
            for x in range(0, self.width, tile_width):
                random_tileset = random.choice(list(tilesets.values()))
                random_tileset = pygame.image.load(random_tileset)
                positions.append((random_tileset, x, y))
        return positions

    def draw_tilesets(self, positions):
        """Draw the tilesets at positions"""
        for tileset, position_x, position_y in positions:
            self.screen.blit(tileset, (position_x, position_y))

        
class GameObject:
    """Base class for game objects with common attributes"""
    def __init__(self, height, width, image, current_frame, frames, animation_speed, animation_counter, rectangle, position_x, position_y, speed):
        self.height = height
        self.width = width
        self.image = image
        self.current_frame = current_frame
        self.frames = frames
        self.animation_counter = animation_counter
        self.animation_speed = animation_speed
        self.rectangle = rectangle
        self.position_x = position_x
        self.position_y = position_y
        self.speed = speed
    
    def get_collision(self, position_x = None, position_y = None):
        """Get the collision of the object"""
        shift_amount = self.width // 2
        if not position_x:
            position_x = self.position_x
        if not position_y:
            position_y = self.position_y
        character_rect = pygame.Rect(
            position_x + (self.width - self.width * 3 // 4) // 2 - shift_amount, 
            position_y + (self.height - self.height * 2 // 3) // 2, 
            self.width * 3 // 4,
            self.height * 3 // 4
        )
        return character_rect

    def set_collision(self, rectangle = None):
        """Set the collision of the object"""
        if not rectangle:
            self.rectangle = self.get_collision()
        self.rectangle = rectangle

    def draw_collision(self, screen):
        """Draw the collision of the object"""
        character_rect = self.get_collision()
        pygame.draw.rect(screen, (255, 0, 0), character_rect, 2)

    def check_collisions(self, window_screen: Screen):
        """Check for collisions with the screen objects"""
        for collision_image, position_x, position_y in window_screen.collidable_positions[window_screen.current_area]:
            collision_rect = pygame.Rect(
                position_x,
                position_y,
                collision_image.get_width(),
                collision_image.get_height()
            )
            # rectangle = self.get_collision()
            if self.rectangle.colliderect(collision_rect):
                return True
    
    def set_image(self, image = None):
        if not image:
            if self.frames is not None:
                self.image = self.frames[self.current_frame]

    def move(self, new_position_x, new_position_y, window_screen: Screen, MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN):
        moved = False
        moving_left = False
        position_x = new_position_x
        position_y = new_position_y
        # self.position_x = new_position_x
        # self.position_y = new_position_y
        character_rect = self.get_collision(new_position_x, new_position_y)
        self.set_collision(character_rect)

        
        if MOVE_LEFT:
            new_position_x -= self.speed
            self.rectangle.x = new_position_x - self.width // 2
            self.set_collision(character_rect)
            if not self.check_collisions(window_screen):
                # character_x = new_position_x
                self.position_x = new_position_x
                position_x = new_position_x
                moved = True
                moving_left = True
            else:
                print("Collision detected")
                
        if MOVE_RIGHT:
            new_position_x += self.speed
            self.rectangle.x = new_position_x
            self.set_collision(character_rect)
            if not self.check_collisions(window_screen):
                # character_x = new_position_x
                self.position_x = new_position_x
                position_x = new_position_x
                moved = True
                moving_left = False
            else:
                print("Collision detected")
        if MOVE_UP:
            new_position_y -= self.speed
            self.rectangle.y = new_position_y 
            self.set_collision(character_rect)
            if not self.check_collisions(window_screen):
                # character_y = new_position_y
                position_y = new_position_y
                self.position_y = new_position_y
                moved = True
                moving_left = False
            else:
                print("Collision detected")
        if MOVE_DOWN:
            new_position_y += self.speed
            self.rectangle.y = new_position_y
            self.set_collision(character_rect)
            if not self.check_collisions(window_screen):
                self.position_y = new_position_y
                position_y = new_position_y
                moved = True
                moving_left = False
                print("Moving down")
            else:
                print("Collision detected")

        # Update the frame only if moved left or right
        if moved and (MOVE_LEFT or MOVE_RIGHT):
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.animation_counter = 0
        
        return position_x, position_y, moving_left, moved, self.animation_counter

    def __post_init__(self):
        self.set_collision()
        self.set_image()


class Pet(GameObject):
    """Class for pet objects"""
    # inherit from the GameObject class
    pass
    # def __init__(self, height, width, image, frames, position):
    #     super().__init__(height, width, image, frames, position)

class Accessory(GameObject):
    """Class for accessory objects"""
    # inherit from the GameObject class
    pass


class Character(GameObject):
    """Class for character"""
    def __init__(
        self,
        height = 128,
        width = 112,
        image = None,
        current_frame = 0,
        frames = None,
        animation_speed = 10,
        animation_counter = 0,
        rectangle = None,
        position_x = 0,
        position_y = 0,
        speed = 5,
        accessory: Accessory = None,
        pet: Pet = None
        ):
        # pylint: disable=too-many-function-args
        super().__init__(
            height,
            width,
            image,
            current_frame,
            frames,
            animation_speed,
            animation_counter,
            rectangle,
            position_x,
            position_y,
            speed
        )
        self.accessory = accessory
        self.pet = pet

    def set_accessory(self, accessory):
        """Set the accessories of the character"""
        self.accessory = accessory

    def set_pet(self, pet):
        """Set the pet of the character"""
        self.pet = pet

    def get_accessory(self):
        """Get the accessories of the character"""
        return self.accessory

    def get_pet(self):
        """Get the pet for the character"""
        return self.pet
