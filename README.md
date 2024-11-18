# Allpaper

> Imperfect but awesome. Happy contributing!

**Allpaper** is a Python-based tool for creating a collage of cheatsheets and using it as your desktop wallpaper. It's a perfect solution for developers and productivity enthusiasts who want quick access to frequently used commands, all displayed beautifully on their screen background.

### Features
- Create a collage of up to **4 cheatsheets** on a 2x2 grid layout for readability.
- Convert Markdown cheatsheets into beautiful rendered images using **imgkit** and **markdown2**.
- Save the generated wallpaper in the `wallpapers` folder of the project.
- Update your desktop wallpaper automatically (currently configured for **GNOME**).

### Requirements
- Python 3.x
- `Pillow` (PIL fork) - for handling images
- `markdown2` - for rendering markdown to HTML
- `imgkit` - for rendering HTML to an image
- `wkhtmltopdf` - required by `imgkit` to convert HTML to images

### Installation
First, make sure you have Python installed, and then install the dependencies:

```sh
pip install -r requirements.txt
```

You also need to install `wkhtmltopdf` for rendering HTML:

- On Debian-based systems (Ubuntu, etc.):
  ```sh
  sudo apt-get install wkhtmltopdf
  ```
- On macOS with Homebrew:
  ```sh
  brew install wkhtmltopdf
  ```

### Directory Structure
The project uses a simple directory structure:

- **cheatsheets/**: Place your `.txt` markdown files here. Each file will be treated as a separate cheatsheet.
- **wallpapers/**: Generated wallpapers will be saved here. Make sure to create this directory before running the script.
- **tmp/**: Temporary files generated during the rendering process will be saved here.

If these directories are empty, consider adding `.gitkeep` files to ensure they're tracked by Git.

### Usage

1. **Create Cheatsheets**: Create markdown-formatted `.txt` files and put them in the `cheatsheets/` directory. These cheatsheets should include frequently used commands, scripts, or anything you'd like to have on your wallpaper.

2. **Run the Script**:

   - To generate a new wallpaper from existing cheatsheets:
     ```sh
     python allpaper.py
     ```

   - To create a new cheatsheet:
     ```sh
     python allpaper.py cheatify
     ```
     This will allow you to paste the content for the new cheatsheet right from the command line.

3. **Set Wallpaper**: The script will automatically generate a collage and set it as your desktop wallpaper if you're using GNOME. The generated wallpaper will be saved in `wallpapers/cheatsheet_collage.png`.

### Example Cheatsheet
Create a `.txt` file in the `cheatsheets` directory. Here's an example `git_cheatsheet.txt`:

```markdown
# Git Cheatsheet

## Basic Commands
- Initialize repo: `git init`
- Clone repo: `git clone <repo-url>`
- Add changes: `git add .`
- Commit changes: `git commit -m "your message"`
- Push to remote: `git push origin <branch>`
```

### Customization
- **Font Size and Style**: You can change the font size, style, and colors by modifying the `markdown_to_image()` function in `allpaper.py`. It uses inline CSS to style the rendered Markdown.
- **Number of Slots**: The script currently uses **4 slots** in a **2x2** grid for better readability, but you can adjust this if needed.

### Tips for Portability
To ensure that your project is portable:
- Make sure you include `.gitkeep` files in `tmp/` and `wallpapers/` directories to ensure they are tracked by Git.
- Use relative paths within the script to avoid hard-coded paths that could vary between systems.

### Contributing
Feel free to submit pull requests or open issues for new features, suggestions, or bugs.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgements
- **Pillow** for image manipulation.
- **markdown2** and **imgkit** for Markdown rendering.
- **wkhtmltopdf** for converting HTML to images.
