# YOLO11n inference demo

Модель: `yolo11n.pt`  
Задача: object detection на готових зображеннях  
Режим: inference, без навчання YOLO  
Пристрій за замовчуванням: CPU

## Що є в папці

- `requirements-yolo.txt` - залежності для запуску.
- `run_yolo_demo.py` - запускає модель, зберігає annotated images і CSV з detections.
- `yolo11n_inference_demo.ipynb` - notebook для заняття.
- `images/` - вхідні зображення.
- `models/` - локальні ваги моделі.
- `results/` - результати запуску.

## Швидкий запуск

Відкрийте термінал у цій папці.
Створіть середовище і встановіть залежності:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements-yolo.txt
```

Якщо Jupyter запускається не з цього `.venv`, зареєструйте kernel:

```bash
python -m ipykernel install --user --name yolo12-venv --display-name "Python YOLO12 venv"
```

Запустіть inference:

```bash
python run_yolo_demo.py
```

Після запуску перевірте:

- `results/*_detected.jpg` - зображення з bounding boxes;
- `results/detections.csv` - таблиця з класами, confidence і координатами boxes.

## Запуск з іншим зображенням

```bash
python run_yolo_demo.py --source path/to/image.jpg
```

або для папки:

```bash
python run_yolo_demo.py --source path/to/images
```

## Корисні параметри

```bash
python run_yolo_demo.py --conf 0.4 --imgsz 640
```

- `--conf` - мінімальна впевненість detection.
- `--imgsz` - розмір зображення, до якого YOLO масштабує input.
- `--device cpu` - безпечний варіант.
- `--device mps` - можна спробувати на Apple Silicon, якщо PyTorch підтримує MPS у встановленому середовищі.

## Пояснення

1. Звичайна CNN classification model повертає один клас для всього зображення.
2. Object detection model повертає кілька об'єктів: `class`, `confidence`, `bounding box`.
3. `yolo11n.pt` - мала nano-версія, тому вона зручна для CPU-demo.
4. Запускаємо готову модель. Навчання власної YOLO-моделі потребує розмічених bounding boxes і зазвичай GPU.

Джерела:

- https://docs.ultralytics.com/quickstart
- https://docs.ultralytics.com/models/yolo11
