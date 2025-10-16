import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import json

# Import forensic tools
from forensics.metadata_extractor import extract_metadata
from forensics.ela import perform_ela
from forensics.frequency_analysis import analyze_frequency
from forensics.noise_analysis import extract_noise_map
from forensics.jpeg_analysis import analyze_jpeg_artifacts
from forensics.chromatic_analysis import analyze_chromatic_aberration
from forensics.color_analysis import analyze_color_distribution
from forensics.texture_analysis import analyze_texture_consistency
from forensics.classifier import classify_image

# Import advanced forensic tools
from forensics.gan_detection import detect_gan_fingerprint
from forensics.noise_inconsistency import analyze_noise_inconsistency
from forensics.benford_analysis import benford_law_analysis
from forensics.cfa_detection import detect_cfa_pattern
from forensics.double_jpeg import detect_double_jpeg_compression
from forensics.gradient_analysis import analyze_gradient_anomalies

class MetaForensApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MetaForens")
        self.root.geometry("1000x700")

        # Main frame
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left panel for controls
        left_panel = tk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        # Right panel for image and results
        self.right_panel = tk.Frame(main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Left Panel Widgets ---
        # Title/Logo
        title_label = tk.Label(left_panel, text="MetaForens", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(left_panel, text="AI Image Detection", font=("Arial", 9))
        subtitle_label.pack(pady=(0, 10))
        
        self.upload_button = tk.Button(left_panel, text="Upload Image", command=self.upload_image, bg="#4CAF50", fg="white")
        self.upload_button.pack(pady=10, fill=tk.X)

        self.analyze_button = tk.Button(left_panel, text="Analyze Image", command=self.analyze_image, state=tk.DISABLED, bg="#2196F3", fg="white")
        self.analyze_button.pack(pady=10, fill=tk.X)

        # Verdict frame
        verdict_frame = tk.LabelFrame(left_panel, text="VERDICT", font=("Arial", 10, "bold"))
        verdict_frame.pack(pady=10, fill=tk.X)
        
        self.verdict_label = tk.Label(verdict_frame, text="Upload and analyze\nan image", font=("Arial", 11, "bold"), fg="gray", wraplength=280, justify=tk.CENTER)
        self.verdict_label.pack(pady=10)
        
        self.confidence_label = tk.Label(verdict_frame, text="", font=("Arial", 9), fg="gray")
        self.confidence_label.pack(pady=(0, 5))
        
        # Probability bars
        prob_frame = tk.Frame(verdict_frame)
        prob_frame.pack(pady=5, fill=tk.X, padx=5)
        
        tk.Label(prob_frame, text="AI Generated:", font=("Arial", 8)).grid(row=0, column=0, sticky='w')
        self.ai_gen_label = tk.Label(prob_frame, text="0%", font=("Arial", 8, "bold"), fg="#f44336")
        self.ai_gen_label.grid(row=0, column=1, sticky='e')
        
        tk.Label(prob_frame, text="AI Edited:", font=("Arial", 8)).grid(row=1, column=0, sticky='w')
        self.ai_edit_label = tk.Label(prob_frame, text="0%", font=("Arial", 8, "bold"), fg="#ff9800")
        self.ai_edit_label.grid(row=1, column=1, sticky='e')
        
        tk.Label(prob_frame, text="Real Photo:", font=("Arial", 8)).grid(row=2, column=0, sticky='w')
        self.real_photo_label = tk.Label(prob_frame, text="0%", font=("Arial", 8, "bold"), fg="#4CAF50")
        self.real_photo_label.grid(row=2, column=1, sticky='e')
        
        prob_frame.columnconfigure(1, weight=1)

        # Frame for detailed results
        results_frame = tk.LabelFrame(left_panel, text="Detailed Analysis")
        results_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=10, font=("Courier", 8))
        scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_text.insert(tk.END, "Results will be shown here.")
        self.results_text.config(state=tk.DISABLED)


        # --- Right Panel Widgets ---
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.image_frame = tk.Frame(self.notebook)
        self.ela_frame = tk.Frame(self.notebook)
        self.freq_frame = tk.Frame(self.notebook)
        self.noise_frame = tk.Frame(self.notebook)

        self.notebook.add(self.image_frame, text='Original Image')
        self.notebook.add(self.ela_frame, text='ELA')
        self.notebook.add(self.freq_frame, text='Frequency')
        self.notebook.add(self.noise_frame, text='Noise Map')

        self.image_label = tk.Label(self.image_frame, text="Upload an image to begin", bg="lightgrey")
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        self.ela_label = tk.Label(self.ela_frame, bg="lightgrey")
        self.ela_label.pack(fill=tk.BOTH, expand=True)
        
        self.freq_label = tk.Label(self.freq_frame, bg="lightgrey")
        self.freq_label.pack(fill=tk.BOTH, expand=True)

        self.noise_label = tk.Label(self.noise_frame, bg="lightgrey")
        self.noise_label.pack(fill=tk.BOTH, expand=True)


        self.filepath = None

    def upload_image(self):
        """Opens a file dialog to select an image and displays it."""
        f_types = [('Image Files', '*.jpg *.jpeg *.png')]
        self.filepath = filedialog.askopenfilename(filetypes=f_types)
        if not self.filepath:
            return

        try:
            self.display_image(self.filepath, self.image_label)
            self.analyze_button.config(state=tk.NORMAL)
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Image loaded. Ready to analyze.")
            self.results_text.config(state=tk.DISABLED)
            
            # Reset verdict
            self.verdict_label.config(text="Ready to analyze", fg="gray")
            self.confidence_label.config(text="")
            self.ai_gen_label.config(text="0%")
            self.ai_edit_label.config(text="0%")
            self.real_photo_label.config(text="0%")

            # Clear previous analysis images
            for label in [self.ela_label, self.freq_label, self.noise_label]:
                label.config(image='', text='')
                label.image = None

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")
            self.filepath = None

    def analyze_image(self):
        """Performs all forensic analyses on the uploaded image."""
        if not self.filepath:
            messagebox.showwarning("Warning", "Please upload an image first.")
            return
        
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Analyzing...\n\n")
        self.verdict_label.config(text="Analyzing...", fg="blue")
        self.root.update_idletasks()

        # 1. Metadata Analysis
        self.results_text.insert(tk.END, "=== METADATA ANALYSIS ===\n")
        metadata = extract_metadata(self.filepath)
        if metadata.get('anomalies'):
            for anomaly in metadata['anomalies']:
                self.results_text.insert(tk.END, f"⚠ {anomaly}\n")
        self.results_text.insert(tk.END, f"Format: {metadata.get('format', 'Unknown')}\n")
        self.results_text.insert(tk.END, f"Size: {metadata.get('size', 'Unknown')}\n\n")
        self.root.update_idletasks()

        # 2. JPEG Artifacts Analysis
        self.results_text.insert(tk.END, "=== JPEG ANALYSIS ===\n")
        jpeg_analysis = analyze_jpeg_artifacts(self.filepath)
        self.results_text.insert(tk.END, f"Blockiness Score: {jpeg_analysis.get('blockiness_score', 0):.2f}\n")
        self.results_text.insert(tk.END, f"Quality Estimate: {jpeg_analysis.get('compression_quality_estimate', 'N/A')}\n")
        if jpeg_analysis.get('is_suspicious'):
            self.results_text.insert(tk.END, "⚠ Suspicious JPEG patterns detected\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 3. Chromatic Aberration Analysis
        self.results_text.insert(tk.END, "=== CHROMATIC ABERRATION ===\n")
        chromatic_analysis = analyze_chromatic_aberration(self.filepath)
        self.results_text.insert(tk.END, f"Aberration Score: {chromatic_analysis.get('aberration_score', 0):.6f}\n")
        if chromatic_analysis.get('has_chromatic_aberration'):
            self.results_text.insert(tk.END, "✓ Natural lens aberration present\n")
        if chromatic_analysis.get('is_suspicious'):
            self.results_text.insert(tk.END, "⚠ Missing expected aberration\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 4. Color Distribution Analysis
        self.results_text.insert(tk.END, "=== COLOR ANALYSIS ===\n")
        color_analysis = analyze_color_distribution(self.filepath)
        self.results_text.insert(tk.END, f"Avg Saturation: {color_analysis.get('color_saturation_avg', 0):.2f}\n")
        self.results_text.insert(tk.END, f"Histogram Uniformity: {color_analysis.get('histogram_uniformity', 0):.2f}\n")
        if color_analysis.get('ai_signature_detected'):
            self.results_text.insert(tk.END, "⚠ AI color signature detected\n")
        if color_analysis.get('unusual_patterns'):
            self.results_text.insert(tk.END, "⚠ Unusual color patterns\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 5. Texture Consistency Analysis
        self.results_text.insert(tk.END, "=== TEXTURE ANALYSIS ===\n")
        texture_analysis = analyze_texture_consistency(self.filepath)
        self.results_text.insert(tk.END, f"Texture Variance: {texture_analysis.get('texture_variance', 0):.2f}\n")
        self.results_text.insert(tk.END, f"Smoothness Score: {texture_analysis.get('smoothness_score', 0):.2f}\n")
        if texture_analysis.get('repetition_detected'):
            self.results_text.insert(tk.END, "⚠ Repetitive patterns found\n")
        if texture_analysis.get('is_suspicious'):
            self.results_text.insert(tk.END, "⚠ Suspicious texture patterns\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 6. ADVANCED: GAN Fingerprint Detection
        self.results_text.insert(tk.END, "=== GAN FINGERPRINT DETECTION ===\n")
        gan_detection = detect_gan_fingerprint(self.filepath)
        self.results_text.insert(tk.END, f"High-Freq Score: {gan_detection.get('high_freq_pattern_score', 0):.6f}\n")
        self.results_text.insert(tk.END, f"Spectral Residual: {gan_detection.get('spectral_residual_score', 0):.2f}\n")
        if gan_detection.get('gan_signature_detected'):
            self.results_text.insert(tk.END, "⚠⚠ GAN SIGNATURE DETECTED\n")
        if gan_detection.get('is_suspicious'):
            self.results_text.insert(tk.END, "⚠ Suspicious frequency patterns\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 7. ADVANCED: Noise Inconsistency
        self.results_text.insert(tk.END, "=== NOISE INCONSISTENCY ===\n")
        noise_inconsistency = analyze_noise_inconsistency(self.filepath)
        self.results_text.insert(tk.END, f"Regions Analyzed: {noise_inconsistency.get('regions_analyzed')}\n")
        self.results_text.insert(tk.END, f"Suspicious Regions: {noise_inconsistency.get('suspicious_regions')}\n")
        self.results_text.insert(tk.END, f"Noise Variance STD: {noise_inconsistency.get('noise_variance_std', 0):.2f}\n")
        if noise_inconsistency.get('is_suspicious'):
            self.results_text.insert(tk.END, f"⚠ Noise inconsistency ({noise_inconsistency.get('confidence')} confidence)\n")
        else:
            self.results_text.insert(tk.END, "✓ Consistent sensor noise\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 8. ADVANCED: Benford's Law
        self.results_text.insert(tk.END, "=== BENFORD'S LAW ANALYSIS ===\n")
        benford_analysis = benford_law_analysis(self.filepath)
        self.results_text.insert(tk.END, f"Deviation: {benford_analysis.get('benford_deviation', 0):.4f}\n")
        self.results_text.insert(tk.END, f"P-value: {benford_analysis.get('p_value', 0):.4f}\n")
        if benford_analysis.get('follows_benford'):
            self.results_text.insert(tk.END, "✓ Follows Benford's Law (natural)\n")
        if benford_analysis.get('is_suspicious'):
            self.results_text.insert(tk.END, "⚠ Deviates from Benford's Law\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 9. ADVANCED: CFA Pattern Detection
        self.results_text.insert(tk.END, "=== CFA PATTERN DETECTION ===\n")
        cfa_detection = detect_cfa_pattern(self.filepath)
        self.results_text.insert(tk.END, f"CFA Strength: {cfa_detection.get('cfa_strength', 0):.4f}\n")
        self.results_text.insert(tk.END, f"Pattern Type: {cfa_detection.get('pattern_type', 'Unknown')}\n")
        if cfa_detection.get('cfa_pattern_detected'):
            self.results_text.insert(tk.END, "✓✓ REAL CAMERA SENSOR DETECTED\n")
        if cfa_detection.get('is_suspicious'):
            self.results_text.insert(tk.END, "⚠ No CFA pattern (not from camera)\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 10. ADVANCED: Double JPEG Compression
        self.results_text.insert(tk.END, "=== DOUBLE JPEG COMPRESSION ===\n")
        double_jpeg = detect_double_jpeg_compression(self.filepath)
        self.results_text.insert(tk.END, f"Compression Est: {double_jpeg.get('compression_count_estimate')} time(s)\n")
        if double_jpeg.get('double_compression_detected'):
            self.results_text.insert(tk.END, "⚠ Double compression detected (edited)\n")
        if double_jpeg.get('likely_edited'):
            self.results_text.insert(tk.END, "⚠ Image likely edited\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 11. ADVANCED: Gradient Analysis
        self.results_text.insert(tk.END, "=== GRADIENT ANALYSIS ===\n")
        gradient_analysis = analyze_gradient_anomalies(self.filepath)
        self.results_text.insert(tk.END, f"Gradient Smoothness: {gradient_analysis.get('gradient_smoothness', 0):.2f}\n")
        self.results_text.insert(tk.END, f"Sharp Transitions: {gradient_analysis.get('sharp_transition_count')}\n")
        if gradient_analysis.get('unnatural_smoothness_detected'):
            self.results_text.insert(tk.END, "⚠ Unnatural smoothness detected\n")
        self.results_text.insert(tk.END, "\n")
        self.root.update_idletasks()

        # 12. ELA
        self.results_text.insert(tk.END, "=== ERROR LEVEL ANALYSIS ===\n")
        ela_image = perform_ela(self.filepath)
        if ela_image:
            self.display_image(ela_image, self.ela_label)
            self.results_text.insert(tk.END, "✓ ELA visualization generated\n\n")
        else:
            self.results_text.insert(tk.END, "✗ ELA failed\n\n")
        self.root.update_idletasks()

        # 13. Frequency Analysis
        self.results_text.insert(tk.END, "=== FREQUENCY ANALYSIS ===\n")
        freq_image = analyze_frequency(self.filepath)
        if freq_image:
            self.display_image(freq_image, self.freq_label)
            self.results_text.insert(tk.END, "✓ Frequency spectrum generated\n\n")
        else:
            self.results_text.insert(tk.END, "✗ Frequency analysis failed\n\n")
        self.root.update_idletasks()
        
        # 14. Noise Analysis
        self.results_text.insert(tk.END, "=== NOISE PATTERN ANALYSIS ===\n")
        noise_map = extract_noise_map(self.filepath)
        if noise_map:
            self.display_image(noise_map, self.noise_label)
            self.results_text.insert(tk.END, "✓ Noise map generated\n\n")
        else:
            self.results_text.insert(tk.END, "✗ Noise analysis failed\n\n")
        self.root.update_idletasks()

        # 15. CLASSIFICATION - Final Verdict
        self.results_text.insert(tk.END, "="*40 + "\n")
        self.results_text.insert(tk.END, "=== FINAL CLASSIFICATION ===\n")
        self.results_text.insert(tk.END, "="*40 + "\n\n")
        
        classification = classify_image(
            metadata, 
            jpeg_analysis, 
            chromatic_analysis, 
            color_analysis, 
            texture_analysis,
            gan_detection,
            noise_inconsistency,
            benford_analysis,
            cfa_detection,
            double_jpeg,
            gradient_analysis,
            self.filepath
        )
        
        # Update verdict display
        verdict = classification['verdict']
        confidence = classification['confidence']
        probs = classification['probabilities']
        
        # Set verdict color
        if 'AI Generated' in verdict:
            verdict_color = "#f44336"  # Red
        elif 'AI Edited' in verdict:
            verdict_color = "#ff9800"  # Orange
        else:
            verdict_color = "#4CAF50"  # Green
        
        self.verdict_label.config(text=verdict, fg=verdict_color)
        self.confidence_label.config(text=f"Confidence: {confidence}")
        
        # Update probability labels
        self.ai_gen_label.config(text=f"{probs['ai_generated']}%")
        self.ai_edit_label.config(text=f"{probs['ai_edited']}%")
        self.real_photo_label.config(text=f"{probs['real_photo']}%")
        
        # Display verdict in results
        self.results_text.insert(tk.END, f"VERDICT: {verdict}\n")
        self.results_text.insert(tk.END, f"Confidence: {confidence}\n\n")
        self.results_text.insert(tk.END, "Probabilities:\n")
        self.results_text.insert(tk.END, f"  AI Generated:  {probs['ai_generated']}%\n")
        self.results_text.insert(tk.END, f"  AI Edited:     {probs['ai_edited']}%\n")
        self.results_text.insert(tk.END, f"  Real Photo:    {probs['real_photo']}%\n\n")
        
        # Display evidence
        self.results_text.insert(tk.END, "Key Evidence:\n")
        evidence = classification['evidence']
        for category, items in evidence.items():
            if items:
                self.results_text.insert(tk.END, f"\n{category.upper()}:\n")
                for item in items:
                    self.results_text.insert(tk.END, f"  • {item}\n")
        
        self.results_text.config(state=tk.DISABLED)
        messagebox.showinfo("Analysis Complete", f"Verdict: {verdict}\nConfidence: {confidence}")

    def display_image(self, image_path_or_obj, label):
        """Displays an image on a given label."""
        if isinstance(image_path_or_obj, str):
            img = Image.open(image_path_or_obj)
        else: # It's a PIL Image object
            img = image_path_or_obj

        # Use a fixed size for display in the tabs for consistency
        img.thumbnail((self.right_panel.winfo_width() - 20, self.right_panel.winfo_height() - 40))
        photo = ImageTk.PhotoImage(img)

        label.config(image=photo, text="")
        label.image = photo

if __name__ == "__main__":
    root = tk.Tk()
    app = MetaForensApp(root)
    root.mainloop()
