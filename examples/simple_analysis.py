"""
Simple Analysis Example
Demonstrates basic usage of MetaForens library
"""

from metaforens import MetaForens

# Initialize the detector
detector = MetaForens()

# Analyze a single image
image_path = "your_image.jpg"  # Replace with your image path

print(f"Analyzing: {image_path}\n")

try:
    # Perform analysis
    result = detector.analyze(image_path)
    
    # Print the summary
    print(detector.get_summary(result))
    
    # Access specific results
    print("\nQuick Access:")
    print(f"Verdict: {result['verdict']}")
    print(f"Confidence: {result['confidence']}")
    print(f"AI Generated Probability: {result['probabilities']['ai_generated']}%")
    
except FileNotFoundError:
    print(f"Error: Image file '{image_path}' not found")
except ValueError as e:
    print(f"Error: {e}")
