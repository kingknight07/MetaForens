import numpy as np
from PIL import Image
import cv2

def analyze_jpeg_artifacts(image_path):
    """
    Analyzes JPEG compression artifacts and quantization tables.
    AI-generated images often have unusual or missing JPEG artifacts.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        dict: Analysis results including artifact scores.
    """
    results = {
        'has_jpeg_artifacts': False,
        'blockiness_score': 0.0,
        'compression_quality_estimate': 0,
        'is_suspicious': False
    }
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return results
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculate blockiness (8x8 JPEG blocks)
        h, w = gray.shape
        block_size = 8
        
        # Detect block boundaries by looking at intensity differences
        blockiness = 0
        count = 0
        
        for i in range(block_size, h, block_size):
            diff = np.abs(gray[i, :].astype(float) - gray[i-1, :].astype(float))
            blockiness += np.mean(diff)
            count += 1
            
        for j in range(block_size, w, block_size):
            diff = np.abs(gray[:, j].astype(float) - gray[:, j-1].astype(float))
            blockiness += np.mean(diff)
            count += 1
        
        if count > 0:
            blockiness /= count
            results['blockiness_score'] = float(blockiness)
            results['has_jpeg_artifacts'] = blockiness > 2.0
            
        # Estimate compression quality (simplified)
        # Higher blockiness suggests lower quality or multiple compressions
        if blockiness > 5.0:
            results['compression_quality_estimate'] = 'Low (60-75)'
        elif blockiness > 2.0:
            results['compression_quality_estimate'] = 'Medium (75-90)'
        else:
            results['compression_quality_estimate'] = 'High (90-100) or Uncompressed'
            # Very low blockiness in a supposed JPEG can indicate AI generation
            results['is_suspicious'] = True
            
    except Exception as e:
        print(f"Error in JPEG analysis: {e}")
        
    return results
