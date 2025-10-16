import numpy as np
from PIL import Image
import cv2 # OpenCV for denoising

def extract_noise_map(image_path):
    """
    Extracts a noise map from an image by subtracting a denoised version.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        PIL.Image: An image representing the noise map.
    """
    try:
        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError("Image not found or could not be read by OpenCV.")
            
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Denoise the image using a non-local means filter
        # This is a good filter for preserving edges while removing noise.
        denoised_img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        denoised_img_rgb = cv2.cvtColor(denoised_img, cv2.COLOR_BGR2RGB)

        # Convert to PIL images for subtraction
        original_pil = Image.fromarray(img_rgb)
        denoised_pil = Image.fromarray(denoised_img_rgb)

        # Calculate the difference to get the noise map
        noise_map = Image.fromarray(np.abs(np.array(original_pil, dtype=np.int16) - np.array(denoised_pil, dtype=np.int16)).astype(np.uint8))

        return noise_map

    except Exception as e:
        print(f"Error during noise analysis: {e}")
        return None

if __name__ == '__main__':
    # This is for testing purposes.
    try:
        # Create a dummy image for testing
        from PIL import Image
        dummy_img = Image.new('RGB', (256, 256), color = 'red')
        for i in range(256):
            for j in range(256):
                if (i+j) % 2 == 0:
                    dummy_img.putpixel((i,j), (0,0,0))
        dummy_img.save("test_noise.png")
        
        noise_result = extract_noise_map("test_noise.png")
        if noise_result:
            noise_result.show()
            noise_result.save("noise_result.png")
            print("Noise analysis complete. Result saved to noise_result.png")
        else:
            print("Noise analysis failed.")
            
        import os
        os.remove("test_noise.png")

    except (ImportError, NameError):
        print("Pillow, numpy, or opencv-python is not installed. Cannot run test.")
    except Exception as e:
        print(f"An error occurred: {e}")
