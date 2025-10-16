"""
Test script to verify MetaForens library functionality
Run this after installation to ensure everything works correctly.
"""

from metaforens import MetaForens
import sys

def test_library():
    """Test basic library functionality"""
    print("=" * 60)
    print("MetaForens Library Test")
    print("=" * 60)
    
    # Initialize detector
    print("\n1. Initializing detector...")
    try:
        detector = MetaForens()
        print(f"   ✓ MetaForens v{detector.version} initialized successfully")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Check if test image exists
    if len(sys.argv) > 1:
        test_image = sys.argv[1]
    else:
        print("\n2. No test image provided")
        print("   Usage: python test_library.py <path_to_image>")
        print("   Skipping image analysis test...")
        return True
    
    # Test single image analysis
    print(f"\n2. Testing single image analysis...")
    print(f"   Image: {test_image}")
    
    try:
        result = detector.analyze(test_image)
        print(f"   ✓ Analysis completed successfully")
        print(f"\n   Results:")
        print(f"   - Verdict: {result['verdict']}")
        print(f"   - Confidence: {result['confidence']}")
        print(f"   - AI Generated: {result['probabilities']['ai_generated']:.1f}%")
        print(f"   - AI Edited: {result['probabilities']['ai_edited']:.1f}%")
        print(f"   - Real Photo: {result['probabilities']['real_photo']:.1f}%")
    except FileNotFoundError:
        print(f"   ✗ Error: Image file not found: {test_image}")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test detailed analysis
    print(f"\n3. Testing detailed analysis...")
    try:
        result_detailed = detector.analyze(test_image, return_detailed=True)
        if 'detailed' in result_detailed:
            print(f"   ✓ Detailed analysis working")
            print(f"   - Available analyses: {len(result_detailed['detailed'])} modules")
        else:
            print(f"   ✗ Detailed analysis not returning expected data")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test summary generation
    print(f"\n4. Testing summary generation...")
    try:
        summary = detector.get_summary(result)
        if summary and len(summary) > 0:
            print(f"   ✓ Summary generation working")
        else:
            print(f"   ✗ Summary generation failed")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    
    # Print full summary
    print("\nFull Analysis Summary:")
    print(summary)
    
    return True

if __name__ == "__main__":
    success = test_library()
    sys.exit(0 if success else 1)
