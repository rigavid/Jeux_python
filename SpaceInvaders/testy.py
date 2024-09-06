import pygame

# Initialisation de Pygame
pygame.init()

# Dimensions initiales de la fenêtre
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

pygame.display.set_caption("Fenêtre Pygame Redimensionnable")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Vérifier si la fenêtre est redimensionnée
        elif event.type == pygame.VIDEORESIZE:
            # Obtenir les nouvelles dimensions
            new_width, new_height = event.w, event.h
            if (new_width, new_height) != (width, height):
                width, height = new_width, new_height
                # Redimensionner la surface de la fenêtre
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Remplir l'écran avec une couleur (par exemple, blanc)
    screen.fill((255, 255, 255))

    # Mettre à jour l'affichage
    pygame.display.flip()

pygame.quit()
