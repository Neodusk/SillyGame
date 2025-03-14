import pygame
import sys
from game_objects import Screen, Character, Pet, Accessory

ACCESSORIES = [
    './accessories/1 Icons/Icon30_01.png',
    './accessories/1 Icons/Icon30_02.png',
    './accessories/1 Icons/Icon30_03.png'
]

PETS = [
    './slime_pet/PNG/Slime1/Walk/Slime1_Walk_body.png',
    './slime_pet/PNG/Slime2/Walk/Slime2_Walk_body.png',
    './slime_pet/PNG/Slime3/Walk/Slime3_Walk_body.png'
]


def load_accessories(current_accessory_index):
    # current_accessory_index = 0
    accessory_image = pygame.image.load(ACCESSORIES[current_accessory_index])
    accessory_width, accessory_height = accessory_image.get_size()
    scaled_accessory_width = accessory_width * 2  # Adjust the scaling factor as needed
    scaled_accessory_height = accessory_height * 2  # Adjust the scaling factor as needed
    accessory_image = pygame.transform.scale(accessory_image, (scaled_accessory_width, scaled_accessory_height))
    return accessory_image, scaled_accessory_width, scaled_accessory_height

def get_next_menu_item(current_index, list_items):
    return (current_index + 1) % len(list_items)

def get_next_accessory(current_index):
    return get_next_menu_item(current_index, ACCESSORIES)

def get_next_pet(current_index):
    return get_next_menu_item(current_index, PETS)

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