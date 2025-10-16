# ============================================
# METAFORENS - CIFAKE DATASET TESTING
# Complete Google Colab Code (FIXED VERSION)
# ============================================

# ============================================
# STEP 1: INSTALLATION & SETUP
# ============================================
print("="*60)
print("STEP 1: Installing Dependencies & Setting Up MetaForens")
print("="*60)

!pip install -q kaggle pillow numpy pandas matplotlib seaborn tqdm opencv-python scikit-image scipy scikit-learn

import os
import sys

# Ensure we're in /content directory
os.chdir('/content')

print("\nCloning MetaForens repository...")
# Clean any existing clone
!rm -rf MetaForens
!git clone https://github.com/kingknight07/MetaForens.git

# Verify clone succeeded
if not os.path.exists('/content/MetaForens'):
    print("❌ Clone failed! Trying alternative method...")
    !git clone --depth 1 https://github.com/kingknight07/MetaForens.git
    
if not os.path.exists('/content/MetaForens'):
    raise Exception("Failed to clone repository. Please check your internet connection.")

# Change to repository directory
os.chdir('/content/MetaForens')
print(f"✓ Working directory: {os.getcwd()}")

# List files to verify structure
print("\n📂 Repository structure:")
!ls -la

# Add to Python path to ensure proper imports
sys.path.insert(0, '/content/MetaForens')

print("\nInstalling MetaForens requirements...")
!pip install -q -r requirements.txt

# Install in development mode
print("Installing MetaForens library...")
!pip install -q -e .

# Verify the fix is present
print("\n🔍 Verifying import fix...")
!grep "from forensics.noise_inconsistency" metaforens.py

print("\n✅ Installation complete!\n")

# ============================================
# STEP 2: TEST IMPORTS
# ============================================
print("="*60)
print("STEP 2: Testing Imports")
print("="*60)

try:
    from metaforens import MetaForens, analyze_image
    detector = MetaForens()
    print(f"✓ MetaForens imported successfully")
    print(f"✓ Version: {detector.version}")
    print(f"✓ Forensic analyses: {detector.analyses_count}")
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
    raise

print("\n✅ All imports successful!\n")

# ============================================
# STEP 3: KAGGLE CREDENTIALS
# ============================================
print("="*60)
print("STEP 3: Kaggle Setup")
print("="*60)
print("\nPlease upload your kaggle.json file")
print("Get it from: https://www.kaggle.com/settings")
print("Click 'Create New API Token'\n")

from google.colab import files
uploaded = files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

print("\n✅ Kaggle credentials configured!\n")

# ============================================
# STEP 4: DOWNLOAD CIFAKE DATASET
# ============================================
print("="*60)
print("STEP 4: Downloading CIFAKE Dataset")
print("="*60)

print("\nDownloading dataset (this may take a few minutes)...")
!kaggle datasets download -d birdy654/cifake-real-and-ai-generated-synthetic-images

print("\nExtracting dataset...")
!unzip -q cifake-real-and-ai-generated-synthetic-images.zip -d cifake_dataset

print("\n✅ Dataset downloaded and extracted!")

# Check structure
print("\nDataset structure:")
!ls -la cifake_dataset/train/

# ============================================
# STEP 5: DATASET EXPLORATION
# ============================================
print("\n" + "="*60)
print("STEP 5: Dataset Exploration")
print("="*60)

import random
from PIL import Image
import matplotlib.pyplot as plt

# Define paths
real_path = "cifake_dataset/train/REAL"
fake_path = "cifake_dataset/train/FAKE"

# Count images
real_images = [f for f in os.listdir(real_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
fake_images = [f for f in os.listdir(fake_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

print(f"\n📊 Dataset Statistics:")
print(f"Real images: {len(real_images):,}")
print(f"Fake (AI) images: {len(fake_images):,}")
print(f"Total images: {len(real_images) + len(fake_images):,}")

# Visualize samples
def show_samples(n=5):
    fig, axes = plt.subplots(2, n, figsize=(15, 6))
    fig.suptitle('Sample Images from CIFAKE Dataset', fontsize=16, fontweight='bold')
    
    real_samples = random.sample(real_images, n)
    for idx, img_name in enumerate(real_samples):
        img = Image.open(os.path.join(real_path, img_name))
        axes[0, idx].imshow(img)
        axes[0, idx].set_title('REAL', fontsize=12, color='green')
        axes[0, idx].axis('off')
    
    fake_samples = random.sample(fake_images, n)
    for idx, img_name in enumerate(fake_samples):
        img = Image.open(os.path.join(fake_path, img_name))
        axes[1, idx].imshow(img)
        axes[1, idx].set_title('FAKE (AI)', fontsize=12, color='red')
        axes[1, idx].axis('off')
    
    plt.tight_layout()
    plt.show()

print("\nDisplaying sample images...")
show_samples(5)

# ============================================
# STEP 6: SINGLE IMAGE TESTING
# ============================================
print("\n" + "="*60)
print("STEP 6: Testing on Individual Images")
print("="*60)

# Test on real image
test_real_img = os.path.join(real_path, real_images[0])
print(f"\n🔍 Analyzing REAL image: {real_images[0]}")
result_real = detector.analyze(test_real_img)

print(f"\n📊 Results:")
print(f"  Verdict: {result_real['verdict']}")
print(f"  Confidence: {result_real['confidence']}")
print(f"  Probabilities:")
print(f"    • AI Generated: {result_real['probabilities']['ai_generated']:.2f}%")
print(f"    • AI Edited: {result_real['probabilities']['ai_edited']:.2f}%")
print(f"    • Real Photo: {result_real['probabilities']['real_photo']:.2f}%")

# Test on fake image
test_fake_img = os.path.join(fake_path, fake_images[0])
print(f"\n🔍 Analyzing FAKE (AI-generated) image: {fake_images[0]}")
result_fake = detector.analyze(test_fake_img)

print(f"\n📊 Results:")
print(f"  Verdict: {result_fake['verdict']}")
print(f"  Confidence: {result_fake['confidence']}")
print(f"  Probabilities:")
print(f"    • AI Generated: {result_fake['probabilities']['ai_generated']:.2f}%")
print(f"    • AI Edited: {result_fake['probabilities']['ai_edited']:.2f}%")
print(f"    • Real Photo: {result_fake['probabilities']['real_photo']:.2f}%")

# ============================================
# STEP 7: BATCH TESTING
# ============================================
print("\n" + "="*60)
print("STEP 7: Batch Testing (Sample of 200 images)")
print("="*60)

from tqdm import tqdm
import pandas as pd

def test_batch(n_real=100, n_fake=100):
    """Test on sample of images"""
    results = []
    
    # Test real images
    print(f"\n🔍 Testing {n_real} REAL images...")
    real_sample = random.sample(real_images, min(n_real, len(real_images)))
    
    for img_name in tqdm(real_sample, desc="Analyzing REAL images"):
        img_path = os.path.join(real_path, img_name)
        try:
            result = detector.analyze(img_path)
            results.append({
                'image': img_name,
                'true_label': 'REAL',
                'predicted_verdict': result['verdict'],
                'confidence': result['confidence'],
                'ai_generated_prob': result['probabilities']['ai_generated'],
                'ai_edited_prob': result['probabilities']['ai_edited'],
                'real_photo_prob': result['probabilities']['real_photo']
            })
        except Exception as e:
            print(f"Error on {img_name}: {str(e)[:100]}")
    
    # Test fake images
    print(f"\n🔍 Testing {n_fake} FAKE (AI-generated) images...")
    fake_sample = random.sample(fake_images, min(n_fake, len(fake_images)))
    
    for img_name in tqdm(fake_sample, desc="Analyzing FAKE images"):
        img_path = os.path.join(fake_path, img_name)
        try:
            result = detector.analyze(img_path)
            results.append({
                'image': img_name,
                'true_label': 'FAKE',
                'predicted_verdict': result['verdict'],
                'confidence': result['confidence'],
                'ai_generated_prob': result['probabilities']['ai_generated'],
                'ai_edited_prob': result['probabilities']['ai_edited'],
                'real_photo_prob': result['probabilities']['real_photo']
            })
        except Exception as e:
            print(f"Error on {img_name}: {str(e)[:100]}")
    
    return pd.DataFrame(results)

# Run batch test
df_results = test_batch(n_real=100, n_fake=100)

# Save results
df_results.to_csv('metaforens_cifake_results.csv', index=False)
print("\n✅ Results saved to 'metaforens_cifake_results.csv'")

# Display sample results
print("\n📋 Sample Results (first 10):")
print(df_results[['image', 'true_label', 'predicted_verdict', 'confidence']].head(10).to_string(index=False))

# ============================================
# STEP 8: CALCULATE PERFORMANCE METRICS
# ============================================
print("\n" + "="*60)
print("STEP 8: Performance Metrics")
print("="*60)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns

# Map predictions to binary labels
df_results['predicted_binary'] = df_results['predicted_verdict'].apply(
    lambda x: 'REAL' if 'Real' in x else 'FAKE'
)

# Calculate metrics
accuracy = accuracy_score(df_results['true_label'], df_results['predicted_binary'])
precision = precision_score(df_results['true_label'], df_results['predicted_binary'], pos_label='FAKE')
recall = recall_score(df_results['true_label'], df_results['predicted_binary'], pos_label='FAKE')
f1 = f1_score(df_results['true_label'], df_results['predicted_binary'], pos_label='FAKE')

print(f"\n📊 METAFORENS PERFORMANCE:")
print(f"\n  ✅ Overall Accuracy: {accuracy*100:.2f}%")
print(f"  🎯 Precision (AI Detection): {precision*100:.2f}%")
print(f"  🔍 Recall (AI Detection): {recall*100:.2f}%")
print(f"  📈 F1-Score: {f1*100:.2f}%")

# Confusion Matrix
cm = confusion_matrix(df_results['true_label'], df_results['predicted_binary'], labels=['REAL', 'FAKE'])

print(f"\n📋 Confusion Matrix:")
print(f"{'':20} Predicted REAL  Predicted FAKE")
print(f"Actual REAL      {cm[0][0]:^14}  {cm[0][1]:^14}")
print(f"Actual FAKE      {cm[1][0]:^14}  {cm[1][1]:^14}")

# Detailed breakdown
real_df = df_results[df_results['true_label'] == 'REAL']
fake_df = df_results[df_results['true_label'] == 'FAKE']

real_correct = (real_df['predicted_binary'] == 'REAL').sum()
fake_correct = (fake_df['predicted_binary'] == 'FAKE').sum()

print(f"\n📌 Detailed Breakdown:")
print(f"  Real images correctly identified: {real_correct}/{len(real_df)} ({real_correct/len(real_df)*100:.2f}%)")
print(f"  Fake images correctly identified: {fake_correct}/{len(fake_df)} ({fake_correct/len(fake_df)*100:.2f}%)")

# Visualize Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Count'},
            xticklabels=['Predicted REAL', 'Predicted FAKE'],
            yticklabels=['Actual REAL', 'Actual FAKE'],
            annot_kws={'size': 16})
plt.title(f'MetaForens Confusion Matrix on CIFAKE Dataset\nAccuracy: {accuracy*100:.1f}%', 
          fontsize=14, fontweight='bold', pad=20)
plt.ylabel('True Label', fontsize=12, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.show()

# ============================================
# STEP 9: CONFIDENCE ANALYSIS
# ============================================
print("\n" + "="*60)
print("STEP 9: Confidence Level Analysis")
print("="*60)

df_results['is_correct'] = df_results['true_label'] == df_results['predicted_binary']

correct_df = df_results[df_results['is_correct'] == True]
incorrect_df = df_results[df_results['is_correct'] == False]

print(f"\n📊 Confidence Distribution:")
print(f"  Correct predictions: {len(correct_df)}")
print(f"  Incorrect predictions: {len(incorrect_df)}")

# Visualize confidence levels
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Correct predictions
if len(correct_df) > 0:
    confidence_correct = correct_df['confidence'].value_counts()
    axes[0].bar(confidence_correct.index, confidence_correct.values, color='green', alpha=0.7, edgecolor='black')
    axes[0].set_title(f'Confidence Levels for CORRECT Predictions\n(n={len(correct_df)})', 
                     fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Confidence Level', fontsize=11)
    axes[0].set_ylabel('Count', fontsize=11)
    axes[0].grid(axis='y', alpha=0.3)

# Incorrect predictions
if len(incorrect_df) > 0:
    confidence_incorrect = incorrect_df['confidence'].value_counts()
    axes[1].bar(confidence_incorrect.index, confidence_incorrect.values, color='red', alpha=0.7, edgecolor='black')
    axes[1].set_title(f'Confidence Levels for INCORRECT Predictions\n(n={len(incorrect_df)})', 
                     fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Confidence Level', fontsize=11)
    axes[1].set_ylabel('Count', fontsize=11)
    axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('confidence_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n  High confidence correct: {len(correct_df[correct_df['confidence'] == 'High'])}")
print(f"  High confidence incorrect: {len(incorrect_df[incorrect_df['confidence'] == 'High'])}")

# ============================================
# STEP 10: PROBABILITY DISTRIBUTIONS
# ============================================
print("\n" + "="*60)
print("STEP 10: Probability Distribution Analysis")
print("="*60)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Probability Distributions: REAL vs FAKE Images', fontsize=16, fontweight='bold')

# Real images
axes[0, 0].hist(real_df['ai_generated_prob'], bins=20, color='blue', alpha=0.7, edgecolor='black')
axes[0, 0].set_title('REAL Images: AI Generated Probability', fontweight='bold')
axes[0, 0].set_xlabel('Probability (%)')
axes[0, 0].set_ylabel('Count')
axes[0, 0].axvline(50, color='red', linestyle='--', linewidth=2, label='50% threshold')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

axes[0, 1].hist(real_df['ai_edited_prob'], bins=20, color='orange', alpha=0.7, edgecolor='black')
axes[0, 1].set_title('REAL Images: AI Edited Probability', fontweight='bold')
axes[0, 1].set_xlabel('Probability (%)')
axes[0, 1].set_ylabel('Count')
axes[0, 1].grid(alpha=0.3)

axes[0, 2].hist(real_df['real_photo_prob'], bins=20, color='green', alpha=0.7, edgecolor='black')
axes[0, 2].set_title('REAL Images: Real Photo Probability', fontweight='bold')
axes[0, 2].set_xlabel('Probability (%)')
axes[0, 2].set_ylabel('Count')
axes[0, 2].grid(alpha=0.3)

# Fake images
axes[1, 0].hist(fake_df['ai_generated_prob'], bins=20, color='blue', alpha=0.7, edgecolor='black')
axes[1, 0].set_title('FAKE Images: AI Generated Probability', fontweight='bold')
axes[1, 0].set_xlabel('Probability (%)')
axes[1, 0].set_ylabel('Count')
axes[1, 0].axvline(50, color='red', linestyle='--', linewidth=2, label='50% threshold')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

axes[1, 1].hist(fake_df['ai_edited_prob'], bins=20, color='orange', alpha=0.7, edgecolor='black')
axes[1, 1].set_title('FAKE Images: AI Edited Probability', fontweight='bold')
axes[1, 1].set_xlabel('Probability (%)')
axes[1, 1].set_ylabel('Count')
axes[1, 1].grid(alpha=0.3)

axes[1, 2].hist(fake_df['real_photo_prob'], bins=20, color='green', alpha=0.7, edgecolor='black')
axes[1, 2].set_title('FAKE Images: Real Photo Probability', fontweight='bold')
axes[1, 2].set_xlabel('Probability (%)')
axes[1, 2].set_ylabel('Count')
axes[1, 2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('probability_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

# Average probabilities
print(f"\n📊 Average Probabilities:")
print(f"\n  REAL Images:")
print(f"    AI Generated: {real_df['ai_generated_prob'].mean():.2f}%")
print(f"    AI Edited: {real_df['ai_edited_prob'].mean():.2f}%")
print(f"    Real Photo: {real_df['real_photo_prob'].mean():.2f}%")

print(f"\n  FAKE Images:")
print(f"    AI Generated: {fake_df['ai_generated_prob'].mean():.2f}%")
print(f"    AI Edited: {fake_df['ai_edited_prob'].mean():.2f}%")
print(f"    Real Photo: {fake_df['real_photo_prob'].mean():.2f}%")

# ============================================
# STEP 11: GENERATE PERFORMANCE REPORT
# ============================================
print("\n" + "="*60)
print("STEP 11: Generating Performance Report")
print("="*60)

report = f"""
{'='*70}
METAFORENS PERFORMANCE REPORT ON CIFAKE DATASET
{'='*70}

Dataset Information:
  Source: CIFAKE (Real and AI-Generated Synthetic Images)
  URL: https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images
  
Test Configuration:
  Total images tested: {len(df_results)}
  Real images: {len(real_df)}
  Fake (AI) images: {len(fake_df)}

PERFORMANCE METRICS:
  Overall Accuracy: {accuracy*100:.2f}%
  Precision (AI Detection): {precision*100:.2f}%
  Recall (AI Detection): {recall*100:.2f}%
  F1-Score: {f1*100:.2f}%

DETAILED BREAKDOWN:
  Real images correctly identified: {real_correct}/{len(real_df)} ({real_correct/len(real_df)*100:.2f}%)
  Fake images correctly identified: {fake_correct}/{len(fake_df)} ({fake_correct/len(fake_df)*100:.2f}%)

VERDICT DISTRIBUTION:
{df_results['predicted_verdict'].value_counts().to_string()}

CONFIDENCE DISTRIBUTION:
{df_results['confidence'].value_counts().to_string()}

AVERAGE PROBABILITIES - REAL IMAGES:
  AI Generated: {real_df['ai_generated_prob'].mean():.2f}%
  AI Edited: {real_df['ai_edited_prob'].mean():.2f}%
  Real Photo: {real_df['real_photo_prob'].mean():.2f}%

AVERAGE PROBABILITIES - FAKE IMAGES:
  AI Generated: {fake_df['ai_generated_prob'].mean():.2f}%
  AI Edited: {fake_df['ai_edited_prob'].mean():.2f}%
  Real Photo: {fake_df['real_photo_prob'].mean():.2f}%

{'='*70}
Report generated by MetaForens v{detector.version}
GitHub: https://github.com/kingknight07/MetaForens
{'='*70}
"""

# Save report
with open('metaforens_performance_report.txt', 'w') as f:
    f.write(report)

print(report)
print("\n✅ Report saved to 'metaforens_performance_report.txt'")

# ============================================
# STEP 12: DOWNLOAD RESULTS
# ============================================
print("\n" + "="*60)
print("STEP 12: Downloading Results")
print("="*60)

print("\n📥 Preparing files for download...")

files.download('metaforens_cifake_results.csv')
files.download('metaforens_performance_report.txt')
files.download('confusion_matrix.png')
files.download('confidence_analysis.png')
files.download('probability_distributions.png')

print("\n✅ All files downloaded!")

# ============================================
# FINAL SUMMARY
# ============================================
print("\n" + "="*70)
print("🎉 TESTING COMPLETE!")
print("="*70)

print(f"""
✅ MetaForens successfully tested on CIFAKE dataset!

📊 Key Results:
  • Accuracy: {accuracy*100:.2f}%
  • Images tested: {len(df_results)}
  • Real images identified: {real_correct}/{len(real_df)} ({real_correct/len(real_df)*100:.1f}%)
  • Fake images identified: {fake_correct}/{len(fake_df)} ({fake_correct/len(fake_df)*100:.1f}%)

📁 Generated Files:
  ✓ metaforens_cifake_results.csv - Detailed results
  ✓ metaforens_performance_report.txt - Performance summary
  ✓ confusion_matrix.png - Confusion matrix visualization
  ✓ confidence_analysis.png - Confidence level analysis
  ✓ probability_distributions.png - Probability distributions

📚 Repository: https://github.com/kingknight07/MetaForens
👤 Author: kingknight07
📧 Email: shuklaayush0704@gmail.com

Thank you for using MetaForens! 🔍
""")

print("="*70)
