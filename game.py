import pygame
from pygame.locals import * 

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_velocity = pygame.Vector2(0, 0)
gravity = 500  # pixels per second squared
dragging = False
previous_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
mouse_speed = pygame.Vector2(0, 0)
bounce_damping = 0.7
friction = 0.98


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mouse click is inside the circle
            if player_pos.distance_to(mouse_pos) <= 40:
                dragging = True
                player_velocity = pygame.Vector2(0, 0)  # Reset velocity when picked up
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                player_velocity = mouse_speed  # Give the ball inertia from mouse speed
            dragging = False
    
    current_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())

    if dragging:
        # Update the circle position to the mouse position
        player_pos = current_mouse_pos

        if dt > 0:  # Avoid division by zero
            mouse_speed = (current_mouse_pos - previous_mouse_pos) / dt
        
        
    else:
        # Apply gravity to the velocity
        player_velocity.y += gravity * dt
        # Update the circle position with the velocity
        player_pos += player_velocity * dt
        # Check for collision with the bottom of the screen
        if player_pos.y + 40 > screen.get_height():
            player_pos.y = screen.get_height() - 40
            player_velocity.y *= -bounce_damping # Stop the ball when it hits the ground
            player_velocity.x *= friction
        if player_pos.x + 40 > screen.get_width():
            player_pos.x = screen.get_width() - 40
            player_velocity.x *= -bounce_damping
        if player_pos.y - 40 < 0:
            player_pos.y = 40
            player_velocity.y *= -bounce_damping# Stop the ball when it hits the ground
        if player_pos.x - 40 < 0:
            player_pos.x = 40
            player_velocity.x *= -bounce_damping
    
    previous_mouse_pos = current_mouse_pos

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # Draw the circle
    pygame.draw.circle(screen, "red", player_pos, 40)

    # Display the mouse speed
    font = pygame.font.SysFont(None, 36)
    speed_text = font.render(f'Mouse Speed: {mouse_speed.length():.2f} px/s', True, pygame.Color('white'))
    screen.blit(speed_text, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
