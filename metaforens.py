"""
MetaForens - AI Image Detection Library
Detect AI-generated and AI-edited images using advanced forensic analysis.

Author: kingknight07
Email: shuklaayush0704@gmail.com
GitHub: https://github.com/kingknight07/MetaForens
"""

from PIL import Image
import os

# Import all forensic modules
from forensics.metadata_extractor import extract_metadata
from forensics.ela import perform_ela
from forensics.frequency_analysis import analyze_frequency
from forensics.noise_analysis import analyze_noise
from forensics.jpeg_analysis import analyze_jpeg
from forensics.chromatic_analysis import analyze_chromatic_aberration
from forensics.color_analysis import analyze_color_distribution
from forensics.texture_analysis import analyze_texture_consistency
from forensics.gan_detection import detect_gan_fingerprint
from forensics.noise_inconsistency import detect_noise_inconsistency
from forensics.benford_analysis import analyze_benford
from forensics.cfa_detection import detect_cfa_pattern
from forensics.double_jpeg import detect_double_jpeg
from forensics.gradient_analysis import analyze_gradients
from forensics.classifier import classify_image


class MetaForens:
    """
    Main class for AI image detection using forensic analysis.
    
    Usage:
        detector = MetaForens()
        result = detector.analyze('path/to/image.jpg')
        print(result['verdict'])  # "AI Generated", "AI Edited / Modified", or "Likely Real Photo"
        print(result['confidence'])  # "High", "Medium", or "Low"
        print(result['probabilities'])  # Percentage breakdown
    """
    
    def __init__(self):
        """Initialize the MetaForens detector."""
        self.version = "1.0.0"
    
    def analyze(self, image_path, return_detailed=False):
        """
        Analyze an image to detect AI generation or manipulation.
        
        Args:
            image_path (str): Path to the image file
            return_detailed (bool): If True, returns detailed analysis from all modules
        
        Returns:
            dict: Analysis results containing:
                - verdict (str): Classification result
                - confidence (str): Confidence level (High/Medium/Low)
                - probabilities (dict): Percentage breakdown
                - evidence (dict): Evidence for each category
                - raw_scores (dict): Raw scoring data
                - detailed (dict): Detailed analysis from all modules (if return_detailed=True)
        
        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If file is not a valid image
        """
        
        # Validate image path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            # Verify it's a valid image
            img = Image.open(image_path)
            img.verify()
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")
        
        # Perform all forensic analyses
        print(f"Analyzing image: {os.path.basename(image_path)}")
        
        # 1. Metadata extraction
        print("  [1/11] Extracting metadata...")
        metadata = extract_metadata(image_path)
        
        # 2. JPEG analysis
        print("  [2/11] Analyzing JPEG artifacts...")
        jpeg_analysis = analyze_jpeg(image_path)
        
        # 3. Chromatic aberration
        print("  [3/11] Checking chromatic aberration...")
        chromatic_analysis = analyze_chromatic_aberration(image_path)
        
        # 4. Color distribution
        print("  [4/11] Analyzing color distribution...")
        color_analysis = analyze_color_distribution(image_path)
        
        # 5. Texture consistency
        print("  [5/11] Checking texture consistency...")
        texture_analysis = analyze_texture_consistency(image_path)
        
        # 6. GAN fingerprint detection
        print("  [6/11] Detecting GAN fingerprints...")
        gan_detection = detect_gan_fingerprint(image_path)
        
        # 7. Noise inconsistency
        print("  [7/11] Analyzing noise patterns...")
        noise_inconsistency = detect_noise_inconsistency(image_path)
        
        # 8. Benford's Law analysis
        print("  [8/11] Running Benford's Law test...")
        benford_analysis = analyze_benford(image_path)
        
        # 9. CFA pattern detection
        print("  [9/11] Detecting camera sensor patterns...")
        cfa_detection = detect_cfa_pattern(image_path)
        
        # 10. Double JPEG compression
        print(" [10/11] Checking for double compression...")
        double_jpeg = detect_double_jpeg(image_path)
        
        # 11. Gradient analysis
        print(" [11/11] Analyzing image gradients...")
        gradient_analysis = analyze_gradients(image_path)
        
        # Classify the image
        print("  Classifying image...")
        result = classify_image(
            metadata=metadata,
            jpeg_analysis=jpeg_analysis,
            chromatic_analysis=chromatic_analysis,
            color_analysis=color_analysis,
            texture_analysis=texture_analysis,
            gan_detection=gan_detection,
            noise_inconsistency=noise_inconsistency,
            benford_analysis=benford_analysis,
            cfa_detection=cfa_detection,
            double_jpeg=double_jpeg,
            gradient_analysis=gradient_analysis,
            image_path=image_path
        )
        
        print(f"  ✓ Analysis complete: {result['verdict']} ({result['confidence']} confidence)")
        
        # Add detailed analysis if requested
        if return_detailed:
            result['detailed'] = {
                'metadata': metadata,
                'jpeg_analysis': jpeg_analysis,
                'chromatic_analysis': chromatic_analysis,
                'color_analysis': color_analysis,
                'texture_analysis': texture_analysis,
                'gan_detection': gan_detection,
                'noise_inconsistency': noise_inconsistency,
                'benford_analysis': benford_analysis,
                'cfa_detection': cfa_detection,
                'double_jpeg': double_jpeg,
                'gradient_analysis': gradient_analysis
            }
        
        return result
    
    def batch_analyze(self, image_paths, return_detailed=False):
        """
        Analyze multiple images.
        
        Args:
            image_paths (list): List of image file paths
            return_detailed (bool): If True, returns detailed analysis
        
        Returns:
            dict: Dictionary mapping image paths to their analysis results
        """
        results = {}
        total = len(image_paths)
        
        print(f"\nBatch analyzing {total} images...\n")
        
        for idx, image_path in enumerate(image_paths, 1):
            print(f"\n[{idx}/{total}] Processing: {os.path.basename(image_path)}")
            try:
                results[image_path] = self.analyze(image_path, return_detailed)
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                results[image_path] = {'error': str(e)}
        
        print(f"\n✓ Batch analysis complete: {total} images processed")
        return results
    
    def get_summary(self, result):
        """
        Get a human-readable summary of the analysis result.
        
        Args:
            result (dict): Result from analyze() method
        
        Returns:
            str: Formatted summary text
        """
        if 'error' in result:
            return f"Error: {result['error']}"
        
        summary = []
        summary.append("=" * 60)
        summary.append(f"VERDICT: {result['verdict']}")
        summary.append(f"CONFIDENCE: {result['confidence']}")
        summary.append("=" * 60)
        summary.append("\nProbability Breakdown:")
        summary.append(f"  AI Generated:  {result['probabilities']['ai_generated']:.1f}%")
        summary.append(f"  AI Edited:     {result['probabilities']['ai_edited']:.1f}%")
        summary.append(f"  Real Photo:    {result['probabilities']['real_photo']:.1f}%")
        
        if 'categorized_evidence' in result:
            evidence = result['categorized_evidence']
            
            if evidence.get('ai_generated'):
                summary.append("\n\nAI Generated Evidence:")
                for ev in evidence['ai_generated']:
                    summary.append(f"  • {ev}")
            
            if evidence.get('ai_edited'):
                summary.append("\n\nAI Edited Evidence:")
                for ev in evidence['ai_edited']:
                    summary.append(f"  • {ev}")
            
            if evidence.get('real_photo'):
                summary.append("\n\nReal Photo Evidence:")
                for ev in evidence['real_photo']:
                    summary.append(f"  • {ev}")
        
        summary.append("\n" + "=" * 60)
        return "\n".join(summary)


# Convenience function for quick analysis
def analyze_image(image_path, return_detailed=False):
    """
    Quick function to analyze a single image.
    
    Args:
        image_path (str): Path to the image file
        return_detailed (bool): If True, returns detailed analysis
    
    Returns:
        dict: Analysis results
    
    Example:
        >>> import metaforens
        >>> result = metaforens.analyze_image('photo.jpg')
        >>> print(result['verdict'])
        'Likely Real Photo'
    """
    detector = MetaForens()
    return detector.analyze(image_path, return_detailed)


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        detector = MetaForens()
        result = detector.analyze(image_path)
        print("\n" + detector.get_summary(result))
    else:
        print("MetaForens - AI Image Detection Library")
        print("Usage: python metaforens.py <image_path>")
        print("\nOr import in your Python code:")
        print("  from metaforens import MetaForens")
        print("  detector = MetaForens()")
        print("  result = detector.analyze('image.jpg')")
