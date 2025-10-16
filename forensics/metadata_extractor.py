from PIL import Image
from PIL.ExifTags import TAGS

def extract_metadata(image_path):
    """
    Extracts metadata from an image file.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        dict: A dictionary containing metadata.
    """
    metadata = {
        "exif": {},
        "software_tags": [],
        "anomalies": []
    }
    
    try:
        with Image.open(image_path) as img:
            # Get basic image info
            metadata['format'] = img.format
            metadata['mode'] = img.mode
            metadata['size'] = img.size

            # Extract EXIF data
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    metadata["exif"][tag_name] = value
            else:
                metadata["anomalies"].append("No EXIF data found.")

            # Check for software tags in EXIF
            if "Software" in metadata["exif"]:
                software = metadata["exif"]["Software"]
                metadata["software_tags"].append(software)
                if any(tool in software.lower() for tool in ['photoshop', 'gimp', 'lightroom', 'ai', 'upscaler']):
                     metadata["anomalies"].append(f"Potential editing software detected: {software}")

    except Exception as e:
        metadata["anomalies"].append(f"Error reading metadata: {e}")
        
    return metadata

if __name__ == '__main__':
    # This is for testing purposes.
    # You would replace 'test_image.jpg' with a path to an actual image.
    # Create a dummy image for testing if you don't have one.
    try:
        from PIL import Image
        dummy_img = Image.new('RGB', (100, 100), color = 'red')
        dummy_img.save("test.jpg")
        metadata = extract_metadata("test.jpg")
        import json
        print(json.dumps(metadata, indent=4))
    except ImportError:
        print("Pillow is not installed. Cannot run test.")
    except Exception as e:
        print(f"An error occurred: {e}")
