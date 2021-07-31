import argparse
import sys
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

import numpy as np

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.augmentations import letterbox
from utils.general import check_img_size, check_requirements, check_imshow, colorstr, non_max_suppression, \
    apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path, save_one_box
from utils.plots import colors, plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized

global cmd_options  # used by the param parsing

@torch.no_grad()
def run(filename, # include path of the file
        weights='yolov5s.pt',  # model.pt path(s)
        source='data/images',  # file/dir/URL/glob, 0 for webcam
        imgsz=640,  # inference size (pixels)
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        update=False,  # update all models
        project='runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        ):
    # save_img = not nosave and not source.endswith('.txt')  # save inference images
    save_img = False
    save_txt = False
    ret_msg = ''

    # Directories
    # save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    # (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Initialize
    set_logging()
    device = select_device(device)
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names
    if half:
        model.half()  # to FP16

    # Dataloader
    # # Read image
    # self.count += 1
    path = source
    img0 = cv2.imread(path)  # BGR
    im0s = img0
    assert img0 is not None, 'Image Not Found ' + path
    # print(f'image {self.count}/{self.nf} {path}: ', end='')

    # # Padded resize
    img = letterbox(img0, imgsz, stride=stride)[0]

    # # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    dataset = LoadImages(source, img_size=imgsz, stride=stride)
    bs = 1  # batch_size

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    t1 = time_synchronized()
    pred = model(img, augment=False, visualize=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
    t2 = time_synchronized()

    # Process detections
    for i, det in enumerate(pred):  # detections per image
        p, s, im0, frame = path, '', im0s.copy(), getattr(dataset, 'frame', 0)

        p = Path(p)  # to Path
        s += '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        imc = im0.copy() if save_crop else im0  # for save_crop
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

            # Write results
            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                ret_msg += str(line)

    print(f'Done. ({time.time() - t0:.3f}s)')
    return ret_msg

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    opt = parser.parse_args()
    return opt

def main(cmd_options):
    print(colorstr('detect: ') + ', '.join(f'{k}={v}' for k, v in vars(cmd_options).items()))
    check_requirements(exclude=('tensorboard', 'thop'))
    filename = ''
    mesg = run(filename, **vars(cmd_options))
    print('Inference results: \n', mesg)

if __name__ == "__main__":
    cmd_options = parse_opt()
    main(cmd_options)