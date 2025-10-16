import numpy as np
from PIL import Image
from scipy.fft import fft2, fftshift
import os

def analyze_frequency(image_path):
    """
    Analyzes the frequency domain of an image.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        PIL.Image: A visual representation of the frequency spectrum.
    """
    try:
        with Image.open(image_path).convert('L') as img: # Convert to grayscale
            # Convert image to numpy array
            np_image = np.array(img)
            
            # Perform 2D Fast Fourier Transform
            f_transform = fft2(np_image)
            
            # Shift the zero frequency component to the center
            f_transform_shifted = fftshift(f_transform)
            
            # Get the magnitude spectrum (log scale for visualization)
            magnitude_spectrum = np.log(np.abs(f_transform_shifted) + 1)
            
            # Normalize the magnitude spectrum to 0-255 for image display
            magnitude_spectrum = (magnitude_spectrum / np.max(magnitude_spectrum)) * 255
            magnitude_spectrum = magnitude_spectrum.astype(np.uint8)
            
            # Create an image from the magnitude spectrum
            freq_image = Image.fromarray(magnitude_spectrum)
            
            return freq_image

    except Exception as e:
        print(f"Error during frequency analysis: {e}")
        return None

if __name__ == '__main__':
    # This is for testing purposes.
    try:
        # Create a dummy image for testing
        from PIL import Image
        dummy_img = Image.new('RGB', (256, 256), color = 'green')
        dummy_img.save("test_freq.jpg")
        
        freq_result = analyze_frequency("test_freq.jpg")
        if freq_result:
            freq_result.show()
            freq_result.save("freq_result.png")
            print("Frequency analysis complete. Result saved to freq_result.png")
        else:
            print("Frequency analysis failed.")
            
        os.remove("test_freq.jpg")

    except ImportError:
        print("Pillow or numpy or scipy is not installed. Cannot run test.")
    except Exception as e:
        print(f"An error occurred: {e}")
