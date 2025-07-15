```python
# YOLOv5 Note Recognition Model

This repository contains a YOLOv5 model trained to recognize musical noteheads from sheet music images.


## Files

- `best.pt`: Trained model weights
- `detect.py`: Inference script
- `dataset.yaml`: Dataset configuration file

## Usage

```bash
python detect.py --weights best.pt --img 640 --conf 0.25 --source path/to/image.jpg

```
