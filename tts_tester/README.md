# MayaStudio TTS Tester

A standalone testing tool to validate Google Cloud Text-to-Speech quality for Sinhala dialogue before building the full application.

## 🎯 Purpose

This tool allows you to:
- Test Google TTS with actual Sinhala dialogue
- Evaluate voice quality and naturalness
- Check pronunciation accuracy
- Compare different voices
- Verify timing/duration estimates
- Decide if Google TTS meets project requirements

## 📋 Prerequisites

1. **Google Cloud Account** with Text-to-Speech API enabled
2. **Service Account Key** (JSON file) with TTS permissions
3. **Python 3.8+** installed

## 🚀 Quick Start

### Step 1: Set Up Google Cloud Credentials

```bash
# Set environment variable pointing to your service account key
# Windows (PowerShell)
$env:GOOGLE_APPLICATION_CREDENTIALS="D:\YOUTUBE-STORY\MayaStudio\mayastudio-service-account.json"

# Windows (CMD)
set GOOGLE_APPLICATION_CREDENTIALS=D:\YOUTUBE-STORY\MayaStudio\mayastudio-service-account.json

# Linux/Mac
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/mayastudio-service-account.json"
```

### Step 2: Install Dependencies

```bash
cd tts_tester
pip install -r requirements.txt
```

### Step 3: Run the Tester

```bash
python app.py
```

### Step 4: Open in Browser

Navigate to: **http://localhost:5000**

## 🎤 How to Use

### Testing Full JSON File

1. Open `docs/maya_e01_s03_tts_test.json`
2. Copy the entire contents
3. Paste into the text area
4. Select a voice from the dropdown
5. Adjust speaking rate and pitch if needed
6. Click **"Generate Audio"**
7. Listen to each generated clip

### Testing Single Line

You can also test a single dialogue quickly:

```json
{
  "audio": {
    "type": "dialogue",
    "speaker_id": "amaya",
    "text_for_tts": "මම මේ සින්දුව ගොඩක් වාරයක් ඇහුවා.",
    "language_code": "si-LK"
  }
}
```

### Testing with Character Voices

To use character-specific voices:

```json
{
  "characters": {
    "amaya": {
      "voice_name": "si-LK-Standard-A",
      "speaking_rate": 0.96,
      "pitch_semitones": 0.0
    }
  },
  "shots": [
    {
      "shot_id": "test-001",
      "audio": {
        "speaker_id": "amaya",
        "text_for_tts": "හලෝ, මේ test එකක්."
      }
    }
  ]
}
```

## 🔍 What to Evaluate

### 1. **Voice Quality**
- ✅ Natural sounding?
- ✅ Clear pronunciation?
- ✅ Appropriate emotion/tone?
- ⚠️ Robotic or unnatural?

### 2. **Pronunciation**
- ✅ Correct Sinhala phonetics?
- ✅ Proper stress and intonation?
- ⚠️ Mispronounced words?
- ⚠️ English words in Sinhala text?

### 3. **Timing**
- ✅ Duration matches expectations?
- ✅ Speaking pace natural?
- ⚠️ Too fast or too slow?

### 4. **Consistency**
- ✅ Same character sounds consistent?
- ✅ Quality maintained across clips?
- ⚠️ Voice changes unexpectedly?

## 🎛️ Voice Parameters

### Available Voices

Run this to list all Sinhala voices:

```bash
# From the tts_tester directory
python
>>> from google.cloud import texttospeech as tts
>>> client = tts.TextToSpeechClient()
>>> voices = client.list_voices(language_code='si-LK').voices
>>> for v in voices: print(v.name, v.ssml_gender.name)
```

Expected voices:
- `si-LK-Standard-A` (Female)
- `si-LK-Standard-B` (Male)
- `si-LK-Wavenet-A` (Female, premium)
- `si-LK-Wavenet-B` (Male, premium)

### Speaking Rate
- `0.25` - Very slow (0.25x speed)
- `0.5` - Slow (0.5x speed)
- `1.0` - Normal (default)
- `1.5` - Fast (1.5x speed)
- `4.0` - Very fast (4x speed)

### Pitch
- `-20.0` to `20.0` semitones
- `-12` = 1 octave lower
- `0` = Normal pitch
- `+12` = 1 octave higher

## 📊 Results Interpretation

### Good Results ✅
```
Duration: 4500ms (planned: 4000ms, delta: +500ms)
```
- Minor timing variance is acceptable
- Delta of ±1000ms is usually fine
- Quality sounds natural

### Concerning Results ⚠️
```
Duration: 8000ms (planned: 4000ms, delta: +4000ms)
```
- Large timing variance (2x planned)
- Robotic or unnatural voice
- Mispronunciations
- Inconsistent quality

### Decision Criteria

**Proceed with Google TTS if:**
- ✅ 80%+ of clips sound natural
- ✅ Pronunciation is 90%+ accurate
- ✅ Timing variance < ±30%
- ✅ Voice quality is consistent

**Consider alternatives if:**
- ❌ Voice sounds too robotic
- ❌ Frequent mispronunciations
- ❌ Quality inconsistent
- ❌ Timing highly unpredictable

## 🐛 Troubleshooting

### "No si-LK voices available"

**Cause:** Google TTS doesn't have Sinhala voices, or they're not enabled

**Solution:**
1. Check if Sinhala is supported in your region
2. Try different Google Cloud project
3. Contact Google Cloud support
4. Consider alternative TTS providers

### "Application Default Credentials not found"

**Cause:** GOOGLE_APPLICATION_CREDENTIALS not set

**Solution:**
```bash
# Set the environment variable before running
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
python app.py
```

### "Invalid JSON"

**Cause:** Malformed JSON in input

**Solution:**
- Validate JSON using jsonlint.com
- Check for trailing commas
- Ensure proper quotes (double, not single)

### "Permission denied"

**Cause:** Service account lacks TTS permissions

**Solution:**
1. Go to Google Cloud Console
2. IAM & Admin → Service Accounts
3. Grant "Cloud Text-to-Speech User" role

## 📁 File Structure

```
tts_tester/
├── app.py              # Flask server + HTML interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Advanced Usage

### Batch Testing Multiple Voices

Modify the JSON to test different voices:

```json
{
  "characters": {
    "test_wavenet": { "voice_name": "si-LK-Wavenet-A" },
    "test_standard": { "voice_name": "si-LK-Standard-A" }
  },
  "shots": [
    {
      "audio": {
        "speaker_id": "test_wavenet",
        "text_for_tts": "මේක Wavenet voice test එකක්."
      }
    },
    {
      "audio": {
        "speaker_id": "test_standard",
        "text_for_tts": "මේක Standard voice test එකක්."
      }
    }
  ]
}
```

### Exporting Audio Files

Audio is generated in-memory for testing. To save files:

```python
# Modify app.py to save files
import pathlib

output_dir = pathlib.Path('output')
output_dir.mkdir(exist_ok=True)

# In generate_audio(), after generating response:
audio_file = output_dir / f"{shot_id}.wav"
audio_file.write_bytes(response.audio_content)
```

## 🎯 Next Steps Based on Results

### If TTS Quality is Good ✅
1. Proceed with full MayaStudio development
2. Use tested voices in production
3. Document optimal parameters per character
4. Build confidence in TTS approach

### If TTS Quality is Poor ❌
1. Try alternative voices (Wavenet vs Standard)
2. Adjust speaking rate and pitch
3. Test with different text samples
4. Consider alternative providers:
   - Amazon Polly
   - Microsoft Azure TTS
   - ElevenLabs
   - Custom voice models

### If Results are Mixed ⚠️
1. Identify problematic patterns
2. Test edge cases (questions, emotions)
3. Compare multiple providers
4. Plan hybrid approach (TTS + human recording)

## 📞 Support

If you encounter issues:
1. Check Google Cloud console for errors
2. Verify API quotas and billing
3. Test with English text first
4. Review service account permissions

## 💡 Tips

- **Test representative samples:** Use actual dialogue from your scripts
- **Compare voices:** Listen to all available voices
- **Test emotions:** Try different tones (calm, angry, sad)
- **Check edge cases:** Numbers, English words, punctuation
- **Document findings:** Note which voices work best

---

**Ready to test?** Run `python app.py` and open http://localhost:5000

Good luck! 🎤
