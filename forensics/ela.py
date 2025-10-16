from PIL import Image, ImageChops, ImageEnhance
import os

def perform_ela(image_path, quality=90):
    """
    Performs Error Level Analysis (ELA) on an image.
    
    Args:
        image_path (str): The path to the image file.
        quality (int): The JPEG quality to use for re-saving the image.
        
    Returns:
        PIL.Image: An image representing the ELA result.
    """
    try:
        original_image = Image.open(image_path).convert('RGB')
        
        # Re-save the image at a specific quality
        temp_filename = 'temp_ela_image.jpg'
        original_image.save(temp_filename, 'JPEG', quality=quality)
        
        # Load the re-saved image
        resaved_image = Image.open(temp_filename)
        
        # Find the difference between the original and re-saved images
        ela_image = ImageChops.difference(original_image, resaved_image)
        
        # Enhance the ELA image to make differences more visible
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0:
            max_diff = 1
        
        scale = 255.0 / max_diff
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        
        # Clean up the temporary file
        os.remove(temp_filename)
        
        return ela_image
        
    except Exception as e:
        print(f"Error during ELA: {e}")
        # Clean up if error occurs
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return None

if __name__ == '__main__':
    # This is for testing purposes.
    # You would replace 'test_image.jpg' with a path to an actual image.
    try:
        # Create a dummy image for testing
        from PIL import Image
        dummy_img = Image.new('RGB', (100, 100), color = 'blue')
        dummy_img.save("test_ela.jpg")
        
        ela_result = perform_ela("test_ela.jpg")
        if ela_result:
            ela_result.show()
            ela_result.save("ela_result.png")
            print("ELA analysis complete. Result saved to ela_result.png")
        else:
            print("ELA analysis failed.")
            
        os.remove("test_ela.jpg")

    except ImportError:
        print("Pillow is not installed. Cannot run test.")
    except Exception as e:
        print(f"An error occurred: {e}")
