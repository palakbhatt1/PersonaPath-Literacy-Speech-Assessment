# PersonaPath: Literacy & Speech Assessment AI

PersonaPath is a multi-modal AI system designed to act as a developmental speaking and personality assessment coach. It assesses and provides feedback for two primary demographics:
- **Phase 1 (Ages 5-10):** A Literacy Coach focused on pronunciation alignment, word-per-minute (WPM) reading speed, and hesitation detection.
- **Phase 2 (Ages 10+):** A Presentation Pro focused on vocal confidence and emotional delivery.

## 📁 Repository Structure

```text
PersonaPath-Literacy-Speech-Assessment/
│
├── notebooks/                   # Jupyter notebooks for training and inference
│   ├── Day1_2_CNN_Emotion_Training.ipynb        # Fine-tunes MobileNetV2 on FER-2013
│   ├── Day3_LSTM_Confidence_Training.ipynb      # Trains LSTM on Mini LibriSpeech
│   └── Day4_5_PersonaPath_App.ipynb             # Gradio Dashboard with Claude API
│
├── data/                        # Directory for local datasets (ignored in git)
├── models/                      # Directory for local saved models (ignored in git)
├── docs/                        # Project documentation and plans
│
├── requirements.txt             # Python dependencies
└── README.md                    # Project overview
```

## 🧠 Model Architecture

This project utilizes a multi-model architecture:
1. **Wav2Vec 2.0 (`facebook/wav2vec2-base-960h`):** Pretrained Transformer used for accurate speech-to-text transcription and pronunciation alignment using Levenshtein distance matching.
2. **MobileNetV2 (CNN):** Fine-tuned on the FER-2013 dataset to classify facial emotions from video frames.
3. **2-Layer LSTM (RNN):** Trained on MFCC sequences extracted from the Mini LibriSpeech dataset to predict vocal confidence.

*All metrics and inferences are piped to the **Anthropic Claude API** to generate actionable, personalized, and encouraging coaching feedback.*

## 🚀 Getting Started

The project is structured to run directly in **Google Colab** to leverage free GPUs (like the T4).

### Running the Notebooks
1. Upload the notebooks in the `notebooks/` directory to your Google Drive / Google Colab.
2. Mount your Google Drive when prompted in the notebooks (used for saving checkpoints and visualizations).
3. **Training:** Run the CNN and LSTM notebooks to train and save your Phase 2 models. You can push them to your Hugging Face Hub directly from the notebook.
4. **App Interface:** Run the `PersonaPath_App` notebook. You will need an **Anthropic API Key** to run the Claude feedback generation.

### Dependencies
If running locally, install dependencies via:
```bash
pip install -r requirements.txt
```
