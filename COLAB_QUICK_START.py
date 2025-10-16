# ============================================
# METAFORENS - QUICK START (COLAB)
# Minimal code to get MetaForens working
# ============================================

# STEP 1: Install dependencies
print("Installing dependencies...")
!pip install -q pillow numpy opencv-python scipy scikit-image

# STEP 2: Clone repository
import os
os.chdir('/content')  # Start in /content

print("\nCloning MetaForens...")
!rm -rf MetaForens  # Remove if exists
!git clone https://github.com/kingknight07/MetaForens.git

# STEP 3: Navigate and install
os.chdir('MetaForens')
print(f"Current directory: {os.getcwd()}")
print("\nRepository contents:")
!ls -la

# STEP 4: Install MetaForens
print("\nInstalling MetaForens...")
!pip install -q -e .

# STEP 5: Test imports
print("\n" + "="*60)
print("Testing MetaForens Import")
print("="*60)

import sys
sys.path.insert(0, '/content/MetaForens')

try:
    from metaforens import MetaForens, analyze_image
    detector = MetaForens()
    print(f"\n✅ SUCCESS!")
    print(f"   Version: {detector.version}")
    print(f"   Analyses: {detector.analyses_count}")
    print(f"\n🎉 MetaForens is ready to use!")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
    # Debug info
    print("\n🔍 Debugging Information:")
    print("Python path:")
    for p in sys.path[:5]:
        print(f"  - {p}")
    
    print("\nChecking metaforens.py imports:")
    !grep "from forensics" metaforens.py | head -15

# STEP 6: Quick test on a sample image
print("\n" + "="*60)
print("Quick Test")
print("="*60)

# Create a test image
from PIL import Image
import numpy as np

test_img = Image.new('RGB', (100, 100), color='red')
test_img.save('test_image.jpg')

print("\nAnalyzing test image...")
result = detector.analyze('test_image.jpg')

print(f"\nResults:")
print(f"  Verdict: {result['verdict']}")
print(f"  Confidence: {result['confidence']}")
print(f"  AI Probability: {result['probabilities']['ai_generated']:.1f}%")

print("\n" + "="*60)
print("✅ MetaForens is working correctly!")
print("="*60)
print("\nNext steps:")
print("1. Upload your images")
print("2. Use: result = detector.analyze('your_image.jpg')")
print("3. Or use the full CIFAKE test code")
print("\nRepository: https://github.com/kingknight07/MetaForens")
print("="*60)
