"""
Detailed Report Example
Generate comprehensive forensic reports with all analysis data
"""

from metaforens import MetaForens
import json

# Initialize detector
detector = MetaForens()

# Analyze with detailed results
image_path = "your_image.jpg"  # Replace with your image path

print(f"Generating detailed report for: {image_path}\n")

try:
    # Get detailed analysis
    result = detector.analyze(image_path, return_detailed=True)
    
    # Print main summary
    print(detector.get_summary(result))
    
    # Print detailed forensic data
    print("\n" + "=" * 60)
    print("DETAILED FORENSIC ANALYSIS")
    print("=" * 60)
    
    detailed = result['detailed']
    
    # CFA Detection
    print("\n1. CFA Pattern Detection (Camera Sensor):")
    cfa = detailed['cfa_detection']
    print(f"   Pattern Detected: {cfa.get('cfa_pattern_detected', False)}")
    print(f"   Pattern Type: {cfa.get('pattern_type', 'None')}")
    print(f"   Strength: {cfa.get('cfa_strength', 0):.4f}")
    
    # GAN Detection
    print("\n2. GAN Fingerprint Detection:")
    gan = detailed['gan_detection']
    print(f"   Signature Detected: {gan.get('gan_signature_detected', False)}")
    print(f"   Suspicious: {gan.get('is_suspicious', False)}")
    print(f"   High-Freq Score: {gan.get('high_freq_pattern_score', 0):.4f}")
    
    # Noise Inconsistency
    print("\n3. Noise Inconsistency Analysis:")
    noise = detailed['noise_inconsistency']
    print(f"   Suspicious: {noise.get('is_suspicious', False)}")
    print(f"   Confidence: {noise.get('confidence', 'N/A')}")
    print(f"   Suspicious Regions: {noise.get('suspicious_regions', 0)}/16")
    
    # Benford's Law
    print("\n4. Benford's Law Analysis:")
    benford = detailed['benford_analysis']
    print(f"   Follows Benford: {benford.get('follows_benford', False)}")
    print(f"   Deviation: {benford.get('benford_deviation', 0):.4f}")
    print(f"   P-Value: {benford.get('p_value', 0):.4f}")
    
    # Metadata
    print("\n5. Metadata Analysis:")
    metadata = detailed['metadata']
    print(f"   Has EXIF: {bool(metadata.get('exif', {}))}")
    print(f"   Software Tags: {metadata.get('software_tags', [])}")
    print(f"   Anomalies: {len(metadata.get('anomalies', []))}")
    
    # Double JPEG
    print("\n6. Double JPEG Compression:")
    djpeg = detailed['double_jpeg']
    print(f"   Double Compression: {djpeg.get('double_compression_detected', False)}")
    print(f"   Compression Count: {djpeg.get('compression_count_estimate', 1)}")
    
    # Gradient Analysis
    print("\n7. Gradient Analysis:")
    gradient = detailed['gradient_analysis']
    print(f"   Unnatural Smoothness: {gradient.get('unnatural_smoothness_detected', False)}")
    print(f"   Smoothness Score: {gradient.get('gradient_smoothness', 0):.2f}")
    
    # Chromatic Aberration
    print("\n8. Chromatic Aberration:")
    chromatic = detailed['chromatic_analysis']
    print(f"   Has Aberration: {chromatic.get('has_chromatic_aberration', False)}")
    print(f"   Aberration Score: {chromatic.get('aberration_score', 0):.5f}")
    
    # Color Analysis
    print("\n9. Color Distribution:")
    color = detailed['color_analysis']
    print(f"   AI Signature: {color.get('ai_signature_detected', False)}")
    print(f"   Saturation Avg: {color.get('color_saturation_avg', 0):.2f}")
    
    # Texture Analysis
    print("\n10. Texture Consistency:")
    texture = detailed['texture_analysis']
    print(f"    Repetition Detected: {texture.get('repetition_detected', False)}")
    print(f"    Texture Variance: {texture.get('texture_variance', 0):.2f}")
    
    # JPEG Analysis
    print("\n11. JPEG Artifacts:")
    jpeg = detailed['jpeg_analysis']
    print(f"    Suspicious: {jpeg.get('is_suspicious', False)}")
    print(f"    Quality Estimate: {jpeg.get('compression_quality_estimate', 'Unknown')}")
    
    print("\n" + "=" * 60)
    
    # Optional: Save to JSON file
    save_json = input("\nSave detailed report to JSON? (y/n): ").lower()
    if save_json == 'y':
        output_file = image_path.replace('.jpg', '_report.json').replace('.png', '_report.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"✓ Report saved to: {output_file}")
    
except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found")
except Exception as e:
    print(f"Error: {e}")
