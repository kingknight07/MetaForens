import numpy as np
import cv2
from scipy import ndimage

def analyze_noise_inconsistency(image_path):
    """
    Advanced local noise analysis - divides image into regions and compares noise.
    Real photos have consistent sensor noise. AI images have inconsistent or missing noise.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: Noise inconsistency analysis results
    """
    results = {
        'noise_variance_inconsistency': 0.0,
        'regions_analyzed': 0,
        'suspicious_regions': 0,
        'noise_variance_std': 0.0,
        'is_suspicious': False,
        'confidence': 'Low'
    }
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return results
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # Divide image into grid (e.g., 4x4 = 16 regions)
        grid_size = 4
        region_h = h // grid_size
        region_w = w // grid_size
        
        noise_variances = []
        
        for i in range(grid_size):
            for j in range(grid_size):
                # Extract region
                y_start = i * region_h
                y_end = (i + 1) * region_h
                x_start = j * region_w
                x_end = (j + 1) * region_w
                
                region = gray[y_start:y_end, x_start:x_end]
                
                # Extract noise using high-pass filter
                # Denoise the region
                denoised = cv2.GaussianBlur(region, (5, 5), 0)
                noise = region.astype(float) - denoised.astype(float)
                
                # Calculate noise variance
                noise_var = np.var(noise)
                noise_variances.append(noise_var)
        
        results['regions_analyzed'] = len(noise_variances)
        
        # Calculate standard deviation of noise variances
        # Real photos: consistent noise across regions (low std)
        # AI images: inconsistent noise (high std) or uniformly low noise
        noise_std = np.std(noise_variances)
        noise_mean = np.mean(noise_variances)
        
        results['noise_variance_std'] = float(noise_std)
        results['noise_variance_inconsistency'] = float(noise_std / (noise_mean + 1e-6))
        
        # Count suspicious regions (very low or very high noise)
        for nv in noise_variances:
            if nv < 1.0 or nv > noise_mean * 3:
                results['suspicious_regions'] += 1
        
        # Decision criteria
        # Very low average noise suggests AI generation
        if noise_mean < 5.0:
            results['is_suspicious'] = True
            results['confidence'] = 'High'
        # High inconsistency suggests editing/manipulation
        elif noise_std > 50.0:
            results['is_suspicious'] = True
            results['confidence'] = 'Medium'
        # Too many suspicious regions
        elif results['suspicious_regions'] > len(noise_variances) * 0.5:
            results['is_suspicious'] = True
            results['confidence'] = 'Medium'
            
    except Exception as e:
        print(f"Error in noise inconsistency analysis: {e}")
    
    return results
