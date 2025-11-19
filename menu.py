import pygame
import sys
from pathlib import Path

# -----------------------------
# تنظیمات کلی و ثابت‌ها
# -----------------------------
WIDTH = 1500
HEIGHT = 750

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

class Menu:
    def __init__(self, screen_m):
        """
        screen_m: شیء pygame.display (بهتره از main.py ارسال شود)
        """
        self.screen_m = screen_m
        # پس‌زمینه منو
        self.menu_bg_m = pygame.image.load(str(ASSETS_DIR / "menu_bg.png")).convert()
        self.menu_bg_m = pygame.transform.scale(self.menu_bg_m, (WIDTH, HEIGHT))  

        self.title_logo = pygame.image.load(str(ASSETS_DIR / "title_logo.png")).convert_alpha()
        self.title_logo = pygame.transform.smoothscale(self.title_logo, (200, 200))   

        # فونت‌ها
        self.font_title_m = pygame.font.SysFont(None, 96)
        self.font_button_m = pygame.font.SysFont(None, 48)

        btn_w = 300
        btn_h = 70
        center_x = WIDTH // 2
        start_y = 300
        gap = 100

        self.start_button_rect_m = pygame.Rect(center_x - btn_w//2, start_y, btn_w, btn_h)
        self.shop_button_rect_m  = pygame.Rect(center_x - btn_w//2, start_y + gap, btn_w, btn_h)
        self.guide_button_rect_m = pygame.Rect(center_x - btn_w//2, start_y + 2*gap, btn_w, btn_h)
        self.exit_button_rect_m  = pygame.Rect(WIDTH - 120, HEIGHT - 60, 100, 40) 

        # رنگ‌ها
        self.color_button_m = (50, 50, 120)
        self.color_button_hover_m = (80, 80, 170)
        self.color_text_m = (255, 255, 255)

        try:
            pygame.mixer.music.load(str(ASSETS_DIR / "menu_music.mp3")) 
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print("Warning: couldn't load menu_music.mp3:", e)

        try:
            self.click_sound_m = pygame.mixer.Sound(str(ASSETS_DIR / "click.wav"))  #  افکت کلیک
        except Exception as e:
            print("Warning: couldn't load click.wav:", e)
            self.click_sound_m = None

    def draw_button_m(self, rect, text, mouse_pos):
        
        if rect.collidepoint(mouse_pos):
            color = self.color_button_hover_m
        else:
            color = self.color_button_m
        pygame.draw.rect(self.screen_m, color, rect, border_radius=8)
        txt_surf = self.font_button_m.render(text, True, self.color_text_m)
        txt_rect = txt_surf.get_rect(center=rect.center)
        self.screen_m.blit(txt_surf, txt_rect)

    def run_m(self):
        clock = pygame.time.Clock()
        
        try:
            pygame.mixer.music.play(-1)
        except:
            pass

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.start_button_rect_m.collidepoint(event.pos):
                        if self.click_sound_m: self.click_sound_m.play()
                        print("Start clicked") 
                        return "start" 
                    elif self.shop_button_rect_m.collidepoint(event.pos):
                        return "shop" 
                    elif self.guide_button_rect_m.collidepoint(event.pos):
                        return "guide"
                    elif self.exit_button_rect_m.collidepoint(event.pos):
                        if self.click_sound_m: self.click_sound_m.play()
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

            # رسم
            self.screen_m.blit(self.menu_bg_m, (0,0))
           
            title_rect = self.title_logo.get_rect(center=(WIDTH//2, 150))
            self.screen_m.blit(self.title_logo, title_rect)

            # دکمه‌ها
            self.draw_button_m(self.start_button_rect_m, "Start", mouse_pos)
            self.draw_button_m(self.shop_button_rect_m, "Shop", mouse_pos)
            self.draw_button_m(self.guide_button_rect_m, "Guide", mouse_pos)
            
            exit_surf = self.font_button_m.render("Exit", True, self.color_text_m)
            exit_rect = exit_surf.get_rect(center=self.exit_button_rect_m.center)
            pygame.draw.rect(self.screen_m, (120,30,30), self.exit_button_rect_m, border_radius=6)
            self.screen_m.blit(exit_surf, exit_rect)

            pygame.display.flip()
            clock.tick(60)
