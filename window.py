import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Game Terrain")

# Colors
TERRAIN_COLOR_TOP_BOTTOM = (0, 120, 200)  # Darker at the top and bottom
TERRAIN_COLOR_MIDDLE = (130, 151, 239)     # Lighter at the center
SLOT_COLOR = (77, 186, 238)              # Slot color

# Gradient generation function
def draw_bidirectional_gradient(surface, color_top_bottom, color_middle, rect, pulse_factor):
    mid_y = rect.height // 2
    for y in range(rect.top, rect.bottom):
        # Calculate blend factor
        if y < mid_y:  # Top half gradient
            blend_factor = y / mid_y
        else:  # Bottom half gradient
            blend_factor = (rect.bottom - y) / mid_y
        
        # Adjust middle color brightness with pulse
        adjusted_middle = [
            int(color_middle[i] * (1 - 0.07 * pulse_factor))  # Brightness fluctuates by up to 20%
            for i in range(3)
        ]
        
        # Interpolate colors
        color = [
            int(color_top_bottom[i] + (adjusted_middle[i] - color_top_bottom[i]) * blend_factor)
            for i in range(3)
        ]
        pygame.draw.line(surface, color, (rect.left, y), (rect.right, y))

# Function to draw an image in the slot
def draw_image_in_slot(image_path, slot_rect):
    image = pygame.image.load(image_path)  # Load the image
    # Scale image to be 90% of the slot size (10% smaller)
    new_width = int(slot_rect.width * 0.9)
    new_height = int(slot_rect.height * 0.9)
    image = pygame.transform.scale(image, (new_width, new_height))  # Resize image to fit slot
    # Position the image to be centered in the slot
    image_rect = image.get_rect(center=slot_rect.center)
    screen.blit(image, image_rect.topleft)  # Draw image at the centered position


# Slot dimensions (scaled up)
slot_width = (170 / 1.5) * 1.2 # Increase size by 1.5x
slot_height = (240 / 1.5) * 1.2  # Increase size by 1.5x
slot_margin = 10  # Increased margin between slots (more space between them)
slot_vertical_gap = HEIGHT // 1  # Increase vertical gap

# Check if the bottom slots fit within the screen, adjust if necessary
available_height = HEIGHT - (2 * slot_vertical_gap + slot_height)  # Check available space for bottom cards
if available_height < 0:
    slot_vertical_gap = HEIGHT // 4  # Adjust the gap if necessary

# Main game loop
def main():
    global slot_vertical_gap
    clock = pygame.time.Clock()
    running = True
    time_elapsed = 0  # Track elapsed time for pulsating animation

    # Example image path for card
    card_image_path = "assets/show.png"  # Your image path from upload

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update time for pulse effect
        time_elapsed += clock.get_time() / 1000  # Convert milliseconds to seconds
        pulse_factor = (math.sin(time_elapsed * 2) + 1) / 2  # Oscillates between 0 and 1 smoothly

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw terrain with animated bidirectional gradient
        gradient_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        draw_bidirectional_gradient(screen, TERRAIN_COLOR_TOP_BOTTOM, TERRAIN_COLOR_MIDDLE, gradient_rect, pulse_factor)

        # Calculate center positions
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Draw bottom slots (player)
        y_offset_player = center_y + slot_vertical_gap  # Vertical offset for the player
        for i in range(3):
            x = center_x - 1.5 * slot_width - slot_margin + i * (slot_width + slot_margin)
            slot_rect = pygame.Rect(x, y_offset_player, slot_width, slot_height)
            pygame.draw.rect(screen, SLOT_COLOR, slot_rect)
            draw_image_in_slot(card_image_path, slot_rect)  # Draw the image in the slot

        # Draw the card on top of the bottom middle slot
        middle_slot_x = center_x - 0.5 * slot_width  # Align with the middle slot
        middle_slot_y = y_offset_player - slot_height - 20  # Position above the bottom middle slot
        middle_slot_rect = pygame.Rect(middle_slot_x, middle_slot_y, slot_width, slot_height)
        pygame.draw.rect(screen, SLOT_COLOR, middle_slot_rect)  # Draw the card slot
        draw_image_in_slot(card_image_path, middle_slot_rect)  # Draw the image in the card slot

        # Draw top slots (opponent)
        y_offset_opponent = center_y - slot_vertical_gap - slot_height  # Vertical offset for the opponent
        for i in range(3):
            x = center_x - 1.5 * slot_width - slot_margin + i * (slot_width + slot_margin)
            slot_rect = pygame.Rect(x, y_offset_opponent, slot_width, slot_height)
            pygame.draw.rect(screen, SLOT_COLOR, slot_rect)
            draw_image_in_slot(card_image_path, slot_rect)  # Draw the image in the slot

        # Draw the card on top of the top middle slot
        top_middle_slot_x = center_x - 0.5 * slot_width  # Align with the middle slot
        top_middle_slot_y = y_offset_opponent + slot_height + 20  # Position below the top middle slot
        top_middle_slot_rect = pygame.Rect(top_middle_slot_x, top_middle_slot_y, slot_width, slot_height)
        pygame.draw.rect(screen, SLOT_COLOR, top_middle_slot_rect)  # Draw the card slot
        draw_image_in_slot(card_image_path, top_middle_slot_rect)  # Draw the image in the card slot

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
