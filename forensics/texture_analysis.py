import numpy as np
from PIL import Image
import cv2

def analyze_texture_consistency(image_path):
    """
    Analyzes texture patterns for consistency.
    AI-generated images can have repetitive or overly smooth textures.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        dict: Analysis results.
    """
    results = {
        'texture_variance': 0.0,
        'smoothness_score': 0.0,
        'repetition_detected': False,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return results
            
        # Calculate local variance
        kernel_size = 15
        mean = cv2.blur(img.astype(float), (kernel_size, kernel_size))
        sqr_mean = cv2.blur(img.astype(float)**2, (kernel_size, kernel_size))
        variance = sqr_mean - mean**2
        
        results['texture_variance'] = float(np.mean(variance))
        
        # Calculate smoothness using Laplacian
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        smoothness = np.var(laplacian)
        results['smoothness_score'] = float(smoothness)
        
        # AI images often have very low variance (too smooth) or very high (overly textured)
        if results['texture_variance'] < 50:
            results['is_suspicious'] = True
        elif results['texture_variance'] > 5000:
            results['is_suspicious'] = True
            
        # Check for repetitive patterns using autocorrelation
        # This is a simplified check
        h, w = img.shape
        if h > 100 and w > 100:
            sample = img[h//4:h//2, w//4:w//2]
            # Look for self-similarity
            result_corr = cv2.matchTemplate(img, sample, cv2.TM_CCOEFF_NORMED)
            max_val = np.max(result_corr)
            
            # Find peaks (excluding the center which is always 1.0)
            threshold = 0.8
            peaks = np.where(result_corr > threshold)
            if len(peaks[0]) > 2:  # More than just the original location
                results['repetition_detected'] = True
                
    except Exception as e:
        print(f"Error in texture analysis: {e}")
        
    return results
