import os
import sys
import json
import zipfile
import io
import hashlib
import argparse
import re
import urllib.request

from PIL import Image, ImageDraw, ImageFont


# ============================================================
# FontScratch
# ============================================================

VERSION = "1.0.0"

SUPPORTED_FORMATS = {
    ".ttf",
    ".otf"
}

SOCIAL_URL = (
    "https://raw.githubusercontent.com/"
    "BayLak-Egypt/baylak-egypt.github.io/"
    "refs/heads/main/mysocial.txt"
)

GITHUB_URL = "https://github.com/BayLak-Egypt"


# ============================================================
# Terminal Colors
# ============================================================

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"
GRAY = "\033[90m"


def color(text, c):
    return f"{c}{text}{RESET}"


# ============================================================
# FontScratch Banner
# ============================================================

BANNER = r"""
                                         
 ####   ####    ##   #####  #####  ####  #    # 
#      #    #  #  #  #    #   #   #    # #    # 
 ####  #      #    # #    #   #   #      ###### 
     # #      ###### #####    #   #      #    # 
#    # #    # #    # #   #    #   #    # #    # 
 ####   ####  #    # #    #   #    ####  #    # 
         Your Path Toward Building Systems ;0
 
"""


def show_banner():
    print(color(BANNER, CYAN))



# ============================================================
# Social Links
# ============================================================

def get_social_links():
    """
    Fetch social media links from the BayLak GitHub repository.
    """

    try:
        request = urllib.request.Request(
            SOCIAL_URL,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            content = response.read().decode(
                "utf-8"
            ).strip()

        matches = re.findall(
            r"(\w+)\s*=\s*(\S+)",
            content
        )

        if not matches:
            return [
                ("text", "No social links found.")
            ]

        formatted_data = [
            (
                "header",
                "MY SOCIAL MEDIA (LIVE)"
            ),
            (
                "line",
                "----------------------------------------"
            )
        ]

        for platform, raw_link in matches:

            clean_link = re.sub(
                r"^(https?://)?(www\.)?",
                "",
                raw_link
            ).strip()

            formatted_data.append(
                (
                    "link",
                    platform.capitalize(),
                    clean_link
                )
            )

        return formatted_data

    except Exception:
        return [
            (
                "error",
                "CONNECTION ERROR"
            ),
            (
                "line",
                "----------------------------------------"
            ),
            (
                "text",
                "Failed to fetch links from GitHub."
            )
        ]


# ============================================================
# Print Social Links
# ============================================================

def print_social_links():

    data = get_social_links()

    print()

    for item in data:

        if item[0] == "header":

            print(
                color(
                    f"🌐 {item[1]}",
                    CYAN
                )
            )

        elif item[0] == "line":

            print(
                color(
                    item[1],
                    GRAY
                )
            )

        elif item[0] == "link":

            _, platform, link = item

            print(
                f"{color(platform.ljust(14), GREEN)}"
                f"{color(link, WHITE)}"
            )

        elif item[0] == "error":

            print(
                color(
                    f"⚠ {item[1]}",
                    RED
                )
            )

        elif item[0] == "text":

            print(item[1])

    print()


# ============================================================
# About Page
# ============================================================

def show_about():

    print()

    print(
        color(
            "╔══════════════════════════════════════════════════╗",
            CYAN
        )
    )

    print(
        color(
            "║                  FontScratch                   ",
            CYAN
        )
    )

    print(
        color(
            "║              Scratch Font Tool                 ",
            CYAN
        )
    )

    print(
        color(
            "╚══════════════════════════════════════════════════╝",
            CYAN
        )
    )

    print()

    print(
        color(
            "FontScratch",
            GREEN
        ),
        "is a lightweight command-line tool designed"
    )

    print(
        "for generating",
        color(
            "Scratch Sprite3",
            YELLOW
        ),
        "files from font files."
    )

    print()

    print(
        color(
            "Supported formats:",
            CYAN
        ),
        ".TTF / .OTF"
    )

    print(
        color(
            "Version:",
            CYAN
        ),
        VERSION
    )

    print()

    print(
        color(
            "Made by BayLak",
            GREEN
        )
    )

    print(
        color(
            "GitHub: ",
            CYAN
        ),
        GITHUB_URL
    )

    print()

    print(
        color(
            "Your Path Toward Building Systems",
            YELLOW
        )
    )

    print()

    print(
        color(
            "Fetching BayLak social media links...",
            YELLOW
        )
    )

    print_social_links()

    print(
        color(
            "Thank you for using FontScratch!",
            GREEN
        )
    )

    print()


# ============================================================
# Sprite Generator
# ============================================================

def create_sprite(font_path, output_name):

    # Scratch-compatible sprite structure
    sprite_json = {
        "isStage": False,
        "name": output_name,
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": {},
        "comments": {},
        "currentCostume": 0,
        "costumes": [],
        "sounds": [],
        "volume": 100,
        "visible": True,
        "x": 0,
        "y": 0,
        "size": 100,
        "direction": 90,
        "draggable": False,
        "rotationStyle": "all around"
    }

    # --------------------------------------------------------
    # Check Font Extension
    # --------------------------------------------------------

    extension = os.path.splitext(
        font_path
    )[1].lower()

    if extension not in SUPPORTED_FORMATS:

        print(
            color(
                f"[-] Unsupported font format: {extension}",
                RED
            )
        )

        print(
            color(
                "[!] Supported formats: .ttf, .otf",
                YELLOW
            )
        )

        return False

    # --------------------------------------------------------
    # Load Font
    # --------------------------------------------------------

    try:

        font = ImageFont.truetype(
            font_path,
            64
        )

    except Exception as e:

        print(
            color(
                f"[-] Failed to load font: {e}",
                RED
            )
        )

        return False

    # Characters to generate
    text_chars = (
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
    )

    new_files = {}

    print()

    print(
        color(
            f"[*] Font   : {font_path}",
            CYAN
        )
    )

    print(
        color(
            f"[*] Format : {extension.upper()}",
            CYAN
        )
    )

    print(
        color(
            f"[*] Sprite : {output_name}",
            CYAN
        )
    )

    print()

    print(
        color(
            "[*] Generating Scratch costumes...",
            YELLOW
        )
    )

    # --------------------------------------------------------
    # Generate Character Images
    # --------------------------------------------------------

    for char in text_chars:

        # Transparent image
        img = Image.new(
            "RGBA",
            (100, 100),
            (255, 255, 255, 0)
        )

        draw = ImageDraw.Draw(img)

        # Draw character
        draw.text(
            (20, 10),
            char,
            font=font,
            fill="black"
        )

        # Save PNG into memory
        buffer = io.BytesIO()

        img.save(
            buffer,
            format="PNG"
        )

        data = buffer.getvalue()

        # Generate MD5 hash
        file_hash = hashlib.md5(
            data
        ).hexdigest()

        md5ext = f"{file_hash}.png"

        new_files[md5ext] = data

        # Add costume
        sprite_json["costumes"].append({
            "name": char,
            "bitmapResolution": 1,
            "dataFormat": "png",
            "assetId": file_hash,
            "md5ext": md5ext,
            "rotationCenterX": 50,
            "rotationCenterY": 50
        })

    # --------------------------------------------------------
    # Create Sprite3
    # --------------------------------------------------------

    final_filename = (
        f"{output_name}.sprite3"
    )

    try:

        with zipfile.ZipFile(
            final_filename,
            "w",
            zipfile.ZIP_DEFLATED
        ) as archive:

            archive.writestr(
                "sprite.json",
                json.dumps(
                    sprite_json,
                    ensure_ascii=False,
                    separators=(",", ":")
                )
            )

            for filename, data in new_files.items():

                archive.writestr(
                    filename,
                    data
                )

    except Exception as e:

        print(
            color(
                f"[-] Failed to create Sprite3: {e}",
                RED
            )
        )

        return False

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print()

    print(
        color(
            f"[+] Successfully created: {final_filename}",
            GREEN
        )
    )

    print(
        color(
            f"[+] Generated costumes: {len(text_chars)}",
            GREEN
        )
    )

    print()

    return True


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        prog="FontScratch",

        description=(
            "FontScratch - Create Scratch Sprite3 files "
            "from TTF and OTF fonts."
        ),

        epilog=(
            "Made by BayLak | "
            "https://github.com/BayLak-Egypt"
        )
    )

    # --------------------------------------------------------
    # Font Argument
    # --------------------------------------------------------

    parser.add_argument(
        "font",
        nargs="?",
        help=(
            "Path to the font file "
            "(.ttf or .otf)"
        )
    )

    # --------------------------------------------------------
    # Output Argument
    # --------------------------------------------------------

    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Custom Sprite name "
            "(optional)"
        )
    )

    # --------------------------------------------------------
    # About Argument
    # --------------------------------------------------------

    parser.add_argument(
        "--about",
        action="store_true",
        help="Show FontScratch About Page"
    )

    # --------------------------------------------------------
    # Parse Arguments
    # --------------------------------------------------------

    args = parser.parse_args()

    # --------------------------------------------------------
    # About
    # --------------------------------------------------------

    if args.about:

        show_about()

        return

    # --------------------------------------------------------
    # Font Required
    # --------------------------------------------------------

    if not args.font:

        parser.print_help()

        return

    # --------------------------------------------------------
    # Check Font File
    # --------------------------------------------------------

    if not os.path.isfile(args.font):

        print(
            color(
                "[-] Error: Font file not found.",
                RED
            )
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Check Font Extension
    # --------------------------------------------------------

    extension = os.path.splitext(
        args.font
    )[1].lower()

    if extension not in SUPPORTED_FORMATS:

        print(
            color(
                f"[-] Error: Unsupported format '{extension}'.",
                RED
            )
        )

        print(
            color(
                "[!] FontScratch supports:",
                YELLOW
            )
        )

        print(
            "    - TrueType Font (.ttf)"
        )

        print(
            "    - OpenType Font (.otf)"
        )

        sys.exit(1)

    # --------------------------------------------------------
    # Determine Output Name
    # --------------------------------------------------------

    if args.output:

        base_name = args.output

        if base_name.lower().endswith(
            ".sprite3"
        ):

            base_name = base_name[:-7]

    else:

        base_name = os.path.splitext(
            os.path.basename(args.font)
        )[0]

    # --------------------------------------------------------
    # Generate Sprite
    # --------------------------------------------------------

    success = create_sprite(
        args.font,
        base_name
    )

    if not success:

        sys.exit(1)


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":

    show_banner()

    main()
