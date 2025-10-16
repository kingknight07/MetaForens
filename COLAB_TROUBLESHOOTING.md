# Google Colab Troubleshooting Guide

## Error: "cannot import name 'detect_noise_inconsistency'"

This error occurs due to import name mismatches. The fix has been applied to the GitHub repository.

### Quick Fix in Colab:

If you still see this error after cloning, run these commands in a Colab cell:

```python
# Verify you have the latest version
!cd /content/MetaForens && git pull origin main

# Check the actual content
!grep "from forensics.noise_inconsistency" /content/MetaForens/metaforens.py
```

**Expected output:** Should show `analyze_noise_inconsistency` (not `detect_noise_inconsistency`)

### Manual Verification:

```python
# Check what functions are actually available
import sys
sys.path.insert(0, '/content/MetaForens')

from forensics.noise_inconsistency import *
print("Available functions:", dir())
```

### Alternative: Direct Import Test

```python
# Test imports one by one
try:
    from forensics.noise_analysis import extract_noise_map
    print("✓ noise_analysis OK")
except Exception as e:
    print(f"✗ noise_analysis: {e}")

try:
    from forensics.jpeg_analysis import analyze_jpeg_artifacts
    print("✓ jpeg_analysis OK")
except Exception as e:
    print(f"✗ jpeg_analysis: {e}")

try:
    from forensics.noise_inconsistency import analyze_noise_inconsistency
    print("✓ noise_inconsistency OK")
except Exception as e:
    print(f"✗ noise_inconsistency: {e}")

try:
    from forensics.benford_analysis import benford_law_analysis
    print("✓ benford_analysis OK")
except Exception as e:
    print(f"✗ benford_analysis: {e}")

try:
    from forensics.double_jpeg import detect_double_jpeg_compression
    print("✓ double_jpeg OK")
except Exception as e:
    print(f"✗ double_jpeg: {e}")

try:
    from forensics.gradient_analysis import analyze_gradient_anomalies
    print("✓ gradient_analysis OK")
except Exception as e:
    print(f"✗ gradient_analysis: {e}")
```

### If Problem Persists:

1. **Restart Colab Runtime:**
   - Runtime → Restart runtime
   - Re-run all cells from the beginning

2. **Clear Previous Installations:**
   ```python
   !rm -rf /content/MetaForens
   !pip uninstall -y metaforens
   ```
   
   Then re-run the installation cells.

3. **Clone Specific Commit:**
   ```python
   !git clone https://github.com/kingknight07/MetaForens.git
   !cd /content/MetaForens && git checkout dc279bb  # Commit with import fixes
   ```

4. **Direct File Check:**
   ```python
   # View the actual import line
   !head -30 /content/MetaForens/metaforens.py | grep -A 5 "from forensics"
   ```

## Expected Correct Imports

The `metaforens.py` file should have these imports (lines 13-27):

```python
from forensics.metadata_extractor import extract_metadata
from forensics.ela import perform_ela
from forensics.frequency_analysis import analyze_frequency
from forensics.noise_analysis import extract_noise_map
from forensics.jpeg_analysis import analyze_jpeg_artifacts
from forensics.chromatic_analysis import analyze_chromatic_aberration
from forensics.color_analysis import analyze_color_distribution
from forensics.texture_analysis import analyze_texture_consistency
from forensics.gan_detection import detect_gan_fingerprint
from forensics.noise_inconsistency import analyze_noise_inconsistency
from forensics.benford_analysis import benford_law_analysis
from forensics.cfa_detection import detect_cfa_pattern
from forensics.double_jpeg import detect_double_jpeg_compression
from forensics.gradient_analysis import analyze_gradient_anomalies
from forensics.classifier import classify_image
```

## Verification Steps

After installation, verify with:

```python
from metaforens import MetaForens
detector = MetaForens()
print(f"✓ MetaForens v{detector.version}")
print(f"✓ {detector.analyses_count} forensic analyses loaded")
```

Expected output:
```
✓ MetaForens v1.0.0
✓ 15 forensic analyses loaded
```

## Contact

If issues persist:
- GitHub Issues: https://github.com/kingknight07/MetaForens/issues
- Email: shuklaayush0704@gmail.com
