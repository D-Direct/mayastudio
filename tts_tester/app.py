"""
MayaStudio TTS Tester - Standalone Testing Tool
A simple Flask app to test Google Cloud TTS with Sinhala dialogue
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
from google.cloud import texttospeech as tts
import json
import io
import wave
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)

# HTML template for the testing interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MayaStudio TTS Tester</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 32px; margin-bottom: 10px; }
        .header p { opacity: 0.9; font-size: 16px; }
        .content { padding: 30px; }
        .section {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
        }
        .section h2 {
            font-size: 20px;
            margin-bottom: 15px;
            color: #333;
        }
        textarea {
            width: 100%;
            min-height: 200px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        .control-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            color: #555;
            font-size: 14px;
        }
        select, input[type="number"] {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 100%;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .results {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }
        .results h3 {
            font-size: 18px;
            margin-bottom: 15px;
            color: #333;
        }
        .result-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
        }
        .result-item strong { color: #667eea; }
        .audio-player {
            margin-top: 15px;
            width: 100%;
        }
        .error {
            background: #fee;
            border-left-color: #e53e3e;
            color: #c53030;
        }
        .success {
            background: #efe;
            border-left-color: #38a169;
            color: #276749;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .loading.active { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .info-box {
            background: #e6f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .info-box code {
            background: #d9ecff;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎤 MayaStudio TTS Tester</h1>
            <p>Test Google Cloud Text-to-Speech with Sinhala Dialogue</p>
        </div>

        <div class="content">
            <!-- JSON Input Section -->
            <div class="section">
                <h2>📋 Paste JSON Data</h2>
                <div class="info-box">
                    <strong>Tip:</strong> Paste your complete JSON from <code>maya_e01_s03_tts_test.json</code>
                    or just a single shot object to test quickly.
                </div>
                <textarea id="jsonInput" placeholder='Paste your JSON here...'>
                </textarea>
            </div>

            <!-- Voice Configuration -->
            <div class="section">
                <h2>🎛️ Voice Configuration</h2>
                <div class="controls">
                    <div class="control-group">
                        <label for="voiceName">Voice Name</label>
                        <select id="voiceName">
                            <option value="">Loading voices...</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="speakingRate">Speaking Rate</label>
                        <input type="number" id="speakingRate" value="1.0" min="0.25" max="4.0" step="0.05">
                    </div>
                    <div class="control-group">
                        <label for="pitchSemitones">Pitch (Semitones)</label>
                        <input type="number" id="pitchSemitones" value="0.0" min="-20.0" max="20.0" step="0.5">
                    </div>
                </div>
            </div>

            <!-- Generate Button -->
            <div class="section">
                <button id="generateBtn" onclick="generateAudio()">
                    🎵 Generate Audio
                </button>
            </div>

            <!-- Loading Indicator -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Generating audio...</p>
            </div>

            <!-- Results Section -->
            <div id="results"></div>
        </div>
    </div>

    <script>
        // Load available voices on page load
        async function loadVoices() {
            try {
                const response = await fetch('/api/voices');
                const voices = await response.json();
                const select = document.getElementById('voiceName');
                select.innerHTML = voices.map(v =>
                    `<option value="${v.name}">${v.name} (${v.gender})</option>`
                ).join('');
            } catch (error) {
                console.error('Error loading voices:', error);
                document.getElementById('voiceName').innerHTML =
                    '<option value="">Error loading voices</option>';
            }
        }

        async function generateAudio() {
            const jsonInput = document.getElementById('jsonInput').value;
            const voiceName = document.getElementById('voiceName').value;
            const speakingRate = parseFloat(document.getElementById('speakingRate').value);
            const pitchSemitones = parseFloat(document.getElementById('pitchSemitones').value);

            if (!jsonInput.trim()) {
                showError('Please paste JSON data first');
                return;
            }

            const resultsDiv = document.getElementById('results');
            const loadingDiv = document.getElementById('loading');
            const generateBtn = document.getElementById('generateBtn');

            // Clear previous results
            resultsDiv.innerHTML = '';
            loadingDiv.classList.add('active');
            generateBtn.disabled = true;

            try {
                const data = JSON.parse(jsonInput);

                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        data: data,
                        voice_name: voiceName,
                        speaking_rate: speakingRate,
                        pitch_semitones: pitchSemitones
                    })
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || 'Generation failed');
                }

                showResults(result);
            } catch (error) {
                showError(error.message);
            } finally {
                loadingDiv.classList.remove('active');
                generateBtn.disabled = false;
            }
        }

        function showResults(result) {
            const resultsDiv = document.getElementById('results');
            let html = '<div class="results"><h3>✅ Generated Audio</h3>';

            result.clips.forEach((clip, index) => {
                html += `
                    <div class="result-item">
                        <strong>${clip.shot_id || 'Clip ' + (index + 1)}</strong><br>
                        Speaker: ${clip.speaker || 'N/A'}<br>
                        Text: "${clip.text}"<br>
                        Duration: ${clip.duration_ms}ms
                        ${clip.planned_duration_ms ? `(planned: ${clip.planned_duration_ms}ms, delta: ${clip.duration_ms - clip.planned_duration_ms}ms)` : ''}<br>
                        <audio controls class="audio-player" src="/api/audio/${clip.audio_id}"></audio>
                    </div>
                `;
            });

            if (result.timing_report) {
                html += `
                    <div class="result-item success">
                        <strong>📊 Timing Report</strong><br>
                        Total clips: ${result.timing_report.total_clips}<br>
                        Total duration: ${result.timing_report.total_duration_ms}ms<br>
                        Average delta: ${Math.round(result.timing_report.average_delta_ms)}ms
                    </div>
                `;
            }

            html += '</div>';
            resultsDiv.innerHTML = html;
        }

        function showError(message) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = `
                <div class="results">
                    <div class="result-item error">
                        <strong>❌ Error</strong><br>
                        ${message}
                    </div>
                </div>
            `;
        }

        // Load voices when page loads
        loadVoices();
    </script>
</body>
</html>
"""

# Store generated audio clips in memory (for testing only)
audio_cache = {}

@app.route('/')
def index():
    """Serve the HTML testing interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/voices', methods=['GET'])
def list_voices():
    """List available Sinhala voices from Google Cloud TTS"""
    try:
        client = tts.TextToSpeechClient()
        voices = client.list_voices(language_code='si-LK').voices

        si_lk_voices = [
            {
                'name': v.name,
                'language_codes': list(v.language_codes),
                'gender': v.ssml_gender.name
            }
            for v in voices if 'si-LK' in v.language_codes
        ]

        if not si_lk_voices:
            return jsonify({
                'error': 'No si-LK voices available',
                'message': 'Google Cloud TTS may not have Sinhala voices enabled for your project'
            }), 404

        return jsonify(si_lk_voices)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_audio():
    """Generate audio from JSON data"""
    try:
        request_data = request.json
        data = request_data.get('data')
        voice_name = request_data.get('voice_name')
        speaking_rate = request_data.get('speaking_rate', 1.0)
        pitch_semitones = request_data.get('pitch_semitones', 0.0)

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        client = tts.TextToSpeechClient()
        clips = []
        total_duration = 0
        total_delta = 0

        # Handle both single shot and full project format
        shots = data.get('shots', [data] if 'audio' in data else [])
        characters = data.get('characters', {})

        for shot in shots:
            audio_data = shot.get('audio', shot)
            text = audio_data.get('text_for_tts') or audio_data.get('text_original')

            if not text:
                continue  # Skip non-dialogue shots

            # Determine voice to use
            speaker_id = audio_data.get('speaker_id')
            final_voice_name = voice_name
            final_speaking_rate = speaking_rate
            final_pitch = pitch_semitones

            # Use character-specific settings if available
            if speaker_id and speaker_id in characters:
                char = characters[speaker_id]
                if char.get('voice_name'):
                    final_voice_name = char['voice_name']
                final_speaking_rate = char.get('speaking_rate', speaking_rate)
                final_pitch = char.get('pitch_semitones', pitch_semitones)

            if not final_voice_name:
                return jsonify({'error': 'No voice_name specified. Please select a voice or set it in character data.'}), 400

            # Generate audio
            voice = tts.VoiceSelectionParams(
                language_code='si-LK',
                name=final_voice_name
            )

            audio_config = tts.AudioConfig(
                audio_encoding=tts.AudioEncoding.LINEAR16,
                speaking_rate=final_speaking_rate,
                pitch=final_pitch,
                sample_rate_hertz=24000
            )

            synthesis_input = tts.SynthesisInput(text=text)

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )

            # Calculate actual duration
            with wave.open(io.BytesIO(response.audio_content), 'rb') as w:
                duration_ms = round(w.getnframes() * 1000 / w.getframerate())

            # Store audio in cache
            audio_id = f"clip_{len(audio_cache)}"
            audio_cache[audio_id] = response.audio_content

            planned_duration = shot.get('planned_duration_ms', 0)
            delta = duration_ms - planned_duration if planned_duration else 0

            total_duration += duration_ms
            if planned_duration:
                total_delta += delta

            clips.append({
                'shot_id': shot.get('shot_id', f'shot_{len(clips) + 1}'),
                'speaker': speaker_id,
                'text': text,
                'duration_ms': duration_ms,
                'planned_duration_ms': planned_duration,
                'delta_ms': delta,
                'audio_id': audio_id,
                'voice_used': final_voice_name
            })

        if not clips:
            return jsonify({'error': 'No dialogue found in JSON data'}), 400

        return jsonify({
            'success': True,
            'clips': clips,
            'timing_report': {
                'total_clips': len(clips),
                'total_duration_ms': total_duration,
                'average_delta_ms': total_delta / len(clips) if clips else 0
            }
        })

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    """Retrieve generated audio clip"""
    if audio_id not in audio_cache:
        return jsonify({'error': 'Audio not found'}), 404

    return send_file(
        io.BytesIO(audio_cache[audio_id]),
        mimetype='audio/wav',
        as_attachment=False,
        download_name=f'{audio_id}.wav'
    )

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎤 MayaStudio TTS Tester")
    print("="*60)
    print("\n📋 Setup Instructions:")
    print("   1. Make sure Google Cloud credentials are configured")
    print("   2. Open http://localhost:5000 in your browser")
    print("   3. Paste your JSON data")
    print("   4. Select voice and parameters")
    print("   5. Click 'Generate Audio' to test\n")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
