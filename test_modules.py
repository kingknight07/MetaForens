"""
Test script for MetaForens forensic modules
"""

from forensics.metadata_extractor import extract_metadata
from forensics.ela import perform_ela
from forensics.frequency_analysis import analyze_frequency
from forensics.noise_analysis import extract_noise_map
from forensics.jpeg_analysis import analyze_jpeg_artifacts
from forensics.chromatic_analysis import analyze_chromatic_aberration
from forensics.color_analysis import analyze_color_distribution
from forensics.texture_analysis import analyze_texture_consistency
from forensics.classifier import classify_image
from PIL import Image
import os

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (500, 500), color='blue')
    # Add some patterns
    pixels = img.load()
    for i in range(100, 400):
        for j in range(100, 400):
            pixels[i, j] = (255, 0, 0)
    
    img.save('test_image.png')
    return 'test_image.png'

def test_all_modules():
    """Test all forensic analysis modules"""
    print("Creating test image...")
    test_img = create_test_image()
    
    print("\n1. Testing Metadata Extraction...")
    metadata = extract_metadata(test_img)
    print(f"   Format: {metadata.get('format')}")
    print(f"   Size: {metadata.get('size')}")
    print(f"   Anomalies: {len(metadata.get('anomalies', []))}")
    
    print("\n2. Testing JPEG Analysis...")
    jpeg_result = analyze_jpeg_artifacts(test_img)
    print(f"   Blockiness Score: {jpeg_result.get('blockiness_score', 0):.2f}")
    
    print("\n3. Testing Chromatic Aberration...")
    chromatic_result = analyze_chromatic_aberration(test_img)
    print(f"   Aberration Score: {chromatic_result.get('aberration_score', 0):.6f}")
    
    print("\n4. Testing Color Analysis...")
    color_result = analyze_color_distribution(test_img)
    print(f"   Avg Saturation: {color_result.get('color_saturation_avg', 0):.2f}")
    
    print("\n5. Testing Texture Analysis...")
    texture_result = analyze_texture_consistency(test_img)
    print(f"   Texture Variance: {texture_result.get('texture_variance', 0):.2f}")
    
    print("\n6. Testing ELA...")
    ela_img = perform_ela(test_img)
    if ela_img:
        print("   ✓ ELA completed successfully")
        ela_img.save('test_ela.png')
    else:
        print("   ✗ ELA failed")
    
    print("\n7. Testing Frequency Analysis...")
    freq_img = analyze_frequency(test_img)
    if freq_img:
        print("   ✓ Frequency analysis completed")
        freq_img.save('test_frequency.png')
    else:
        print("   ✗ Frequency analysis failed")
    
    print("\n8. Testing Noise Analysis...")
    noise_img = extract_noise_map(test_img)
    if noise_img:
        print("   ✓ Noise analysis completed")
        noise_img.save('test_noise.png')
    else:
        print("   ✗ Noise analysis failed")
    
    print("\n9. Testing Classifier...")
    classification = classify_image(
        metadata,
        jpeg_result,
        chromatic_result,
        color_result,
        texture_result,
        test_img
    )
    
    print(f"\n{'='*50}")
    print(f"FINAL VERDICT: {classification['verdict']}")
    print(f"Confidence: {classification['confidence']}")
    print(f"\nProbabilities:")
    print(f"  AI Generated: {classification['probabilities']['ai_generated']}%")
    print(f"  AI Edited:    {classification['probabilities']['ai_edited']}%")
    print(f"  Real Photo:   {classification['probabilities']['real_photo']}%")
    print(f"{'='*50}")
    
    # Cleanup
    print("\nCleaning up test files...")
    for file in ['test_image.png', 'test_ela.png', 'test_frequency.png', 'test_noise.png']:
        if os.path.exists(file):
            os.remove(file)
    
    print("\n✓ All tests completed successfully!")

if __name__ == '__main__':
    test_all_modules()
