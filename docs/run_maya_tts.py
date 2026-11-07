"""MayaStudio Sinhala TTS probe. pip install google-cloud-texttospeech
Authenticate using Application Default Credentials; run --list-voices first.
"""
import argparse, json, pathlib, re, wave, io, struct
from google.cloud import texttospeech as tts

def safe(s): return re.sub(r'[^a-zA-Z0-9_-]','_',s)
def main():
 p=argparse.ArgumentParser();p.add_argument('--json',default='maya_e01_s03_tts_test.json');p.add_argument('--out',default='maya_audio');p.add_argument('--list-voices',action='store_true');p.add_argument('--dry-run',action='store_true');p.add_argument('--assemble',action='store_true');a=p.parse_args()
 data=json.loads(pathlib.Path(a.json).read_text(encoding='utf-8'))
 out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
 if a.dry_run:
  for sh in data['shots']:
   au=sh['audio']
   if au['text_original']: print(sh['shot_id'],au['speaker_id'],au['text_original'])
  return
 client=tts.TextToSpeechClient()
 if a.list_voices:
  voices=client.list_voices(language_code='si-LK').voices
  for v in voices:print(v.name,','.join(v.language_codes),v.ssml_gender.name)
  if not voices:print('No si-LK voices returned. Do not silently substitute another language.')
  return
 available={v.name:v for v in client.list_voices(language_code='si-LK').voices if 'si-LK' in v.language_codes}
 if not available:raise SystemExit('No si-LK voices available from this API/account. Stop and investigate supported providers.')
 report=[];clips=[]
 for sh in data['shots']:
  au=sh['audio'];txt=au['text_for_tts'];id=sh['shot_id'];duration=sh['planned_duration_ms']
  if not txt:
   report.append({'shot_id':id,'kind':au['type'],'planned_ms':duration,'actual_ms':None});continue
  ch=data['characters'][au['speaker_id']];name=ch['voice_name']
  if not name:raise SystemExit(f"Set characters.{au['speaker_id']}.voice_name to an available si-LK voice from --list-voices")
  if name not in available:raise SystemExit(f'Voice {name} is not an available si-LK voice')
  voice=tts.VoiceSelectionParams(language_code='si-LK',name=name)
  cfg=tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16,speaking_rate=ch['speaking_rate'],pitch=ch['pitch_semitones'])
  resp=client.synthesize_speech(input=tts.SynthesisInput(text=txt),voice=voice,audio_config=cfg)
  path=out/(safe(id)+'.wav');path.write_bytes(resp.audio_content)
  with wave.open(io.BytesIO(resp.audio_content),'rb') as w: actual=round(w.getnframes()*1000/w.getframerate())
  report.append({'shot_id':id,'speaker':au['speaker_id'],'tone_requested':au['delivery']['tone'],'planned_ms':duration,'actual_ms':actual,'delta_ms':actual-duration,'file':str(path)})
  clips.append((sh,path,actual))
  print(id,au['speaker_id'],actual,'ms')
 (out/'timing_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 if a.assemble:
  # Sequential dialogue-only assembly: preserve actual duration, with 250 ms gaps.
  # No shot-length truncation and no simulated ambience.
  params=None;pcm=bytearray()
  for sh,path,actual in clips:
   with wave.open(str(path),'rb') as w:
    fmt=(w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getcomptype())
    if params is None:params=fmt
    if fmt!=params:raise SystemExit('Inconsistent audio formats; resample with FFmpeg before assembly')
    pcm.extend(w.readframes(w.getnframes()))
    pcm.extend(b'\x00'*int(params[2]*0.25)*params[0]*params[1])
  with wave.open(str(out/'dialogue_only.wav'),'wb') as w:
   w.setnchannels(params[0]);w.setsampwidth(params[1]);w.setframerate(params[2]);w.writeframes(pcm)
  print('Wrote',out/'dialogue_only.wav')
if __name__=='__main__':main()
