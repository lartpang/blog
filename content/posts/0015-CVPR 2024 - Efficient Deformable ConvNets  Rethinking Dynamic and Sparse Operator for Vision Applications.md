---
title: "CVPR 2024 - Efficient Deformable ConvNets: Rethinking Dynamic and Sparse Operator for Vision Applications"
date: 2024-04-10 06:24:56
tags: ["paper"]
---


<!--more-->

# CVPR 2024 - Efficient Deformable ConvNets - Rethinking Dynamic and Sparse Operator for Vision Applications

![](https://img-blog.csdnimg.cn/direct/91218b5449e44dc08281d227cb980f2e.png)

* 论文：<https://arxiv.org/abs/2401.06197>
* 代码：<https://github.com/OpenGVLab/DCNv4>

本文提出了高效的 DCNv4，这是一个专为视觉应用设计的高效有效的运算符。

![](https://img-blog.csdnimg.cn/direct/f6d3749cbc2b43a0a67f49bca6ca344e.png)

DCNv4 通过两个关键增强解决了其前身 DCNv3 的限制：

* 在空间聚合中去除 softmax 归一化，以增强其动态特性和表达能力；
* 优化内存访问，最小化冗余操作以加快速度。通过对现有实现进行指令级内核剖析，发现 DCNv3 已经很轻量级，计算成本不到 1%，而内存访问成本占了 99%。因此重新审视运算符实现，并发现许多内存访问在 DCN 的前向过程中是冗余的，可以通过优化来实现更快的 DCNv4 实现。

![](https://img-blog.csdnimg.cn/direct/fe88f4ea9e6746dea0f208d330d20b5a.png)

这些改进使得 DCNv4 与 DCNv3 相比显示出显著更快的收敛速度，并且处理速度大大提高，DCNv4 的速度提高了三倍以上。

将 DCNv4 集成到其他现代骨干架构中，包括 ConvNeXt 和 ViT，替换深度可分离卷积和密集自注意力层。值得注意的是，在没有进行任何超参数调整的情况下，这些经过精心设计的网络在使用 DCNv4 时表现得相当出色，同时速度快得多，显示了动态、稀疏的 DCNv4 的有效性和效率。