import os
from PIL import Image

def process_image(filepath, target_size=(256, 256)):
    print(f"Processing {filepath}")
    try:
        img = Image.open(filepath).convert("RGBA")
        
        # Check corners for background color
        width, height = img.size
        sample_points = [
            (0, 0), (width-1, 0), (0, height-1), (width-1, height-1),
            (width//2, 0), (0, height//2)
        ]
        
        bg_color = img.getpixel((0, 0))
        is_dark_bg = sum(bg_color[:3]) < 100
        
        datas = img.getdata()
        new_data = []
        
        for item in datas:
            luminance = 0.299*item[0] + 0.587*item[1] + 0.114*item[2]
            # Simple threshold for transparency
            if is_dark_bg: 
                 if luminance < 50:
                    new_data.append((0, 0, 0, 0))
                 else:
                    new_data.append(item)
            else: # Light bg
                 if luminance > 200:
                    new_data.append((255, 255, 255, 0))
                 else:
                    new_data.append(item)
                
        img.putdata(new_data)
        
        # Resize
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Save as PNG
        if "raw" in filepath:
             new_filepath = filepath.replace("_raw", "")
        else:
             new_filepath = os.path.splitext(filepath)[0] + ".png"
             
        img.save(new_filepath, "PNG")
        print(f"Saved to {new_filepath}")
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    base_dir = r"e:\Work\AndroidStudioProjects\Bite_Buddy_1.0\app\src\main\res\drawable"
    # Specific list for this run
    files = ["food_ramen_raw.png"]
    
    for f in files:
        full_path = os.path.join(base_dir, f)
        if os.path.exists(full_path):
            process_image(full_path)
        else:
            print(f"File not found: {full_path}")
