---
title: "CVPR 2024 - OVFoodSeg - Elevating Open-Vocabulary Food Image Segmentation via Image-Informed Textual Representation"
date: 2024-04-10 11:12:23
tags: ["paper"]
---


<!--more-->

# CVPR 2024 - OVFoodSeg - Elevating Open-Vocabulary Food Image Segmentation via Image-Informed Textual Representation

* 论文：<https://arxiv.org/abs/2404.01409>

## 主要内容

大量食材之间的类别差异、新食材的出现以及与大型食物分割数据集相关的高注释成本。现有方法主要采用封闭词汇和静态文本嵌入设置，往往无法有效处理食材，特别是新颖和多样化的食材。为此本文提出了一种新的开放词汇食品图像分割（Open-Vocabulary Food Image Segmentation）框架 OVFoodSeg，通过采用图像感知文本表示来提升开放词汇食品图像分割的能力。这一任务和框架旨在解决现有方法在处理新和多样化的食材时的不足。

在整合视觉语言模型 CLIP 的基础上，为了处理食物配料视觉表征中大的类内方差，该方法集成了两个创新模块，即图像到文本学习器 FoodLearner 和图像感知的文本编码器 Image-Informed Text Encoder，丰富了文本嵌入与图像特定的信息，从而有效地将知识从已知的食材转移到新的食材。

OVFoodSeg 的训练过程分为两个阶段：

![image](https://github.com/lartpang/blog/assets/26847524/7d86100e-568c-4a81-92e5-1e26689b1193)

第一阶段是预训练 FoodLearner，使其具备将视觉信息与特定相关食物的文本表征对齐的能力。利用视觉表征利用交叉注意力层更新可学习的 query token，文本信息联合生成文本表征。

* FoodLearner 使用预训练的 BLIP2 中的 qformer 来初始化。训练时配合 query token 输入的可以使图像嵌入，也可以是文本嵌入，甚至可以只有文本嵌入。多种输入形式实现对于这一组件的联合优化。
* 使用 Recipe-1M+ 数据集训练。其中的成分过于详细，类似调料等虽然是食谱的组成部分，但由于它们在图像中是不可见的，因此会造成数据噪声。为了提高配料数据的质量，本文通过特定的 prompt 让 ChatGPT 为每个菜谱获取最直观的配料。然后利用清理后的成分列表作为文本信息，与相应的图像配对后对 FoodLearner 模块进行预训练。

![image](https://github.com/lartpang/blog/assets/26847524/b53ac26c-7911-44f0-acc6-7e6c3efd31d9)

第二阶段是用于分割任务的学习阶段，调整 FoodLearner 和 Image-Informed Text Encoder 以适应分割任务。

* FoodLearner 基于可学习的 query token 与图像特征的交互获得文本诱导的视觉表征，这与 CLIP 文本编码器提出的文本表征直接相加，之后直接送入现有的开集分割算法 SAN 的管线中。
* 训练中使用两个基准数据集，即 FoodSeg103 和 FoodSeg195。对于前者，本文随机选择 20 个类作为新类，剩下的 83 个作为基类。对于后者随机使用 40 类作新类，剩余的用于训练。新类别在训练时不可见，仅用于测试。

通过在大规模食品相关图像文本对数据集上预训练 FoodLearner，OVFoodSeg 成功地将视觉信息与文本表示紧密地联系起来，从而有效地解决了食材图像分割中的大类内变化问题。OVFoodSeg 在两个开放词汇食品图像分割基准测试中都取得了最先进的性能，证明了其有效性和对现有方法的超越。

## 食品相关的分割数据集

食品图像分割是食品计算的核心问题，构建具有像素级掩码注释的大规模数据集是解决这一问题的基础。

* 菜品级别注释：注释都限制在菜品级别的分割注释上，这使得它们不适合用于食材分割。
    * Food201【Im2Calories: towards an automated mobile vision food diary】包含约 12,000 张图片，跨越 201 种菜肴类。
    * UECFoodPix【A new large-scale food image segmentation dataset and its application to food calorie estimation based on grains of rice】和 UEC-FoodPIX Complete【UEC-FoodPIX Complete: A large-scale food image segmentation dataset】，它们包含了大约 10,000 张图片，跨越 102 种菜肴类型用于分割。
* 食材级注释
    * FoodSeg103【A large-scale benchmark for food image segmentation】是第一个具有食材级注释的食物图像分割数据集。包含涉及 103 个食材类别的大约 7,000 个图像。
    * FoodSeg195 由本文基于 FoodSeg103 扩展。额外添加 92 个类创建的。其中包括大约 18k 用于训练的图像和 16k 用于测试的图像，总共 113k 个带注释的掩码。额外补充的数据是通过一个政府机构从一个国家的居民那里收集的，用于食物记录。由于保密协定，当前并不会被公开。
* Recipe-1M+【Recipe1m+: a dataset for learning cross-modalembeddings for cooking recipes and food images】是当前最大的图像与食谱成对数据集，有大约 1,000,000 个烹饪食谱。每份食谱都详细介绍了菜肴的名称、烹饪方法、配料表，以及来自不同餐馆的大约 10 张代表这道菜的图片。这个数据集包含了大量的食物照片和配料表。需要注意的是，数据集中的成分列表通常包括“看不见的”成分，如糖、油和盐。