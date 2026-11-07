# TTS Quality Testing Plan

## 🎯 Objective

Validate Google Cloud Text-to-Speech quality for Sinhala dialogue BEFORE investing time in building the full application.

## ⚠️ Critical Decision Point

**This test determines if we proceed with the project or pivot to alternative solutions.**

## 📋 Testing Checklist

### Setup (5 minutes)
- [ ] Google Cloud credentials configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Tester running (`python app.py`)
- [ ] Browser open at http://localhost:5000

### Voice Discovery (10 minutes)
- [ ] List all available si-LK voices
- [ ] Note voice names and types (Standard vs Wavenet)
- [ ] Check if premium voices (Wavenet) are accessible

### Sample Testing (30 minutes)

#### Test 1: Single Line Quality
- [ ] Paste sample JSON from `maya_e01_s03_tts_test.json`
- [ ] Generate first dialogue line
- [ ] Listen carefully to:
  - [ ] Naturalness of voice
  - [ ] Pronunciation accuracy
  - [ ] Emotional delivery
  - [ ] Audio quality (clarity, no artifacts)

#### Test 2: Character Voices
- [ ] Test Amaya's character (female voice)
- [ ] Test Aken's character (male voice)
- [ ] Test Dilan's character (male voice)
- [ ] Compare consistency across characters

#### Test 3: Emotional Range
Test different tones from the JSON:
- [ ] "calm_reflective" (Amaya, shot 2)
- [ ] "controlled_irritation" (Aken, shot 15)
- [ ] "persuasive_calm" (Amaya, shot 17)
- [ ] "challenging" (Aken, shot 19)
- [ ] "calm_certain" (Amaya, shot 20)

#### Test 4: Full Scene
- [ ] Generate all dialogue from the JSON
- [ ] Listen to complete sequence
- [ ] Check flow and consistency
- [ ] Verify timing/pacing

### Voice Comparison (20 minutes)
- [ ] Test same text with Standard voice
- [ ] Test same text with Wavenet voice (if available)
- [ ] Document quality differences
- [ ] Note pricing implications

### Edge Cases (15 minutes)
- [ ] Test English words in Sinhala text ("campaign", "frame", "image")
- [ ] Test questions ("මම කොහෙද?")
- [ ] Test short vs long sentences
- [ ] Test with punctuation variations

## 📊 Evaluation Criteria

### Voice Quality (Weight: 40%)

**Excellent (9-10/10):**
- Sounds like native Sinhala speaker
- Natural intonation and rhythm
- Emotions clearly conveyed
- No robotic artifacts

**Good (7-8/10):**
- Generally natural
- Minor pronunciation issues
- Acceptable emotional range
- Slight robotic quality

**Acceptable (5-6/10):**
- Understandable but mechanical
- Some pronunciation errors
- Limited emotional range
- Noticeable TTS quality

**Poor (1-4/10):**
- Heavily robotic
- Frequent mispronunciations
- Monotone delivery
- Unnatural pacing

### Pronunciation Accuracy (Weight: 30%)

**Track:**
- [ ] Total words tested: _____
- [ ] Correctly pronounced: _____
- [ ] Mispronounced: _____
- [ ] Accuracy: _____%

**Minimum acceptable:** 90% accuracy

### Emotional Delivery (Weight: 20%)

For each tone tested:
- Calm: ☐ Conveyed ☐ Partial ☐ Missing
- Irritation: ☐ Conveyed ☐ Partial ☐ Missing
- Confidence: ☐ Conveyed ☐ Partial ☐ Missing
- Challenge: ☐ Conveyed ☐ Partial ☐ Missing

**Minimum acceptable:** 60% of emotions partially conveyed

### Timing/Pacing (Weight: 10%)

- [ ] Average timing variance: ±_____%
- [ ] Maximum variance: ±_____%

**Acceptable range:** ±30% variance

## ✅ Go/No-Go Decision Matrix

### ✅ PROCEED with Google TTS if:

**All of these:**
- [ ] Voice quality score: ≥ 7/10
- [ ] Pronunciation accuracy: ≥ 90%
- [ ] At least 2 emotions partially conveyed
- [ ] Timing variance: < ±40%

**Confidence level:** High - Build full application

### ⚠️ PROCEED WITH CAUTION if:

**Most of these:**
- [ ] Voice quality score: 5-7/10
- [ ] Pronunciation accuracy: 80-90%
- [ ] At least 1 emotion conveyed
- [ ] Timing variance: < ±50%

**Action:** Plan for manual post-processing or hybrid approach

### ❌ DO NOT PROCEED if:

**Any of these:**
- [ ] Voice quality score: < 5/10
- [ ] Pronunciation accuracy: < 80%
- [ ] No emotions conveyed
- [ ] Timing variance: > ±50%

**Action:** Pivot to alternative TTS provider or manual recording

## 🔄 Alternative TTS Providers to Test

If Google TTS fails, test these:

### 1. Amazon Polly
- Supported: Yes (Sinhala voices available)
- Quality: Generally good
- Pricing: Similar to Google

### 2. Microsoft Azure TTS
- Supported: Check latest docs
- Quality: Competitive
- Pricing: Per-character

### 3. ElevenLabs
- Supported: Custom voice cloning
- Quality: Excellent (AI-powered)
- Pricing: Higher but better quality

### 4. Hybrid Approach
- TTS for simple dialogue
- Human recording for key emotional scenes
- Mix both in final product

## 📝 Testing Notes Template

```
Date: ___________
Tester: ___________

Voice Tested: ___________
Sample Size: ___ clips

Quality Score: ___/10
Notes:
- Strengths:
  •
  •
- Weaknesses:
  •
  •

Pronunciation:
- Correct: ___%
- Issues:
  •

Emotional Range:
- Conveyed: ___
- Missing: ___

Timing:
- Average variance: ±___%
- Acceptable: ☐ Yes ☐ No

Overall Recommendation:
☐ Proceed
☐ Proceed with caution
☐ Do not proceed

Detailed Notes:
```

## 🎤 Voice-Specific Tests

### Amaya (Female, Composed)
```
Expected characteristics:
- Calm, articulate delivery
- Restrained emotional range
- Natural conversational flow

Test lines:
1. "මම මේ සින්දුව ගොඩක් වාරයක් ඇහුවා." (calm)
2. "හඳුනාගන්න එකයි කුතුහලයයි දෙකටම එකට වැඩ කරන්න පුළුවන්." (measured)
3. "නෑ. දැනෙන්නේ කොහොමද කියලා එයාලා දැනටමත් දන්නවා." (certain)

Score: ___/10
Notes:
```

### Aken (Male, Authoritative)
```
Expected characteristics:
- Controlled, firm delivery
- Low register (pitch: -1.0)
- Warm but authoritative

Test lines:
1. "මම කොහෙද?" (direct)
2. "මිනිස්සු මගේ release එක එනකම් බලාගෙන ඉන්නේ." (irritation)
3. "එහෙනම් සාමාන්‍ය version එකකුත් හදන්න." (decisive)

Score: ___/10
Notes:
```

### Dilan (Male, Professional)
```
Expected characteristics:
- Smooth professional delivery
- Neutral pitch
- Diplomatic tone

Test lines:
1. "Results ආවම අපිට කියන්න. Thank you, everyone." (professional)

Score: ___/10
Notes:
```

## 📊 Comparative Analysis

If testing multiple providers:

| Criteria | Google TTS | Amazon Polly | Azure TTS | ElevenLabs |
|----------|-----------|--------------|-----------|------------|
| Quality (/10) | ___ | ___ | ___ | ___ |
| Pronunciation | ___% | ___% | ___% | ___% |
| Emotions | ___/5 | ___/5 | ___/5 | ___/5 |
| Pricing ($/1M chars) | $16 | $16 | $16 | Higher |
| Sinhala Support | Yes | Yes | Check | Custom |
| **Total Score** | ___ | ___ | ___ | ___ |

## 🎯 Success Criteria Summary

**Minimum requirements to proceed:**
- ✅ Voice quality: 7/10
- ✅ Pronunciation: 90%
- ✅ Emotions: 60% partial
- ✅ Timing: ±30%

**If met:** Build MayaStudio with confidence
**If not met:** Reevaluate project feasibility or choose alternative provider

---

**Testing Time:** ~90 minutes
**Decision Impact:** Project continuation
**Next Step:** Document findings and make go/no-go decision
