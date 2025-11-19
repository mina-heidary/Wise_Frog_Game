def Hunt_monster_game(window, coins_start=0):
    import pygame
    import sys
    import random
    import math

    # pygame.init()
    flash_alpha = 0
    dragon_flash_alpha = 0
    coins_collected = coins_start

    # -----screen-----
    # screen = pygame.display.set_mode((1500, 750))
    pygame.display.set_caption("::MONSTER HUNTING::")

    # --- background ---
    bg = pygame.image.load("night.png")
    bg = pygame.transform.scale(bg, (1500, 750))
    clock = pygame.time.Clock()



    # --- sounds ---
    hit_sound = pygame.mixer.Sound("hit.mp3")

    death_sound = pygame.mixer.Sound("over.mp3")

    click_sound = pygame.mixer.Sound("start.mp3")

    shoot_sound = pygame.mixer.Sound("arrow.mp3")

    explosion_sound = pygame.mixer.Sound("explosion.mp3")

    victory_sound = pygame.mixer.Sound("victory.mp3")

    fireball_sound = pygame.mixer.Sound("Whoosh.mp3")
    fireball_sound.set_volume(1.0)

    fireworks_sound = pygame.mixer.Sound("firework.mp3")
    fireworks_sound.set_volume(0.8)

    coins_sound = pygame.mixer.Sound("coins27.mp3")



    # background music
    pygame.mixer.music.load("glory.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # frog flash
    flash_alpha = 0
    # dragon flash
    dragon_flash_alpha = 0

    # seprating channel0 from channel 1
    click_channel = pygame.mixer.Channel(1)
    click_channel.set_volume(1.0)


    # --------------------------------------------------------------------------------
    #  START SCREEN
    # --------------------------------------------------------------------------------
    def show_start_screen():
        title_rect = pygame.Rect(450, 200, 600, 300)
        glow_surface = pygame.Surface((600, 300), pygame.SRCALPHA)
        start_clicked = False

        while not start_clicked:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN and title_rect.collidepoint(e.pos):
                    click_channel.play(click_sound)

                    # white flash while clicking
                    fade_surface = pygame.Surface((1500, 750))
                    fade_surface.fill((0, 0, 0))
                    for alpha in range(0, 255, 8):
                        window.blit(bg, (0, 0))

                        # circular effect
                        glow_surface.fill((0, 0, 0, 0))
                        glow_color = (255, random.randint(120, 220), 0, 140)
                        pygame.draw.circle(glow_surface, glow_color, (300, 150), 230)
                        window.blit(
                            glow_surface, title_rect.topleft, special_flags=pygame.BLEND_ADD
                        )

                        # title for start screen
                        font_title = pygame.font.Font(None, 150)
                        title_text = font_title.render(
                            "Monster Hunting", True, (255, 230, 150)
                        )
                        text_rect = title_text.get_rect(center=title_rect.center)
                        window.blit(title_text, text_rect)
                        fade_surface.set_alpha(alpha)
                        window.blit(fade_surface, (0, 0))
                        pygame.display.update()
                        pygame.time.delay(15)
                    return

            window.blit(bg, (0, 0))

            # circular fire effect
            glow_surface.fill((0, 0, 0, 0))
            glow_color = (255, random.randint(150, 250), 0, random.randint(70, 130))
            pygame.draw.circle(
                glow_surface, glow_color, (300, 150), random.randint(200, 230)
            )
            window.blit(glow_surface, title_rect.topleft, special_flags=pygame.BLEND_ADD)

            # monster hunting text
            font_title = pygame.font.Font(None, 150)
            title_text = font_title.render("Monster Hunting", True, (255, 230, 150))
            text_rect = title_text.get_rect(center=title_rect.center)
            window.blit(title_text, text_rect)

            font_hint = pygame.font.Font(None, 60)
            hint_text = font_hint.render(
                " Click to begin your hunt ", True, (255, 210, 120)
            )
            window.blit(hint_text, (500, 550))

            pygame.display.update()
            clock.tick(60)


    # --------------------------------------------------------------------------------
    #  MAIN GAME LOOP
    # --------------------------------------------------------------------------------
    def game_rloop():
        global flash_alpha, dragon_flash_alpha
        global coins_collected , coins

        # --- player (frog) ---
        player_alive = pygame.image.load("broom.png")
        player_shoot = pygame.image.load("broom 2.png")
        player_dead = pygame.image.load("frog-head4.png")

        player_alive_flip = pygame.transform.flip(player_alive, True, False)
        player_shoot_flip = pygame.transform.flip(player_shoot, True, False)
        player_dead_flip = pygame.transform.flip(player_dead, True, False)

        player_img = player_alive
        player_x, player_y = 80, 550
        player_alive_flag = True
        player_facing_left = False

        # ---frog shooting ---
        bullet_img = pygame.image.load("arrow.png")
        bullet_img = pygame.transform.scale(bullet_img, (80, 40))
        bullets = []
        bullet_speed = 12
        shoot_cooldown = 600
        last_shoot_time = 0

        # --- frog hearts ---
        hearts = [
            pygame.image.load("life4.png"),
            pygame.image.load("life3.png"),
            pygame.image.load("life2.png"),
            pygame.image.load("life1.png"),
        ]
        hearts = [pygame.transform.scale(h, (150, 60)) for h in hearts]
        health = 4

        import random

        # coins image
        coin_img = [
            pygame.image.load("coin1.png"),
            pygame.image.load("coin2.png"),
            pygame.image.load("coin3.png"),
            pygame.image.load("coin4.png"),
            pygame.image.load("coin5.png"),
        ]

        coin_img = [pygame.transform.scale(img, (30, 30)) for img in coin_img]
        
        # coins list
        coins = []
        coins_collected = 0

        # time of the last coin
        last_coin_time = pygame.time.get_ticks()
        #one coin every 6 min
        coins_spawn_delay = 6000
        max_coin = 10




        # --- enemy(dragon) ---
        enemy_frames_original = [
            pygame.image.load("dragon.png"),
            pygame.image.load("dragon-a.png"),
            pygame.image.load("dragon-b.png"),
            pygame.image.load("dragon-c.png"),
        ]
        enemy_frames_original = [
            pygame.transform.scale(img, (300, 250)) for img in enemy_frames_original
        ]
        enemy_frames_left = [
            pygame.transform.flip(img, True, False) for img in enemy_frames_original
        ]
        enemy_frames_right = enemy_frames_original

        enemy_frames = enemy_frames_left
        enemy_index = 0
        enemy_last_frame_time = pygame.time.get_ticks()
        enemy_frame_delay = 400

        enemy_x, enemy_y = 1200, 380
        enemy_speedX, enemy_speedY = 2, 2
        enemy_directionY = 1
        enemy_facing_left = True
        enemy_alive = True

        # ----DRAGON LIFEBAR---

        enemy_life_img = [
            pygame.image.load("health1.png"),
            pygame.image.load("health2.png"),
            pygame.image.load("health3.png"),
            pygame.image.load("health4.png"),
            pygame.image.load("health5.png"),
            pygame.image.load("health6.png"),
            pygame.image.load("health7.png"),
                
        ]

        # size changing if needed
        enemy_life_img = [pygame.transform.scale(img, (100,20)) for img in enemy_life_img]

        # dragon life
        enemy_health = 8

        # --- fireballs ---
        fire_img = pygame.image.load("fireball3.png")
        fire_img = pygame.transform.scale(fire_img, (80, 40))
        fireballs = []
        fire_interval = 4000
        last_fire_time = pygame.time.get_ticks()

        last_hit_time = 0
        damage_cooldown = 1000

        running = True
        victory_mode = False

        fireworks = []

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return coins_collected

            keys = pygame.key.get_pressed()
            current_time = pygame.time.get_ticks()

            # --- movement and shooting ---
            if player_alive_flag:
                if keys[pygame.K_DOWN]:
                    player_y += 7
                if keys[pygame.K_UP]:
                    player_y -= 7
                if keys[pygame.K_LEFT]:
                    player_x -= 9
                    player_facing_left = True
                    player_img = player_alive_flip
                if keys[pygame.K_RIGHT]:
                    player_x += 9
                    player_facing_left = False
                    player_img = player_alive

                if keys[pygame.K_SPACE]:
                    if current_time - last_shoot_time > shoot_cooldown:
                        shoot_sound.play()
                        last_shoot_time = current_time

                        if player_facing_left:
                            player_img = player_shoot_flip
                            bullet_x = player_x
                            bullet_speed_dir = -bullet_speed
                        else:
                            player_img = player_shoot
                            bullet_x = player_x + player_img.get_width() - 40
                            bullet_speed_dir = bullet_speed

                        bullet_y = player_y + 70
                        bullets.append([bullet_x, bullet_y, bullet_speed_dir])
                else:
                    if player_facing_left:
                        player_img = player_alive_flip
                    else:
                        player_img = player_alive

            #prevent page exit 
            player_x = max(0, min(1500 - 383, player_x))
            player_y = max(0, min(750 - 171, player_y))

        
        # frog hits the coins
            player_rect = pygame.Rect(int(player_x), 
            int(player_y), 383, 171)

            for co in coins[:]:
                if player_rect.colliderect(co):
                    coins.remove(co)
                    coins_collected += 1
                    coins_sound.play()    

            #showing coins with delay
            current_time = pygame.time.get_ticks()
            if len(coins) < max_coin and current_time - last_coin_time > coins_spawn_delay:
                x = random.randint(100, 1400)
                y = random.randint(100, 650)
                coins.append(pygame.Rect(x, y, 60, 60))
                last_coin_time = current_time

            
            
            # ---dragon movement ---
            if enemy_alive:
                enemy_y += enemy_speedY * enemy_directionY
                if enemy_y <= 0 or enemy_y >= 750 - 250:
                    enemy_directionY *= -1

                if player_x < enemy_x - 100:
                    enemy_x -= enemy_speedX
                    if not enemy_facing_left:
                        enemy_frames = enemy_frames_left
                        enemy_facing_left = True
                elif player_x > enemy_x + 100:
                    enemy_x += enemy_speedX
                    if enemy_facing_left:
                        enemy_frames = enemy_frames_right
                        enemy_facing_left = False

                if current_time - enemy_last_frame_time > enemy_frame_delay:
                    enemy_index = (enemy_index + 1) % 3
                    enemy_last_frame_time = current_time

                # --- throughing fire---
                if current_time - last_fire_time > fire_interval:
                    enemy_index = 3
                    fire_y = enemy_y + 100
                    if enemy_facing_left:
                        fire_x = enemy_x - 30
                        fire_speed = -10
                    else:
                        fire_x = enemy_x + 250
                        fire_speed = 10

                    fireball_sound.play()

                    fireballs.append([fire_x, fire_y, fire_speed])
                    last_fire_time = current_time

            for f in fireballs:
                f[0] += f[2]
            fireballs = [f for f in fireballs if -100 < f[0] < 1600]

            # --- the movement of arrows---
            for b in bullets:
                b[0] += b[2]
            bullets = [b for b in bullets if -50 < b[0] < 1600]

            # --- arrow hits dragon---
            if enemy_alive:
                enemy_rect = pygame.Rect(enemy_x + 50, enemy_y + 40, 200, 180)
                new_bullets = []
                for b in bullets:
                    bullet_rect = pygame.Rect(b[0], b[1], 50, 20)
                    if bullet_rect.colliderect(enemy_rect):
                        dragon_flash_alpha = 180
                        enemy_health -= 1
                        if enemy_health <= 0:
                            enemy_alive = False

                            explosion_sound.play()

                            pygame.mixer.music.stop()

                            victory_sound.play()
                            victory_mode = True

                            # saving start time
                            victory_start_time = pygame.time.get_ticks()

                            pygame.time.delay(300)
                            fireworks_sound.play(-1)

                            for _ in range(8):

                                fx = random.randint(200, 1300)
                                fy = random.randint(150, 600)

                                for i in range(100):

                                    fireworks.append(
                                        {
                                            "x": fx,
                                            "y": fy,
                                            "vx": random.uniform(-5, 5),
                                            "vy": random.uniform(-8, -2),
                                            "color": random.choice(
                                                [
                                                    (255, 100, 0),
                                                    (255, 255, 255),
                                                    (255, 255, 0),
                                                    (0, 200, 255),
                                                    (255, 0, 180),
                                                    (150, 255, 150),
                                                ]
                                            ),
                                            "life": random.randint(40, 100),
                                        }
                                    )
                        continue

                    new_bullets.append(b)
                bullets = new_bullets

            # ----fire hits frog---
            player_rect = pygame.Rect(
                player_x + 40,
                player_y + 40,
                player_img.get_width() - 80,
                player_img.get_height() - 80,
            )

            new_fireballs = []

            for f in fireballs:
                fire_rect = pygame.Rect(f[0], f[1], 60, 30)
                if fire_rect.colliderect(player_rect) and player_alive_flag:
                    if current_time - last_hit_time > damage_cooldown:
                        health -= 1
                        last_hit_time = current_time
                        hit_sound.play()
                        flash_alpha = 200
                        if health <= 0:
                            player_alive_flag = False
                            player_img = player_dead
                            death_sound.play()
                    continue
                new_fireballs.append(f)
            fireballs = new_fireballs

            if player_alive_flag and player_rect.colliderect(enemy_rect):
                overlap_x = min(player_rect.right, enemy_rect.right) - max(
                    player_rect.left, enemy_rect.left
                )
                overlap_y = min(player_rect.bottom, enemy_rect.bottom) - max(
                    player_rect.top, enemy_rect.top
                )
                if overlap_x > 50 and overlap_y > 50:
                    if current_time - last_hit_time > damage_cooldown:
                        health -= 1
                        last_hit_time = current_time
                        hit_sound.play()
                        flash_alpha = 200
                        if health <= 0:
                            player_alive_flag = False
                            player_img = player_dead
                            death_sound.play()

            # ---draw the scene ---

            # screen
            window.blit(bg, (0, 0))

            # frog
            window.blit(player_img, (player_x, player_y))

            # dragon
            if enemy_alive:
                window.blit(enemy_frames[enemy_index], (enemy_x, enemy_y))

            if enemy_health > 0:
                life_x = enemy_x + 60
                life_y = enemy_y - 40
                index = max(0, min(6 - enemy_health, 5))
                window.blit(enemy_life_img[index], (life_x, life_y))

            # ----addding new fireworks---
            if random.randint(0, 40) == 1:  # once every frame
                fx = random.randint(100, 1400)
                fy = random.randint(150, 600)

                for i in range(60):
                    fireworks.append(
                        {
                            "x": fx,
                            "y": fy,
                            "vx": random.uniform(-4, 4),
                            "vy": random.uniform(-7, -1),
                            "color": random.choice(
                                [
                                    (255, 255, 0),
                                    (255, 100, 0),
                                    (0, 200, 255),
                                    (255, 0, 180),
                                    (255, 255, 255),
                                ]
                            ),
                            "life": random.randint(40, 90),
                        }
                    )

            else:
                if victory_mode:
                    # ----adding new fireworks once every frame
                    if random.randint(0, 40) == 1:
                        fx = random.randint(100, 1400)
                        fy = random.randint(150, 600)
                        fireworks_sound.play()
                        for i in range(60):
                            fireworks.append(
                                {
                                    "x": fx,
                                    "y": fy,
                                    "vx": random.uniform(-4, 4),
                                    "vy": random.uniform(-7, -1),
                                    "color": random.choice(
                                        [
                                            (255, 255, 0),
                                            (255, 100, 0),
                                            (0, 200, 255),
                                            (255, 0, 180),
                                            (255, 255, 255),
                                        ]
                                    ),
                                    "life": random.randint(40, 90),
                                }
                            )

                    # movement and drawing fireball particles
                    for fw in fireworks:
                        fw["x"] += fw["vx"]
                        fw["y"] += fw["vy"]
                        fw["vy"] += 0.2
                        fw["life"] -= 1
                        if fw["life"] > 0:
                            pygame.draw.circle(
                                window, fw["color"], (int(fw["x"]), int(fw["y"])), 4
                            )
                    fireworks[:] = [fw for fw in fireworks if fw["life"] > 0]

                    # VICTORy
                    font_vic = pygame.font.Font(None, 150)
                    text_vic = font_vic.render(" VICTORY ", True, (255, 255, 150))
                    text_rect = text_vic.get_rect(center=(750, 350))
                    window.blit(text_vic, text_rect)

                    # stop sounds after 9sec
                    if pygame.time.get_ticks() - victory_start_time > 9000:
                        fireworks_sound.stop()
                        victory_sound.stop()
                        explosion_sound.stop()
                        pygame.mixer.music.stop()

            for f in fireballs:
                window.blit(fire_img, (f[0], f[1]))
            for b in bullets:
                window.blit(bullet_img, (b[0], b[1]))

            heart_index = max(0, min(3, 4 - health))
            window.blit(hearts[heart_index], (90, 650))

            # red flash for frog
            if flash_alpha > 0:
                flash_surface = pygame.Surface((1500, 750))
                flash_surface.fill((255, 0, 0))
                flash_surface.set_alpha(flash_alpha)
                window.blit(flash_surface, (0, 0))
                flash_alpha = max(0, flash_alpha - 10)

            # white flash for dragon
            if dragon_flash_alpha > 0:
                dragon_flash_surface = pygame.Surface((1500, 750))
                dragon_flash_surface.fill((255, 255, 255))
                dragon_flash_surface.set_alpha(dragon_flash_alpha)
                window.blit(dragon_flash_surface, (0, 0))
                dragon_flash_alpha = max(0, dragon_flash_alpha - 15)

            if not player_alive_flag:
                font_end = pygame.font.Font(None, 120)
                text = font_end.render(" GAME OVER ", True, (255, 80, 80))
                window.blit(text, (500, 300))

            # coins turning animation 
            if isinstance(coin_img ,list):
                coin_index = (pygame.time.get_ticks()// 150) % len(coin_img)
                current_coin_img = coin_img[coin_index]

            else :
                current_coin_img = coin_img

            # showing all coins
            for co in coins:
                window.blit(current_coin_img, (co.x, co.y))

            # coins counter text
            font_coins = pygame.font.Font(None, 60)
            coins_text = font_coins.render(
                f"coins: {coins_collected}", True, (0 ,0 , 0)          
            )

            #frame pose(coins counter)
            coin_rect = coins_text.get_rect(topleft=(90,20))

            # adding marging and padding

            padding = 7
            box_rect = pygame.Rect(
                coin_rect.left - padding,
                coin_rect.top - padding,
                coin_rect.width + padding * 2,
                coin_rect.height + padding * 2
            )

            # drawing frame (outer margin)
            pygame.draw.rect(window, (255, 223, 0), box_rect, border_radius=12)     # GOLDEN FRAME
            pygame.draw.rect(window, (50, 30, 0), box_rect, 4, border_radius=12)   # DARK BROWN FRAME

            # showing the text in the frame
            window.blit(coins_text, coin_rect)

            pygame.display.update()
            clock.tick(60)


    # --------------------------------------------------------------------------------
    #  PLAY THE GAME
    # --------------------------------------------------------------------------------
    show_start_screen()
    game_rloop()

    # کد سالم
