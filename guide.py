import pygame

def run_guide_screen(window):
    pygame.init()
    screen_width, screen_height = window.get_size()
    pygame.display.set_caption("Guide")

    background_img = pygame.image.load("data/background/guide_bg.png").convert()
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

    raw_images = [
        pygame.image.load("guide/1.png"),
        pygame.image.load("guide/2.png"),
        pygame.image.load("guide/3.png"),
        pygame.image.load("guide/4.png"),
        pygame.image.load("guide/6.png"),
        pygame.image.load("guide/7.png"),
        pygame.image.load("guide/5.png")
    ]

    image_size = (100, 100)
    special_size = (250, 90)  

    guide_images = []
    for i, img in enumerate(raw_images):
        size = special_size if i == 6 else image_size
        scaled = pygame.transform.smoothscale(img.convert_alpha(), size)
        guide_images.append(scaled)

    # توضیحات مربوط به هر تصویر
    guide_texts = [
        "Press Left to move left!",
        "Press Down to go down!",
        "Press Up to go up!",
        "Press RIGHT to move right!",
        "Press M to Attack!",
        "Collect to gain scores!",
        "Press Space to JUMP/ATTACK!",
    ]

    
    font = pygame.font.SysFont(None, 36)

    
    exit_img = pygame.image.load("data/menu/botton/exit.png").convert_alpha()
    exit_img = pygame.transform.scale(exit_img, (50, 50))
    exit_rect = exit_img.get_rect(topleft=(20, 20))

    # تنظیمات چیدمان دو ستون عمودی
    columns = 2
    spacing_x = 600
    spacing_y = 140
    start_x = 100
    start_y = 120

    running = True
    while running:
        window.blit(background_img, (0, 0))
        window.blit(exit_img, exit_rect)

        for i in range(len(guide_images)):
            col = i % columns
            row = i // columns

            current_size = special_size if i == 6 else image_size
            img_x = start_x + col * spacing_x
            img_y = start_y + row * spacing_y
            text_x = img_x + current_size[0] + 20
            text_y = img_y + current_size[1] // 2

            window.blit(guide_images[i], (img_x, img_y))
            text_surface = font.render(guide_texts[i], True, (255, 255, 255))
            text_rect = text_surface.get_rect(midleft=(text_x, text_y))
            window.blit(text_surface, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if exit_rect.collidepoint(mouse):
                    return "menu"