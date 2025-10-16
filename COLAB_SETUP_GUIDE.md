# Google Colab Setup Guide for MetaForens

## 🚀 Quick Start (Recommended)

### Option 1: Simple Test (5 minutes)

Copy and paste this into a Google Colab cell:

```python
# Install and test MetaForens
!pip install -q pillow numpy opencv-python scipy scikit-image
import os
os.chdir('/content')
!rm -rf MetaForens
!git clone https://github.com/kingknight07/MetaForens.git
os.chdir('MetaForens')
!pip install -q -e .

# Test it works
import sys
sys.path.insert(0, '/content/MetaForens')
from metaforens import MetaForens
detector = MetaForens()
print(f"✅ MetaForens v{detector.version} loaded with {detector.analyses_count} analyses!")
```

### Option 2: Use Pre-Made Scripts

We provide ready-to-use Colab scripts:

1. **COLAB_QUICK_START.py** - Simple installation test (~2 minutes)
   - Tests installation
   - Verifies all imports work
   - Runs quick test on sample image
   
2. **COLAB_CIFAKE_TEST.py** - Full CIFAKE dataset testing (~30-60 minutes)
   - Downloads CIFAKE dataset (120K images)
   - Tests MetaForens on 200 sample images
   - Generates performance metrics, confusion matrix, visualizations
   - Provides downloadable reports

## 📋 Step-by-Step Instructions

### For COLAB_QUICK_START.py

1. Open [Google Colab](https://colab.research.google.com)
2. Create a new notebook
3. Copy code from: [COLAB_QUICK_START.py](https://github.com/kingknight07/MetaForens/blob/main/COLAB_QUICK_START.py)
4. Paste into a cell and run it (Shift+Enter)
5. Wait ~2 minutes for installation and testing

**Expected Output:**
```
✅ SUCCESS!
   Version: 1.0.0
   Analyses: 15
🎉 MetaForens is ready to use!
```

### For COLAB_CIFAKE_TEST.py (Full Dataset Testing)

1. Open [Google Colab](https://colab.research.google.com)
2. Create a new notebook
3. Copy code from: [COLAB_CIFAKE_TEST.py](https://github.com/kingknight07/MetaForens/blob/main/COLAB_CIFAKE_TEST.py)
4. Paste into a cell and run it
5. When prompted, upload your `kaggle.json` file
   - Get it from [Kaggle Settings](https://www.kaggle.com/settings)
   - Click "Create New API Token"
6. Wait for testing to complete (~30-60 minutes)
7. Download generated reports and visualizations

**Expected Output:**
```
✅ Overall Accuracy: XX.XX%
🎯 Precision (AI Detection): XX.XX%
🔍 Recall (AI Detection): XX.XX%
📈 F1-Score: XX.XX%
```

## 🔧 Troubleshooting

### Issue: "cannot import name 'detect_noise_inconsistency'"

**Solution:** This is fixed in the latest version. Ensure you're cloning the latest code:

```python
import os
os.chdir('/content')
!rm -rf MetaForens  # Clean old version
!git clone https://github.com/kingknight07/MetaForens.git
os.chdir('MetaForens')
!git log --oneline -1  # Should show commit dc279bb or later
```

### Issue: "FileNotFoundError: [Errno 2] No such file or directory"

**Solution:** Make sure you navigate to `/content` first:

```python
import os
os.chdir('/content')  # Start from /content
!git clone https://github.com/kingknight07/MetaForens.git
os.chdir('MetaForens')  # Then navigate to MetaForens
```

### Issue: "ModuleNotFoundError"

**Solution:** Install requirements and MetaForens in the correct order:

```python
os.chdir('/content/MetaForens')
!pip install -q -r requirements.txt
!pip install -q -e .
```

### Issue: Import still fails after installation

**Solution:** Restart runtime and try again:

1. Runtime → Restart runtime
2. Re-run all cells from the beginning
3. Make sure you're using the absolute path:
   ```python
   import sys
   sys.path.insert(0, '/content/MetaForens')
   ```

### Verify Installation Manually

Run this to check everything is correct:

```python
import os
os.chdir('/content/MetaForens')

# Check imports in metaforens.py
!grep "from forensics.noise_inconsistency" metaforens.py
# Expected: from forensics.noise_inconsistency import analyze_noise_inconsistency

!grep "from forensics.benford_analysis" metaforens.py
# Expected: from forensics.benford_analysis import benford_law_analysis

# Test actual import
from forensics.noise_inconsistency import analyze_noise_inconsistency
from forensics.benford_analysis import benford_law_analysis
print("✅ All imports working correctly!")
```

## 📊 Using MetaForens in Your Own Code

After successful installation, use MetaForens like this:

### Analyze a Single Image

```python
from metaforens import analyze_image

# Upload your image first (using Colab's file upload)
from google.colab import files
uploaded = files.upload()

# Analyze it
image_name = list(uploaded.keys())[0]
result = analyze_image(image_name)

print(f"Verdict: {result['verdict']}")
print(f"Confidence: {result['confidence']}")
print(f"AI Generated: {result['probabilities']['ai_generated']:.1f}%")
print(f"AI Edited: {result['probabilities']['ai_edited']:.1f}%")
print(f"Real Photo: {result['probabilities']['real_photo']:.1f}%")
```

### Analyze Multiple Images

```python
from metaforens import MetaForens
import os

detector = MetaForens()

# Analyze all images in a folder
image_folder = 'my_images'
results = []

for img_file in os.listdir(image_folder):
    if img_file.lower().endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(image_folder, img_file)
        result = detector.analyze(img_path)
        results.append({
            'image': img_file,
            'verdict': result['verdict'],
            'confidence': result['confidence'],
            'ai_prob': result['probabilities']['ai_generated']
        })

# Convert to DataFrame for easy viewing
import pandas as pd
df = pd.DataFrame(results)
print(df)
```

### Get Detailed Forensic Analysis

```python
result = detector.analyze('your_image.jpg')

# Access individual forensic analyses
print("\n🔬 Forensic Analysis Details:")
print(f"Metadata: {result['analyses']['metadata']}")
print(f"ELA Score: {result['analyses']['ela']}")
print(f"JPEG Artifacts: {result['analyses']['jpeg_artifacts']}")
print(f"GAN Detection: {result['analyses']['gan_fingerprint']}")
print(f"Noise Inconsistency: {result['analyses']['noise_inconsistency']}")
print(f"Benford's Law: {result['analyses']['benford_law']}")
```

## 🎯 Expected Performance

Based on our testing with the CIFAKE dataset:

- **Accuracy**: 70-90% (varies by image type)
- **Best Detection**: GAN-generated images
- **Challenging**: High-quality edited images
- **Special Handling**: Pre-2015 images (automatically marked as Real)

## 📚 Additional Resources

- **Repository**: https://github.com/kingknight07/MetaForens
- **Issues**: https://github.com/kingknight07/MetaForens/issues
- **Troubleshooting Guide**: [COLAB_TROUBLESHOOTING.md](https://github.com/kingknight07/MetaForens/blob/main/COLAB_TROUBLESHOOTING.md)
- **Library Documentation**: [README_LIBRARY.md](https://github.com/kingknight07/MetaForens/blob/main/README_LIBRARY.md)

## 💡 Tips for Best Results

1. **Image Quality**: Higher resolution images give better results
2. **JPEG Images**: Work best with JPEG compression analysis
3. **Metadata**: Include EXIF data when possible (helps with age detection)
4. **Batch Processing**: Use `batch_analyze()` for multiple images
5. **Old Photos**: Pre-2020 images automatically get adjusted scoring

## 🆘 Still Having Issues?

1. Check [COLAB_TROUBLESHOOTING.md](https://github.com/kingknight07/MetaForens/blob/main/COLAB_TROUBLESHOOTING.md)
2. Verify you have the latest code: `!git pull origin main`
3. Restart Colab runtime and try again
4. Open an issue on GitHub with error details
5. Email: shuklaayush0704@gmail.com

## ⭐ Quick Reference

| Task | Code |
|------|------|
| Install | `!git clone https://github.com/kingknight07/MetaForens.git && cd MetaForens && pip install -e .` |
| Import | `from metaforens import MetaForens, analyze_image` |
| Analyze | `result = analyze_image('image.jpg')` |
| Batch | `detector.batch_analyze(['img1.jpg', 'img2.jpg'])` |
| Summary | `print(detector.get_summary(result))` |

---

**Author**: kingknight07  
**Email**: shuklaayush0704@gmail.com  
**License**: MIT
