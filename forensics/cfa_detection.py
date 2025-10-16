import numpy as np
import cv2

def detect_cfa_pattern(image_path):
    """
    Detects Color Filter Array (CFA) patterns (Bayer pattern).
    Real digital cameras use CFA sensors. AI images lack this pattern.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: CFA pattern detection results
    """
    results = {
        'cfa_pattern_detected': False,
        'cfa_strength': 0.0,
        'pattern_type': 'None',
        'is_real_camera': False,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return results
        
        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]
        
        # Sample a region from the center (avoiding edges)
        center_h, center_w = h // 2, w // 2
        sample_size = min(256, h // 4, w // 4)
        
        region = img_rgb[
            center_h - sample_size:center_h + sample_size,
            center_w - sample_size:center_w + sample_size
        ]
        
        # Separate color channels
        r = region[:, :, 0].astype(float)
        g = region[:, :, 1].astype(float)
        b = region[:, :, 2].astype(float)
        
        # Check for Bayer pattern artifacts (2x2 periodic pattern)
        # In Bayer pattern: RGGB or GBRG arrangement
        
        # Calculate correlation at different offsets
        def calculate_periodic_correlation(channel, offset=2):
            """Check for periodic patterns"""
            h, w = channel.shape
            if h < offset * 2 or w < offset * 2:
                return 0.0
                
            # Compare pixels with their offset neighbors
            shifted_h = channel[offset:, :]
            shifted_v = channel[:, offset:]
            original_h = channel[:-offset, :]
            original_v = channel[:, :-offset]
            
            # Calculate correlation
            corr_h = np.corrcoef(shifted_h.flatten(), original_h.flatten())[0, 1]
            corr_v = np.corrcoef(shifted_v.flatten(), original_v.flatten())[0, 1]
            
            return (corr_h + corr_v) / 2
        
        # Check for 2-pixel periodicity (CFA signature)
        cfa_corr_r = calculate_periodic_correlation(r, 2)
        cfa_corr_g = calculate_periodic_correlation(g, 2)
        cfa_corr_b = calculate_periodic_correlation(b, 2)
        
        # Average CFA correlation
        cfa_strength = (cfa_corr_r + cfa_corr_g + cfa_corr_b) / 3
        results['cfa_strength'] = float(cfa_strength)
        
        # Real cameras show weak but detectable CFA patterns
        # Correlation around 0.7-0.95 is typical for real photos
        if 0.65 < cfa_strength < 0.98:
            results['cfa_pattern_detected'] = True
            results['is_real_camera'] = True
            results['pattern_type'] = 'Bayer-like'
        elif cfa_strength > 0.98:
            # Too perfect - might be upscaled or AI
            results['is_suspicious'] = True
            results['pattern_type'] = 'Suspiciously perfect'
        else:
            # No CFA pattern - likely not from a real camera
            results['is_suspicious'] = True
            results['pattern_type'] = 'No CFA detected'
        
        # Additional check: Green channel has higher resolution in Bayer
        g_detail = np.std(g)
        r_detail = np.std(r)
        b_detail = np.std(b)
        
        # In real Bayer, green channel typically has more detail
        if g_detail > max(r_detail, b_detail) * 1.1:
            results['is_real_camera'] = True
            
    except Exception as e:
        print(f"Error in CFA pattern detection: {e}")
    
    return results
