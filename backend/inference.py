import os
import urllib.request
import string
import numpy as np
import cv2
import librosa
import Levenshtein
import cmudict
from moviepy import VideoFileClip
from collections import Counter

# --- Lazy Loading Logic to prevent hanging the import ---
_MODELS_LOADED = False
_device_w2v = None
_processor_w2v = None
_model_w2v = None
_cmu = None
_lstm_model = None
_scaler_mean = None
_scaler_scale = None
_cnn_model = None
_whisper_model = None
_face_cascade = None

EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def load_models_once():
    global _MODELS_LOADED, _device_w2v, _processor_w2v, _model_w2v, _cmu, _lstm_model, _scaler_mean, _scaler_scale, _cnn_model, _whisper_model, _face_cascade
    if _MODELS_LOADED:
        return
        
    print("Loading AI Pipelines (Wav2Vec2 + LSTM + CNN + Whisper)...")
    import torch
    from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
    import tensorflow as tf
    import whisper
    
    # Phase 1 Models
    _device_w2v = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    _processor_w2v = Wav2Vec2Processor.from_pretrained('facebook/wav2vec2-base-960h')
    _model_w2v = Wav2Vec2ForCTC.from_pretrained('facebook/wav2vec2-base-960h')
    _model_w2v.to(_device_w2v)
    _cmu = cmudict.dict()

    # Phase 2 Models
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    WEIGHTS_DIR = os.path.join(BASE_DIR, "weights")
    
    lstm_model_path = os.path.join(WEIGHTS_DIR, "lstm_confidence_final.keras")
    scaler_mean_path = os.path.join(WEIGHTS_DIR, "scaler_mean.npy")
    scaler_scale_path = os.path.join(WEIGHTS_DIR, "scaler_scale.npy")
    cnn_model_path = os.path.join(WEIGHTS_DIR, "cnn_emotion_phase4.keras")

    _lstm_model = tf.keras.models.load_model(lstm_model_path)
    _scaler_mean = np.load(scaler_mean_path)
    _scaler_scale = np.load(scaler_scale_path)

    def build_emotion_model():
        data_augmentation = tf.keras.Sequential([
            tf.keras.layers.Resizing(224, 224),
            tf.keras.layers.RandomFlip("horizontal"),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
        ])
        base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
        base_model.trainable = False
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(None, None, 3)),
            data_augmentation,
            tf.keras.layers.Lambda(lambda x: tf.keras.applications.mobilenet_v2.preprocess_input(x)),
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(7, activation='softmax')
        ])
        return model

    _cnn_model = build_emotion_model()
    _cnn_model.load_weights(cnn_model_path)
    _whisper_model = whisper.load_model("tiny")

    cascade_path = os.path.join(WEIGHTS_DIR, "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascade_path):
        cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        urllib.request.urlretrieve(cascade_url, cascade_path)
    _face_cascade = cv2.CascadeClassifier(cascade_path)
    _MODELS_LOADED = True

# ==========================================
# PHASE 1 CORE NLP FUNCTIONS
# ==========================================
def clean_word(word):
    return word.lower().translate(str.maketrans('', '', string.punctuation))

def get_phonemes(word):
    w = clean_word(word)
    return [p.rstrip('012') for p in _cmu[w][0]] if w in _cmu else None

def phoneme_distance(w1, w2):
    p1, p2 = get_phonemes(w1), get_phonemes(w2)
    if p1 is None or p2 is None:
        return None
    return Levenshtein.distance(' '.join(p1), ' '.join(p2))

def get_score(ref_w, spoken_w):
    if ref_w == spoken_w:
        return 'green'
    dist = phoneme_distance(ref_w, spoken_w)
    if dist is None:
        dist = Levenshtein.distance(ref_w, spoken_w)
    similarity = Levenshtein.ratio(ref_w, spoken_w)
    if similarity > 0.55:
        return 'grey'
    if dist is not None and dist <= 4:
        return 'grey'
    return 'red'

def normalize_word(word):
    for sfx, trim in [('ing', 3), ('ed', 2), ('ly', 2)]:
        if word.endswith(sfx):
            return word[:-trim]
    return word

def generate_tip(word_scores):
    red_words = [ws['word'] for ws in word_scores if ws['score'] == 'red']
    grey_words = [ws['word'] for ws in word_scores if ws['score'] == 'grey']
    if not red_words and not grey_words:
        return 'Perfect reading! Every word was spot-on. Amazing work!'
    if red_words:
        focus = red_words[0]
        return f"Great job! Let's try saying '{focus}' again slowly. Break it into syllables. You're doing amazing!"
    focus = grey_words[0]
    return f"Very nice! Try pronouncing '{focus}' one more time - almost perfect! Keep going!"

def pronunciation_pipeline(audio_path, reference_text):
    load_models_once()
    import torch
    speech, sr = librosa.load(audio_path, sr=16000)
    duration_sec = librosa.get_duration(y=speech, sr=sr)
    duration_min = duration_sec / 60

    inputs = _processor_w2v(speech, return_tensors='pt', sampling_rate=16000).input_values.to(_device_w2v)
    with torch.no_grad():
        logits = _model_w2v(inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = _processor_w2v.decode(predicted_ids[0]).lower()
    spoken_words = transcription.split()
    ref_words = [clean_word(w) for w in reference_text.split()]

    editops = Levenshtein.editops(ref_words, spoken_words)
    word_scores = [{'word': w, 'spoken': w, 'score': 'green'} for w in ref_words]

    def safe_get(lst, idx):
        return lst[idx] if idx < len(lst) else ''

    for op, i, j in editops:
        if op == 'replace':
            ref_w, spoken_w = ref_words[i], safe_get(spoken_words, j)
            if not spoken_w:
                word_scores[i].update(score='red', spoken='')
                continue
            ref_n, sp_n = normalize_word(ref_w), normalize_word(spoken_w)
            if Levenshtein.ratio(ref_n, sp_n) < 0.2:
                word_scores[i].update(score='red', spoken='')
                continue
            word_scores[i].update(score=get_score(ref_n, sp_n), spoken=spoken_w)
        elif op == 'delete':
            ref_w = ref_words[i]
            color = 'grey' if ref_w in {'the','a','and','to','of','in','on'} else 'red'
            word_scores[i].update(score=color, spoken='')

    wpm = len(spoken_words) / duration_min if duration_min > 0 else 0
    intervals = librosa.effects.split(speech, top_db=25)
    hesitations = sum(
        1 for k in range(1, len(intervals))
        if (intervals[k][0] - intervals[k-1][1]) / sr > 0.5
    )
    tip = generate_tip(word_scores)
    green = sum(1 for ws in word_scores if ws['score'] == 'green')
    total = len(word_scores)
    accuracy = round((green / total) * 100) if total else 0

    return {
        'transcription': transcription,
        'word_scores': word_scores,
        'wpm': round(wpm, 1),
        'hesitations': hesitations,
        'tip': tip,
        'accuracy': accuracy,
        'duration': round(duration_sec, 1),
    }


# ==========================================
# PHASE 2 CORE FUNCTIONS
# ==========================================
def extract_features(y, sr, n_mfcc=13, max_frames=200):
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)
    pitch = librosa.yin(y, fmin=50, fmax=500)[np.newaxis, :]
    pitch = np.nan_to_num(pitch, nan=0.0)
    rms = librosa.feature.rms(y=y)
    zcr = librosa.feature.zero_crossing_rate(y)
    t = mfcc.shape[1]
    features = np.vstack([mfcc, delta, delta2, pitch[:, :t], rms[:, :t], zcr[:, :t]]).T
    if features.shape[0] >= max_frames: features = features[:max_frames]
    else: features = np.vstack([features, np.zeros((max_frames - features.shape[0], features.shape[1]))])
    return features.astype(np.float32)

def analyze_presentation(video_path):
    load_models_once()
    cap = cv2.VideoCapture(video_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('temp_video.mp4', fourcc, fps, (width, height))

    emotions_counter = Counter()
    while True:
        ret, frame = cap.read()
        if not ret: break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = _face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(60, 60))
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            preds = _cnn_model.predict(np.expand_dims(cv2.resize(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB), (224, 224)).astype(np.float32), axis=0), verbose=0)[0]
            emotion = EMOTIONS[np.argmax(preds)]
            emotions_counter[emotion] += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            break
        out.write(frame)
    cap.release()
    out.release()

    audio_path = "temp_audio.wav"
    try:
        video = VideoFileClip(video_path)
        if video.audio is None: return {"error": "Video has no audio."}
        video.audio.write_audiofile(audio_path, logger=None)
    except Exception as e:
        return {"error": f"Audio extraction failed: {str(e)}"}

    os.makedirs("static", exist_ok=True)
    os.system(f"ffmpeg -y -i temp_video.mp4 -i {audio_path} -c:v libx264 -c:a aac -strict experimental static/processed_video.mp4")

    y, sr = librosa.load(audio_path, sr=16000)
    duration = librosa.get_duration(y=y, sr=sr)
    intervals = librosa.effects.split(y, top_db=30)
    voiced_secs = sum((end - start) for start, end in intervals) / sr
    silence_ratio = 1 - (voiced_secs / duration) if duration > 0 else 1
    rms_arr = librosa.feature.rms(y=y)[0]
    rms_mean = float(np.mean(rms_arr))

    energy_contour = []
    if len(rms_arr) >= 20:
        bins = np.array_split(rms_arr, 20)
        energy_contour = [float(np.mean(b)) for b in bins]
    else:
        energy_contour = [float(x) for x in rms_arr] + [0.0]*(20-len(rms_arr))

    max_e = max(energy_contour) if max(energy_contour) > 0 else 1
    energy_contour = [round(e/max_e, 2) for e in energy_contour]

    f0 = librosa.yin(y, fmin=50, fmax=500)
    pitch_std = float(np.std(f0[f0 > 0])) if len(f0[f0 > 0]) > 10 else 0.0

    result = _whisper_model.transcribe(audio_path, initial_prompt="Um, uh, like, so, you know.")
    words = [w.strip('.,?!;') for w in result['text'].lower().split()]
    filler_counts = {fw: words.count(fw) for fw in ['um', 'uh', 'like', 'so']}
    wpm = int((len(words) / (result['segments'][-1]['end'] if result['segments'] else 1.0)) * 60) if words else 0

    features = np.expand_dims(((extract_features(y, sr) - _scaler_mean) / _scaler_scale).astype(np.float32), axis=0)
    raw_score = float(_lstm_model.predict(features, verbose=0)[0][0]) * 100

    adjusted_score = raw_score
    if silence_ratio > 0.35: adjusted_score -= 10
    if rms_mean < 0.02: adjusted_score -= 8
    if pitch_std < 20: adjusted_score -= 7
    total_fillers = sum(filler_counts.values())
    if total_fillers > 5: adjusted_score -= (total_fillers - 5) * 1.5

    adjusted_score = round(max(0, min(100, adjusted_score)), 1)

    coaching = []
    if adjusted_score > 80: coaching.append("Excellent overall delivery and confidence.")
    elif adjusted_score > 60: coaching.append("Good delivery, but room for improvement in pacing and vocal energy.")
    else: coaching.append("Delivery appears hesitant. Focus on steady pacing and reducing filler words.")

    if wpm < 110: coaching.append(f"Pace is a bit slow ({wpm} wpm). Try to reach ~130 wpm.")
    elif wpm > 160: coaching.append(f"Pace is very fast ({wpm} wpm). Slow down after key points.")

    if total_fillers > 2: coaching.append(f"Try to reduce filler words. You used {total_fillers} in this short clip.")

    if pitch_std < 15: coaching.append("Vocal tone is somewhat monotone. Try varying your pitch to sound more engaging.")

    return {
        "raw_confidence": round(raw_score, 1),
        "adjusted_confidence": adjusted_score,
        "wpm": wpm,
        "silence_ratio": round(silence_ratio, 2),
        "pitch_std": round(pitch_std, 1),
        "dominant_emotion": emotions_counter.most_common(1)[0][0] if emotions_counter else "Neutral",
        "filler_counts": filler_counts,
        "energy_contour": energy_contour,
        "coaching": coaching,
        "processed_video_url": "/static/processed_video.mp4"
    }
