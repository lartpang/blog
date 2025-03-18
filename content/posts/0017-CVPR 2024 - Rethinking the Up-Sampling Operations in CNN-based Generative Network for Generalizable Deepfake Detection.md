---
title: "CVPR 2024 - Rethinking the Up-Sampling Operations in CNN-based Generative Network for Generalizable Deepfake Detection"
date: 2024-04-10 06:22:51
tags: ["paper"]
---


<!--more-->

# CVPR 2024 - Rethinking the Up-Sampling Operations in CNN-based Generative Network for Generalizable Deepfake Detection

* 论文：<https://arxiv.org/abs/2312.10461>
* 代码：<https://github.com/chuangchuangtan/NPR-DeepfakeDetection>

![image](https://github.com/lartpang/blog/assets/26847524/0c7f34a2-8f24-458e-84c9-37b8253deb5c)

本文主要研究了基于 CNN 的生成网络中的上采样操作，以实现通用的深度伪造检测。研究者发现，上采样操作不仅可以产生基于频率的伪造 artifact，还可以产生更广义的伪造 artifact。研究者提出了邻近像素关系（NPR）的概念，用作训练检测模型的 artifact 表示。研究者通过在包含 28 种不同生成模型样本的开放世界数据集上进行的全面分析，验证了所提出 NPR 的有效性。

* 上采样操作的研究：研究者发现，上采样操作在常见的生成模型中普遍存在，这些操作不仅在频率域上影响整个图像，还在像素级上留下痕迹。
* 邻近像素关系（NPR）：研究者提出了邻近像素关系（NPR）的概念，用作训练检测模型的 artifact 表示。NPR 有效地捕捉了与图像细节相关的 artifact，如头发、眼睛和胡子等。NPR（Neighboring Pixel Relationships）是一种用于检测合成图像中本地上采样痕迹的简单而有效的特征表示方法。它通过计算相邻像素之间的关系来揭示图像细节中的上采样痕迹。在实际应用中，可以通过调整窗口大小 l 和指数 j 来优化 NPR 的性能。实验表明，当 l=2 且 j=1 时，NPR 具有较好的性能。此外，NPR 可以应用于不同类型的图像生成技术，如 GAN 和扩散生成的图像，具有较强的泛化能力。
* NPR 的计算过程如下：
  1. 选择一个大小为 l×l 的窗口，窗口中心位于像素点 (x, y)。
  2. 在窗口内，计算窗口中心像素值与窗口内其他像素值的差值，并将这些差值存储在一个向量 vc 中。
  3. 对于向量 vc 中的每个元素 vi，计算其与指定参考值的差值，即 vi-vj。
  4. 将这些差值组成的向量视为一个特征表示，记作 NPR。
* NPR 的有效性验证：研究者通过对包含 28 种不同生成模型样本的开放世界数据集进行的全面分析，验证了所提出 NPR 的有效性。实验结果显示，NPR 在 28 种不同的生成模型上都有很好的泛化能力，相比于现有方法，NPR 带来了显著的 11.6% 的提升。
* 如何实现检测算法：本文中的检测算法是通过训练一个二元分类器 D 来实现的，该分类器利用训练图像的相邻像素关系（NPR）作为特征提取器 f 的输入，以区分真实图像和合成图像。在测试阶段，分类器 D 根据 NPR 特征来预测测试图像是否为真实图像。为了训练这个分类器，作者们首先将 ProGAN 生成器的训练集作为真实图像，然后使用各种 GAN 和扩散模型生成合成图像。这些合成图像与真实图像混合在一起，用于训练二元分类器 D。在训练过程中，NPR 特征被提取出来并输入到分类器 D 中，以使其学习如何区分真实图像和合成图像。在测试阶段，对于给定的测试图像，NPR 特征被提取出来并输入到训练好的分类器 D 中，以预测该图像是否为真实图像。