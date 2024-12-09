from frontend.menu import *
from frontend.button import *
from frontend.pve_mode import *

import pygame
import sys
import math

WIDTH, HEIGHT = 1600, 900

# Colors
TERRAIN_COLOR_TOP_BOTTOM = (0, 120, 200)  # Darker at the top and bottom
TERRAIN_COLOR_MIDDLE = (0, 151, 239)     # Lighter at the center
SLOT_COLOR = (77, 186, 238)              # Slot color

pygame.init()
pygame.display.set_caption("Pokémon Card Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))




def main():
    colors = (0, 0, 0)
    menu = MainMenu(screen, colors)
    current_screen = menu
    
    clock = pygame.time.Clock()
    time_elapsed = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            current_screen.handle_events(event)
        
        current_screen.draw()

        if isinstance(current_screen, MainMenu):
            continue
        elif isinstance(current_screen, PVEGame):
            current_screen = PVEGame(screen)
        # Add more checks for other game modes/screens like PVP, DeckBuilder, etc.

        # Update time for pulse effect

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
