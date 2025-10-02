# simple-pose

Convierte cualquier video en el mismo video con el **skeleton** de MediaPipe superpuesto y exporta un **CSV** con todos los landmarks por frame.

## Requisitos

- Python 3.9–3.12
- Windows/macOS/Linux
- (Opcional) ffmpeg en PATH para mejores codecs, pero no es obligatorio

## Instalación

1) Clonar repositorio
```bash
git clone https://github.com/MARIA-RF/pose_detector.git
cd pose_detector
```
2) Crear venv y activar (Windows)
```bash
py -m venv .venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Windows
.venv\Scripts\Activate
# macOS/Linux
# source .venv/bin/activate

python.exe -m pip install --upgrade pip
pip install -r requirements.txt

```
## Ejecución

```bash
python run_pose.py --input videos\video1.mp4
