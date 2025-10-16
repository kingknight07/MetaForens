# MetaForens - Advanced AI Image Detection Tool

MetaForens is a comprehensive forensic analysis tool designed to detect whether an image is AI-generated, AI-edited, or a genuine photograph using state-of-the-art forensic techniques.

## Features

### 🔬 Advanced Multi-Layer Forensic Analysis (15 Techniques)

#### Core Analyses

1. **Metadata Extraction**
   - Extracts EXIF data (camera info, timestamps, GPS)
   - Detects software editing signatures
   - Flags missing or suspicious metadata

2. **JPEG Artifact Analysis**
   - Analyzes compression patterns and blockiness
   - Detects quality inconsistencies
   - Identifies multiple compression artifacts

3. **Chromatic Aberration Analysis**
   - Checks for natural lens aberration patterns
   - Detects absence of expected optical effects
   - Validates camera lens signatures

4. **Color Distribution Analysis**
   - Analyzes histogram patterns
   - Detects unusual color saturation
   - Identifies AI-specific color signatures

5. **Texture Consistency Analysis**
   - Measures texture variance and smoothness
   - Detects repetitive patterns (clone stamp)
   - Identifies unnatural texture distributions

#### 🚀 Advanced Forensic Techniques (NEW!)

6. **GAN Fingerprint Detection** ⭐
   - Deep frequency domain analysis using DCT/FFT
   - Detects specific patterns left by Generative Adversarial Networks
   - Analyzes high-frequency components and spectral residuals
   - Identifies unnatural smoothness characteristic of AI generation

7. **Advanced Noise Inconsistency Analysis** ⭐
   - Divides image into regions for local noise analysis
   - Compares noise patterns across the image
   - Real photos have consistent sensor noise
   - AI images show inconsistent or artificially low noise

8. **Benford's Law Analysis** ⭐
   - Applies statistical analysis to pixel gradient distributions
   - Natural images follow Benford's Law
   - AI-generated images often deviate significantly
   - Uses chi-square test for statistical validation

9. **CFA (Color Filter Array) Pattern Detection** ⭐⭐ (MOST IMPORTANT)
   - Detects Bayer pattern from digital camera sensors
   - Real cameras always have CFA patterns
   - AI-generated images completely lack this pattern
   - Strongest indicator of real vs. AI images

10. **Double JPEG Compression Detection** ⭐
    - Detects signs of multiple JPEG compressions
    - Analyzes quantization table mismatches
    - Multiple compressions indicate editing
    - Estimates number of compression cycles

11. **Gradient Anomaly Detection** ⭐
    - Analyzes gradient smoothness and naturalness
    - Detects unnaturally smooth transitions
    - AI images often have unusual gradient patterns
    - Checks for sharp artificial boundaries

#### Visual Forensic Tools

12. **Error Level Analysis (ELA)**
    - Visualizes compression inconsistencies
    - Highlights edited regions
    - Shows tampering artifacts

13. **Frequency Domain Analysis**
    - Analyzes FFT patterns
    - Detects unusual frequency signatures
    - Identifies AI-generation markers

14. **Noise Pattern Analysis**
    - Extracts camera sensor noise visually
    - Shows noise distribution map
    - Validates sensor authenticity

### 🎯 Advanced AI-Powered Classification

The tool combines ALL forensic features using an advanced weighted scoring system:

**Weighted Priority System:**
- CFA Pattern Detection: 15% (Highest - most reliable)
- GAN Fingerprint: 12%
- Noise Inconsistency: 12%
- Benford's Law: 10%
- Double JPEG: 10%
- Gradient Analysis: 8%
- Metadata: 8%
- Chromatic Aberration: 8%
- JPEG Analysis: 7%
- Color & Texture: 5% each

**Outputs:**
- **Final Verdict**: AI Generated, AI Edited, or Likely Real Photo
- **Confidence Level**: High (>65%), Medium (50-65%), or Low (<50%)
- **Probability Scores**: Precise percentage for each category
- **Detailed Evidence**: Comprehensive list of findings for each analysis
- **Raw Scores**: Internal scoring breakdown for transparency

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- Pillow (PIL)
- NumPy
- SciPy
- OpenCV (cv2)

## Usage

Run the application:

```bash
python app.py
```

### Steps:
1. Click "Upload Image" and select a JPEG or PNG file
2. Click "Analyze Image" to start the forensic analysis
3. View the verdict and probability scores in the left panel
4. Examine forensic visualizations in the tabs:
   - Original Image
   - ELA (Error Level Analysis)
   - Frequency Spectrum
   - Noise Map
5. Read detailed analysis results in the scrollable text area

## How It Works

### Analysis Pipeline

```
Input Image
    ↓
Metadata Extraction → Feature Score
    ↓
JPEG Analysis → Feature Score
    ↓
Chromatic Analysis → Feature Score
    ↓
Color Analysis → Feature Score
    ↓
Texture Analysis → Feature Score
    ↓
Visual Analyses (ELA, Frequency, Noise)
    ↓
Feature Fusion (Weighted Scoring)
    ↓
Classification Algorithm
    ↓
Final Verdict + Probabilities
```

### Scoring System

Each forensic test contributes to three scores:
- AI Generated Score
- AI Edited Score
- Real Photo Score

Weights are assigned based on the reliability of each test:
- Metadata: 25%
- Color Analysis: 20%
- JPEG Analysis: 15%
- Chromatic Aberration: 15%
- Texture Analysis: 15%
- ELA: 10%

## Limitations

- The tool uses heuristic-based analysis, not machine learning
- Accuracy depends on image quality and format
- Some AI-generated images may be undetectable
- Real photos with heavy editing may be flagged as AI
- Best results with high-resolution images

## Future Enhancements

- Deep learning model integration (CNN/ViT)
- Training on real vs AI dataset
- Advanced GAN fingerprint detection
- Blockchain verification support
- Batch processing capability
- API endpoint for integration

## Project Structure

```
MetaForens/
├── app.py                      # Main Tkinter application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── forensics/                  # Forensic analysis modules
    ├── __init__.py
    ├── metadata_extractor.py   # EXIF and metadata analysis
    ├── ela.py                  # Error Level Analysis
    ├── frequency_analysis.py   # FFT analysis
    ├── noise_analysis.py       # Sensor noise extraction
    ├── jpeg_analysis.py        # JPEG artifact detection
    ├── chromatic_analysis.py   # Chromatic aberration check
    ├── color_analysis.py       # Color distribution analysis
    ├── texture_analysis.py     # Texture consistency check
    └── classifier.py           # Feature fusion & classification
```

## License

This project is provided as-is for educational and research purposes.

## Author

Created as a comprehensive forensic tool for detecting AI-manipulated images.

## Disclaimer

This tool provides probabilistic assessments and should not be used as the sole means of verification for critical applications. Always combine with other verification methods and expert analysis when authenticity is crucial.
