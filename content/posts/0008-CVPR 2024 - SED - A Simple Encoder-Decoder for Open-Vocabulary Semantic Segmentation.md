---
title: "CVPR 2024 - SED - A Simple Encoder-Decoder for Open-Vocabulary Semantic Segmentation"
date: 2024-04-11 06:37:48
tags: ["paper"]
---

<!--more-->

- Author: lartpang
- Link: https://github.com/lartpang/blog/issues/16

# CVPR 2024 - SED - A Simple Encoder-Decoder for Open-Vocabulary Semantic Segmentation

* 论文：<https://arxiv.org/abs/2311.15537>
* 代码：<https://github.com/xb534/SED>

这篇文章提出了一种名为 SED 的简单编码器解码器，用于结合 CLIP 的 open-vocabulary 能力实现了开放词汇语义分割。在多个语义分割数据集上的实验证明了 SED 在开放词汇准确性和效率方面的优势。当使用 ConvNeXt-B 时，SED 在 ADE20K 上的 mIoU 得分为 31.6%，并且在单个 A6000 上每张图像只需 82 毫秒。

> [!note]
本文的方法受启发于最近的 CAT-Seg（通过 cost map 微调图像编码器没有损坏 CLIP 的 open-vocabulary 能力），主要差异包括三点：
> 1. 本文是一个不需要额外视觉 encoder 的更加简单的框架，同时具有更好的性能和更快的推理速度。
> 2. 本文利用分层图像编码器生成 cost map 并且执行跳层融合，这显著提升了性能，并且计算成本与图像尺寸呈线性。
> 3. 本文在解码器中引入了一个简单的大核操作，并逐步融合特征，同时设计了一个 category early rejection strategy 来加速推理同时不损害性能。

## 模型细节

![image](https://github.com/lartpang/blog/assets/26847524/0b093332-8726-409b-af5f-db6e5ed13a11)

SED 方法包括一个 hierarchical encoder-based cost map generation 和一个带有 category early rejection strategy 的 gradual fusion decoder。

| Gradual Fusion Decoder                                                                              | Category Early Rejection                                                                        |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| ![image](https://github.com/lartpang/blog/assets/26847524/b0f1daf1-2cbe-4193-bac3-ef006c4e605a)<br> | ![image](https://github.com/lartpang/blog/assets/26847524/020d6c4e-820e-4e77-88a5-75da1555412d) |

* hierarchical encoder：不使用普通的直筒型 ViT 视觉编码器，而是基于分层的 ConvNeXt 视觉编码器，从而帮助更好地捕捉不同层次的空间信息，增强局部性，并且与输入大小成线性复杂度。利用其可以获得多层级特征图 $F_2, F_3, F_4, F_5$。其中的 $F_5$ 利用最后的 MLP 层转换获得图像嵌入 $F_v \in \mathbb{R}^{H_v \times W_v \times D_t}$，结合文本嵌入集合（对应 $N$ 类，每类 $P$ 个模板，设计与 CAT-Seg 一致） $E \in \mathbb{R}^{N \times P \times D_t}$ 获得像素级的 4D image-text cost map $F_{cv} \in \mathbb{R}^{H_v \times W_v \times N \times P}$ 。
* gradual fusion decoder：解码器采用自顶向下的结构将 cost map 和不同级别的 backbone 特征图结合起来进行分割。通过级联特征聚合模块（FAM）和跳层融合模块（SFM）来逐步组合视觉编码器的多层级特征图 $F_2, F_3, F_4$ 从而生成高分辨率特征图 $F_h$，这通过一个输出层转换为不同类别的分割图预测。需要注意的是，**CAT-Seg 中观察到，直接对图像编码器回传梯度会破坏 open-vocabulary semantic segmentation 性能。所以这里对 skip-layer fusion 模块到图像编码器的梯度进行了截断。**
    * FAM 分别利用大核深度卷积执行空间融合，利用线性自注意力操作执行类别融合。
    * SFM 利用层次编码器的浅层特征 $F_2, F_3, F_4$ 增强 FAM 输出特征图的局部细节。并进一步融合原始的 cost map。
* category early rejection strategy：因为类别数量增大时，解码器中的推理成本会显著增加。但是实际上大多数图像仅包含数个语义类别。所以本文在解码器中引入的类别早期拒绝方案，可以在早期层有效地预测现有类别并拒绝不存在的类别，从而显著提高推理速度。从而最多提供 4.7 倍的速度提升而不会出现显著的性能下降。
    * 训练期间，如图 4a，添加的辅助卷积分治分别预测分割图，并受真值监督。为了避免对模型训练的负面影响，这里阶段了其与 decoder 主体间的梯度。
    * 推理期间，如图 4b，引入 top-k 策略来预测存在的语义类别。通过对每个像素选择选择 top-k 个最大激活类别，从而生成一个所有像素的并集，移除未选择类别后的特征图（$H' \times W' \times N' \times D$）被送到下一个解码器层中。论文中观察到 k=8 的时候确保了大多数存在的类别被识别。

## 实验设定

* 训练集：COCO-Stuff 的训练集，包含大约 118k 密集标注的 171 类目标。
* 测试集：跨数据集测试。
    * ADE20K，包含 20K training 和 2K validation => A-150 和 A-847。
    * PASCAL VOC，包含 1.5k training 和 1.5k validation => PAS-20。
    * PASCAL-Context 来自原始的 PASCAL VOC 数据集 => PC-59 和 PC-459。
* 模型设定：
    * 基于 ConvNeXt-B/L 视觉编码器形式的预训练 CLIP。
    * 类别模板数量 $P$ 同 CAT-Seg 一致，均为 80。
    * 文本编码器冻结，只训练图像编码器和解码器。
    * GPU: 4xA6000 with the mini-batch of 4 images。
    * 图像编码器学习率多乘以一个 0.01 倍的因子。
    * 共 80k 次迭代。
    * 训练时剪裁图像 $768 \times 768$ 大小，测试时直接放缩图像到 $768 \times 768$ 大小。

| Vision Encoder 形式和微调策略的消融                                                                           | Decoder 结构的消融                                                                                   | 早退结构的消融                                                                                             |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| ![image](https://github.com/lartpang/blog/assets/26847524/75713d34-2009-44ee-bae8-37ea4e938696)<br> | ![image](https://github.com/lartpang/blog/assets/26847524/822ff308-f033-4b59-8855-f83a0e2b86cf) | ![image](https://github.com/lartpang/blog/assets/26847524/0fe7a5e1-173e-446e-b384-55eab2101490)<br> |
