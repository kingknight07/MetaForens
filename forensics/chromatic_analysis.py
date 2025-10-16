import numpy as np
from PIL import Image
import cv2

def analyze_chromatic_aberration(image_path):
    """
    Analyzes chromatic aberration patterns.
    Real camera lenses have characteristic chromatic aberration.
    AI-generated images often lack this or have inconsistent patterns.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        dict: Analysis results.
    """
    results = {
        'has_chromatic_aberration': False,
        'aberration_score': 0.0,
        'pattern_consistency': 0.0,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return results
            
        # Split into color channels
        b, g, r = cv2.split(img)
        
        # Apply edge detection on each channel
        edges_r = cv2.Canny(r, 100, 200)
        edges_g = cv2.Canny(g, 100, 200)
        edges_b = cv2.Canny(b, 100, 200)
        
        # Calculate edge misalignment (chromatic aberration shows as edge shifts)
        # XOR between channel edges
        rg_diff = cv2.bitwise_xor(edges_r, edges_g)
        gb_diff = cv2.bitwise_xor(edges_g, edges_b)
        rb_diff = cv2.bitwise_xor(edges_r, edges_b)
        
        # Calculate aberration score
        aberration = (np.sum(rg_diff) + np.sum(gb_diff) + np.sum(rb_diff)) / (3.0 * img.shape[0] * img.shape[1])
        results['aberration_score'] = float(aberration)
        
        # Real cameras have some chromatic aberration
        if aberration > 0.001:
            results['has_chromatic_aberration'] = True
        else:
            # Too perfect - suspicious for a real photo
            results['is_suspicious'] = True
            
        # Check pattern consistency (real aberration increases toward edges)
        h, w = img.shape[:2]
        center_region = img[h//4:3*h//4, w//4:3*w//4]
        edge_region = np.concatenate([
            img[0:h//4, :].flatten(),
            img[3*h//4:, :].flatten(),
            img[:, 0:w//4].flatten(),
            img[:, 3*w//4:].flatten()
        ])
        
        results['pattern_consistency'] = 0.5  # Placeholder
        
    except Exception as e:
        print(f"Error in chromatic aberration analysis: {e}")
        
    return results
