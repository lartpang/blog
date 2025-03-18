---
title: "CVPR 2024 - Rethinking Interactive Image Segmentationwith Low Latency, High Quality, and Diverse Prompts"
date: 2024-04-10 06:51:40
tags: ["paper"]
---

<!--more-->

- Author: lartpang
- Link: https://github.com/lartpang/blog/issues/12

# CVPR 2024 - Rethinking Interactive Image Segmentationwith Low Latency, High Quality, and Diverse Prompts

* 论文：<https://arxiv.org/bas/2404.00741>
* 代码：<https://github.com/uncbiag/SegNext>

![image](https://github.com/lartpang/blog/assets/26847524/70061347-789b-4334-bc13-012d1c713723)

这篇文章主要研究了如何在保持低延迟的同时提高交互式图像分割的质量，并实现多种提示的兼容性。

![image](https://github.com/lartpang/blog/assets/26847524/9ecd883a-f0d5-46ed-a9ce-77426d7cae07)

研究人员提出了一种名为 SegNext 的方法，它重新引入了专家模型中常用的密集视觉提示的表示和融合方式，以促进高质量的分割。该方法将五种不同的视觉提示（包括点击、框、涂鸦、多边形和遮罩）统一在一个密集图上。

所提方法也支持文本提示，即使用 CLIP 来将文本提示编码成向量，并通过交叉注意力块将其与图像嵌入融合。尽管文本提示的性能可能具有很大的提升空间，但是配合视觉提示仍然展现出了具有希望的表现。

实验结果显示，**密集表示和融合视觉提示**是实现高质量分割的关键设计选择。与现有的专家模型相比，该方法能够在保持低延迟的同时实现更好的分割效果。

交互式图像分割是一个长期存在的计算机视觉任务，旨在精确地划分特定的图像区域。然而，现有的专家模型和通用模型在实现低延迟、高质量的交互式分割以及支持多种提示方面存在困难。现有方法无法实现低延时高性能的原因主要有以下几点：

* 现有方法通常只支持有限的提示，如点击或简单的文本描述，缺乏多样性，这限制了模型的泛化能力。
* 许多方法采用联合编码的方式处理图像和提示，导致计算复杂度高，延迟较大。
* 在处理图像分割任务时，现有方法往往需要对整个图像进行重新计算，每次更新提示都需要重新计算，这也增加了延迟。

相比之下，本文提出的方法通过引入密集的视觉提示和优化模型结构，实现了低延时和高性能的图像分割效果。

与 SAM 这类专家模型的关键差异主要在于表征视觉提示的方式不同。本文采用密集表征来保留空间信息。这样的密集设计导致了高质量的分割效果。
