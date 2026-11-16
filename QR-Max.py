#!/usr/bin/env python3
import sys
import os
import time
import socket
import urllib.request
import urllib.parse
from pathlib import Path

# Force a global socket timeout
socket.setdefaulttimeout(10)

# Try importing PIL for gradient generation and logo embedding
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# ====================================
# Terminal Colors
# ====================================
R = "\033[31m" # Red
G = "\033[32m" # Green
Y = "\033[33m" # Yellow
B = "\033[34m" # Blue
M = "\033[35m" # Magenta
C = "\033[36m" # Cyan
W = "\033[37m" # White
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

def type_text(text, delay=0.005):
    """Prints text with a smooth typing animation effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

# ====================================
# Dedicated QR-Max Banner
# ====================================
BANNER = f"""{C}
 ██████╗ ██████╗       ███╗   ███╗ █████╗ ██╗  ██╗
██╔═══██╗██╔══██╗      ████╗ ████║██╔══██╗╚██╗██╔╝
██║   ██║██████╔╝█████╗██╔████╔██║███████║ ╚███╔╝ 
██║▄▄ ██║██╔══██╗╚════╝██║╚██╔╝██║██╔══██║ ██╔██╗ 
╚██████╔╝██║  ██║      ██║ ╚═╝ ██║██║  ██║██╔╝ ██╗
 ╚══██═╝ ╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
                                                  {RESET}"""

def banner():
    print(BANNER)
    type_text(G + "       [+] Advanced URL QR Code Generator & Renderer" + RESET, 0.003)
    type_text(Y + "       [+] Multiple Gradient & Solid Themes + Direct-to-Downloads" + RESET, 0.003)
    type_text(C + "       " + "═" * 58 + RESET + "\n", 0.002)

def select_color_choice():
    type_text(f"\n{W}  Select QR Code Color Theme:{RESET}", 0.01)
    type_text(f"  {C}[1]{W} Classic Black (Solid)", 0.005)
    type_text(f"  {G}[2]{W} Matrix Green (Solid)", 0.005)
    type_text(f"  {B}[3]{W} Cyber Blue (Solid)", 0.005)
    type_text(f"  {R}[4]{W} Neon Red (Solid)", 0.005)
    type_text(f"  {Y}[5]{W} Metallic Gold (Solid)", 0.005)
    type_text(f"  {C}[6]{W} Blue & Red Gradient", 0.005)
    type_text(f"  {M}[7]{W} Purple & Pink Gradient", 0.005)
    type_text(f"  {B}[8]{W} Cyan & Purple Gradient", 0.005)
    type_text(f"  {Y}[9]{W} Sunset Orange & Gold Gradient", 0.005)
    
    choice = input(f"{C}qr-max/color{W} > {RESET}").strip()
    return choice

def apply_gradient(file_path, start_rgb, end_rgb):
    """Applies a smooth horizontal color gradient across QR modules."""
    if not PIL_AVAILABLE:
        return
    try:
        img = Image.open(file_path).convert("RGBA")
        width, height = img.size

        gradient = Image.new("RGBA", (width, height))
        for x in range(width):
            ratio = x / width if width > 1 else 0
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            for y in range(height):
                gradient.putpixel((x, y), (r, g, b, 255))

        mask = Image.new("L", (width, height), 0)
        pixels = img.load()
        mask_pixels = mask.load()
        for x in range(width):
            for y in range(height):
                if pixels[x, y][0] < 128:
                    mask_pixels[x, y] = 255
                else:
                    mask_pixels[x, y] = 0

        background = Image.new("RGBA", (width, height), (255, 255, 255, 255))
        background.paste(gradient, (0, 0), mask)
        background.save(file_path)
    except Exception as e:
        type_text(f"{Y}[!]{W} Gradient application skipped: {e}{RESET}", 0.005)

def process_and_save(payload, filename, color_choice="1", logo_path=""):
    safe_name = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    if not safe_name:
        safe_name = "qrcode_output"

    encoded_url = urllib.parse.quote(payload)

    type_text(f"\n{GRAY}[~] Generating QR code...{RESET}", 0.005)

    # 1. Render ASCII/ANSI QR code directly in the terminal
    try:
        req = urllib.request.Request(
            f"https://qrenco.de/{encoded_url}",
            headers={'User-Agent': 'curl/7.68.0'}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            ascii_art = response.read().decode('utf-8')
            type_text(f"\n{G}[+]{W} Terminal QR Code Display:\n", 0.01)
            print(ascii_art)
    except Exception as e:
        type_text(f"\n{Y}[!]{W} Terminal ASCII render skipped: {e}{RESET}", 0.01)

    # 2. Save PNG image directly to user's Downloads directory
    try:
        output_dir = Path.home() / "Downloads"
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / f"{safe_name}.png"

        solid_colors = {
            "1": "000000",
            "2": "00FF00",
            "3": "0077FF",
            "4": "FF0033",
            "5": "FFD700"
        }

        gradients = {
            "6": ((0, 0, 255), (255, 0, 0)),       # Blue to Red
            "7": ((128, 0, 128), (255, 20, 147)),   # Purple to Pink
            "8": ((0, 255, 255), (138, 43, 226)),   # Cyan to Purple
            "9": ((255, 69, 0), (255, 215, 0))      # Sunset Orange to Gold
        }

        if color_choice in gradients:
            # Download base black & white first, then apply selected gradient via PIL
            img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_url}&color=000000"
            urllib.request.urlretrieve(img_url, file_path)
            start_rgb, end_rgb = gradients[color_choice]
            apply_gradient(file_path, start_rgb, end_rgb)
        else:
            hex_code = solid_colors.get(color_choice, "000000")
            img_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_url}&color={hex_code}"
            urllib.request.urlretrieve(img_url, file_path)

        # 3. Optional Logo Embedding
        if logo_path:
            if not logo_path.startswith("/"):
                logo_path = f"/home/kali/{logo_path}"
            
            logo_file = Path(logo_path)
            if logo_file.exists():
                if PIL_AVAILABLE:
                    try:
                        qr_img = Image.open(file_path).convert("RGBA")
                        logo_img = Image.open(logo_file).convert("RGBA")
                        
                        qr_width, qr_height = qr_img.size
                        logo_size = int(qr_width * 0.22)
                        logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                        
                        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                        qr_img.paste(logo_img, pos, logo_img)
                        qr_img.save(file_path)
                        type_text(f"{G}[+]{W} Center logo embedded successfully!", 0.005)
                    except Exception as le:
                        type_text(f"{Y}[!]{W} Could not embed logo: {le}{RESET}", 0.005)
                else:
                    type_text(f"{Y}[!]{W} Logo path provided, but Pillow is not installed.{RESET}", 0.005)
            else:
                type_text(f"{Y}[!]{W} Logo file not found at: {logo_path}{RESET}", 0.005)

        type_text(f"\n{G}[+]{W} Done! PLease check your Downloads directory ({file_path}){RESET}", 0.01)
    except Exception as e:
        type_text(f"\n{R}[!]{W} Failed to save QR code image: {e}{RESET}", 0.01)

def generate_qr():
    type_text(f"\n{Y}[?]{W} Enter target URL: {RESET}", 0.01)
    target_url = input(f"{C}qr-max{W} > {RESET}").strip()
    if not target_url:
        type_text(f"\n{R}[!]{W} URL cannot be empty.{RESET}", 0.01)
        return

    type_text(f"\n{Y}[?]{W} Enter QR code name (filename): {RESET}", 0.01)
    qr_name = input(f"{C}qr-max{W} > {RESET}").strip()
    if not qr_name:
        qr_name = "qrcode_output"

    type_text(f"\n{Y}[?]{W} Enter logo path in middle (optional) [Please Include /home/kali/]: {RESET}", 0.01)
    logo_path = input(f"{C}qr-max{W} > {RESET}").strip()

    color_choice = select_color_choice()
    process_and_save(target_url, qr_name, color_choice, logo_path)

    type_text(f"\n{Y}[*]{W} Press Enter to return to menu...", 0.01)
    input()

def main():
    while True:
        banner()
        type_text(f"{W}  Select an option from the menu:\n{RESET}", 0.01)
        type_text(f"  {C}[{G}01{C}]{W} Generate URL QR Code", 0.01)
        type_text(f"  {C}[{G}02{C}]{W} About QR-Max Framework", 0.01)
        type_text(f"  {C}[{G}03{C}]{W} Exit QR-Max\n", 0.01)

        choice = input(f"{C}qr-max{W} > {RESET}").strip()

        if choice == "1" or choice == "01":
            generate_qr()
        elif choice == "2" or choice == "02":
            type_text(f"\n{B}[Info]{W} QR-Max is a zero-install utility designed to instantly generate", 0.01)
            type_text(f"       URL QR codes with terminal previews, optional center logos,", 0.01)
            type_text(f"       and multiple solid and gradient color themes saved directly to your Downloads folder.{RESET}", 0.01)
            type_text(f"\n{Y}[*] Press Enter to continue...{RESET}", 0.01)
            input()
        elif choice == "3" or choice == "03":
            type_text(f"\n{R}[-*]{W} Exiting QR-Max. Stay secure!\n", 0.01)
            sys.exit(0)
        else:
            type_text(f"\n{R}[!]{W} Invalid option selected. Try again.{RESET}", 0.01)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        type_text(f"\n\n{R}[-*]{W} Program interrupted by user. Exiting...{RESET}\n", 0.01)
        sys.exit(0)