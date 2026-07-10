from PIL import Image

def analyze_image():
    try:
        img = Image.open("123_edited.jpg")
        w, h = img.size
        print(f"Dimensions: {w}x{h}")
        
        # Check colors of 4 corners
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((w - 1, 0)),
            img.getpixel((0, h - 1)),
            img.getpixel((w - 1, h - 1))
        ]
        print("Corner colors (RGB):", corners)
        
        # Check some edge pixels to see if the background is uniform
        edge_pixels = []
        for x in range(0, w, w // 10):
            edge_pixels.append(img.getpixel((x, 0)))
            edge_pixels.append(img.getpixel((x, h - 1)))
        for y in range(0, h, h // 10):
            edge_pixels.append(img.getpixel((0, y)))
            edge_pixels.append(img.getpixel((w - 1, y)))
            
        avg_r = sum(p[0] for p in edge_pixels) / len(edge_pixels)
        avg_g = sum(p[1] for p in edge_pixels) / len(edge_pixels)
        avg_b = sum(p[2] for p in edge_pixels) / len(edge_pixels)
        print(f"Average Edge RGB: ({avg_r:.1f}, {avg_g:.1f}, {avg_b:.1f})")
        
    except Exception as e:
        print("Error analyzing:", e)

if __name__ == "__main__":
    analyze_image()
