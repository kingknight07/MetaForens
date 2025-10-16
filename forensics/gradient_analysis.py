import numpy as np
import cv2

def analyze_gradient_anomalies(image_path):
    """
    Analyzes gradient smoothness and naturalness.
    AI images often have unnaturally smooth gradients or sharp transitions.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: Gradient analysis results
    """
    results = {
        'gradient_smoothness': 0.0,
        'gradient_consistency': 0.0,
        'unnatural_smoothness_detected': False,
        'sharp_transition_count': 0,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return results
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculate gradients
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        
        gradient_magnitude = np.sqrt(gx**2 + gy**2)
        gradient_direction = np.arctan2(gy, gx)
        
        # Calculate gradient smoothness
        # Real photos have continuous gradients
        # AI images may have discontinuous gradients
        
        # Second-order gradients
        gxx = cv2.Sobel(gx, cv2.CV_64F, 1, 0, ksize=3)
        gyy = cv2.Sobel(gy, cv2.CV_64F, 0, 1, ksize=3)
        
        second_order_magnitude = np.sqrt(gxx**2 + gyy**2)
        
        # Calculate smoothness ratio
        # Low values = smooth (suspicious for AI)
        # High values = natural texture variation
        smoothness = np.mean(gradient_magnitude) / (np.mean(second_order_magnitude) + 1e-6)
        results['gradient_smoothness'] = float(smoothness)
        
        # Check for unnatural smoothness
        # AI-generated images often have smooth gradients (low second-order)
        if smoothness > 10.0:
            results['unnatural_smoothness_detected'] = True
            results['is_suspicious'] = True
        
        # Analyze gradient direction consistency
        # Calculate local variance in gradient direction
        direction_variance = []
        
        h, w = gradient_direction.shape
        window_size = 16
        
        for i in range(0, h - window_size, window_size):
            for j in range(0, w - window_size, window_size):
                window = gradient_direction[i:i+window_size, j:j+window_size]
                # Use circular variance for angles
                direction_variance.append(np.var(window))
        
        if len(direction_variance) > 0:
            avg_dir_variance = np.mean(direction_variance)
            results['gradient_consistency'] = float(avg_dir_variance)
            
            # Very low variance = too consistent (AI-like)
            if avg_dir_variance < 0.5:
                results['is_suspicious'] = True
        
        # Count sharp transitions
        # AI images sometimes have unnatural sharp edges
        threshold = np.percentile(gradient_magnitude, 95)
        sharp_edges = gradient_magnitude > threshold
        
        # Count connected components of sharp edges
        from scipy import ndimage
        labeled, num_features = ndimage.label(sharp_edges)
        results['sharp_transition_count'] = int(num_features)
        
        # Natural photos: moderate number of sharp transitions
        # AI images: either too few or too many
        if num_features < 10 or num_features > 1000:
            results['is_suspicious'] = True
        
        # Analyze gradient histogram
        # Natural images have specific gradient distributions
        hist, bins = np.histogram(gradient_magnitude, bins=50, range=(0, np.max(gradient_magnitude)))
        
        # Check for unnatural peaks in gradient histogram
        # Smooth decay expected in natural images
        peaks = 0
        for i in range(1, len(hist) - 1):
            if hist[i] > hist[i-1] and hist[i] > hist[i+1]:
                peaks += 1
        
        # Too many peaks suggests artificial generation
        if peaks > 5:
            results['is_suspicious'] = True
            
    except Exception as e:
        print(f"Error in gradient analysis: {e}")
    
    return results
