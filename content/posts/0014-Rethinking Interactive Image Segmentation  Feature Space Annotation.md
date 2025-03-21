---
title: "Rethinking Interactive Image Segmentation: Feature Space Annotation"
date: 2024-04-10 06:26:16
tags: ["paper"]
---

<!--more-->

- Author: lartpang
- Link: https://github.com/lartpang/blog/issues/10

# Rethinking Interactive Image Segmentation Feature Space Annotation

* 论文：<https://arxiv.org/abs/2101.04378>
* 代码：<https://github.com/LIDS-UNICAMP/rethinking-interactive-image-segmentation>

本文提出了一种新的交互式图像分割方法，通过特征空间注释来同时对多张图像进行分割注释，这与现有的交互式分割方法在图像领域进行注解的方式形成了鲜明对比。研究结果表明，这种特征空间注解的方法在前景分割数据集上可以取得与最先进的方法相媲美的结果。

* 交互式图像分割方法：现有的交互式图像分割方法主要依赖于用户的点击、矩形框或者多边形等输入，以实现像素级的注解。然而，这些方法仍然需要大量的用户努力，成为深度学习应用的一个瓶颈。
* 特征空间注解的新方法：本文提出了一种新的交互式图像分割方法，通过特征空间投影来进行同时图像分割注解。这种方法与现有方法的不同之处在于，它不是在图像领域进行注解，而是在特征空间中进行操作，从而大大减少了用户的注解负担。
* 实验结果：实验结果表明，这种新方法在前景分割数据集上可以取得与最先进的方法相当的结果。在语义分割的 Cityscapes 数据集上，它达到了 91.5% 的精度，比原始注解程序快了 74.75 倍。

总的来说，本文提出了一种新的交互式图像分割方法，通过特征空间注解，可以在保持结果竞争力的同时，大大提高用户的注解效率。这种方法为交互式图像注解提供了一个新的方向，可以与其他现有方法相结合，实现更有效的注解。