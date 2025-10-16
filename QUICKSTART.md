# Quick Start Guide - MetaForens Library

## Installation

```bash
git clone https://github.com/kingknight07/MetaForens.git
cd MetaForens
pip install -r requirements.txt
```

## Basic Usage

### 1. Simple Analysis (Recommended)

```python
from metaforens import MetaForens

# Create detector instance
detector = MetaForens()

# Analyze an image
result = detector.analyze('your_image.jpg')

# Print results
print(f"Verdict: {result['verdict']}")
print(f"Confidence: {result['confidence']}")
print(f"AI Generated: {result['probabilities']['ai_generated']}%")
print(f"AI Edited: {result['probabilities']['ai_edited']}%")
print(f"Real Photo: {result['probabilities']['real_photo']}%")
```

### 2. One-Liner

```python
import metaforens

result = metaforens.analyze_image('photo.jpg')
print(result['verdict'])  # "AI Generated", "AI Edited / Modified", or "Likely Real Photo"
```

### 3. With Summary

```python
from metaforens import MetaForens

detector = MetaForens()
result = detector.analyze('image.jpg')

# Get formatted summary
print(detector.get_summary(result))
```

### 4. Batch Processing

```python
from metaforens import MetaForens

detector = MetaForens()

images = ['photo1.jpg', 'photo2.jpg', 'photo3.jpg']
results = detector.batch_analyze(images)

for path, result in results.items():
    print(f"{path}: {result['verdict']}")
```

### 5. Detailed Forensic Data

```python
from metaforens import MetaForens

detector = MetaForens()
result = detector.analyze('image.jpg', return_detailed=True)

# Access specific forensic tests
print("CFA Detection:", result['detailed']['cfa_detection'])
print("GAN Detection:", result['detailed']['gan_detection'])
print("Metadata:", result['detailed']['metadata'])
# ... and 8 more detailed analyses
```

## Command Line Usage

```bash
# Analyze from command line
python metaforens.py your_image.jpg

# Or with the GUI
python app.py
```

## Result Structure

```python
{
    'verdict': 'AI Generated',        # or 'AI Edited / Modified', 'Likely Real Photo'
    'confidence': 'High',             # or 'Medium', 'Low'
    'probabilities': {
        'ai_generated': 85.2,
        'ai_edited': 10.5,
        'real_photo': 4.3
    },
    'evidence': {...},                # Evidence from each test
    'categorized_evidence': {         # Evidence grouped by verdict
        'ai_generated': [...],
        'ai_edited': [...],
        'real_photo': [...]
    },
    'raw_scores': {...}               # Raw scoring data
}
```

## Integration Examples

### Web API Integration

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

### Automation Script

```python
from metaforens import MetaForens
import os

detector = MetaForens()

# Process all images in a directory
for filename in os.listdir('uploads'):
    if filename.endswith(('.jpg', '.png')):
        path = os.path.join('uploads', filename)
        result = detector.analyze(path)
        
        if result['verdict'] == 'AI Generated' and result['confidence'] == 'High':
            # Take action for AI-generated images
            print(f"AI detected: {filename}")
            os.rename(path, f"flagged/{filename}")
```

### Conditional Processing

```python
from metaforens import MetaForens

detector = MetaForens()
result = detector.analyze('image.jpg')

# Make decisions based on results
if result['verdict'] == 'AI Generated' and result['confidence'] == 'High':
    print("This is definitely AI-generated!")
elif result['verdict'] == 'Likely Real Photo' and result['confidence'] == 'High':
    print("This is a genuine camera photo!")
elif result['confidence'] == 'Medium':
    print("Uncertain - manual review recommended")
```

## Tips

1. **For best results**: Use high-quality, uncompressed images
2. **Old images**: The library automatically detects and adjusts for images from before 2020
3. **Batch processing**: Use `batch_analyze()` for multiple images (more efficient)
4. **Detailed mode**: Only use `return_detailed=True` when you need all forensic data (slower)
5. **Confidence levels**: 
   - High = Very reliable (>90% accurate)
   - Medium = Fairly reliable (~75% accurate)
   - Low = Uncertain, manual review recommended

## Support

- GitHub: https://github.com/kingknight07/MetaForens
- Issues: https://github.com/kingknight07/MetaForens/issues
- Email: shuklaayush0704@gmail.com
