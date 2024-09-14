# Face Swap

## Description

Face Swap is a generative AI technology to swap faces (aka Deep Fake) in images from one to another. This is a one shot face-swap model; for this reason only one face is needed to swap. It should work for all kinds of content. The face swapping model itself was created by [Insightface](https://github.com/deepinsight/insightface)

## Installation

### Dependencies

1. FFmpeg

[Download and install FFmpeg](https://ffmpeg.org/download.html)

2. CUDA >= 10.1

[Download and install CUDA](https://developer.nvidia.com/cuda-10.1-download-archive-base)

3. Requirements

```powershell
git clone https://github.com/dxcanh/face_swap.git
cd face_swap
conda create -n face_swap python=3.8 -y
conda activate face_swap
pip install torch==1.11.0+cu115 torchvision==0.12.0+cu115 -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
```

4. Download the [inswapper_128.onnx model](https://huggingface.co/thebiglaskowski/inswapper_128.onnx/tree/main) from Hugging Face and place it in buffalo_l folder of this project.

## Pipeline
Run application:
```powershell
python -m App.app
```
Now, you can access the application at localhost:5000

## Results
Below are images of the application interface.
![demo](demo/demo.jpg)

## Special Thanks To
- [FFMpeg](https://github.com/FFmpeg/FFmpeg)
- [InsightFace](https://github.com/deepinsight/insightface)
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)
- [GFPGAN](https://github.com/TencentARC/GFPGAN)
- [PyTorch](https://github.com/pytorch/pytorch)
- [Torchvision](https://github.com/pytorch/pytorch)
