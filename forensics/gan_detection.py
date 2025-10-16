import numpy as np
from PIL import Image
from scipy import fftpack
from scipy.stats import chisquare
import cv2

def detect_gan_fingerprint(image_path):
    """
    Advanced frequency domain analysis to detect GAN fingerprints.
    GANs often leave specific patterns in high-frequency components.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: GAN fingerprint analysis results
    """
    results = {
        'gan_signature_detected': False,
        'frequency_anomaly_score': 0.0,
        'high_freq_pattern_score': 0.0,
        'spectral_residual_score': 0.0,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return results
        
        # Resize for consistent analysis
        img = cv2.resize(img, (512, 512))
        
        # Perform 2D DCT (Discrete Cosine Transform)
        dct = fftpack.dct(fftpack.dct(img.T, norm='ortho').T, norm='ortho')
        
        # Analyze high-frequency components (where GAN artifacts appear)
        h, w = dct.shape
        
        # Extract different frequency bands
        low_freq = dct[:h//4, :w//4]
        mid_freq = dct[h//4:h//2, w//4:w//2]
        high_freq = dct[h//2:, w//2:]
        
        # Calculate energy in each band
        low_energy = np.sum(np.abs(low_freq))
        mid_energy = np.sum(np.abs(mid_freq))
        high_energy = np.sum(np.abs(high_freq))
        
        total_energy = low_energy + mid_energy + high_energy
        
        if total_energy > 0:
            high_freq_ratio = high_energy / total_energy
            results['high_freq_pattern_score'] = float(high_freq_ratio)
            
            # Real photos have more high-frequency content
            # AI images tend to be smoother with less high-frequency detail
            if high_freq_ratio < 0.05:  # Very low high-frequency content
                results['gan_signature_detected'] = True
                results['is_suspicious'] = True
        
        # Analyze radial frequency spectrum
        # GANs often show unusual circular patterns
        f_transform = np.fft.fft2(img)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.abs(f_shift)
        
        # Calculate radial average
        center_y, center_x = h // 2, w // 2
        y, x = np.ogrid[:h, :w]
        r = np.sqrt((x - center_x)**2 + (y - center_y)**2).astype(int)
        
        # Radial profile
        radial_mean = np.bincount(r.ravel(), magnitude_spectrum.ravel()) / np.bincount(r.ravel())
        
        # Check for unnatural peaks or valleys
        # AI images often show periodic patterns
        if len(radial_mean) > 10:
            radial_diff = np.diff(radial_mean[:min(50, len(radial_mean))])
            anomaly_score = np.std(radial_diff)
            results['frequency_anomaly_score'] = float(anomaly_score)
            
            # High variation in radial spectrum suggests AI generation
            if anomaly_score > 1000:
                results['is_suspicious'] = True
        
        # Spectral residual analysis (detects upsampling artifacts)
        log_spectrum = np.log(magnitude_spectrum + 1)
        spectral_residual = log_spectrum - cv2.GaussianBlur(log_spectrum, (3, 3), 0)
        residual_energy = np.sum(np.abs(spectral_residual))
        results['spectral_residual_score'] = float(residual_energy)
        
        # AI images often have lower spectral residual
        if residual_energy < 50000:
            results['is_suspicious'] = True
            
    except Exception as e:
        print(f"Error in GAN fingerprint detection: {e}")
    
    return results
