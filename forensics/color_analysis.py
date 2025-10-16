import numpy as np
from PIL import Image
import cv2

def analyze_color_distribution(image_path):
    """
    Analyzes color distribution and histogram patterns.
    AI-generated images often have unusual color distributions.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        dict: Analysis results.
    """
    results = {
        'histogram_uniformity': 0.0,
        'color_saturation_avg': 0.0,
        'unusual_patterns': False,
        'ai_signature_detected': False
    }
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return results
            
        # Convert to HSV for better color analysis
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Analyze saturation
        saturation = hsv[:, :, 1]
        results['color_saturation_avg'] = float(np.mean(saturation))
        
        # Calculate histogram for each channel
        hist_h = cv2.calcHist([hsv], [0], None, [256], [0, 256])
        hist_s = cv2.calcHist([hsv], [1], None, [256], [0, 256])
        hist_v = cv2.calcHist([hsv], [2], None, [256], [0, 256])
        
        # Calculate uniformity (entropy)
        def calculate_entropy(hist):
            hist = hist / np.sum(hist)
            hist = hist[hist > 0]
            return -np.sum(hist * np.log2(hist))
        
        entropy_h = calculate_entropy(hist_h)
        entropy_s = calculate_entropy(hist_s)
        entropy_v = calculate_entropy(hist_v)
        
        avg_entropy = (entropy_h + entropy_s + entropy_v) / 3.0
        results['histogram_uniformity'] = float(avg_entropy)
        
        # AI images often have very high saturation or unusual distributions
        if results['color_saturation_avg'] > 180:
            results['unusual_patterns'] = True
            results['ai_signature_detected'] = True
        
        # Check for unrealistic color peaks
        hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
        hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
        hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])
        
        # Look for unusual spikes in histogram
        for hist in [hist_b, hist_g, hist_r]:
            max_val = np.max(hist)
            mean_val = np.mean(hist)
            if max_val > mean_val * 50:  # Very high spike
                results['unusual_patterns'] = True
                
    except Exception as e:
        print(f"Error in color analysis: {e}")
        
    return results
