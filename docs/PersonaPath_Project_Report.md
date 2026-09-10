# PersonaPath Project Report

## 1. Project Overview

PersonaPath is a multi-modal speaking assessment project focused on analyzing presentation delivery through both visual and vocal signals. The current implementation work, based on the active project notebooks, focuses on the **Presentation Pro** phase.

The system uses two complementary AI modules:

1. **Video-based facial emotion recognition**
   - A fine-tuned MobileNetV2 CNN predicts facial emotion from video frames.
   - The model classifies faces into FER-2013 emotion categories.

2. **Audio-based vocal confidence scoring**
   - A 2-layer LSTM predicts a vocal confidence score from direct audio features.
   - The model uses MFCCs, delta features, pitch, energy, and zero crossing rate.

Together, these modules support a presentation feedback pipeline where a user can upload or record a speaking clip and receive emotion and vocal confidence indicators.

This report considers progress only from the following notebooks:

- `notebooks/CNN_Emotion_Training.ipynb`
- `notebooks/LSTM_Confidence_Training.ipynb`
- `notebooks/Test_LSTM_Confidence_Model.ipynb`
- `notebooks/Test_Video_Emotion.ipynb`

## 2. CNN Emotion Recognition Module

### 2.1 Objective

The CNN module predicts facial emotion from images/video frames. It is intended to support the visual side of Presentation Pro by detecting facial emotional cues during a speaking video.

### 2.2 Dataset

The notebook uses the FER-2013 dataset from Hugging Face:

```text
Dataset: AutumnQiu/fer2013
Train samples: 28,709
Validation samples: 3,589
Test samples: 3,589
```

Emotion classes:

```text
Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
```

### 2.3 Model Architecture

The model is based on MobileNetV2 with transfer learning:

```text
Input image
-> Resize to 224x224
-> RandomFlip / RandomRotation / RandomZoom
-> MobileNetV2 preprocess_input
-> MobileNetV2 base
-> GlobalAveragePooling2D
-> Dense(128, ReLU)
-> Dropout(0.2)
-> Dense(7, Softmax)
```

The initial MobileNetV2 base is loaded with ImageNet weights. Training begins with the base frozen, then later phases unfreeze deeper layers for fine-tuning.

### 2.4 Training Strategy

The CNN notebook includes several training stages:

- Baseline training with a frozen MobileNetV2 base.
- Refined training with learning-rate reduction.
- Class-weighted fine-tuning to address FER-2013 imbalance.
- Phase 3 fine-tuning by unfreezing the top 30 MobileNetV2 layers.
- Phase 4 fine-tuning by unfreezing the top 50 MobileNetV2 layers.

Callbacks used include:

- `EarlyStopping`
- `ModelCheckpoint`
- `ReduceLROnPlateau`

### 2.5 CNN Results

The notebook records the following final training progress:

```text
Baseline validation accuracy: 52.00%
Phase 3 validation accuracy: 60.66%
Phase 4 continued best validation accuracy: 62.61%
Total gain over baseline: +10.61 percentage points
```

The final fine-tuned model is saved to Google Drive:

```text
/content/drive/MyDrive/PersonaPath/checkpoints/cnn_emotion_phase4.keras
```

### 2.6 CNN Visualizations

The CNN notebook saves multiple visualizations to Drive:

- FER-2013 class distribution
- Raw sample images
- Training accuracy/loss curves
- Refined training curves
- Fine-tuning comparison curves
- Phase 4 continued training curves
- Overall training summary

## 3. Video Emotion Inference Module

### 3.1 Objective

`Test_Video_Emotion.ipynb` tests the trained CNN emotion model on an input video. The goal is to produce an output video with:

- face bounding boxes
- emotion labels
- prediction confidence scores
- preserved audio when possible

### 3.2 Inference Pipeline

The notebook performs the following steps:

1. Loads the fine-tuned CNN model from Drive or local paths.
2. Handles Keras Lambda deserialization issues by rebuilding the MobileNetV2 architecture and loading weights if needed.
3. Runs a smoke test to verify model prediction works.
4. Opens the input video with OpenCV.
5. Detects faces using Haar cascade face detection.
6. Crops each detected face.
7. Resizes the face crop to `224x224`.
8. Runs emotion prediction.
9. Draws bounding boxes and labels on each frame.
10. Writes an annotated output video.
11. Uses `ffmpeg` to preserve audio and encode browser-friendly H.264 output.

### 3.3 Video Test Result

The notebook output shows a successful full video run:

```text
Frames processed: 338
Frames with faces: 338
Detected faces: 339
Predictions: 339
Prediction errors: 0
Audio preserved: True
Output video: output_emotion.mp4
```

This confirms that video emotion inference works end-to-end.

## 4. LSTM Vocal Confidence Module

### 4.1 Objective

The LSTM module estimates vocal confidence from speech audio. It does not classify facial emotion and does not evaluate pronunciation correctness. Instead, it predicts a confidence score from acoustic delivery cues.

The output is:

```text
Vocal confidence score: 0-100
```

### 4.2 Dataset

The notebook uses Mini LibriSpeech from OpenSLR:

```text
Dataset: Mini LibriSpeech
Purpose: proxy confidence training
Input type: speech audio clips
```

LibriSpeech does not contain human confidence labels. Therefore, the project creates proxy labels based on acoustic properties.

### 4.3 Proxy Label Generation

The confidence label is computed from:

- speech density
- RMS energy
- pitch variation

The proxy confidence score is in the range `[0, 1]`.

Observed label statistics:

```text
Mean: 0.742
Standard deviation: 0.071
Minimum: 0.457
Maximum: 0.955
```

This showed that the dataset was imbalanced toward higher-confidence labels.

### 4.4 Audio Feature Extraction

The LSTM uses direct numerical audio features rather than spectrogram images.

Each audio clip is loaded at:

```text
Sample rate: 16 kHz
```

The feature extractor creates:

```text
13 MFCC features
13 delta MFCC features
13 delta-delta MFCC features
1 pitch/F0 feature
1 RMS energy feature
1 zero crossing rate feature
```

Total:

```text
42 features per frame
```

Each sequence is padded or truncated to:

```text
200 frames
```

Final input shape:

```text
(200, 42)
```

### 4.5 Preprocessing

The notebook now performs preprocessing more carefully:

1. Splits the data before normalization.
2. Fits `StandardScaler` only on the training set.
3. Applies the same scaler to validation and test sets.
4. Saves scaler parameters for inference:

```text
/content/drive/MyDrive/PersonaPath/lstm_features/scaler_mean.npy
/content/drive/MyDrive/PersonaPath/lstm_features/scaler_scale.npy
```

This avoids validation/test leakage into preprocessing.

### 4.6 Imbalance Handling

A key issue was that labels were clustered mostly in medium/high confidence ranges. To address this, the notebook creates confidence bins:

```text
Low (<0.60): 73
Medium (0.60-0.75): 755
High (>=0.75): 691
```

The split is stratified by these bins:

```text
Train:      (1063, 200, 42)
Validation: (228, 200, 42)
Test:       (228, 200, 42)
```

Sample weights are used during training:

```text
Low confidence weight: 6.948
Medium confidence weight: 0.671
High confidence weight: 0.732
```

This prevents the model from ignoring rare low-confidence examples.

### 4.7 LSTM Architecture

The LSTM model architecture is:

```text
Input(200, 42)
-> LSTM(128, return_sequences=True)
-> Dropout(0.3)
-> LSTM(64)
-> Dropout(0.3)
-> Dense(32, ReLU)
-> Dense(1, Sigmoid)
```

Training configuration:

```text
Loss: Mean Squared Error
Optimizer: Adam
Metric: Mean Absolute Error
Batch size: 64
Maximum epochs: 50
```

Callbacks:

- `EarlyStopping`
- `ModelCheckpoint`
- `ReduceLROnPlateau`
- `CSVLogger`
- `BackupAndRestore`

### 4.8 LSTM Results

Final test results:

```text
Test MSE: 0.0022
Test MAE: 0.0344
Mean-baseline MAE: 0.0569
LSTM improvement over baseline: 2.25 confidence points
Prediction standard deviation: 0.0585
Target standard deviation: 0.0740
```

Human-readable interpretation:

```text
Average error: 3.4 confidence points on a 0-100 scale
```

Bin-wise evaluation:

```text
Low confidence:
  LSTM MAE: 6.34 points
  Mean baseline MAE: 18.16 points
  Test samples: 11

Medium confidence:
  LSTM MAE: 3.08 points
  Mean baseline MAE: 4.35 points
  Test samples: 114

High confidence:
  LSTM MAE: 3.53 points
  Mean baseline MAE: 5.84 points
  Test samples: 103
```

The model beats the mean baseline in all confidence bins, which suggests it learned useful acoustic patterns rather than simply predicting the label mean.

### 4.9 LSTM Saved Assets

The final model and best checkpoint are saved to Drive:

```text
/content/drive/MyDrive/PersonaPath/checkpoints/lstm_confidence_best.keras
/content/drive/MyDrive/PersonaPath/checkpoints/lstm_confidence_final.keras
```

Additional saved artifacts:

- scaler mean
- scaler scale
- training log CSV
- model summary
- test metrics JSON
- test predictions CSV
- score distribution plot
- MFCC heatmap
- high/low normalized MFCC comparison
- feature-confidence correlation plot
- feature comparison plot
- training curves
- predicted vs actual scatter
- residual distribution
- target vs prediction distribution
- bin-wise MAE vs baseline plot

The Hugging Face upload cell is configured for:

```text
iamnotpalak/personapath-lstm-vocal-confidence-mfcc
```

The inspected output confirms that at least the final model upload started/succeeded. The full Hugging Face repository should still be manually checked to verify all artifacts completed uploading.

## 5. LSTM Test Notebook

`Test_LSTM_Confidence_Model.ipynb` tests the saved vocal confidence model on new audio.

The notebook:

1. Loads the saved final LSTM model.
2. Loads saved scaler parameters.
3. Extracts the same 42 audio features.
4. Applies normalization.
5. Predicts a raw vocal confidence score.
6. Optionally applies heuristic adjustment based on presentation-style delivery cues.

Test outputs:

```text
Test_confidence_aud1.wav -> 83.9/100
test_confidence_aud2.wav -> 76.5/100
```

For the second test audio, additional delivery statistics were computed:

```text
Duration: 13.04 seconds
Silence ratio: 0.5755
RMS mean: 0.0302
Pitch standard deviation: 119.6248
Raw LSTM confidence: 76.5/100
Adjusted vocal confidence: 66.5/100
```

The adjusted score subtracts simple penalties for:

- high silence ratio
- very low RMS volume
- monotone pitch

This makes the score more aligned with human presentation-quality intuition.

## 6. Current Overall Progress

Completed:

- CNN emotion model trained on FER-2013.
- CNN model fine-tuned to 62.61% validation accuracy.
- CNN checkpoint saved to Drive.
- Video emotion inference notebook works end-to-end.
- Output video includes detected faces, emotion labels, confidence scores, and preserved audio.
- LSTM vocal confidence model trained on direct audio features.
- LSTM feature count corrected to 42.
- LSTM label imbalance addressed with stratified splitting and sample weights.
- LSTM evaluated against mean baseline.
- LSTM beats baseline overall and in all confidence bins.
- LSTM final model and scaler saved to Drive.
- LSTM testing notebook works on new audio.
- Hugging Face upload cells exist for CNN and LSTM.

## 7. Limitations

### CNN Limitations

- FER-2013 is a controlled facial emotion dataset, so webcam/video emotion predictions may be noisy in real-world lighting and pose conditions.
- Haar cascade face detection may fail on side profiles, occlusions, or poor lighting.
- The model predicts facial emotion classes, not full presentation confidence.

### LSTM Limitations

- The LSTM uses proxy confidence labels, not human-labeled confidence annotations.
- It predicts acoustic confidence cues, not true psychological confidence.
- Low-confidence test samples are limited, with only 11 examples in the low-confidence bin.
- LibriSpeech is clean read speech, not natural presentation speech with realistic nervousness, filler words, or audience pressure.
- The adjusted confidence score uses simple heuristics and should be described as post-processing, not learned model behavior.

## 8. Recommended Next Steps

1. Verify both Hugging Face repositories manually.
2. Add a short README section explaining:
   - CNN emotion recognition
   - LSTM proxy vocal confidence
   - required Drive/Hugging Face model files
3. Test both models on more real presentation-style videos/audio clips.
4. Combine CNN emotion output and LSTM confidence output in one final application notebook or Gradio app.
5. Add filler-word detection and WPM to improve presentation feedback.
6. Use the adjusted vocal confidence score in the final demo, while also reporting the raw LSTM score.

## 9. Final Summary

PersonaPath currently has two working AI components:

```text
Video frames -> MobileNetV2 CNN -> facial emotion prediction
Audio signal -> 42-feature LSTM -> vocal confidence score
```

The CNN pipeline is trained, saved, and tested on video. The LSTM pipeline is trained, evaluated, saved, and tested on new audio. The most important improvement is that the LSTM is now validated against a mean baseline and performs better across low, medium, and high confidence bins.

The project is ready to be presented as a working prototype for multi-modal presentation analysis, with the honest framing that vocal confidence is a proxy estimate based on acoustic delivery cues.
