import pygame
import sys
from game_objects import Screen, Character, Pet, Accessory
from assets import get_frames, load_accessories, get_next_accessory, get_next_pet


def character_creation_screen(character: Character, window_screen: Screen):
    """Character creation screen"""
    # Colors
    BLACK = (0, 0, 0)
    ARROW_COLOR = (0, 0, 0)  # Color for the arrows
    
    # accessories = ['./accessories/1 Icons/Icon30_01.png', './accessories/1 Icons/Icon30_02.png', './accessories/1 Icons/Icon30_03.png']
    current_accessory_index = 0
    accessory_image, scaled_accessory_width, scaled_accessory_height = load_accessories(current_accessory_index)

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
    pet_image = pet_frames[0]
    pet_width, pet_height = pet_image.get_size()
    # hat_added = False
    # pet_added = False
    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed

    
    
    
    creation_running = True
    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
    pet_added = False
    hat_added = False
    positions = window_screen.initialize_random_tilesets()
    pet = None
    accesory = None
    while creation_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # it is best practice to use event.type to check for non-continuous pressing of keys
            # so things outside of movement etc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(pet)
                    character.set_pet(pet)
                    character.set_accessory(accesory)
                    creation_running = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # Change accessory with right arrow key
                    current_accessory_index = get_next_accessory(current_accessory_index)
                    accessory_image, scaled_accessory_width, scaled_accessory_height = load_accessories(current_accessory_index)
                    accessory_x_offset = (character.width - scaled_accessory_width) // 2
                    accessory_y_offset = character.height // 2
                    hat_added = True
                    accesory = Accessory(
                        height=scaled_accessory_height,
                        width=scaled_accessory_width,
                        image=accessory_image,
                        position_x=accessory_x_offset,
                        position_y=accessory_y_offset
                    )

                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                  # Change accessory with left arrow key
                  current_accessory_index = get_next_accessory(current_accessory_index)
                  accessory_image, scaled_accessory_width, scaled_accessory_height = load_accessories(current_accessory_index)
                  accessory_x_offset = (character.width - scaled_accessory_width) // 2
                  accessory_y_offset = character.height // 2
                  hat_added = True
                  accesory = Accessory(
                        height=scaled_accessory_height,
                        width=scaled_accessory_width,
                        image=accessory_image,
                        position_x=accessory_x_offset,
                        position_y=accessory_y_offset
                    )
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    # Change pet with down arrow key
                    current_pet_index = get_next_pet(current_pet_index)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
                    pet = Pet(
                        height=scaled_pet_height,
                        width=scaled_pet_width,
                        image=pet_image,
                        frames=pet_frames
                    )
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # Change pet with up arrow key
                    current_pet_index = get_next_pet(current_pet_index)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
                    pet = Pet(
                        height=scaled_pet_height,
                        width=scaled_pet_width,
                        image=pet_image,
                        frames=pet_frames
                    )
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (left_arrow_x <= mouse_x <= left_arrow_x + arrow_width and
                        left_arrow_y <= mouse_y <= left_arrow_y + arrow_height):
                    current_accessory_index = get_next_accessory(current_accessory_index)
                    accessory_image, scaled_accessory_width, scaled_accessory_height = load_accessories(current_accessory_index)
                    accessory_x_offset = (character.width - scaled_accessory_width) // 2
                    accessory_y_offset = character.height // 2
                    hat_added = True
                    accesory = Accessory(
                        height=scaled_accessory_height,
                        width=scaled_accessory_width,
                        image=accessory_image,
                        position_x=accessory_x_offset,
                        position_y=accessory_y_offset
                    )
                elif (right_arrow_x <= mouse_x <= right_arrow_x + arrow_width and
                        right_arrow_y <= mouse_y <= right_arrow_y + arrow_height):
                    current_accessory_index = get_next_accessory(current_accessory_index)
                    accessory_image, scaled_accessory_width, scaled_accessory_height = load_accessories(current_accessory_index)
                    accessory_x_offset = (character.width - scaled_accessory_width) // 2
                    accessory_y_offset = character.height // 2
                    hat_added = True
                    accesory = Accessory(
                        height=scaled_accessory_height,
                        width=scaled_accessory_width,
                        image=accessory_image,
                        position_x=accessory_x_offset,
                        position_y=accessory_y_offset
                    )
                elif (pet_left_arrow_x <= mouse_x <= pet_left_arrow_x + arrow_width and
                        pet_left_arrow_y <= mouse_y <= pet_left_arrow_y + arrow_height):
                    current_pet_index = get_next_pet(current_pet_index)
                    pet_image = pets_frames[current_pet_index][0]  # Use the first frame of the new pet
                    pet_width, pet_height = pet_image.get_size()
                    scaled_pet_width = pet_width * 2  # Adjust the scaling factor as needed
                    scaled_pet_height = pet_height * 2  # Adjust the scaling factor as needed
                    pet_image = pygame.transform.scale(pet_image, (scaled_pet_width, scaled_pet_height))
                    pet_added = True
                    pet_frames = [pygame.transform.scale(frame, (scaled_pet_width, scaled_pet_height)) for frame in pets_frames[current_pet_index]]
                    pet = Pet(
                        height=scaled_pet_height,
                        width=scaled_pet_width,
                        image=pet_image,
                        frames=pet_frames
                    )
                    
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
                    pet = Pet(
                        height=scaled_pet_height,
                        width=scaled_pet_width,
                        image=pet_image,
                        frames=pet_frames
                    )
                else:
                    print("No arrow clicked")

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