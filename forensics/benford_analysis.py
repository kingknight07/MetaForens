import numpy as np
from collections import Counter

def benford_law_analysis(image_path):
    """
    Applies Benford's Law to pixel value distributions.
    Natural images follow Benford's Law. AI-generated images often deviate.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: Benford's Law analysis results
    """
    import cv2
    
    results = {
        'benford_deviation': 0.0,
        'chi_square_statistic': 0.0,
        'p_value': 0.0,
        'follows_benford': False,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return results
        
        # Get all pixel values
        pixels = img.flatten()
        
        # Calculate first digit distribution
        # Use gradient magnitudes for more meaningful analysis
        gx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(gx**2 + gy**2).flatten()
        
        # Remove zeros and get first digits
        magnitude = magnitude[magnitude > 0]
        first_digits = []
        
        for val in magnitude:
            # Get first significant digit
            val_str = f"{val:.10f}"
            for char in val_str:
                if char.isdigit() and char != '0':
                    first_digits.append(int(char))
                    break
        
        if len(first_digits) == 0:
            return results
        
        # Count first digits
        digit_counts = Counter(first_digits)
        observed = np.array([digit_counts.get(d, 0) for d in range(1, 10)])
        
        # Benford's Law expected distribution
        benford_expected = np.array([np.log10(1 + 1/d) for d in range(1, 10)])
        expected = benford_expected * len(first_digits)
        
        # Normalize
        if np.sum(observed) > 0:
            observed_freq = observed / np.sum(observed)
            
            # Calculate deviation from Benford's Law
            deviation = np.sum(np.abs(observed_freq - benford_expected))
            results['benford_deviation'] = float(deviation)
            
            # Chi-square test
            from scipy.stats import chisquare
            
            # Avoid division by zero
            expected_safe = np.where(expected < 1, 1, expected)
            chi2, p_val = chisquare(observed, expected_safe)
            
            results['chi_square_statistic'] = float(chi2)
            results['p_value'] = float(p_val)
            
            # If p-value < 0.05, significantly different from Benford's Law
            # This suggests artificial generation
            if p_val < 0.05:
                results['is_suspicious'] = True
            else:
                results['follows_benford'] = True
            
            # Additional check: deviation threshold
            if deviation > 0.15:
                results['is_suspicious'] = True
                
    except Exception as e:
        print(f"Error in Benford's Law analysis: {e}")
    
    return results
