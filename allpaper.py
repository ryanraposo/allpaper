import os
import markdown2
import imgkit
from PIL import Image

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # Project root directory
CHEATSHEETS_DIR = os.path.join(PROJECT_ROOT, "cheatsheets")  # Folder containing text cheatsheets in project root
OUTPUT_WALLPAPER = os.path.join(PROJECT_ROOT, "wallpapers", "cheatsheet_collage.png")  # Output wallpaper path in project root
SCREEN_RESOLUTION = (1920, 1080)  # Adjust according to your screen resolution
BACKGROUND_COLOR = (30, 30, 30)  # Dark grey background
SLOT_BACKGROUND_COLOR = (50, 50, 50)  # Slightly different background for each slot

# Ensure directories exist
os.makedirs(CHEATSHEETS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_WALLPAPER), exist_ok=True)

# Function to get cheatsheet files
def get_cheatsheets(directory):
    cheatsheets = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".txt")]
    return cheatsheets[:4]  # Limit to 4 cheatsheets for better readability

# Function to create an image from a Markdown cheatsheet
def markdown_to_image(md_content, output_path, width):
    # Convert markdown content to HTML
    html_content = markdown2.markdown(md_content)
    
    # Wrap HTML in a basic structure for better presentation
    full_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: rgb(50, 50, 50);
                color: white;
                width: {width}px;
                padding: 30px;
                box-sizing: border-box;
                overflow: hidden;
                word-wrap: break-word;
                font-size: 24px;
            }}
            h1, h2, h3 {{
                color: #ffcc00;
                font-size: 32px;
                margin-bottom: 15px;
            }}
            ul {{
                padding-left: 25px;
            }}
            li {{
                margin-bottom: 15px;
            }}
            code {{
                background-color: #333;
                padding: 4px 6px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Convert HTML to image using imgkit without forcing the height
    options = {
        'format': 'png',
        'width': width,
        'quiet': ''  # Suppresses verbose output from wkhtmltopdf
    }
    imgkit.from_string(full_html, output_path, options=options)

# Function to create a collage of cheatsheets
def create_collage(cheatsheets, output_file, screen_resolution):
    # Create a blank image for the wallpaper
    wallpaper = Image.new("RGB", screen_resolution, BACKGROUND_COLOR)

    # Calculate slots
    num_slots = 4
    slot_width = screen_resolution[0] // 2
    slot_height = screen_resolution[1] // 2
    padding = 30

    # Draw each cheatsheet in its respective slot
    for index, cheatsheet in enumerate(cheatsheets):
        # Determine position based on slot index for rows and columns
        row = index // 2
        col = index % 2

        x, y = col * slot_width, row * slot_height

        # Convert cheatsheet to an image using a dynamic height
        markdown_output_path = os.path.join(PROJECT_ROOT, "tmp", f"cheatsheet_{index}.png")
        os.makedirs(os.path.dirname(markdown_output_path), exist_ok=True)

        with open(cheatsheet, "r") as f:
            markdown_content = f.read()
            markdown_to_image(markdown_content, markdown_output_path, width=slot_width - 2 * padding)

        # Open the generated image and calculate resizing if needed
        cheatsheet_image = Image.open(markdown_output_path)

        # Resize to fit within the slot while preserving the aspect ratio
        aspect_ratio = cheatsheet_image.width / cheatsheet_image.height
        target_height = slot_height - 2 * padding
        target_width = min(slot_width - 2 * padding, int(target_height * aspect_ratio))

        cheatsheet_image = cheatsheet_image.resize((target_width, target_height), Image.LANCZOS)

        # Center the cheatsheet image within the slot
        paste_x = x + padding + (slot_width - 2 * padding - target_width) // 2
        paste_y = y + padding

        wallpaper.paste(cheatsheet_image, (paste_x, paste_y))

    # Save the wallpaper
    wallpaper.save(output_file)

# Function to set the generated image as wallpaper
def set_wallpaper(image_path):
    # Set wallpaper using gsettings (specific for GNOME)
    os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}")

# Function to create a new cheatsheet from pasted text
def create_cheatsheet_from_input(input_text):
    # Create a filename based on current timestamp
    import time
    filename = f"cheatsheet_{int(time.time())}.txt"
    filepath = os.path.join(CHEATSHEETS_DIR, filename)
    
    # Write the input text to the file
    with open(filepath, "w") as f:
        f.write(input_text)
    
    print(f"Cheatsheet saved as {filename}")

# Function to get multiline input safely
def get_multiline_input():
    print("Paste your cheatsheet content below. Enter a single '.' on a new line when you are done:")
    lines = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "cheatify":
            # Create a new cheatsheet from pasted text
            input_text = get_multiline_input()
            if input_text.strip():
                create_cheatsheet_from_input(input_text)
            else:
                print("No input provided. Aborting cheatsheet creation.")
        elif sys.argv[1] == "init":
            # Create a blank starter cheatsheet collage
            create_collage([], OUTPUT_WALLPAPER, SCREEN_RESOLUTION)
            print(f"Blank starter cheatsheet collage saved at: {OUTPUT_WALLPAPER}")
        else:
            print(f"Unknown command: {sys.argv[1]}")
    else:
        # Get cheatsheets and create the collage
        cheatsheets = get_cheatsheets(CHEATSHEETS_DIR)
        if not cheatsheets:
            print("No cheatsheets found in the directory. Please add some .txt files.")
        else:
            create_collage(cheatsheets, OUTPUT_WALLPAPER, SCREEN_RESOLUTION)
            set_wallpaper(OUTPUT_WALLPAPER)
            print("Wallpaper updated with cheatsheet collage!")
