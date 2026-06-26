from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run YOLO11n inference on images.")
    parser.add_argument(
        "--model",
        default=str(ROOT / "models" / "yolo11n.pt"),
        help="Path to local model weights or Ultralytics model name, e.g. yolo11n.pt.",
    )
    parser.add_argument(
        "--source",
        default=str(ROOT / "images"),
        help="Image file or directory with images.",
    )
    parser.add_argument(
        "--output",
        default=str(ROOT / "results"),
        help="Directory for annotated images and detections.csv.",
    )
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold.")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size.")
    parser.add_argument("--device", default="cpu", help="Device: cpu, mps, cuda, cuda:0.")
    return parser.parse_args()


def collect_images(source: Path) -> list[Path]:
    if source.is_file():
        return [source]
    if source.is_dir():
        return sorted(path for path in source.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)
    raise FileNotFoundError(f"Source does not exist: {source}")


def resolve_model(model: str) -> str:
    model_path = Path(model)
    if model_path.exists():
        return str(model_path)

    local_default = ROOT / "models" / "yolo11n.pt"
    if model == str(local_default):
        print(
            "Model weights not found at models/yolo11n.pt.\n"
            "Run: python prepare_yolo_assets.py\n"
            "Or pass --model yolo11n.pt to let Ultralytics download it automatically.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    return model


def save_annotated_image(result, output_dir: Path) -> Path:
    output_path = output_dir / f"{Path(result.path).stem}_detected.jpg"
    annotated_bgr = result.plot()
    annotated_rgb = annotated_bgr[..., ::-1]
    Image.fromarray(annotated_rgb).save(output_path, quality=95)
    return output_path


def main() -> None:
    args = parse_args()

    try:
        from ultralytics import YOLO
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: ultralytics.\n"
            "Install it with: python -m pip install -r requirements-yolo.txt"
        ) from exc

    source = Path(args.source).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    images = collect_images(source)
    if not images:
        raise SystemExit(f"No images found in: {source}")

    model_ref = resolve_model(args.model)
    model = YOLO(model_ref)

    results = model.predict(
        source=[str(path) for path in images],
        conf=args.conf,
        imgsz=args.imgsz,
        device=args.device,
        verbose=False,
    )

    csv_path = output_dir / "detections.csv"
    rows: list[dict[str, object]] = []

    for result in results:
        annotated_path = save_annotated_image(result, output_dir)
        boxes = result.boxes

        print(f"\n{Path(result.path).name} -> {annotated_path.relative_to(ROOT)}")
        if boxes is None or len(boxes) == 0:
            print("  No detections")
            continue

        for box in boxes:
            class_id = int(box.cls.item())
            class_name = result.names[class_id]
            confidence = float(box.conf.item())
            xmin, ymin, xmax, ymax = [float(value) for value in box.xyxy[0].tolist()]

            rows.append(
                {
                    "image": Path(result.path).name,
                    "class": class_name,
                    "confidence": round(confidence, 4),
                    "xmin": round(xmin, 1),
                    "ymin": round(ymin, 1),
                    "xmax": round(xmax, 1),
                    "ymax": round(ymax, 1),
                }
            )
            print(
                f"  {class_name:12s} conf={confidence:.2f} "
                f"box=({xmin:.0f}, {ymin:.0f}, {xmax:.0f}, {ymax:.0f})"
            )

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["image", "class", "confidence", "xmin", "ymin", "xmax", "ymax"],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved table: {csv_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

