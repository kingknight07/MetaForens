import numpy as np
from PIL import Image

def classify_image(metadata, jpeg_analysis, chromatic_analysis, color_analysis, texture_analysis, 
                   gan_detection, noise_inconsistency, benford_analysis, cfa_detection, 
                   double_jpeg, gradient_analysis, image_path):
    """
    Advanced AI Image Classifier
    Combines multiple forensic analyses to determine if an image is AI-generated, AI-edited, or real.
    
    Args:
        metadata (dict): Metadata analysis results
        jpeg_analysis (dict): JPEG artifacts analysis
        chromatic_analysis (dict): Chromatic aberration analysis
        color_analysis (dict): Color distribution analysis
        texture_analysis (dict): Texture consistency analysis
        gan_detection (dict): GAN fingerprint detection results
        noise_inconsistency (dict): Advanced noise analysis results
        benford_analysis (dict): Benford's Law analysis results
        cfa_detection (dict): CFA pattern detection results
        double_jpeg (dict): Double JPEG compression results
        gradient_analysis (dict): Gradient anomaly detection results
        image_path (str): Path to the image
        
    Returns:
        dict: Classification results with probabilities and evidence
    """
    
    # Initialize scores for each category
    ai_generated_score = 0
    ai_edited_score = 0
    real_photo_score = 0
    
    # Evidence collection
    evidence = {
        'ai_generated': [],
        'ai_edited': [],
        'real_photo': []
    }
    
    # Check if image is old (pre-2020) based on metadata
    is_old_image = False
    image_year = None
    
    if metadata.get('exif'):
        # Try to extract date from EXIF
        date_fields = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized', 'DateTime']
        for field in date_fields:
            date_str = metadata['exif'].get(field, '')
            if date_str and len(str(date_str)) >= 4:
                try:
                    # Extract year (first 4 characters)
                    year_str = str(date_str)[:4]
                    if year_str.isdigit():
                        image_year = int(year_str)
                        if 1990 <= image_year < 2020:  # Old image (before AI era)
                            is_old_image = True
                            evidence['real_photo'].append(f"✓ Old image from {image_year} (pre-AI era)")
                        break
                except:
                    pass
    
    # Weight configuration (total = 100)
    # Adjust weights for old images
    if is_old_image:
        weights = {
            'metadata': 15,           # Trust metadata more for old images
            'chromatic': 12,          # Old cameras had more aberration
            'double_jpeg': 5,         # Multiple re-saves are normal for old images
            'gan_fingerprint': 15,    # GAN is still definitive (didn't exist back then)
            'cfa_detection': 10,      # Less reliable for old/compressed images
            'noise_inconsistency': 10,
            'benford_law': 8,
            'gradient': 8,
            'color': 7,
            'texture': 5,
            'jpeg': 5
        }
    else:
        weights = {
            'cfa_detection': 15,      # Strongest indicator for modern images
            'gan_fingerprint': 12,    # Very strong AI indicator
            'noise_inconsistency': 12,
            'benford_law': 10,
            'metadata': 8,
            'double_jpeg': 8,
            'gradient': 8,
            'chromatic': 7,
            'color': 7,
            'texture': 7,
            'jpeg': 6
        }
    
    # 1. CFA DETECTION - Most Critical Test (Real camera vs AI/Screen)
    cfa_evidence = []
    
    if cfa_detection.get('cfa_pattern_detected'):
        real_photo_score += weights['cfa_detection']
        evidence['real_photo'].append("✓✓ Camera sensor pattern (CFA) detected - Strong indicator of real camera photo")
        cfa_evidence.append(f"CFA detected: {cfa_detection.get('pattern_type')}")
    else:
        # No CFA = either AI generated OR old/heavily compressed image
        cfa_strength = cfa_detection.get('cfa_strength', 0)
        
        if is_old_image:
            # For old images, lack of CFA is more acceptable (compression degradation)
            if cfa_strength >= 0.01:  # Any detectable pattern in old image is good
                real_photo_score += weights['cfa_detection'] * 0.7
                evidence['real_photo'].append(f"✓ Weak CFA detected ({cfa_strength:.4f}) - Acceptable for old/compressed image")
                cfa_evidence.append(f"Weak CFA (old image): {cfa_strength:.4f}")
            else:
                # Even very weak CFA in old image doesn't mean AI
                real_photo_score += weights['cfa_detection'] * 0.3
                ai_edited_score += weights['cfa_detection'] * 0.4
                evidence['real_photo'].append(f"⚠ CFA degraded by age/compression ({image_year})")
                cfa_evidence.append(f"CFA lost to compression (pre-{image_year})")
        else:
            # For modern images, no CFA is more suspicious
            if cfa_strength < 0.02:  # Very low = likely AI generated
                ai_generated_score += weights['cfa_detection']
                evidence['ai_generated'].append("⚠⚠ No camera sensor pattern - Not taken with a camera")
                cfa_evidence.append("No CFA pattern detected")
            else:  # Weak CFA = might be edited/compressed
                ai_edited_score += weights['cfa_detection'] * 0.7
                ai_generated_score += weights['cfa_detection'] * 0.3
                evidence['ai_edited'].append("⚠ Weak camera sensor pattern - Possibly edited or compressed")
                cfa_evidence.append(f"Weak CFA: {cfa_strength:.4f}")
    
    # 2. GAN FINGERPRINT DETECTION
    gan_evidence = []
    
    if gan_detection.get('gan_signature_detected'):
        ai_generated_score += weights['gan_fingerprint']
        evidence['ai_generated'].append(f"⚠⚠ GAN fingerprint detected (High-freq: {gan_detection.get('high_freq_pattern_score', 0):.4f})")
        gan_evidence.append("GAN signature detected")
    elif gan_detection.get('is_suspicious'):
        ai_generated_score += weights['gan_fingerprint'] * 0.5
        ai_edited_score += weights['gan_fingerprint'] * 0.3
        evidence['ai_generated'].append("⚠ Suspicious frequency patterns detected")
        gan_evidence.append("Suspicious frequency patterns")
    else:
        real_photo_score += weights['gan_fingerprint'] * 0.5
        evidence['real_photo'].append("✓ Natural frequency patterns")
        gan_evidence.append("Natural frequency patterns")
    
    # 3. NOISE INCONSISTENCY ANALYSIS
    noise_evidence = []
    
    if noise_inconsistency.get('is_suspicious'):
        confidence_level = noise_inconsistency.get('confidence', 'Low')
        suspicious_count = noise_inconsistency.get('suspicious_regions', 0)
        
        if confidence_level == 'High' and suspicious_count >= 3:
            ai_generated_score += weights['noise_inconsistency']
            evidence['ai_generated'].append(f"⚠ Inconsistent noise across {suspicious_count} regions - AI artifact")
            noise_evidence.append(f"High noise inconsistency ({suspicious_count} regions)")
        elif confidence_level in ['High', 'Medium']:
            ai_edited_score += weights['noise_inconsistency']
            evidence['ai_edited'].append(f"⚠ Regional noise inconsistency ({suspicious_count} regions) - Likely edited")
            noise_evidence.append(f"Noise inconsistency in {suspicious_count} regions")
        else:
            ai_edited_score += weights['noise_inconsistency'] * 0.5
            evidence['ai_edited'].append("⚠ Minor noise inconsistencies detected")
            noise_evidence.append("Minor noise variations")
    else:
        real_photo_score += weights['noise_inconsistency']
        evidence['real_photo'].append("✓ Consistent sensor noise throughout image")
        noise_evidence.append("Consistent sensor noise")
    
    # 4. BENFORD'S LAW ANALYSIS
    benford_evidence = []
    
    if benford_analysis.get('follows_benford'):
        real_photo_score += weights['benford_law']
        evidence['real_photo'].append(f"✓ Follows Benford's Law (p={benford_analysis.get('p_value', 0):.3f}) - Natural distribution")
        benford_evidence.append("Follows Benford's Law")
    elif benford_analysis.get('is_suspicious'):
        deviation = benford_analysis.get('benford_deviation', 0)
        if deviation > 0.15:
            ai_generated_score += weights['benford_law']
            evidence['ai_generated'].append(f"⚠ Significant deviation from Benford's Law ({deviation:.3f}) - Unnatural distribution")
            benford_evidence.append(f"Deviates from Benford's Law ({deviation:.3f})")
        else:
            ai_edited_score += weights['benford_law'] * 0.6
            evidence['ai_edited'].append(f"⚠ Minor deviation from Benford's Law ({deviation:.3f})")
            benford_evidence.append(f"Minor Benford deviation ({deviation:.3f})")
    
    # 5. METADATA ANALYSIS
    metadata_evidence = []
    
    anomalies = metadata.get('anomalies', [])
    has_exif = metadata.get('exif', {})
    software_tags = metadata.get('software_tags', [])
    
    if not has_exif or 'No EXIF data found' in str(anomalies):
        # No EXIF could mean AI or edited
        if not software_tags:
            ai_generated_score += weights['metadata']
            evidence['ai_generated'].append("⚠ No EXIF data - Not from a camera")
            metadata_evidence.append("No EXIF data")
        else:
            ai_edited_score += weights['metadata']
            evidence['ai_edited'].append(f"⚠ Editing software detected: {', '.join(software_tags)}")
            metadata_evidence.append(f"Software: {', '.join(software_tags)}")
    else:
        # Has EXIF - good sign
        real_photo_score += weights['metadata']
        evidence['real_photo'].append("✓ Camera metadata present")
        metadata_evidence.append("EXIF data present")
        
        # Check for AI/editing software
        ai_software = ['ai', 'neural', 'adobe', 'photoshop', 'gimp', 'paint', 'canva']
        if any(any(ai_term in tag.lower() for ai_term in ai_software) for tag in software_tags):
            ai_edited_score += weights['metadata'] * 0.5
            evidence['ai_edited'].append(f"⚠ Editing software in metadata: {', '.join(software_tags)}")
            metadata_evidence.append(f"Editing software: {', '.join(software_tags)}")
    
    # 6. DOUBLE JPEG COMPRESSION
    double_jpeg_evidence = []
    
    if double_jpeg.get('double_compression_detected'):
        if is_old_image:
            # Multiple compressions are NORMAL for old images (re-saved many times)
            real_photo_score += weights['double_jpeg'] * 0.5
            evidence['real_photo'].append(f"✓ Multiple compressions expected for old image ({double_jpeg.get('compression_count_estimate')} cycles)")
            double_jpeg_evidence.append(f"Normal re-compression for old image")
        else:
            # For modern images, double compression suggests editing
            ai_edited_score += weights['double_jpeg']
            evidence['ai_edited'].append(f"⚠ Double JPEG compression detected ({double_jpeg.get('compression_count_estimate')} cycles)")
            double_jpeg_evidence.append(f"Double compression ({double_jpeg.get('compression_count_estimate')} times)")
    elif double_jpeg.get('likely_edited'):
        if is_old_image:
            real_photo_score += weights['double_jpeg'] * 0.3
            double_jpeg_evidence.append("Compression artifacts (age-related)")
        else:
            ai_edited_score += weights['double_jpeg'] * 0.6
            evidence['ai_edited'].append("⚠ Compression artifacts suggest editing")
            double_jpeg_evidence.append("Compression artifacts")
    else:
        real_photo_score += weights['double_jpeg'] * 0.4
        double_jpeg_evidence.append("Single compression")
    
    # 7. GRADIENT ANALYSIS
    gradient_evidence = []
    
    if gradient_analysis.get('unnatural_smoothness_detected'):
        smoothness = gradient_analysis.get('gradient_smoothness', 0)
        if smoothness > 15:  # Very smooth - AI characteristic
            ai_generated_score += weights['gradient']
            evidence['ai_generated'].append(f"⚠ Unnatural smoothness ({smoothness:.1f}) - AI artifact")
            gradient_evidence.append(f"Unnatural smoothness ({smoothness:.1f})")
        else:
            ai_edited_score += weights['gradient'] * 0.7
            evidence['ai_edited'].append(f"⚠ Smoothing detected ({smoothness:.1f})")
            gradient_evidence.append(f"Smoothing detected")
    else:
        real_photo_score += weights['gradient'] * 0.5
        evidence['real_photo'].append("✓ Natural gradient transitions")
        gradient_evidence.append("Natural gradients")
    
    # 8. CHROMATIC ABERRATION
    chromatic_evidence = []
    
    if chromatic_analysis.get('has_chromatic_aberration'):
        real_photo_score += weights['chromatic']
        evidence['real_photo'].append(f"✓ Natural lens aberration present ({chromatic_analysis.get('aberration_score', 0):.5f})")
        chromatic_evidence.append("Natural lens aberration")
    elif chromatic_analysis.get('is_suspicious'):
        ai_generated_score += weights['chromatic'] * 0.6
        ai_edited_score += weights['chromatic'] * 0.4
        evidence['ai_generated'].append("⚠ Missing expected lens aberration - Too perfect")
        chromatic_evidence.append("Missing lens aberration")
    
    # 9. COLOR DISTRIBUTION
    color_evidence = []
    
    if color_analysis.get('ai_signature_detected'):
        ai_generated_score += weights['color']
        evidence['ai_generated'].append(f"⚠ AI color signature (Saturation: {color_analysis.get('color_saturation_avg', 0):.1f})")
        color_evidence.append("AI color signature")
    elif color_analysis.get('unusual_patterns'):
        ai_edited_score += weights['color'] * 0.7
        evidence['ai_edited'].append("⚠ Unusual color distribution patterns")
        color_evidence.append("Unusual color patterns")
    else:
        real_photo_score += weights['color'] * 0.5
        evidence['real_photo'].append("✓ Natural color distribution")
        color_evidence.append("Natural colors")
    
    # 10. TEXTURE CONSISTENCY
    texture_evidence = []
    
    if texture_analysis.get('repetition_detected'):
        ai_edited_score += weights['texture']
        evidence['ai_edited'].append("⚠ Repetitive texture patterns (clone stamp detected)")
        texture_evidence.append("Clone stamp detected")
    elif texture_analysis.get('is_suspicious'):
        variance = texture_analysis.get('texture_variance', 0)
        if variance < 50:  # Very uniform
            ai_generated_score += weights['texture'] * 0.6
            evidence['ai_generated'].append(f"⚠ Overly uniform texture ({variance:.1f})")
            texture_evidence.append("Overly uniform texture")
        else:
            ai_edited_score += weights['texture'] * 0.5
            texture_evidence.append("Suspicious texture")
    else:
        real_photo_score += weights['texture'] * 0.5
        evidence['real_photo'].append("✓ Natural texture variation")
        texture_evidence.append("Natural texture")
    
    # 11. JPEG ARTIFACTS
    jpeg_evidence = []
    
    if jpeg_analysis.get('is_suspicious'):
        quality = jpeg_analysis.get('compression_quality_estimate', 'Unknown')
        if 'Uncompressed' in str(quality) or 'Very High' in str(quality):
            # Uncompressed is unusual for photos but common for AI
            ai_generated_score += weights['jpeg'] * 0.6
            evidence['ai_generated'].append(f"⚠ Unusual compression: {quality}")
            jpeg_evidence.append(f"Unusual compression: {quality}")
        else:
            ai_edited_score += weights['jpeg'] * 0.5
            evidence['ai_edited'].append(f"⚠ Suspicious JPEG patterns ({quality})")
            jpeg_evidence.append(f"Suspicious patterns")
    
    # Calculate total and percentages
    total_score = ai_generated_score + ai_edited_score + real_photo_score
    
    if total_score == 0:
        total_score = 100  # Prevent division by zero
        real_photo_score = 50
        ai_edited_score = 30
        ai_generated_score = 20
    
    ai_gen_pct = round((ai_generated_score / total_score) * 100, 2)
    ai_edit_pct = round((ai_edited_score / total_score) * 100, 2)
    real_pct = round((real_photo_score / total_score) * 100, 2)
    
    # Determine verdict
    max_score = max(ai_generated_score, ai_edited_score, real_photo_score)
    
    # Special handling for old images
    if is_old_image and real_photo_score > ai_generated_score * 0.7:
        # If it's from pre-AI era and has reasonable real score, favor real photo
        verdict = "Likely Real Photo"
    elif max_score == ai_generated_score:
        # Double check: Old images can't be AI generated if they predate AI technology
        if is_old_image and image_year < 2015:  # Before modern GAN era
            verdict = "Likely Real Photo"
            evidence['real_photo'].append(f"✓✓ Image predates modern AI technology ({image_year})")
        else:
            verdict = "AI Generated"
    elif max_score == ai_edited_score:
        verdict = "AI Edited / Modified"
    else:
        verdict = "Likely Real Photo"
    
    # Calculate confidence based on score separation
    score_diff = max_score - sorted([ai_generated_score, ai_edited_score, real_photo_score])[-2]
    score_ratio = score_diff / total_score if total_score > 0 else 0
    
    # More lenient confidence for old images
    if is_old_image:
        if score_ratio > 0.15:  # Lower threshold for old images
            confidence = "High"
        elif score_ratio > 0.08:
            confidence = "Medium"
        else:
            confidence = "Low"
    else:
        if score_ratio > 0.25:  # Clear winner (>25% gap)
            confidence = "High"
        elif score_ratio > 0.12:  # Moderate separation (>12% gap)
            confidence = "Medium"
        else:  # Close scores
            confidence = "Low"
    
    # Additional confidence adjustments
    if verdict == "Likely Real Photo":
        if is_old_image:
            # Old images get benefit of doubt
            if confidence == "Low":
                confidence = "Medium"
        else:
            # Real photos should have strong CFA (for modern images)
            if cfa_detection.get('cfa_pattern_detected'):
                if confidence == "Medium":
                    confidence = "High"
            else:
                # No CFA = can't be high confidence real photo
                if confidence == "High":
                    confidence = "Medium"
    
    elif verdict == "AI Generated":
        # AI generated should have NO CFA
        if not cfa_detection.get('cfa_pattern_detected') and gan_detection.get('gan_signature_detected'):
            if confidence == "Medium":
                confidence = "High"
        # Can't be AI generated if it's from before AI era
        if is_old_image and image_year < 2015:
            verdict = "Likely Real Photo"
            confidence = "Medium"
            evidence['real_photo'].append("✓✓ Corrected: Image too old to be AI-generated")
    
    # Compile all evidence for display
    all_evidence = {
        'cfa': cfa_evidence,
        'gan': gan_evidence,
        'noise': noise_evidence,
        'benford': benford_evidence,
        'double_jpeg': double_jpeg_evidence,
        'gradient': gradient_evidence,
        'metadata': metadata_evidence,
        'chromatic': chromatic_evidence,
        'jpeg': jpeg_evidence,
        'color': color_evidence,
        'texture': texture_evidence
    }
    
    return {
        'verdict': verdict,
        'confidence': confidence,
        'probabilities': {
            'ai_generated': ai_gen_pct,
            'ai_edited': ai_edit_pct,
            'real_photo': real_pct
        },
        'evidence': all_evidence,
        'categorized_evidence': evidence,
        'raw_scores': {
            'ai_generated': round(ai_generated_score, 3),
            'ai_edited': round(ai_edited_score, 3),
            'real_photo': round(real_photo_score, 3)
        }
    }
