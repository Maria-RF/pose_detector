# simple-pose

Convierte cualquier video en el mismo video con el **skeleton** de MediaPipe superpuesto y exporta un **CSV** con todos los landmarks por frame.

## Requisitos

- Python 3.9–3.12
- Windows/macOS/Linux
- (Opcional) ffmpeg en PATH para mejores codecs, pero no es obligatorio

## Instalación

```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate
# macOS/Linux
# source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

```
## Ejecución
python run_pose.py --input "ruta\al\video.mp4"
