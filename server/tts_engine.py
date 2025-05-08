import torch
from io import BytesIO
import wave
import numpy as np
from nltk.tokenize import sent_tokenize
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration

class TTSEngine:
    def __init__(self,
                 model_name="parler-tts/parler-tts-mini-expresso",
                 device=None):
        self.device = device or ("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = (
            ParlerTTSForConditionalGeneration
            .from_pretrained(model_name)
            .to(self.device)
            .eval()
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.sr = self.model.config.sampling_rate

    def _chunk_text(self, text: str) -> list[str]:
        paras = [p.strip() for p in text.split('\n\n') if p.strip()]
        chunks = []
        for p in paras:
            if len(p.split()) > 150:
                sents = sent_tokenize(p)
                for i in range(0, len(sents), 5):
                    chunks.append(" ".join(sents[i:i+5]).strip())
            else:
                chunks.append(p)
        return chunks

    def text_to_audio(self, text: str, voice: str, emotion: str) -> bytes:
        bio = BytesIO()
        wf = wave.open(bio, "wb")
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(self.sr)

        description = (
            f"{voice} narrates this story in a {emotion} tone "
            "with clear, expressive, high quality audio."
        )
        desc_inputs = self.tokenizer(
            description,
            return_tensors="pt",
            add_special_tokens=True
        ).to(self.device)

        for chunk in self._chunk_text(text):
            prompt_inputs = self.tokenizer(
                chunk,
                return_tensors="pt",
                add_special_tokens=True
            ).to(self.device)

            with torch.no_grad():
                wav_tensor = self.model.generate(
                    **desc_inputs,
                    prompt_input_ids=prompt_inputs.input_ids
                )

            wav = wav_tensor.cpu().numpy().squeeze()
            if wav.ndim > 1:
                wav = wav.flatten()

            pcm = (wav * 32767).astype(np.int16)
            wf.writeframes(pcm.tobytes())

            # small pause
            silence = np.zeros(int(0.2 * self.sr), dtype=np.int16)
            wf.writeframes(silence.tobytes())

            # cleanup per-chunk
            del wav, pcm, silence, wav_tensor, prompt_inputs

        wf.close()
        output_bytes = bio.getvalue()

        #clear temporary GPU memory
        del desc_inputs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return output_bytes