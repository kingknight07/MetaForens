"""
MetaForens Forensic Analysis Modules
"""

# Core forensic modules
from .metadata_extractor import extract_metadata
from .ela import perform_ela
from .frequency_analysis import analyze_frequency
from .noise_analysis import extract_noise_map
from .jpeg_analysis import analyze_jpeg_artifacts
from .chromatic_analysis import analyze_chromatic_aberration
from .color_analysis import analyze_color_distribution
from .texture_analysis import analyze_texture_consistency

# Advanced forensic modules
from .gan_detection import detect_gan_fingerprint
from .noise_inconsistency import analyze_noise_inconsistency
from .benford_analysis import benford_law_analysis
from .cfa_detection import detect_cfa_pattern
from .double_jpeg import detect_double_jpeg_compression
from .gradient_analysis import analyze_gradient_anomalies

# Classifier
from .classifier import classify_image

__all__ = [
    # Core modules
    'extract_metadata',
    'perform_ela',
    'analyze_frequency',
    'extract_noise_map',
    'analyze_jpeg_artifacts',
    'analyze_chromatic_aberration',
    'analyze_color_distribution',
    'analyze_texture_consistency',
    
    # Advanced modules
    'detect_gan_fingerprint',
    'analyze_noise_inconsistency',
    'benford_law_analysis',
    'detect_cfa_pattern',
    'detect_double_jpeg_compression',
    'analyze_gradient_anomalies',
    
    # Classifier
    'classify_image'
]
# Contains various image forensic analysis tools

__all__ = [
    'metadata_extractor',
    'ela',
    'frequency_analysis',
    'noise_analysis',
    'jpeg_analysis',
    'chromatic_analysis',
    'color_analysis',
    'texture_analysis',
    'classifier',
    'gan_detection',
    'noise_inconsistency',
    'benford_analysis',
    'cfa_detection',
    'double_jpeg',
    'gradient_analysis'
]
