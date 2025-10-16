# MetaForens Library - Complete Setup Guide

## ✅ Repository Successfully Created!

**GitHub Repository**: https://github.com/kingknight07/MetaForens

**Author**: kingknight07  
**Email**: shuklaayush0704@gmail.com

---

## 📦 What's Included

### Core Library Files
- **`metaforens.py`** - Main library interface (MetaForens class)
- **`forensics/`** - All 15 forensic analysis modules
- **`setup.py`** - Package configuration for pip installation
- **`requirements.txt`** - Dependencies

### GUI Application
- **`app.py`** - Tkinter GUI application for visual analysis

### Documentation
- **`README_LIBRARY.md`** - Comprehensive library documentation
- **`QUICKSTART.md`** - Quick start guide with examples
- **`TECHNICAL_DETAILS.md`** - Deep technical documentation
- **`LICENSE`** - MIT License

### Examples
- **`examples/simple_analysis.py`** - Basic usage
- **`examples/batch_processing.py`** - Process multiple images
- **`examples/detailed_report.py`** - Generate detailed reports

### Testing
- **`test_library.py`** - Library functionality test
- **`test_modules.py`** - Individual module tests

---

## 🚀 Installation

### For Users

```bash
# Clone the repository
git clone https://github.com/kingknight07/MetaForens.git
cd MetaForens

# Install dependencies
pip install -r requirements.txt

# Install the library (optional, for system-wide usage)
pip install -e .
```

### For Developers

```bash
# Clone and install in development mode
git clone https://github.com/kingknight07/MetaForens.git
cd MetaForens
pip install -e .
```

---

## 💻 Usage as a Library

### 1. Simple Analysis

```python
from metaforens import MetaForens

# Create detector
detector = MetaForens()

# Analyze image
result = detector.analyze('path/to/image.jpg')

# Get results
print(result['verdict'])        # "AI Generated", "AI Edited / Modified", or "Likely Real Photo"
print(result['confidence'])     # "High", "Medium", or "Low"
print(result['probabilities'])  # Percentage breakdown
```

### 2. One-Liner (Quick Analysis)

```python
import metaforens

result = metaforens.analyze_image('photo.jpg')
print(result['verdict'])
```

### 3. Batch Processing

```python
from metaforens import MetaForens

detector = MetaForens()
images = ['img1.jpg', 'img2.jpg', 'img3.jpg']

results = detector.batch_analyze(images)

for path, result in results.items():
    print(f"{path}: {result['verdict']} ({result['confidence']})")
```

### 4. Detailed Forensic Data

```python
from metaforens import MetaForens

detector = MetaForens()
result = detector.analyze('image.jpg', return_detailed=True)

# Access individual forensic analyses
print(result['detailed']['cfa_detection'])
print(result['detailed']['gan_detection'])
print(result['detailed']['metadata'])
# ... 11 total analyses available
```

### 5. Formatted Summary

```python
from metaforens import MetaForens

detector = MetaForens()
result = detector.analyze('image.jpg')

# Print human-readable summary
print(detector.get_summary(result))
```

---

## 🎯 Result Structure

```python
{
    'verdict': 'AI Generated',           # Classification
    'confidence': 'High',                # Confidence level
    'probabilities': {
        'ai_generated': 85.2,            # Percentages
        'ai_edited': 10.5,
        'real_photo': 4.3
    },
    'evidence': {                        # Evidence from each test
        'cfa': [...],
        'gan': [...],
        'noise': [...]
        # ... 11 total
    },
    'categorized_evidence': {            # Grouped by verdict
        'ai_generated': [...],
        'ai_edited': [...],
        'real_photo': [...]
    },
    'raw_scores': {                      # Raw scores
        'ai_generated': 82.5,
        'ai_edited': 12.3,
        'real_photo': 5.2
    }
}
```

---

## 🖥️ Command Line Usage

```bash
# Using the library module
python metaforens.py image.jpg

# Using the test script
python test_library.py image.jpg

# Launch GUI
python app.py
```

---

## 📊 Features

### 15 Forensic Analyses
1. **CFA Pattern Detection** - Camera sensor patterns (15% weight)
2. **GAN Fingerprint** - AI generator signatures (12% weight)
3. **Noise Inconsistency** - Regional noise analysis (12% weight)
4. **Benford's Law** - Statistical validation (10% weight)
5. **Metadata Extraction** - EXIF data analysis (8% weight)
6. **Double JPEG** - Compression cycles (8% weight)
7. **Gradient Analysis** - Smoothness detection (8% weight)
8. **Chromatic Aberration** - Lens effects (7% weight)
9. **Color Distribution** - Color signatures (7% weight)
10. **Texture Consistency** - Clone detection (7% weight)
11. **JPEG Artifacts** - Compression quality (6% weight)

### Smart Features
- **Age Detection**: Automatically adjusts for old images (pre-2020)
- **Weighted Scoring**: Hierarchical importance of tests
- **Evidence Collection**: Detailed reasoning for verdicts
- **Confidence Levels**: High/Medium/Low reliability

---

## 🧪 Testing

```bash
# Test library functionality
python test_library.py path/to/test_image.jpg

# Test individual modules
python test_modules.py
```

---

## 📚 Documentation

- **README_LIBRARY.md** - Full library documentation
- **QUICKSTART.md** - Quick reference guide
- **TECHNICAL_DETAILS.md** - Algorithm details
- **examples/** - Usage examples with code

---

## 🤝 Integration Examples

### Web API (Flask)

```python
from flask import Flask, request, jsonify
from metaforens import MetaForens

app = Flask(__name__)
detector = MetaForens()

@app.route('/analyze', methods=['POST'])
def analyze():
    image_path = request.json['image_path']
    result = detector.analyze(image_path)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
```

### Automation

```python
from metaforens import MetaForens
import os

detector = MetaForens()

for filename in os.listdir('images'):
    if filename.endswith('.jpg'):
        result = detector.analyze(f'images/{filename}')
        if result['verdict'] == 'AI Generated':
            print(f"AI detected: {filename}")
```

---

## 📄 License

MIT License - see LICENSE file

---

## 👤 Author

**kingknight07**
- GitHub: https://github.com/kingknight07
- Email: shuklaayush0704@gmail.com
- Repository: https://github.com/kingknight07/MetaForens

---

## 🎉 Next Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kingknight07/MetaForens.git
   ```

2. **Install dependencies**:
   ```bash
   cd MetaForens
   pip install -r requirements.txt
   ```

3. **Test the library**:
   ```bash
   python test_library.py your_image.jpg
   ```

4. **Use in your code**:
   ```python
   from metaforens import MetaForens
   detector = MetaForens()
   result = detector.analyze('image.jpg')
   print(result['verdict'])
   ```

5. **Try the GUI**:
   ```bash
   python app.py
   ```

---

## 📞 Support

- **Issues**: https://github.com/kingknight07/MetaForens/issues
- **Email**: shuklaayush0704@gmail.com
- **Documentation**: See README_LIBRARY.md and QUICKSTART.md

---

**Happy Detecting! 🔍**
