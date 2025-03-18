---
title: "CVPR 2024 - Rethinking the Evaluation Protocol of Domain Generalization"
date: 2024-04-10 06:23:52
tags: ["paper"]
---

<!--more-->

> <https://github.com/lartpang/blog/issues/8>

# CVPR 2024 - Rethinking the Evaluation Protocol of Domain Generalization

![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/c97dafb81fc74a22ba6b43d48dd2f2da.png)

* 论文：<https://arxiv.org/abs/2305.15253>

这篇文章主要讨论了领域泛化评估协议的重新思考，特别是如何处理可能存在的测试数据信息泄露风险。作者首先指出，当前的领域泛化评估协议可能存在问题，可能导致测试数据信息泄露，进而影响评估的公平性和准确性。为了解决这个问题，作者提出了两个建议：

* 一是建议领域泛化算法在进行比较和评估时应采用自监督预训练权重或随机权重作为初始化；
* 二是建议对每个训练模型在多个测试域上进行评估。

作者还根据这些建议重新评估了十个代表性的领域泛化算法，并提供了三个新的测试leaderboard。这些更改和新的测试leaderboard将鼓励未来的研究，并促进领域泛化的更准确评估。