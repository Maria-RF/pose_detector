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

1) Crear carpeta y entrar (si aún no lo hiciste)
mkdir simple-pose
cd simple-pose

2) Crear venv y activar (Windows)
python -m venv .venv
.venv\Scripts\Activate
pip install --upgrade pip
pip install -r requirements.txt

3) Ejecutar sobre cualquier video
python run_pose.py --input "ruta\al\video.mp4"
