from PIL import Image, ImageDraw, ImageFont
import os

def create_flat_image(flat_no, bhk, location, rent, filename, color):
    # Create image
    img = Image.new('RGB', (400, 300), color)
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a system font
        title_font = ImageFont.truetype("arial.ttf", 28)
        detail_font = ImageFont.truetype("arial.ttf", 16)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        detail_font = ImageFont.load_default()
    
    # Draw text
    draw.text((200, 120), f"Flat {flat_no}", font=title_font, fill='white', anchor='mm')
    draw.text((200, 160), f"{bhk} BHK • {location}", font=detail_font, fill='white', anchor='mm')
    draw.text((200, 180), f"₹{rent:,}/month", font=detail_font, fill='white', anchor='mm')
    
    # Save image
    img.save(f"images/{filename}")
    print(f"Created {filename}")

# Create images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Create flat images
create_flat_image("A101", 2, "Sector 32", 25000, "flat1.jpg", (102, 126, 234))
create_flat_image("B202", 1, "Sector 60", 18000, "flat2.jpg", (240, 147, 251))
create_flat_image("C303", 3, "Sector 21", 35000, "flat3.jpg", (79, 172, 254))
create_flat_image("D404", 2, "Sector 22", 30000, "flat4.jpg", (79, 172, 254))
create_flat_image("E505", 2, "Sector 32", 25000, "flat5.jpg", (102, 126, 234))
create_flat_image("F606", 1, "Sector 60", 18000, "flat6.jpg", (240, 147, 251))
create_flat_image("G707", 3, "Sector 21", 35000, "flat7.jpg", (79, 172, 254))
create_flat_image("H808", 2, "Sector 22", 30000, "flat8.jpg", (79, 172, 254))

print("All flat images created successfully!")