import sys
import torch
from pathlib import Path

# Add YOLOv5 repo to path
yolov5_path = 'C:/Users/karth/Desktop/UPSKILL/HALO/PHASE1/yolov5'
sys.path.append(yolov5_path)

# Import detect module from yolov5
from detect import run

def webcam_inference():
    weights_path = 'C:/Users/karth/Desktop/UPSKILL/HALO/PHASE1/runs/train/weights/best.pt'
    
    run(
        weights=weights_path,
        source=0,  # 0 = default webcam
        imgsz=(416, 416),
        conf_thres=0.75,
        iou_thres=0.45,
        device='0' if torch.cuda.is_available() else 'cpu',
        project='runs/detect',
        name='webcam_results',
        exist_ok=True,
        view_img=True,
        save_txt=False,
        save_conf=True
    )

if __name__ == "__main__":
    webcam_inference()
