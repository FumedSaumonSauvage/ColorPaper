from PIL import Image, ImageDraw, ImageFont
import requests
import random

def get_color_name(hex_color):
    """Gets the closest color name for a given hex code using an online API."""
    try:
        url = f"https://www.thecolorapi.com/id?hex={hex_color[1:]}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        name = data["name"]["value"]
        return name
    except requests.exceptions.RequestException as e:
        print(f"Error fetching color name: {e}")
        return "Anonyme"
    except (KeyError, TypeError) as e:
        print(f"Error parsing API response: {e}")
        return None

def hex_to_rgb(hex_color):
    """Converts a hex color code to an RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def generate_uniform_color_image(hex_color, filename, size=(1920, 1080)):
    """Generates an image of a uniform color."""
    rgb_color = hex_to_rgb(hex_color)
    img = Image.new("RGB", size, rgb_color)

    draw = ImageDraw.Draw(img)
    color_name = get_color_name(hex_color)
    if color_name:
        name_text = color_name
        hex_text = hex_color
    else:
        name_text = "Anonyme"
        hex_text = hex_color

    fontHex = ImageFont.truetype("nudicamono-medium-webfont.ttf", 50)
    fontName = ImageFont.truetype("salome-webfont.ttf", 50)

    brightness = (rgb_color[0] * 299 + rgb_color[1] * 587 + rgb_color[2] * 114) / 1000
    text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)

    name_bbox = draw.textbbox((0, 0), name_text, font=fontName)
    name_width = name_bbox[2] - name_bbox[0]
    name_height = name_bbox[3] - name_bbox[1]

    hex_bbox = draw.textbbox((0, 0), hex_text, font=fontHex)
    hex_width = hex_bbox[2] - hex_bbox[0]
    hex_height = hex_bbox[3] - hex_bbox[1]

    total_height = name_height + hex_height + 10

    x = (size[0] - max(name_width, hex_width)) / 2
    y = (size[1] - total_height) / 2

    draw.text((x, y), name_text, fill=text_color, font=fontName)
    draw.text((x, y + name_height + 25), hex_text, fill=text_color, font=fontHex)

    img.save(filename)
    print(f"Image saved as {filename}")

if __name__ == "__main__":
    num_colors = 300
    screen_size = 1920, 1080

    for i in range(num_colors):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        filename = f"wp_{hex_color[1:]}.png"
        generate_uniform_color_image(hex_color, filename, screen_size)

    print(f"Generated {num_colors} random color images.") 
