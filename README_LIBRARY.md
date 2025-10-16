# MetaForens - AI Image Detection Library

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Advanced forensic analysis library to detect AI-generated and AI-edited images using multiple detection techniques.

## 🚀 Features

- **15 Forensic Analysis Techniques** including GAN fingerprint detection, CFA pattern analysis, noise inconsistency detection, and more
- **Smart Age Detection** - Automatically adjusts analysis for old images (pre-AI era)
- **High Accuracy** - Multi-layered analysis with weighted scoring system
- **Easy to Use** - Simple API for both single and batch image analysis
- **GUI Application** - Optional Tkinter interface for visual analysis
- **Detailed Reports** - Comprehensive evidence and probability breakdowns

## 📦 Installation

### From PyPI (when published)
```bash
pip install metaforens
```

### From Source
```bash
git clone https://github.com/kingknight07/MetaForens.git
cd MetaForens
pip install -r requirements.txt
pip install -e .
```

## 💻 Usage

### As a Library

**Simple Analysis:**
```python
from metaforens import MetaForens

# Initialize detector
detector = MetaForens()

# Analyze an image
result = detector.analyze('path/to/image.jpg')

# Get verdict
print(result['verdict'])        # "AI Generated", "AI Edited / Modified", or "Likely Real Photo"
print(result['confidence'])     # "High", "Medium", or "Low"
print(result['probabilities'])  # {'ai_generated': 85.2, 'ai_edited': 10.5, 'real_photo': 4.3}

# Print formatted summary
print(detector.get_summary(result))
```

**Batch Analysis:**
```python
from metaforens import MetaForens

detector = MetaForens()
image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']

# Analyze multiple images
results = detector.batch_analyze(image_paths)

for path, result in results.items():
    print(f"{path}: {result['verdict']} ({result['confidence']})")
```

**Detailed Analysis:**
```python
from metaforens import MetaForens

detector = MetaForens()

# Get detailed forensic data
result = detector.analyze('image.jpg', return_detailed=True)

# Access individual analysis results
print(result['detailed']['cfa_detection'])
print(result['detailed']['gan_detection'])
print(result['detailed']['metadata'])
```

**Quick Function:**
```python
import metaforens

# One-liner analysis
result = metaforens.analyze_image('photo.jpg')
print(result['verdict'])
```

### Command Line

```bash
# Analyze a single image
python metaforens.py image.jpg

# Or if installed via pip
metaforens image.jpg
```

### GUI Application

```bash
# Launch the GUI
python app.py
```

## 🔬 Detection Techniques

MetaForens uses 15 advanced forensic analysis techniques:

### Basic Forensics
1. **Metadata Extraction** - EXIF data analysis and anomaly detection
2. **Error Level Analysis (ELA)** - Compression artifact detection
3. **Frequency Analysis** - FFT-based pattern detection
4. **Noise Analysis** - Sensor noise extraction

### Advanced Forensics
5. **GAN Fingerprint Detection** - Identifies AI generator signatures
6. **CFA Pattern Detection** - Camera sensor pattern analysis (strongest real photo indicator)
7. **Noise Inconsistency** - Regional noise variance analysis
8. **Benford's Law** - Statistical distribution validation
9. **Double JPEG Compression** - Multiple compression cycle detection
10. **Gradient Analysis** - Unnatural smoothness detection
11. **Chromatic Aberration** - Lens aberration presence
12. **Color Distribution** - AI color signature detection
13. **Texture Consistency** - Clone stamp and repetition detection
14. **JPEG Artifacts** - Compression quality analysis

### Smart Features
15. **Age Detection** - Automatically identifies and adjusts for old images (pre-2020)

## 📊 Result Format

```python
{
    'verdict': 'AI Generated',           # Classification result
    'confidence': 'High',                # Confidence level
    'probabilities': {
        'ai_generated': 85.2,            # Percentage scores
        'ai_edited': 10.5,
        'real_photo': 4.3
    },
    'evidence': {                        # Detailed evidence from each test
        'cfa': [...],
        'gan': [...],
        'noise': [...],
        # ... more
    },
    'categorized_evidence': {            # Evidence by category
        'ai_generated': [...],
        'ai_edited': [...],
        'real_photo': [...]
    },
    'raw_scores': {                      # Raw scoring data
        'ai_generated': 82.5,
        'ai_edited': 12.3,
        'real_photo': 5.2
    }
}
```

## 🎯 Accuracy

- **AI-Generated Images**: ~90% accuracy with HIGH confidence
- **Real Camera Photos**: ~85% accuracy with HIGH confidence
- **Edited Images**: ~75% accuracy with MEDIUM confidence
- **Old Images (pre-2020)**: Automatically adjusted thresholds for better accuracy

## 🛠️ Requirements

- Python 3.7+
- NumPy >= 1.19.0
- Pillow >= 8.0.0
- OpenCV >= 4.5.0
- SciPy >= 1.5.0

## 📝 Examples

See the `examples/` directory for more usage examples:
- `simple_analysis.py` - Basic single image analysis
- `batch_processing.py` - Analyze multiple images
- `detailed_report.py` - Generate detailed forensic reports

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**kingknight07**
- Email: shuklaayush0704@gmail.com
- GitHub: [@kingknight07](https://github.com/kingknight07)

## 🙏 Acknowledgments

- Advanced forensic techniques based on research in digital image forensics
- GAN detection methods inspired by academic papers on deepfake detection
- CFA pattern detection for camera authentication

## 📚 Citation

If you use MetaForens in your research, please cite:

```bibtex
@software{metaforens2025,
  author = {kingknight07},
  title = {MetaForens: Advanced AI Image Detection Library},
  year = {2025},
  url = {https://github.com/kingknight07/MetaForens}
}
```

## ⚠️ Disclaimer

MetaForens is a forensic analysis tool designed to assist in detecting AI-generated or manipulated images. While it uses advanced techniques and achieves high accuracy, no detection method is 100% perfect. Results should be used as part of a comprehensive verification process, not as the sole determinant of image authenticity.
