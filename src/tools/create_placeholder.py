import pygame

def create_background():
    # Initialize pygame
    pygame.init()
    
    # Create a surface
    width = 1280
    height = 720
    surface = pygame.Surface((width, height))
    
    # Fill with dark color
    surface.fill((20, 20, 30))  # Dark blue-ish color
    
    # Save the image
    pygame.image.save(surface, "assets/images/scene1_background.png")
    
if __name__ == "__main__":
    create_background() 