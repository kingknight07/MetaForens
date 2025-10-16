"""
MetaForens Library - Live Demo
Quick demonstration of library capabilities
"""

from metaforens import MetaForens
import sys
import os

def demo():
    print("\n" + "=" * 70)
    print(" " * 20 + "MetaForens Library Demo")
    print("=" * 70)
    
    # Initialize
    print("\n📚 Initializing MetaForens library...")
    detector = MetaForens()
    print(f"✓ Version {detector.version} loaded successfully!\n")
    
    # Check for image argument
    if len(sys.argv) < 2:
        print("ℹ️  Usage: python demo.py <image_path>")
        print("\nExample:")
        print("  python demo.py photo.jpg")
        print("\n💡 This library can analyze images to detect:")
        print("  • AI-generated images (from GANs, Stable Diffusion, DALL-E, etc.)")
        print("  • AI-edited/manipulated images (Photoshop, filters, etc.)")
        print("  • Authentic camera photos")
        print("\n📊 Using 15 advanced forensic techniques:")
        print("  1. CFA Pattern Detection (camera sensor)")
        print("  2. GAN Fingerprint Detection")
        print("  3. Noise Inconsistency Analysis")
        print("  4. Benford's Law Statistical Test")
        print("  5. Metadata & EXIF Analysis")
        print("  6. Double JPEG Compression Detection")
        print("  7. Gradient Smoothness Analysis")
        print("  8. Chromatic Aberration Check")
        print("  9. Color Distribution Analysis")
        print(" 10. Texture Consistency Check")
        print(" 11. JPEG Artifact Analysis")
        print("\n🎯 Provides:")
        print("  • Classification verdict")
        print("  • Confidence level (High/Medium/Low)")
        print("  • Probability percentages")
        print("  • Detailed evidence from each test")
        
        print("\n" + "=" * 70)
        print("\n📝 Quick Usage Examples:")
        print("\n# Simple analysis:")
        print("from metaforens import MetaForens")
        print("detector = MetaForens()")
        print("result = detector.analyze('image.jpg')")
        print("print(result['verdict'])")
        
        print("\n# One-liner:")
        print("import metaforens")
        print("result = metaforens.analyze_image('photo.jpg')")
        
        print("\n# Batch processing:")
        print("detector = MetaForens()")
        print("results = detector.batch_analyze(['img1.jpg', 'img2.jpg', 'img3.jpg'])")
        
        print("\n" + "=" * 70)
        return
    
    image_path = sys.argv[1]
    
    # Validate file
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return
    
    print(f"🖼️  Analyzing: {os.path.basename(image_path)}")
    print("=" * 70)
    
    try:
        # Perform analysis
        result = detector.analyze(image_path)
        
        # Display results
        print("\n" + "=" * 70)
        print(" " * 25 + "ANALYSIS RESULTS")
        print("=" * 70)
        
        # Verdict
        verdict_icon = {
            'AI Generated': '🤖',
            'AI Edited / Modified': '✏️',
            'Likely Real Photo': '📸'
        }.get(result['verdict'], '❓')
        
        print(f"\n{verdict_icon}  VERDICT: {result['verdict']}")
        
        # Confidence
        conf_icon = {
            'High': '🟢',
            'Medium': '🟡',
            'Low': '🔴'
        }.get(result['confidence'], '⚪')
        
        print(f"{conf_icon}  CONFIDENCE: {result['confidence']}")
        
        # Probabilities
        print("\n📊 PROBABILITY BREAKDOWN:")
        probs = result['probabilities']
        
        # Create bar chart
        max_prob = max(probs.values())
        for category, pct in probs.items():
            bar_length = int((pct / 100) * 40)
            bar = '█' * bar_length + '░' * (40 - bar_length)
            label = category.replace('_', ' ').title()
            print(f"  {label:20} {bar} {pct:5.1f}%")
        
        # Evidence summary
        print("\n🔍 KEY EVIDENCE:")
        evidence = result.get('categorized_evidence', {})
        
        for category in ['ai_generated', 'ai_edited', 'real_photo']:
            items = evidence.get(category, [])
            if items:
                label = category.replace('_', ' ').title()
                print(f"\n  {label}:")
                for item in items[:3]:  # Show first 3 items
                    print(f"    • {item}")
                if len(items) > 3:
                    print(f"    ... and {len(items) - 3} more")
        
        # Raw scores
        print("\n📈 RAW SCORES:")
        scores = result.get('raw_scores', {})
        for category, score in scores.items():
            label = category.replace('_', ' ').title()
            print(f"  {label:20} {score:6.2f} points")
        
        print("\n" + "=" * 70)
        
        # Recommendation
        print("\n💡 RECOMMENDATION:")
        if result['confidence'] == 'High':
            if result['verdict'] == 'AI Generated':
                print("  This image is very likely AI-generated. High confidence detection.")
            elif result['verdict'] == 'Likely Real Photo':
                print("  This appears to be an authentic camera photo. High confidence.")
            else:
                print("  This image shows clear signs of editing/manipulation.")
        elif result['confidence'] == 'Medium':
            print("  Moderate confidence. Results suggest further investigation may be useful.")
        else:
            print("  Low confidence. Manual verification recommended.")
        
        print("\n" + "=" * 70)
        
        # Option for detailed report
        show_detailed = input("\n❓ Show detailed forensic analysis? (y/n): ").lower()
        if show_detailed == 'y':
            print("\n🔬 Generating detailed report...")
            result_detailed = detector.analyze(image_path, return_detailed=True)
            print("\n" + detector.get_summary(result_detailed))
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo()
