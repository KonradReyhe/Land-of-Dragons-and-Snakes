import pygame
import os

# Initialize pygame
pygame.init()

# Create assets/items directory if it doesn't exist
os.makedirs("assets/items", exist_ok=True)

# Define items and their colors
items = {
    "mysterious_scroll": (200, 150, 100),  # Brown
    "enchanted_coin": (255, 215, 0),      # Gold
    "blindfold": (100, 100, 100)          # Gray
}

# Create a 64x64 surface for each item
for item_id, color in items.items():
    surface = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Draw a simple shape based on the item
    if item_id == "mysterious_scroll":
        # Draw a scroll shape
        pygame.draw.rect(surface, color, (10, 20, 44, 24))
        pygame.draw.rect(surface, color, (5, 15, 54, 34))
    elif item_id == "enchanted_coin":
        # Draw a coin shape
        pygame.draw.circle(surface, color, (32, 32), 25)
        pygame.draw.circle(surface, (255, 255, 0), (32, 32), 20)
    else:  # blindfold
        # Draw a blindfold shape
        pygame.draw.rect(surface, color, (10, 20, 44, 24))
        pygame.draw.rect(surface, (0, 0, 0), (10, 20, 44, 8))
    
    # Save the image
    pygame.image.save(surface, f"assets/items/{item_id}.png")

print("Created placeholder images for marketplace items!") 