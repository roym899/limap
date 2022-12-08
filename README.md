# LIMAP 

## Dependencies
* CMake >= 3.17
* COLMAP [[Guide](https://colmap.github.io/install.html)]
* HDF5
```bash
sudo apt-get install libhdf5-dev
```
* OpenCV (only for installing [pytlbd](https://github.com/B1ueber2y/limap-internal/blob/main/requirements.txt#L33))
```bash
sudo apt-get install libopencv-dev libopencv-contrib-dev libarpack++2-dev libarpack2-dev libsuperlu-dev
```

* Python 3.9 + required packages
```bash
git submodule update --init --recursive
python -m pip install torch==1.11.0 torchvision==0.12.0 # Refer to https://pytorch.org/get-started/previous-versions/ to install packages that are compatible with your CUDA
python -m pip install -r requirements.txt
```

## Installation

```
python -m pip install -Ive . 
```

## Quickstart

Download the test scene **(100 images)** with the following command.
```bash
bash scripts/quickstart.sh
```

To run **Fitnmerge** on Hypersim:
```bash
python runners/hypersim/fitnmerge.py --output_dir outputs/quickstart_fitnmerge
```

To run **Line Reconstruction** on Hypersim:
```bash
python runners/hypersim/triangulation.py --output_dir outputs/quickstart_triangulation
```

[Tips] Options are stored in the config folder: ``cfgs``. You can easily change the options with the Python argument parser. In the following shows an example:
```bash
python runners/hypersim/triangulation.py --sfm.fbase sift --line2d.detector.method lsd \
                                         --line2d.visualize --triangulation.IoU_threshold 0.2 \
                                         --skip_exists --n_visible_views 5
```
In particular, ``skip_exists`` is a very useful option to avoid running point-based SfM and line detection/description repeatedly in each pass.

## Supported line detectors and descriptors

The following line detectors are currently supported:
- [LSD](https://github.com/iago-suarez/pytlsd)
- [SOLD2](https://github.com/cvg/SOLD2)
- [HAWPv3](https://github.com/cherubicXN/hawp)
- [TP-LSD](https://github.com/Siyuada7/TP-LSD)

The following line descriptors/matchers are currently supported:
- [LBD](https://github.com/iago-suarez/pytlbd)
- [SOLD2](https://github.com/cvg/SOLD2)
- [LineTR](https://github.com/yosungho/LineTR)
- [L2D2](https://github.com/hichem-abdellali/L2D2)
- Endpoint matching with [SuperPoint](https://github.com/magicleap/SuperPointPretrainedNetwork) + Nearest Neighbors
- Endpoint matching with [SuperPoint](https://github.com/magicleap/SuperPointPretrainedNetwork) + [SuperGlue](https://github.com/magicleap/SuperGluePretrainedNetwork)

