---
name: transcribe-audio
description: Get a transcript of an audio or video file with timestamps and, when asked, speakers. The host's speech.stt capability first (on-device on the Mac, or the person's cloud key by policy), WhisperX in this worker when the host cannot. Use whenever a job needs the words in a recording.
metadata:
  operator:
    capture: any
    integrations: [elevenlabs, openai, google-ai]
    skills: [glasses-meeting-notes, meeting-action-items]
---

# Transcribe audio

Every skill that reads a recording starts here. Two rungs, tried in this order, and the transcript
always says which one produced it.

## Rung 1: ask the host

If `OPERATOR_CAPABILITY_URL` is set, POST one file at a time:

```
POST $OPERATOR_CAPABILITY_URL
Authorization: Bearer $OPERATOR_INGEST_TOKEN
{"capability": "speech.stt", "policy": "balanced", "prompt": "<what you need>", "mediaPaths": ["/app/inbox/<file>"]}
```

- Say "who said what" or "speakers" in the prompt when you need speakers; the host then prefers a
  transcriber that diarizes.
- `policy`: `balanced` (default: the Mac's own model first, then the person's keys), `cost`,
  `latency`, or `quality` (a cloud transcriber first, when a key is present).
- The reply's `text` is JSON: `{"text", "language", "segments": [{"start", "end", "speaker", "text"}],
  "diarized", "provider", "model", "durationSeconds"}`. `resolved.provider` and `resolved.model` say
  who answered; put them in whatever you write from the transcript.
- A failure reply names every rung it tried and why. Over the one-request size cap: split the file
  with `ffmpeg -i in.mp4 -f segment -segment_time 600 -c copy part%02d.mp4` and send the parts.

## Rung 2: WhisperX in this worker

Only when the capability is absent or failed, and only if `whisperx` is on the PATH (the
`operator.transcribe` pack image has it; the general image does not):

```
ffmpeg -y -i "/app/inbox/<file>" -ac 1 -ar 16000 audio.wav
whisperx audio.wav --model medium --compute_type int8 --output_format json --output_dir out \
  [--diarize --hf_token "$HF_TOKEN"] [--language en]
```

`out/audio.json` has `segments[{start, end, text, speaker?}]`; diarization needs `HF_TOKEN` for the
gated pyannote model, and without it you get segments with no speakers, which you say.

## Deliver

Write `transcript.md` (a line per segment: `[mm:ss] Speaker: text`) beside your reply, and end with:

```operator-result
{"file": "IMG_1201.mov", "provider": "apple-speech", "model": "SpeechTranscriber", "language": "en", "durationSeconds": 312.4, "segments": 41, "diarized": false, "transcript": "transcript.md"}
```

## Works with (optional)

- `elevenlabs` integration (`ELEVENLABS_API_KEY`): Scribe on the host, with speakers.
- The person's OpenAI or Gemini key in the Companion's AI settings: Whisper or Gemini on the host.
- `glasses-meeting-notes` / `meeting-action-items` skills: what to do with the transcript.

## Never

Never present a transcript without saying who produced it. Never fill an `[unclear]` stretch.
Never send audio to a cloud rung yourself; the host decides that by the person's policy.
