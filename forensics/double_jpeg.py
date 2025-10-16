import numpy as np
import cv2
from PIL import Image

def detect_double_jpeg_compression(image_path):
    """
    Detects signs of double JPEG compression.
    Multiple compressions indicate editing. Single compression suggests original photo.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: Double compression analysis results
    """
    results = {
        'double_compression_detected': False,
        'compression_history_score': 0.0,
        'quantization_mismatch': 0.0,
        'likely_edited': False,
        'compression_count_estimate': 1
    }
    
    try:
        # Only applicable to JPEG images
        with Image.open(image_path) as img:
            if img.format != 'JPEG':
                results['note'] = 'Not a JPEG image'
                return results
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return results
        
        # Perform DCT analysis on 8x8 blocks
        h, w = img.shape
        
        # Ensure dimensions are multiples of 8
        h = (h // 8) * 8
        w = (w // 8) * 8
        img = img[:h, :w]
        
        # Analyze DCT coefficients
        from scipy.fftpack import dct
        
        dct_coeffs = []
        
        # Sample multiple 8x8 blocks
        sample_count = 0
        max_samples = 100
        
        for i in range(0, h - 8, 8):
            for j in range(0, w - 8, 8):
                if sample_count >= max_samples:
                    break
                    
                block = img[i:i+8, j:j+8].astype(float)
                dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
                dct_coeffs.append(dct_block.flatten())
                sample_count += 1
            
            if sample_count >= max_samples:
                break
        
        if len(dct_coeffs) == 0:
            return results
        
        dct_coeffs = np.array(dct_coeffs)
        
        # Check for double quantization artifacts
        # In double compression, coefficients show periodic patterns
        
        # Analyze histogram of DCT coefficients
        for idx in range(1, min(10, dct_coeffs.shape[1])):  # Check first few AC coefficients
            coeffs = dct_coeffs[:, idx]
            
            # Create histogram
            hist, bins = np.histogram(coeffs, bins=50)
            
            # Look for periodic peaks (sign of double quantization)
            # Calculate second derivative of histogram
            if len(hist) > 2:
                hist_smooth = np.convolve(hist, np.ones(3)/3, mode='same')
                second_deriv = np.diff(np.diff(hist_smooth))
                
                # Count zero crossings (peaks/valleys)
                zero_crossings = np.sum(np.abs(np.diff(np.sign(second_deriv))))
                
                # Many zero crossings indicate periodic patterns
                if zero_crossings > 10:
                    results['double_compression_detected'] = True
                    results['compression_history_score'] += 1
        
        # Normalize score
        results['compression_history_score'] = float(results['compression_history_score'] / 10)
        
        # Estimate number of compressions
        if results['compression_history_score'] > 0.3:
            results['compression_count_estimate'] = 2
            results['likely_edited'] = True
        if results['compression_history_score'] > 0.6:
            results['compression_count_estimate'] = 3
            results['likely_edited'] = True
        
        # Check for blockiness differences
        # Double compression creates non-uniform blocking
        block_diffs = []
        
        for i in range(0, h - 16, 8):
            for j in range(0, w - 8, 8):
                # Boundary between blocks
                boundary = img[i+7:i+9, j:j+8]
                diff = np.abs(np.diff(boundary.astype(float), axis=0))
                block_diffs.append(np.mean(diff))
        
        if len(block_diffs) > 0:
            # High variance in block differences suggests double compression
            block_diff_variance = np.var(block_diffs)
            results['quantization_mismatch'] = float(block_diff_variance)
            
            if block_diff_variance > 20:
                results['double_compression_detected'] = True
                results['likely_edited'] = True
                
    except Exception as e:
        print(f"Error in double JPEG compression detection: {e}")
    
    return results
