from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve


ROOT = Path(__file__).resolve().parent

ASSETS = {
    ROOT / "models" / "yolo11n.pt": "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11n.pt",
    ROOT / "images" / "bus.jpg": "https://ultralytics.com/images/bus.jpg",
    ROOT / "images" / "zidane.jpg": "https://ultralytics.com/images/zidane.jpg",
}


def download_if_missing(path: Path, url: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and path.stat().st_size > 0:
        print(f"OK: {path.relative_to(ROOT)} already exists")
        return

    print(f"Downloading {url}")
    urlretrieve(url, path)
    print(f"Saved: {path.relative_to(ROOT)} ({path.stat().st_size / 1024 / 1024:.1f} MB)")


def main() -> None:
    for path, url in ASSETS.items():
        download_if_missing(path, url)

    print("\nReady. Run: python run_yolo_demo.py")


if __name__ == "__main__":
    main()

