---
title: "Snippets of OpenVINO-CPP for Model Inference"
date: 2024-03-25 09:41:05
tags: ["opencv"]
---
# Snippets of OpenVINO-CPP for Model Inference

## Header File

```cpp
#include <openvino/openvino.hpp>
```

## Create Infer Request

```cpp
void preprocessing(std::shared_ptr<ov::Model> model) {
  ov::preprocess::PrePostProcessor ppp(model);
  ppp.input().tensor().set_layout("NHWC"); // input data is NHWC from OpenCV Mat
  ppp.input().model().set_layout("NCHW"); // In the model, the layout is NCHW
  model = ppp.build();
}

ov::Core core;

auto model = core.read_model(model_path); # can use onnx or openvino's xml file
preprocessing(model);

auto compiled_model = core.compile_model(model, "CPU");  // Or without `"CPU"`
auto input_port = compiled_model.input();
auto infer_request = compiled_model.create_infer_request();
```

## Input and Output

- single input

```cpp
infer_request.set_input_tensor(blob);
infer_request.crop_net.infer();
```

- single output

```cpp
ov::Tensor single_output = this->point_net.get_output_tensor(0);
```

- multiple outputs

```cpp
ov::Tensor multi_outputs0 = this->point_net.get_output_tensor(0);
ov::Tensor multi_outputs1 = this->point_net.get_output_tensor(1);
```

## OpenCV `cv::Mat` <-> OpenVINO `ov::Tensor`

The key to these steps is the alignment of the data layout.

### `cv::Mat` -> `ov::Tensor`

```cpp
// converting the uint8 3-channels image mat to a float32 tensor
image.convertTo(image, CV_32FC3, 1.0 / 255);
// NHWC layout as mentioned above. (N=1, C=3)
ov::Tensor blob(input_port.get_element_type(), input_port.get_shape(), (float *)image.data);
```

### `ov::Tensor` -> `cv::Mat`

```cpp
// tensor follows the NCHW layout, so tensor_shape is (N,C,H,W)
ov::Shape tensor_shape = tensor.get_shape();
// Due to N=1 and C=1, we can directly assign all data to a new mat.
cv::Mat mat(tensor_shape[2], tensor_shape[3], CV_32F, tensor.data());
```

## Reference

- https://github.com/OpenVINO-dev-contest/YOLOv7_OpenVINO_cpp-python/blob/main/cpp/main_preprocessing.cpp
- https://github.com/openvinotoolkit/openvino/blob/master/samples/cpp/hello_classification/main.cpp