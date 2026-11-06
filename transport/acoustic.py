import wave
import struct
import math
import json
import hashlib
import os

class AcousticTransceiver:
    SAMPLE_RATE = 44100
    CARRIERS = [17500, 18000, 18500, 19000]
    SYMBOL_DURATION = 0.02

    @classmethod
    def synthesize_wav(cls, payload, optical_nonce, filename="qdag_airgap.wav"):
        session_key = hashlib.sha3_256(optical_nonce.encode()).digest()
        raw_bytes = json.dumps(payload).encode()
        encrypted = bytes([b ^ session_key[i % len(session_key)] for i, b in enumerate(raw_bytes)])

        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)
        samples = []

        for byte in encrypted:
            for shift in (6, 4, 2, 0):
                freq = cls.CARRIERS[(byte >> shift) & 3]
                for i in range(samples_per_symbol):
                    t = float(i) / cls.SAMPLE_RATE
                    val = int(32767.0 * 0.3 * math.sin(2.0 * math.pi * freq * t))
                    samples.append(val)

        with wave.open(filename, "w") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(cls.SAMPLE_RATE)
            for s in samples: w.writeframes(struct.pack("<h", s))
        return filename

    @classmethod
    def demodulate_wav(cls, filename, optical_nonce):
        if not os.path.exists(filename): return None, "File audio tidak ditemukan!"
        with wave.open(filename, "r") as w:
            n_frames = w.getnframes()
            samples = struct.unpack(f"<{n_frames}h", w.readframes(n_frames))

        samples_per_symbol = int(cls.SAMPLE_RATE * cls.SYMBOL_DURATION)
        total_symbols = len(samples) // samples_per_symbol
        detected_pairs = []

        for s_idx in range(total_symbols):
            chunk = samples[s_idx * samples_per_symbol : (s_idx + 1) * samples_per_symbol]
            energies = []
            for freq in cls.CARRIERS:
                omega = 2.0 * math.pi * freq / cls.SAMPLE_RATE
                cos_sum = sum(s * math.cos(i * omega) for i, s in enumerate(chunk))
                sin_sum = sum(s * math.sin(i * omega) for i, s in enumerate(chunk))
                energies.append((cos_sum ** 2) + (sin_sum ** 2))
            detected_pairs.append(energies.index(max(energies)))

        recovered_bytes = bytearray()
        for i in range(0, len(detected_pairs), 4):
            if i + 3 < len(detected_pairs):
                byte = (detected_pairs[i] << 6) | (detected_pairs[i+1] << 4) | (detected_pairs[i+2] << 2) | detected_pairs[i+3]
                recovered_bytes.append(byte)

        session_key = hashlib.sha3_256(optical_nonce.encode()).digest()
        decrypted = bytes([b ^ session_key[idx % len(session_key)] for idx, b in enumerate(recovered_bytes)])
        
        try:
            return json.loads(decrypted.decode()), "Sukses"
        except Exception:
            return None, "Dekripsi gagal: Sinyal rusak atau Nonce salah!"
