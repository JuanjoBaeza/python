import os
import sys
import traceback
import tempfile
import gc
import shutil
import subprocess
import threading
import time
import re
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfiltfilt, lfilter
from scipy.ndimage import uniform_filter1d

try:
    import noisereduce as nr
except ImportError:
    nr = None

from PySide6.QtCore import Qt, QThread, Signal, QUrl, QTimer
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget,
    QProgressBar, QComboBox, QSlider, QGroupBox, QFormLayout,
    QPlainTextEdit, QSplitter
)

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
EPS = 1e-12
SUPPORTED = {".wav", ".flac", ".ogg", ".aiff", ".aif", ".mp3"}
AUDIO_FILTER = "Audio (*.wav *.flac *.ogg *.aiff *.aif *.mp3)"

PROFILES = {"Suave": 0.55, "Equilibrado": 1.0, "Intenso": 1.45}
ENGINE_CLASSIC = "Filtros clásicos adaptativos"
ENGINE_RESEMBLE = "Resemble Enhance (IA local)"
ENGINES = [ENGINE_CLASSIC, ENGINE_RESEMBLE]

STYLE_SHEET = """
* { color: #202938; font-family: "Segoe UI", "Arial"; font-size: 10pt; }
QMainWindow, QWidget { background-color: #F3F6FA; color: #202938; }
QLabel { color: #263449; background: transparent; }
QGroupBox {
    background-color: #FFFFFF; color: #172B4D; font-weight: 700;
    border: 1px solid #CBD5E1; border-radius: 10px;
    margin-top: 12px; padding: 14px 10px 10px 10px;
}
QGroupBox::title {
    subcontrol-origin: margin; left: 12px; padding: 0 6px;
    color: #174A8B; background-color: #F3F6FA;
}
QPushButton {
    background-color: #E5EDF7; color: #17365D;
    border: 1px solid #B8C8DC; border-radius: 7px;
    padding: 9px 13px; font-weight: 600;
}
QPushButton:hover { background-color: #D5E5F8; border-color: #6D9ED6; }
QPushButton:pressed { background-color: #BDD5F2; }
QPushButton:disabled {
    background-color: #E9EDF2; color: #8994A3; border-color: #D8DEE7;
}
QPushButton#primaryButton {
    background-color: #1769AA; color: #FFFFFF; border: 1px solid #12568D;
    font-size: 11pt; font-weight: 700; padding: 11px 16px;
}
QPushButton#primaryButton:hover { background-color: #0F5B99; }
QPushButton#primaryButton:pressed { background-color: #0B4779; }
QListWidget, QPlainTextEdit {
    background-color: #FFFFFF; alternate-background-color: #F7FAFD;
    color: #1F2937; border: 1px solid #C7D2E0; border-radius: 8px;
    padding: 7px; selection-background-color: #D6E9FF; selection-color: #123B66;
}
QListWidget::item { padding: 6px; border-radius: 4px; }
QListWidget::item:selected {
    background-color: #D6E9FF; color: #123B66; border: 1px solid #91BDEB;
}
QComboBox {
    background-color: #FFFFFF; color: #202938;
    border: 1px solid #BCC9D8; border-radius: 6px;
    padding: 7px 10px; min-height: 20px;
}
QComboBox:hover { border-color: #6D9ED6; }
QComboBox:focus { border: 2px solid #3182CE; }
QComboBox QAbstractItemView {
    background-color: #FFFFFF; color: #202938;
    selection-background-color: #D6E9FF; selection-color: #123B66;
    border: 1px solid #BCC9D8; outline: 0;
}
QSlider::groove:horizontal {
    height: 6px; background: #D5DEE9; border-radius: 3px;
}
QSlider::sub-page:horizontal { background: #3182CE; border-radius: 3px; }
QSlider::add-page:horizontal { background: #E2E8F0; border-radius: 3px; }
QSlider::handle:horizontal {
    background: #FFFFFF; border: 2px solid #1769AA;
    width: 16px; height: 16px; margin: -6px 0; border-radius: 9px;
}
QProgressBar {
    background-color: #E5EAF1; color: #1F2937; border: 1px solid #C7D2E0;
    border-radius: 6px; text-align: center; min-height: 16px; font-weight: 600;
}
QProgressBar::chunk { background-color: #2F80C9; border-radius: 5px; }
QSplitter::handle { background-color: #CBD5E1; width: 5px; }
QToolTip {
    background-color: #172B4D; color: #FFFFFF;
    border: 1px solid #0F1F36; padding: 5px;
}
"""

# ---------------------------------------------------------------------------
# Audio: lectura, análisis y procesamiento
# ---------------------------------------------------------------------------
def read_audio(path):
    """Lee formatos compatibles con SoundFile y decodifica MP3 mediante PyAV."""
    try:
        return sf.read(path, dtype="float32", always_2d=True)
    except (RuntimeError, ValueError):
        try:
            import av
        except ImportError as exc:
            raise RuntimeError(
                "No se puede abrir este archivo. Para MP3 instala PyAV con: "
                "pip install av"
            ) from exc

        chunks, sample_rate = [], None
        with av.open(str(path)) as container:
            stream = next((s for s in container.streams if s.type == "audio"), None)
            if stream is None:
                raise RuntimeError(f"No se encontró una pista de audio en: {path}")
            sample_rate = stream.rate
            for frame in container.decode(stream):
                data = frame.to_ndarray(format="fltp")
                if data.ndim == 1:
                    data = data[np.newaxis, :]
                chunks.append(data.T.astype(np.float32, copy=False))

        if not chunks:
            raise RuntimeError(f"No se pudo decodificar audio desde: {path}")
        return np.concatenate(chunks, axis=0), int(sample_rate)


def db(x):
    return 20.0 * np.log10(max(float(x), EPS))


def analyze_audio(audio, sr):
    mono = np.mean(audio, axis=1)
    if len(mono) < int(sr * 0.25):
        raise ValueError("El audio debe durar al menos 0,25 segundos.")

    rms = np.sqrt(np.mean(mono ** 2))
    peak = np.max(np.abs(audio))
    frame = max(1, int(sr * 0.04))
    count = len(mono) // frame
    frames = mono[:count * frame].reshape(count, frame)
    frame_rms = np.sqrt(np.mean(frames ** 2, axis=1))
    noise_floor = np.percentile(frame_rms, 10)

    nfft = min(8192, max(1024, 2 ** int(np.floor(np.log2(min(len(mono), 8192))))))
    hop = max(1, nfft // 2)
    window = np.hanning(nfft)
    spectra = []
    for start in range(0, max(1, len(mono) - nfft + 1), hop):
        chunk = mono[start:start + nfft]
        if len(chunk) != nfft:
            break
        spectra.append(np.abs(np.fft.rfft(chunk * window)) ** 2)
    if spectra:
        power = np.mean(spectra, axis=0)
        freqs = np.fft.rfftfreq(nfft, 1 / sr)
    else:
        power = np.abs(np.fft.rfft(mono * np.hanning(len(mono)))) ** 2
        freqs = np.fft.rfftfreq(len(mono), 1 / sr)

    def band_energy(lo, hi):
        mask = (freqs >= lo) & (freqs < min(hi, sr / 2))
        return float(np.sum(power[mask])) if np.any(mask) else 0.0

    bands = {
        "graves_100_300": band_energy(100, 300),
        "cuerpo_300_1000": band_energy(300, 1000),
        "medios_1k_2k": band_energy(1000, 2000),
        "presencia_2k_5k": band_energy(2000, 5000),
        "agudos_5k_10k": band_energy(5000, 10000),
    }
    total = sum(bands.values()) + EPS
    shares = {k: v / total for k, v in bands.items()}
    centroid = float(np.sum(freqs * np.sqrt(power)) / (np.sum(np.sqrt(power)) + EPS))
    crest = float(np.max(np.abs(mono)) / (rms + EPS))
    clipping = float(np.mean(np.abs(audio) >= 0.999))

    metallic_score = min(100.0, max(0.0,
        100 * (0.65 * shares["presencia_2k_5k"] / 0.48 +
               0.35 * max(0.0, (centroid - 2200) / 1800))))

    issues = []
    if shares["presencia_2k_5k"] > 0.43 and centroid > 2200:
        issues.append("Posible exceso de medios-agudos (sonido metálico/nasal).")
    if shares["agudos_5k_10k"] > 0.24:
        issues.append("Posible exceso de agudos o aspereza.")
    if shares["cuerpo_300_1000"] < 0.12:
        issues.append("Posible falta de cuerpo.")
    if crest > 8:
        issues.append("Dinámica amplia: puede convenir compresión moderada.")
    if clipping > 0.001:
        issues.append("Se detectan muestras saturadas; el daño puede ser irreversible.")
    if db(noise_floor) > -42:
        issues.append("Nivel de pausas relativamente alto: podría haber ruido o ambiente.")
    if not issues:
        issues.append("No se detectan desequilibrios espectrales evidentes.")

    return {
        "rms_db": db(rms), "peak_db": db(peak), "noise_db": db(noise_floor),
        "centroid": centroid, "crest": crest, "clipping": clipping,
        "shares": shares, "metallic_score": metallic_score, "issues": issues,
    }


def highpass(audio, sr, cutoff=75):
    if len(audio) < 32 or cutoff >= sr * 0.45:
        return audio
    sos = butter(2, cutoff, btype="highpass", fs=sr, output="sos")
    return sosfiltfilt(sos, audio, axis=0)


def peaking_eq(audio, sr, freq, gain_db, q=1.2):
    if freq >= sr * 0.45 or freq <= 0 or abs(gain_db) < 0.01:
        return audio
    A = 10 ** (gain_db / 40)
    w0 = 2 * np.pi * freq / sr
    alpha = np.sin(w0) / (2 * q)
    b = np.array([1 + alpha * A, -2 * np.cos(w0), 1 - alpha * A])
    a = np.array([1 + alpha / A, -2 * np.cos(w0), 1 - alpha / A])
    return lfilter(b / a[0], a / a[0], audio, axis=0)


def reduce_noise(audio, sr, amount):
    if nr is None or amount <= 0:
        return audio
    out = np.empty_like(audio)
    for ch in range(audio.shape[1]):
        out[:, ch] = nr.reduce_noise(
            y=audio[:, ch], sr=sr, stationary=False,
            prop_decrease=float(np.clip(amount, 0, 1)),
        )
    return out


def compressor(audio, sr, threshold=-21, ratio=2.2):
    win = max(1, int(sr * 0.012))
    power = uniform_filter1d(audio ** 2, size=win, axis=0)
    level = 10 * np.log10(power + EPS)
    over = np.maximum(level - threshold, 0)
    gain_db = -over * (1 - 1 / ratio)
    gain_db = uniform_filter1d(gain_db, size=max(1, int(sr * 0.025)), axis=0)
    return audio * (10 ** (gain_db / 20))


def process_audio(audio, sr, info, strength, noise_amount):
    y = highpass(audio.copy(), sr, 75)

    metallic = info["shares"]["presencia_2k_5k"]
    if metallic > 0.43 and info["centroid"] > 2200:
        y = peaking_eq(y, sr, 3200, -3.0 * strength, 1.2)
        y = peaking_eq(y, sr, 4600, -1.8 * strength, 1.5)
    elif metallic > 0.36:
        y = peaking_eq(y, sr, 3500, -1.2 * strength, 1.3)

    if info["shares"]["agudos_5k_10k"] > 0.24:
        y = peaking_eq(y, sr, 7500, -1.5 * strength, 1.0)

    if info["shares"]["cuerpo_300_1000"] < 0.12:
        y = peaking_eq(y, sr, 250, 1.2 * strength, 0.8)

    y = reduce_noise(y, sr, noise_amount)
    y = compressor(y, sr)

    peak = np.max(np.abs(y))
    if peak > EPS:
        y *= (10 ** (-1 / 20)) / peak
    return np.clip(y, -1.0, 1.0)


# ---------------------------------------------------------------------------
# Motor Resemble Enhance por fragmentos
# ---------------------------------------------------------------------------
RESEMBLE_DEVICE = "cuda"
RESEMBLE_SOLVER = "euler"
RESEMBLE_NFE = 16
RESEMBLE_CHUNK_SECONDS = 300       # 5 minutos por fragmento
RESEMBLE_OVERLAP_SECONDS = 2      # contexto para reducir artefactos en los cortes
RESEMBLE_CHUNK_TIMEOUT_SECONDS = 1800  # 30 minutos por fragmento


class ProcessingCancelled(Exception):
    """El usuario ha solicitado cancelar el procesamiento."""


def _terminate_process(process):
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def run_resemble(path, log, audio, sr, progress_callback=None,
                 cancel_event=None):
    """Procesa fragmentos en una sola ejecución del CLI para cargar el modelo una vez.

    Cada fragmento incluye contexto a ambos lados. Al recomponer, se elimina ese
    contexto y se conserva únicamente la parte central de cada fragmento.
    """
    executable = shutil.which("resemble-enhance")
    if not executable:
        raise RuntimeError(
            "No encuentro 'resemble-enhance' en este entorno Python.\n"
            "Comprueba: which resemble-enhance"
        )

    if audio.ndim != 2 or len(audio) == 0:
        raise RuntimeError("El audio de entrada está vacío o tiene un formato no válido.")

    total_samples = len(audio)
    chunk_samples = max(1, int(RESEMBLE_CHUNK_SECONDS * sr))
    overlap_samples = max(0, int(RESEMBLE_OVERLAP_SECONDS * sr))
    ranges = [(a, min(a + chunk_samples, total_samples))
              for a in range(0, total_samples, chunk_samples)]

    with tempfile.TemporaryDirectory(prefix="voz_ia_chunks_in_") as in_dir, \
         tempfile.TemporaryDirectory(prefix="voz_ia_chunks_out_") as out_dir:
        in_path, out_path = Path(in_dir), Path(out_dir)
        expected = []
        log(f"Resemble Enhance: {len(ranges)} fragmento(s) de hasta "
            f"{RESEMBLE_CHUNK_SECONDS // 60} min, con {RESEMBLE_OVERLAP_SECONDS}s de contexto.")
        log("Se ejecutará el CLI una sola vez para evitar recargar el modelo en cada fragmento.")

        for index, (core_start, core_end) in enumerate(ranges, 1):
            if cancel_event is not None and cancel_event.is_set():
                raise ProcessingCancelled("Procesamiento cancelado por el usuario.")
            read_start = max(0, core_start - overlap_samples)
            read_end = min(total_samples, core_end + overlap_samples)
            name = f"fragmento_{index:04d}.wav"
            sf.write(in_path / name, audio[read_start:read_end], sr, subtype="PCM_16")
            expected.append((name, core_start, core_end, read_start, read_end))
            if progress_callback:
                progress_callback(int(5 + 15 * index / len(ranges)))

        del audio
        gc.collect()

        command = [
            executable, str(in_path), str(out_path),
            "--device", RESEMBLE_DEVICE,
            "--solver", RESEMBLE_SOLVER,
            "--nfe", str(RESEMBLE_NFE),
        ]
        log(f"Configuración IA: {RESEMBLE_DEVICE} | solver={RESEMBLE_SOLVER} | "
            f"nfe={RESEMBLE_NFE} | fragmentos={len(ranges)}")
        log("Iniciando Resemble Enhance...")

        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, errors="replace", bufsize=1
            )
        except OSError as exc:
            raise RuntimeError(f"No se pudo iniciar Resemble Enhance: {exc}") from exc

        output_lines = []
        reader_done = threading.Event()
        state_lock = threading.Lock()
        state = {"fragment": 0, "fragment_started": None}

        def consume_line(line):
            line = line.strip()
            if not line:
                return
            output_lines.append(line)
            log(line[-500:])

            # La CLI anuncia cada archivo con una línea "Processing ...fragmento_NNNN.wav".
            # Ese marcador reinicia el reloj del timeout para el nuevo fragmento.
            file_match = re.search(r"Processing .*fragmento_(\d+)\.wav", line)
            if file_match:
                fragment_number = int(file_match.group(1))
                with state_lock:
                    if fragment_number != state["fragment"]:
                        state["fragment"] = fragment_number
                        state["fragment_started"] = time.monotonic()
                return

            # No usar el contador exterior x/14: solo leer el progreso interno x/11.
            match = re.search(r"(\d+)\s*/\s*(\d+)", line)
            if match and int(match.group(2)) > 0 and progress_callback:
                with state_lock:
                    fragment = state["fragment"]
                if fragment:
                    fraction = min(1.0, int(match.group(1)) / int(match.group(2)))
                    overall = ((fragment - 1) + fraction) / len(ranges)
                    progress_callback(int(15 + 75 * overall))

        def read_output():
            # tqdm actualiza líneas con '\r'; separamos tanto CR como LF.
            try:
                current = []
                while True:
                    char = process.stdout.read(1)
                    if not char:
                        break
                    if char in "\r\n":
                        consume_line(''.join(current))
                        current.clear()
                    else:
                        current.append(char)
                consume_line(''.join(current))
            finally:
                reader_done.set()

        reader = threading.Thread(target=read_output, daemon=True)
        reader.start()
        try:
            while process.poll() is None:
                if cancel_event is not None and cancel_event.is_set():
                    _terminate_process(process)
                    raise ProcessingCancelled("Procesamiento cancelado por el usuario.")
                with state_lock:
                    active_fragment = state["fragment"]
                    fragment_started = state["fragment_started"]
                if fragment_started is not None and time.monotonic() - fragment_started > RESEMBLE_CHUNK_TIMEOUT_SECONDS:
                    _terminate_process(process)
                    raise RuntimeError(
                        f"Resemble Enhance superó el límite de 30 minutos en el "
                        f"fragmento {active_fragment} de {len(ranges)} y se detuvo."
                    )
                time.sleep(0.2)
            reader.join(timeout=5)
        finally:
            if process.poll() is None:
                _terminate_process(process)

        output_log = "\n".join(output_lines)
        if process.returncode != 0:
            raise RuntimeError(
                f"Resemble Enhance terminó con código {process.returncode}.\n"
                + output_log[-4000:]
            )

        pieces = []
        output_sr = None
        for index, (name, core_start, core_end, read_start, read_end) in enumerate(expected, 1):
            candidates = [out_path / name, out_path / (Path(name).stem + ".flac")]
            result_path = next((candidate for candidate in candidates if candidate.is_file()), None)
            if result_path is None:
                # Algunas versiones pueden cambiar la extensión o el subdirectorio.
                matches = list(out_path.rglob(Path(name).stem + ".*"))
                result_path = next((x for x in matches if x.suffix.lower() in {".wav", ".flac"}), None)
            if result_path is None:
                raise RuntimeError(f"No se encontró la salida del fragmento {index}: {name}\n{output_log[-2000:]}")

            enhanced, this_sr = sf.read(result_path, dtype="float32", always_2d=True)
            if output_sr is None:
                output_sr = int(this_sr)
            elif int(this_sr) != output_sr:
                raise RuntimeError("Resemble Enhance devolvió fragmentos con frecuencias de muestreo distintas.")

            left_context_seconds = (core_start - read_start) / sr
            right_context_seconds = (read_end - core_end) / sr
            left_trim = int(round(left_context_seconds * output_sr))
            right_trim = int(round(right_context_seconds * output_sr))
            stop = len(enhanced) - right_trim if right_trim else len(enhanced)
            central = enhanced[left_trim:stop]
            if len(central) == 0:
                raise RuntimeError(f"El fragmento {index} quedó vacío al retirar el contexto.")
            pieces.append(central)
            if progress_callback:
                progress_callback(int(95 + 5 * index / len(expected)))

        result = np.concatenate(pieces, axis=0)
        log(f"Fragmentos recombinados: {len(pieces)}. Duración resultante: {len(result) / output_sr:.1f}s.")
        return result, output_sr


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------
class Worker(QThread):
    log = Signal(str)
    progress = Signal(int)            # 0..100 real
    finished_ok = Signal(list)
    failed = Signal(str)

    def __init__(self, files, output_dir, profile, noise, engine):
        super().__init__()
        self.files = files
        self.output_dir = output_dir
        self.profile = profile
        self.noise = noise
        self.engine = engine
        self.cancel_event = threading.Event()

    def cancel(self):
        self.cancel_event.set()

    def _process_one(self, path, strength, audio, sr, info):
        if self.engine == ENGINE_RESEMBLE:
            def report(value):
                self.progress.emit(value)
            y, out_sr = run_resemble(
                path, self.log.emit, audio, sr,
                progress_callback=report, cancel_event=self.cancel_event,
            )
            if self.noise > 0.01:
                self.log.emit(
                    "La reducción de ruido adicional se omite para evitar "
                    "sobreprocesar la voz."
                )
            return y, out_sr

        y = process_audio(audio, sr, info, strength, self.noise)
        return y, sr

    def run(self):
        outputs = []
        total = len(self.files)
        strength = PROFILES[self.profile]
        try:
            for i, path in enumerate(self.files):
                if self.cancel_event.is_set():
                    raise ProcessingCancelled("Procesamiento cancelado por el usuario.")
                self.log.emit(f"\nAnalizando: {path}")
                audio, sr = read_audio(path)
                info = analyze_audio(audio, sr)
                self.log.emit(
                    f"RMS {info['rms_db']:.1f} dBFS | pico {info['peak_db']:.1f} dBFS | "
                    f"centroide {info['centroid']:.0f} Hz | indicador metálico "
                    f"{info['metallic_score']:.0f}/100"
                )
                for issue in info["issues"]:
                    self.log.emit("  • " + issue)

                # Progreso parcial antes de procesar (10% del tramo del archivo).
                base = i * 100 / total
                step = 100 / total
                self.progress.emit(int(base + step * 0.1))

                y, out_sr = self._process_one(path, strength, audio, sr, info)

                stem = Path(path).stem
                out = str(Path(self.output_dir) / f"{stem}_mejorado.wav")
                sf.write(out, y, out_sr, subtype="PCM_24")
                outputs.append(out)
                self.log.emit(f"Guardado: {out}")
                self.progress.emit(int(base + step))

            self.finished_ok.emit(outputs)
        except ProcessingCancelled as exc:
            self.log.emit(str(exc))
            self.failed.emit(str(exc))
        except Exception:
            self.failed.emit(traceback.format_exc())


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mejorador inteligente de voz")
        self.resize(1050, 700)
        self.files = []
        self.last_output = None
        self.output_dir = None
        self.worker = None

        self._setup_player()
        self._build_ui()
        self._connect_signals()
        self.setStyleSheet(STYLE_SHEET)

    # --- construcción de UI -------------------------------------------------
    def _setup_player(self):
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        header = QLabel("MEJORADOR INTELIGENTE DE VOZ")
        header.setStyleSheet(
            "color: #123B66; font-size: 22px; font-weight: 800; background: transparent;"
        )
        layout.addWidget(header)
        subtitle = QLabel(
            "Análisis acústico · procesamiento secuencial · IA CUDA (prueba conservadora)"
        )
        subtitle.setStyleSheet("color: #526276; font-size: 10pt; background: transparent;")
        layout.addWidget(subtitle)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter, 1)
        splitter.addWidget(self._build_left_panel())
        splitter.addWidget(self._build_right_panel())
        splitter.setSizes([430, 620])

    def _build_left_panel(self):
        left = QWidget()
        left_layout = QVBoxLayout(left)

        buttons = QHBoxLayout()
        self.add_files_btn = QPushButton("Añadir archivos")
        self.add_folder_btn = QPushButton("Añadir carpeta")
        self.remove_btn = QPushButton("Quitar seleccionados")
        for btn in (self.add_files_btn, self.add_folder_btn, self.remove_btn):
            buttons.addWidget(btn)
        left_layout.addLayout(buttons)

        self.file_list = QListWidget()
        left_layout.addWidget(self.file_list, 1)

        preview = QHBoxLayout()
        self.play_original_btn = QPushButton("Reproducir original")
        self.play_output_btn = QPushButton("Reproducir resultado")
        self.stop_btn = QPushButton("Detener")
        for btn in (self.play_original_btn, self.play_output_btn, self.stop_btn):
            preview.addWidget(btn)
        left_layout.addLayout(preview)
        return left

    def _build_right_panel(self):
        right = QWidget()
        right_layout = QVBoxLayout(right)

        settings = QGroupBox("Configuración")
        form = QFormLayout(settings)

        self.profile = QComboBox()
        self.profile.addItems(list(PROFILES.keys()))
        form.addRow("Intensidad de corrección:", self.profile)

        self.engine = QComboBox()
        self.engine.addItems(ENGINES)
        form.addRow("Motor de mejora:", self.engine)

        self.noise_slider = QSlider(Qt.Horizontal)
        self.noise_slider.setRange(0, 100)
        self.noise_slider.setValue(35)
        self.noise_label = QLabel("35%")
        noise_row = QHBoxLayout()
        noise_row.addWidget(self.noise_slider, 1)
        noise_row.addWidget(self.noise_label)
        noise_widget = QWidget()
        noise_widget.setLayout(noise_row)
        form.addRow("Reducción de ruido:", noise_widget)
        right_layout.addWidget(settings)

        self.output_label = QLabel("Carpeta de salida: junto a los originales")
        self.output_label.setWordWrap(True)
        self.output_btn = QPushButton("Elegir carpeta de salida")
        right_layout.addWidget(self.output_label)
        right_layout.addWidget(self.output_btn)

        self.process_btn = QPushButton("Analizar y mejorar")
        self.process_btn.setMinimumHeight(42)
        self.process_btn.setObjectName("primaryButton")
        right_layout.addWidget(self.process_btn)
        self.cancel_btn = QPushButton("Cancelar procesamiento")
        self.cancel_btn.setEnabled(False)
        right_layout.addWidget(self.cancel_btn)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        right_layout.addWidget(self.progress)

        right_layout.addWidget(QLabel("Informe y diagnóstico:"))
        self.log_box = QPlainTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setPlaceholderText(
            "Aquí aparecerá el análisis de cada grabación..."
        )
        right_layout.addWidget(self.log_box, 1)
        return right

    def _connect_signals(self):
        self.add_files_btn.clicked.connect(self.add_files)
        self.add_folder_btn.clicked.connect(self.add_folder)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.output_btn.clicked.connect(self.choose_output)
        self.process_btn.clicked.connect(self.start_processing)
        self.cancel_btn.clicked.connect(self.cancel_processing)
        self.noise_slider.valueChanged.connect(
            lambda v: self.noise_label.setText(f"{v}%")
        )
        self.play_original_btn.clicked.connect(self.play_original)
        self.play_output_btn.clicked.connect(self.play_output)
        self.stop_btn.clicked.connect(self.player.stop)

    # --- gestión de archivos ------------------------------------------------
    def add_paths(self, paths):
        existing = set(self.files)
        for p in paths:
            if Path(p).suffix.lower() in SUPPORTED and p not in existing:
                self.files.append(p)
                self.file_list.addItem(p)
                existing.add(p)

    def add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar audios", "", AUDIO_FILTER
        )
        self.add_paths(paths)

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if folder:
            paths = [
                str(p) for p in Path(folder).rglob("*")
                if p.is_file() and p.suffix.lower() in SUPPORTED
            ]
            self.add_paths(paths)

    def remove_selected(self):
        selected = sorted(
            [self.file_list.row(item) for item in self.file_list.selectedItems()],
            reverse=True,
        )
        for index in selected:
            self.file_list.takeItem(index)
            del self.files[index]

    def choose_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Carpeta de salida")
        if folder:
            self.output_dir = folder
            self.output_label.setText(f"Carpeta de salida: {folder}")

    # --- procesamiento ------------------------------------------------------
    def start_processing(self):
        if not self.files:
            QMessageBox.information(
                self, "Sin archivos", "Añade primero uno o más audios."
            )
            return
        output = self.output_dir or str(Path(self.files[0]).parent)
        self.log_box.clear()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.process_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        self.worker = Worker(
            list(self.files), output, self.profile.currentText(),
            self.noise_slider.value() / 100, self.engine.currentText(),
        )
        self.worker.log.connect(self.log_box.appendPlainText)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished_ok.connect(self.processing_finished)
        self.worker.failed.connect(self.processing_failed)
        self.worker.start()

    def cancel_processing(self):
        if self.worker and self.worker.isRunning():
            self.cancel_btn.setEnabled(False)
            self.log_box.appendPlainText("Solicitando cancelación...")
            self.worker.cancel()

    def processing_finished(self, outputs):
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.process_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.last_output = outputs[-1] if outputs else None
        self.log_box.appendPlainText(f"\nFinalizado: {len(outputs)} archivo(s).")
        QMessageBox.information(
            self, "Proceso terminado", f"Se han creado {len(outputs)} archivo(s)."
        )

    def processing_failed(self, error):
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.process_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.log_box.appendPlainText(error)
        QMessageBox.critical(
            self, "Error de procesamiento",
            "Se produjo un error. Consulta el informe.",
        )

    # --- reproducción -------------------------------------------------------
    def play_original(self):
        item = self.file_list.currentItem()
        if item:
            self.player.setSource(QUrl.fromLocalFile(item.text()))
            self.player.play()

    def play_output(self):
        if self.last_output and os.path.exists(self.last_output):
            self.player.setSource(QUrl.fromLocalFile(self.last_output))
            self.player.play()
        else:
            QMessageBox.information(
                self, "Sin resultado",
                "Procesa un archivo y selecciona el resultado más reciente.",
            )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()