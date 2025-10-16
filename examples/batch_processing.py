"""
Batch Processing Example
Analyze multiple images at once
"""

from metaforens import MetaForens
import os

# Initialize detector
detector = MetaForens()

# List of images to analyze
image_paths = [
    "image1.jpg",
    "image2.jpg",
    "image3.jpg",
    # Add more images...
]

# Or get all images from a directory
def get_images_from_directory(directory):
    """Get all image files from a directory"""
    extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    images = []
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.lower().endswith(extensions):
                images.append(os.path.join(directory, file))
    return images

# Example: Get all images from 'test_images' directory
# image_paths = get_images_from_directory('test_images')

# Batch analyze
results = detector.batch_analyze(image_paths)

# Process results
ai_generated = []
ai_edited = []
real_photos = []

for path, result in results.items():
    if 'error' in result:
        print(f"Error processing {path}: {result['error']}")
        continue
    
    if result['verdict'] == "AI Generated":
        ai_generated.append(path)
    elif result['verdict'] == "AI Edited / Modified":
        ai_edited.append(path)
    else:
        real_photos.append(path)

# Print summary
print("\n" + "=" * 60)
print("BATCH ANALYSIS SUMMARY")
print("=" * 60)
print(f"Total Images: {len(results)}")
print(f"AI Generated: {len(ai_generated)}")
print(f"AI Edited: {len(ai_edited)}")
print(f"Real Photos: {len(real_photos)}")
print("=" * 60)

# Print details for each category
if ai_generated:
    print("\nAI Generated Images:")
    for path in ai_generated:
        result = results[path]
        print(f"  • {os.path.basename(path)} - {result['confidence']} confidence ({result['probabilities']['ai_generated']:.1f}%)")

if ai_edited:
    print("\nAI Edited Images:")
    for path in ai_edited:
        result = results[path]
        print(f"  • {os.path.basename(path)} - {result['confidence']} confidence ({result['probabilities']['ai_edited']:.1f}%)")

if real_photos:
    print("\nReal Photos:")
    for path in real_photos:
        result = results[path]
        print(f"  • {os.path.basename(path)} - {result['confidence']} confidence ({result['probabilities']['real_photo']:.1f}%)")
