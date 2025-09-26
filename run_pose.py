#!/usr/bin/env python3
# run_pose.py
import argparse, csv
from pathlib import Path
import cv2, mediapipe as mp
from tqdm import tqdm

# Conexiones básicas del esqueleto (MediaPipe Pose)
POSE_CONNECTIONS = [
    (11,12),(11,13),(13,15),(12,14),(14,16),
    (11,23),(12,24),(23,24),
    (23,25),(25,27),(27,31),(24,26),(26,28),(28,32),
    (15,17),(17,19),(19,21),(16,18),(18,20),(20,22)
]

def draw_pose(frame, landmarks, vis_thr=0.3, thickness=2, radius=3):
    h, w = frame.shape[:2]
    # líneas
    for a, b in POSE_CONNECTIONS:
        if a < len(landmarks) and b < len(landmarks):
            xa, ya, za, va = landmarks[a]
            xb, yb, zb, vb = landmarks[b]
            if va >= vis_thr and vb >= vis_thr:
                pa = (int(xa*w), int(ya*h))
                pb = (int(xb*w), int(yb*h))
                cv2.line(frame, pa, pb, (0,255,0), thickness, cv2.LINE_AA)
    # puntos
    for (x,y,z,v) in landmarks:
        if v >= vis_thr:
            cv2.circle(frame, (int(x*w), int(y*h)), radius, (0,255,0), -1, cv2.LINE_AA)

def main():
    ap = argparse.ArgumentParser(description="Overlay de pose y export a CSV")
    ap.add_argument("--input", required=True, help="Ruta a video de entrada")
    ap.add_argument("--out_video", default="", help="Salida MP4 con skeleton (por defecto: <input>_pose.mp4)")
    ap.add_argument("--out_csv", default="", help="Salida CSV (por defecto: <input>_pose.csv)")
    ap.add_argument("--model_complexity", type=int, default=1, choices=[0,1,2], help="MediaPipe Pose complexity")
    ap.add_argument("--vis_thr", type=float, default=0.3, help="Umbral de visibility para dibujar")
    ap.add_argument("--alpha", type=float, default=1.0, help="Oscurecer fondo (0..1). 1 = sin oscurecer")
    args = ap.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise FileNotFoundError(f"No existe: {in_path}")

    out_video = Path(args.out_video) if args.out_video else in_path.with_name(in_path.stem + "_pose.mp4")
    out_csv   = Path(args.out_csv)   if args.out_csv   else in_path.with_name(in_path.stem + "_pose.csv")
    out_video.parent.mkdir(parents=True, exist_ok=True)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(in_path))
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir el video: {in_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    W   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)  or 640)
    H   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 360)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # compatible Windows
    vw = cv2.VideoWriter(str(out_video), fourcc, fps, (W, H))

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=args.model_complexity,
        smooth_landmarks=True,
        enable_segmentation=False
    )

    # preparar CSV: columnas = frame_idx, time_sec, x_0,y_0,z_0,v_0, ..., x_32,y_32,z_32,v_32
    num_landmarks = 33
    header = ["frame_idx", "time_sec"]
    for i in range(num_landmarks):
        header += [f"x_{i}", f"y_{i}", f"z_{i}", f"v_{i}"]

    with open(out_csv, "w", newline="", encoding="utf-8") as fcsv:
        writer = csv.writer(fcsv)
        writer.writerow(header)

        frame_idx = 0
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        pbar = tqdm(total=total if total>0 else None, desc="Procesando", unit="f")

        while True:
            ok, frame = cap.read()
            if not ok:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            res = pose.process(rgb)

            # oscurecer si se pidió
            if args.alpha < 1.0:
                frame = (frame * args.alpha).astype(frame.dtype)

            row = [frame_idx, frame_idx / fps]
            landmarks = []
            if res.pose_landmarks:
                for lm in res.pose_landmarks.landmark:
                    landmarks.append((lm.x, lm.y, lm.z, lm.visibility))
            else:
                # si no hay detección, relleno con NaN
                landmarks = [(float("nan"),)*4 for _ in range(num_landmarks)]

            # escribir CSV (wide)
            for (x,y,z,v) in landmarks:
                row += [x,y,z,v]
            writer.writerow(row)

            # dibujar y escribir video
            draw_pose(frame, landmarks, vis_thr=args.vis_thr, thickness=2, radius=3)
            vw.write(frame)

            frame_idx += 1
            pbar.update(1)
        pbar.close()

    pose.close()
    cap.release()
    vw.release()
    print(f"[OK] Video con pose: {out_video}")
    print(f"[OK] CSV de landmarks: {out_csv}")

if __name__ == "__main__":
    main()
