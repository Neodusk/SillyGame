"""Class for character objects"""
import pygame
import random

class Screen:
    def __init__(self, screen, height, width):
        self.screen = screen
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
        self.current_area = "area1"
        self.tileset = pygame.image.load(self.tilesets[self.current_area])
        self.tile_width, self.tile_height = self.tileset.get_size()
    
    def load_tileset(self, tileset):
        """Load the tileset"""
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

    def initialize_random_tilesets(self, tilesets):
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
        for tileset, position_x, position_y in positions:
            self.screen.blit(tileset, (position_x, position_y))


class GameObject:
    """Base class for game objects with common attributes"""
    def __init__(self, height, width, image, current_frame, frames, rectangle, position, speed):
        self.height = height
        self.width = width
        self.image = image
        self.current_frame = current_frame
        self.frames = frames
        self.rectangle = rectangle
        self.position = position # (x, y)
        self.speed = speed
    
    def get_collision(self):
        """Get the collision of the object"""
        shift_amount = self.width // 2
        position_x = self.position[0]
        position_y = self.position[1]
        character_rect = pygame.Rect(
            position_x + (self.width - self.width * 3 // 4) // 2 - shift_amount, 
            position_y + (self.height - self.height * 2 // 3) // 2, 
            self.width * 3 // 4,
            self.height * 3 // 4
        )
        return character_rect

    def draw_collision(self, screen):
        character_rect = self.get_collision()
        pygame.draw.rect(screen, (255, 0, 0), character_rect, 2)

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
        height,
        width,
        image,
        current_frame,
        frames,
        rectangle,
        position,
        speed,
        accessory: Accessory,
        pet: Pet
        ):
        super().__init__(height, width, image, current_frame, frames, rectangle,  position, speed)
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
