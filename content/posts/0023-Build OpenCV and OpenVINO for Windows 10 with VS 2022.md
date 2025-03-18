---
title: "Build OpenCV and OpenVINO for Windows 10 with VS 2022"
date: 2024-03-25 09:38:03
tags: ["opencv"]
---


<!--more-->

# Build OpenCV and OpenVINO for Windows 10 with VS 2022

In this guide, I will build the two powerful open-source libraries, i.e., OpenCV and OpenVINO for running my deeplearning model on windows 10.
Interestingly, both libraries are closely associated with Intel 🖥️. 

## OpenCV 😮 

First of all, we must download the related code projects (`opencv` and `opencv_contrib` containing some plugins for `opencv`) into our computer from this links:

- https://github.com/opencv/opencv/releases
- https://github.com/opencv/opencv_contrib/tags

Make sure the selected versions of the two libararies are the same.
Here, I choice the latest version `4.7.0`.
Because we will recompiling them by ourselves, we can just download the source code zip files.
Put the two unpacked libraries into the same parent folder `opencv_dir` as follows:

```
-opencv_dir
  -opencv-4.7.0
    -...
  -opencv_contrib-4.7.0
    -modules
    -...
```

**NOTE**: To avoid the network issue that may be encountered during using CMake, we need to add the url proxy prefix `https://ghproxy.com/` before the urls of some setting of the relevant modules like `https://ghproxy.com/https://raw.github***`:
- `.cmake` in `opencv-4.7.0/3rdparty/ippicv`
- `.cmake` in `opencv-4.7.0/3rdparty/ffmpeg`
- `CMakeLists.txt` in `opencv_contrib-4.7.0/modules/face`
- Files in `cmake` of `opencv_contrib-4.7.0/modules/xfeatures2d`
- `CMakeLists.txt` in `opencv_contrib-4.7.0/modules/wechat_qrcode`
- `CMakeLists.txt` in `opencv_contrib-4.7.0/modules/cudaoptflow`

Next, start compiling OpenCV.

1. Create the build folder: `cd opencv_dir && mkdir opencv-build-vs2022`
2. Configure and generate the VS solution by CMake with some config items:
  - General:
    - source folder: `<opencv-4.7.0>`
    - build folder: `<opencv-build-vs2022>`
    - `BUILD_OPENCV_WORLD=ON`
    - `CMAKE_BUILD_TYPE=RELEASE`
    - `OPENCV_ENABLE_NONFREE=ON`
    - `BUILD_opencv_dnn=ON`
    - `OPENCV_EXTRA_MODULES_PATH=<opencv_contrib-4.7.0/modules>`
  - CUDA:
    - `WITH_CUDA=ON`
    - `WITH_CUDNN=ON`
    - `WITH_CUBLAS=ON`
    - `WITH_CUFFT=ON`
    - `CUDA_FAST_MATH=ON`
    - `CUDA_ARCH_BIN=7.5` (We can fill the single value corresponding to the real GPU for accelerating the compilation process.)
    - `OPENCV_DNN_CUDA=ON`
3. Go to the build directory: `cd <opencv-build-vs2022>`
4. Start build by cmake and msvc compiler: `cmake --build . --config Release --verbose -j8`
5. Install the built opencv into the `install` folder in the current path: `cmake --install . --prefix install`
6. Add the `bin` directory into the user environment: `<path>\install\x64\vc17\bin`
7. In VS:
    - add the `<path>\install\include` directory into "解决方案资源管理器->右键点击属性->VC++目录->外部包含目录"
    - add the `<path>\install\x64\vc17\lib` directory into "解决方案资源管理器->右键点击属性->VC++目录->库目录"
    - add the `opencv_world470.lib` into "解决方案资源管理器->右键点击属性->链接器->输入->附加依赖项"

## OpenVINO 🍰 

The document of OpenVINO is intuitive and the readability is better than OpenCV.
The relevant content about building and installing the libirary is listed in these links:
- https://github.com/openvinotoolkit/openvino/blob/master/docs/dev/build_windows.md
- https://github.com/openvinotoolkit/openvino/blob/master/docs/dev/cmake_options_for_custom_comiplation.md
- https://github.com/openvinotoolkit/openvino/blob/master/docs/dev/installing.md

After building and install the OpenCV library, it's time to move on to OpenVINO.

1. We need clone the project and the sub modules.
    ```
    git clone https://github.com/openvinotoolkit/openvino.git
    cd openvino
    git submodule update --init --recursive
    ```
2. Create the build folder: `mkdir build && cd build`
3. Configure and generate the VS solution by CMake:
    - `ENABLE_INTEL_GPU=OFF` (We only use the Intel CPU.)
    - Disable some frontend items:
      - `ENABLE_OV_PDPD_FRONTEND=OFF`
      - `ENABLE_OV_TF_FRONTEND=OFF`
      - `ENABLE_OV_TF_LITE_FRONTEND=OFF`
      - `ENABLE_OV_PYTORCH_FRONTEND=OFF`
    - For Python:
      - `ENABLE_PYTHON=ON` It seems that `openvino-dev` needs to be installed first in the detected environment, otherwise a warning message will be thrown in the cmake-gui window.
      - `PYTHON_EXECUTABLE=<python.exe>`
      - `PYTHON_INCLUDE_DIR=<incude directory>`
      - `PYTHON_LIBIRARY=<pythonxx.lib in libs directory>`
    - For OpenCV:
      - `ENABLE_OPENCV=ON`
      - `OpenCV_DIR=<opencv-build-vs2022/install>`
4. Build the library: `cmake --build . --config Release --verbose -j8`
5. Install the library into the `install` directory: `cmake --install . --prefix install`
6. Add the `bin` directory into the environment:
    - `<path>\install\runtime\bin\intel64\Release`
    - `<path>\install\runtime\3rdparty\tbb\bin`
8. In VS:
    - add the `<path>\install\runtime\include` directory into "解决方案资源管理器->右键点击属性->VC++目录->外部包含目录"
    - add the `<path>\install\runtime\lib\intel64\Release` directory into "解决方案资源管理器->右键点击属性->VC++目录->库目录"
    - add the 🌟 `openvino.lib`, 🌟 `openvino_onnx_frontend.lib`, `openvino_c.lib` into "解决方案资源管理器->右键点击属性->链接器->输入->附加依赖项"

## Set DLL path in IDE

- VS: "right click on solution -> Properties -> Debugging -> Environment -> `PATH=<path>\install\x64\vc17\bin;%PATH%`"
- Qt Creator: "Projects -> Build & Run -> Build/Run -> Environment -> Details -> Eidt %PATH% -> Add `<path>\install\x64\vc17\bin`"