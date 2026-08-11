# TTS voice-over source

- Model: `pnnbao-ump/VieNeu-TTS-v3-Turbo`
- SDK: `vieneu==3.2.4`, ONNX CPU backend
- Preset voice: `Phạm Tuyên` (nam, miền Bắc, phong cách tự nhiên)
- Output master: WAV, 48 kHz, mono, 24-bit PCM
- License reported by the model author: Apache-2.0
- Model card: <https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo>
- Generated for this project; no external cloned voice was supplied.
- Revision `v02`: visual timeline accelerated by `1.2×`; technical terms use
  English code-switch pronunciation while the surrounding narration remains Vietnamese.
- Revision `v03`: uses a `2.1×` timeline (`1.75×` faster than revision `v02`),
  reads generic technical terminology in Vietnamese, and pronounces
  `PARTICULATE` as the English method name.
- Revision `v04`: uses a manually written Vietnamese voice script and removes
  the static tail after each spoken beat, leaving only a 0.25-second transition gap.
