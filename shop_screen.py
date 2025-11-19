def show_inventory_screen(window, all_items, item_counts):
    import pygame
    screen_width, screen_height = window.get_size()
    font = pygame.font.SysFont(None, 36)
    running = True

    bg = pygame.Surface((screen_width, screen_height))
    bg.fill((30, 20, 50))  
    while running:
        window.blit(bg, (0, 0))

        title = font.render("Inventory", True, (255, 255, 200))
        window.blit(title, (screen_width // 2 - title.get_width() // 2, 30))

        start_x = 100
        start_y = 100
        spacing_x = 180
        spacing_y = 160
        icon_size = 100

        for i, img in enumerate(all_items):
            row = i // 5
            col = i % 5
            x = start_x + col * spacing_x
            y = start_y + row * spacing_y

            icon = pygame.transform.smoothscale(img, (icon_size, icon_size))
            window.blit(icon, (x, y))

            count = item_counts.get(i, 0)
            count_text = font.render(f"x {count}", True, (255, 255, 255))
            window.blit(count_text, (x + 30, y + icon_size + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        pygame.display.flip()


def run_shop_screen(window, player):
    import pygame
    from ui.settings import SettingIcon
    from ui.setup_icons import create_setting_icons

    pygame.init()
    screen_width, screen_height = window.get_size()
    pygame.display.set_caption("Shop Game")

    pygame.mixer.music.stop()
    pygame.mixer.music.load("data/shop/music.mp3")
    pygame.mixer.music.play(-1)

    bg_image = pygame.image.load("data/shop/shop_background.jpg")
    coin_image = pygame.image.load("data/shop/coin.png").convert_alpha()
    coin_icon = pygame.transform.smoothscale(coin_image, (50, 50))
    diamond_image = pygame.image.load("data/shop/diamond.png").convert_alpha()
    diamond_icon = pygame.transform.smoothscale(diamond_image, (45, 45))

    item_images = [pygame.image.load(f"data/shop/{i+1}.png") for i in range(6)]
    item_size = (120, 120)
    item_images = [pygame.transform.smoothscale(img, item_size) for img in item_images]
    item_prices = [20, 35, 50, 1, 2, 3]
    item_currencies = ["coin", "coin", "coin", "diamond", "diamond", "diamond"]

    price_coin_icon = pygame.transform.smoothscale(coin_image, (20, 20))
    price_diamond_icon = pygame.transform.smoothscale(diamond_image, (25, 20))

    item_positions = []
    padding = 100
    start_x = 500
    start_y = screen_height * 0.3
    for i in range(6):
        row = i // 3
        col = i % 3
        x = start_x + col * (item_size[0] + padding)
        y = start_y + row * (item_size[1] + padding + 20)
        item_positions.append((x, y))

    coin_x, coin_y = 80, 50
    diamond_x, diamond_y = coin_x + 150, coin_y
    sound_on = True
    font = pygame.font.SysFont(None, 36)

    setting_open = False
    setting_img = pygame.image.load("data/menu/botton/setting.png").convert_alpha()
    setting_img = pygame.transform.smoothscale(setting_img, (30, 30))
    setting_rotated = setting_img.copy()
    setting_rect = setting_rotated.get_rect(topright=(screen_width - 20, 20))
    setting_icons = create_setting_icons()

    exit_img = pygame.image.load("data/menu/botton/icon/exit.png").convert_alpha()
    exit_img = pygame.transform.smoothscale(exit_img, (35, 35))
    exit_rect = exit_img.get_rect(topleft=(20, 20))

    purchased_items = {i: 0 for i in range(len(item_images))}
    show_bag_summary = False

    def try_purchase(index):
        price = item_prices[index]
        currency = item_currencies[index]
        if currency == "coin":
            if player.coins >= price:
                player.coins -= price
                purchased_items[index] += 1
                print(f"آیتم {index+1} با {price} سکه خریداری شد")
            else:
                print("سکه کافی نیست")
        else:
            if player.diamonds >= price:
                player.diamonds -= price
                purchased_items[index] += 1
                print(f"آیتم {index+1} با {price} الماس خریداری شد")
            else:
                print("الماس کافی نیست")

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        window.blit(bg_image, (0, 0))

        # نمایش خلاصه خریدها
        if show_bag_summary:
            summary_y = 20
            summary_x = 100
            spacing = 160
            for i in range(len(item_images)):
                if purchased_items[i] > 0:
                    small_icon = pygame.transform.smoothscale(item_images[i], (60, 60))
                    window.blit(small_icon, (summary_x, summary_y))
                    count_text = font.render(f"x {purchased_items[i]}", True, (255, 255, 255))
                    window.blit(count_text, (summary_x + item_size[0] + 10, summary_y + 40))
                    summary_x += spacing

        window.blit(coin_icon, (coin_x, coin_y))
        coin_text = font.render(str(player.coins), True, (255, 255, 255))
        window.blit(coin_text, (coin_x + coin_icon.get_width() + 10, coin_y + 10))

        window.blit(diamond_icon, (diamond_x, diamond_y))
        diamond_text = font.render(str(player.diamonds), True, (255, 255, 255))
        window.blit(diamond_text, (diamond_x + diamond_icon.get_width() + 5, diamond_y + 10))

        for i in range(6):
            x, y = item_positions[i]
            box_rect = pygame.Rect(x - 10, y - 10, item_size[0] + 20, item_size[1] + 20)
            hovered = box_rect.collidepoint(mouse)

            box_surface = pygame.Surface((item_size[0] + 20, item_size[1] + 20), pygame.SRCALPHA)
            if hovered:
                box_surface.fill((220, 210, 240, 220))
                pygame.draw.rect(box_surface, (255, 255, 255), box_surface.get_rect(), 3)
            else:
                box_surface.fill((190, 180, 210, 180))

            window.blit(box_surface, box_rect.topleft)
            window.blit(item_images[i], (x, y))

            price = item_prices[i]
            currency = item_currencies[i]
            icon = price_coin_icon if currency == "coin" else price_diamond_icon

            price_box_width = 70
            price_box_height = 30
            price_box_x = x + (item_size[0] - price_box_width) // 2
            price_box_y = y + item_size[1] + 10

            price_box = pygame.Surface((price_box_width, price_box_height), pygame.SRCALPHA)
            price_box.fill((50, 50, 50, 170))
            window.blit(price_box, (price_box_x, price_box_y))

            window.blit(icon, (price_box_x + 5, price_box_y + 3))
            price_text = font.render(str(price), True, (255, 255, 255))
            window.blit(price_text, (price_box_x + 35, price_box_y + 3))

        window.blit(setting_rotated, setting_rect)
        for icon in setting_icons:
            icon.draw(window)

        window.blit(exit_img, exit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if setting_rect.collidepoint(mouse):
                    setting_open = not setting_open
                    angle = 90 if setting_open else 0
                    setting_rotated = pygame.transform.rotate(setting_img, angle)
                    setting_rect = setting_rotated.get_rect(topright=(screen_width - 20, 20))
                    for icon in setting_icons:
                        if setting_open:
                            icon.show()
                        else:
                            icon.hide()
                        icon.update(setting_rect)

                for icon in setting_icons:
                    if icon.clicked(mouse):
                        if icon.name == "shop":
                            run_shop_screen(window, player)
                        if icon.name == "bag":
                                all_items = item_images + getattr(player, "collected_item_images", [])
                                item_counts = {}

                                for i in range(len(item_images)):
                                    item_counts[i] = purchased_items.get(i, 0)

                                for j, img in enumerate(getattr(player, "collected_item_images", [])):
                                    index = len(item_images) + j
                                    item_counts[index] = getattr(player, "collected_item_counts", {}).get(j, 0)

                                show_inventory_screen(window, all_items, item_counts)

                        if icon.name == "volume":
                            sound_on = not sound_on
                            volume_path = "mute.png" if not sound_on else "volume.png"
                            icon.image = pygame.image.load(f"data/menu/botton/icon/{volume_path}").convert_alpha()
                            icon.image = pygame.transform.smoothscale(icon.image, (30, 30))
                            pygame.mixer.music.set_volume(0 if not sound_on else 1)

                for i in range(6):
                    x, y = item_positions[i]
                    box_rect = pygame.Rect(x - 10, y - 10, item_size[0] + 20, item_size[1] + 20)
                    if box_rect.collidepoint(mouse):
                        try_purchase(i)

                if exit_rect.collidepoint(mouse):
                    running = False

    return