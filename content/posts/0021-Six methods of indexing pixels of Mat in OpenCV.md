---
title: "Six methods of indexing pixels of Mat in OpenCV"
date: 2024-03-25 09:41:52
tags: ["opencv"]
---
# Six methods of indexing pixels of Mat in OpenCV

## `.at<>()`

```cpp
// modify the pixel directly
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols; ++w) {
        image.at<Vec3b>(h, w)[0] = 255;
        image.at<Vec3b>(h, w)[1] = 0;
        image.at<Vec3b>(h, w)[2] = 0;
    }
}

// modify the pixel by the reference
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols; ++w) {
        Vec3b& bgr = image.at<Vec3b>(h, w);
        bgr.val[0] = 0;
        bgr.val[1] = 255;
        bgr.val[2] = 0;
    }
}

// the image has one channel
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols / 2; ++w) {
        image.at<uchar>(h, w) = 128;
    }
}
```

## `.ptr<>()`

```cpp
// use uchar type
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols / 2; ++w) {
        uchar* ptr = image.ptr<uchar>(h, w);
        ptr[0] = 255;
        ptr[1] = 0;
        ptr[2] = 0;
    }
}
// use cv::Vec3b type
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols / 2; ++w) {
        Vec3b* ptr = image.ptr<Vec3b>(h, w);
        ptr->val[0] = 0;
        ptr->val[1] = 255;
        ptr->val[2] = 0;
    }
}

// use the row pointer and the image has one channel
for (int h = 0; h < image.rows; ++h) {
    uchar* ptr = image.ptr(h);
    for (int w = 0; w < image.cols / 2; ++w) {
        ptr[w] = 128;
    }
}

// use the pixel pointer and the image has one channel
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols / 2; ++w) {
        uchar* ptr = image.ptr<uchar>(h, w);
        *ptr = 255;
    }
}
```

## `iterator`

```cpp
// the image has three channels
Mat_<Vec3b>::iterator it = image.begin<Vec3b>();
Mat_<Vec3b>::iterator itend = image.end<Vec3b>();
for (; it != itend; ++it) {
    (*it)[0] = 255;
    (*it)[1] = 0;
    (*it)[2] = 0;
}

// the image has one channel
Mat_<uchar>::iterator it1 = image.begin<uchar>();
Mat_<uchar>::iterator itend1 = image.end<uchar>();
for (; it1 != itend1; ++it1) {
    (*it1) = 128;
}
```

## `.data` pointer

```cpp
// 3 channels
uchar* data = image.data;
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols / 2; ++w) {
        *data++ = 128;
        *data++ = 128;
        *data++ = 128;
    }
}

// 1 channel
uchar* data = image.data;
for (int h = 0; h < image.rows; ++h) {
    for (int w = 0; w < image.cols / 2; ++w) {
        *data++ = 128;
    }
}
```

## `.row()` and `.col()`

```cpp
for (int i = 0; i < 100; ++i) {
    image.row(i).setTo(Scalar(0, 0, 0)); // modify the i th row data
    image.col(i).setTo(Scalar(0, 0, 0)); // modify the i th column data
}
```

## when `isContinuous()` is true

```cpp
Mat image = imread("...");
int nRows = image.rows;
int nCols = image.cols * image.channels();

if (image.isContinuous()) {
    nCols = nRows * nCols;
    nRows = 1;
}

for (int h = 0; h < nRows; ++h) {
    uchar* ptr = image.ptr<uchar>(h);
    for (int w = 0; w < nCols; ++w) {
        // ptr[w] = 128 ;
        *ptr++ = 128;
    }
}
```

## Reference

- http://t.csdn.cn/bSDNn
