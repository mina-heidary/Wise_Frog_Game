from ui.settings import SettingIcon

def create_setting_icons():
    return [
        SettingIcon("volume", "data/menu/botton/icon/volume.png", (30, 30), 105),
        SettingIcon("shop", "data/menu/botton/icon/shop.png", (32, 32), 10),
        SettingIcon("bag", "data/menu/botton/icon/bag.png", (50, 50), 50)
    ]