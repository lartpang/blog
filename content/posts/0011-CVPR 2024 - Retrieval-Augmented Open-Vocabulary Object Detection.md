---
title: "CVPR 2024 - Retrieval-Augmented Open-Vocabulary Object Detection"
date: 2024-04-10 07:50:42
tags: ["paper"]
---


<!--more-->

# CVPR 2024 - Retrieval-Augmented Open-Vocabulary Object Detection

* 论文：<https://arxiv.org/abs/2404.05687>
* 代码：<https://github.com/mlvlab/RALF>

本文提出了一种新的开放词汇目标检测方法 Retrieval-Augmented Losses and visual Features (RALF)。RALF 通过从大型词汇库中检索词汇并增强损失函数和视觉特征来提高检测器对新类别的泛化能力。

该方法由两个部分组成：检索增强损失（RAL）和检索增强视觉特征（RAF）。

| RAL                                                                                             | RAF                                                                                             |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| ![image](https://github.com/lartpang/blog/assets/26847524/6b98d3d3-7a4c-4083-9984-bb29e83fd7fe) | ![image](https://github.com/lartpang/blog/assets/26847524/dceade62-4d39-4246-a6cd-edc389575e45) |

* RAL 通过使用与负词汇库的语义相似性的距离来优化嵌入空间。通过从大型词汇库中，按照语义相似性检索与真实类别标签相关的难负词汇和易负词汇。然后，RAL 使用这些词汇和真实框嵌入来定义难负损失和易负损失。
* RAF 则利用大型语言模型（LLM）生成关于大型词汇库的描述，并从中提取有关目标的详细信息，以增强视觉特征。RAF 首先在离线阶段从目标提案中生成视觉特征。然后，在推理阶段，RAF 使用概念检索器和增强器从概念存储库中检索相关概念，并使用这些概念来增强视觉特征。

通过实验，作者证明了 RALF 在 COCO 和 LVIS 基准数据集上的有效性。特别是在 COCO 数据集的新类别上，APN50 提高了 3.4%，在 LVIS 数据集的新类别上，mask APr 提高了 3.6%。 未命名