---
title: "Arixv 2403 - Parameter-Efficient Fine-Tuning for Large Models A Comprehensive Survey"
date: 2024-04-03 04:46:25
tags: ["paper"]
---
# Arixv 2403 | Parameter-Efficient Fine-Tuning for Large Models: A Comprehensive Survey

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711865052255-f9c75ccf-1daf-488d-ae59-fd854eef2301.png#averageHue=%23f0efef&clientId=u6331460c-e958-4&from=paste&height=176&id=u1a3b8c64&originHeight=351&originWidth=1345&originalType=binary&ratio=2&rotation=0&showTitle=false&size=104896&status=done&style=none&taskId=ue922bda5-62cc-4bb2-b22e-d0a375624b0&title=&width=672.5)

* 论文：[https://arxiv.org/abs/2403.14608](https://arxiv.org/abs/2403.14608)
* 语雀文档：[https://www.yuque.com/lart/papers/gvqrizgggd22g88n](https://www.yuque.com/lart/papers/gvqrizgggd22g88n)

大型模型代表了多个应用领域的突破性进步，在各种任务中取得了显着的成就。然而，其前所未有的规模伴随着巨大的计算成本。这些模型通常由数十亿个参数组成，需要大量的计算资源来执行。特别是，在为特定下游任务定制它们时，特别是在受计算能力限制的硬件平台上，广泛的规模和计算需求带来了相当大的挑战。

参数高效微调 (PEFT) 通过在各种下游任务中有效地调整大型模型，提供了实用的解决方案。具体来说，**PEFT 是指调整预训练大型模型的参数以使其适应特定任务或领域，同时最大限度地减少引入的附加参数或所需的计算资源的数量的过程**。在处理具有高参数量的大规模语言模型时，这种方法尤其重要，因为从头开始微调这些模型可能 computationally expensive 并且 resource-intensive，从而给支撑系统平台的设计带来相当大的挑战。

这份综述：

* 对各种 PEFT 算法进行了全面研究，检查了它们的性能和计算开销。
* 概述了使用不同 PEFT 算法开发的应用程序，并讨论了用于减轻 PEFT 计算成本的常用技术。
* 除了算法角度之外还概述了各种现实世界的系统设计，以研究与不同 PEFT 算法相关的实施成本。

这对于旨在了解 PEFT 算法及其系统实现的研究人员来说是不可或缺的资源，提供了对最新进展和实际应用的详细见解。

大型模型 (LM) 最近引起了公众的极大兴趣。他们理解上下文和细微差别的能力使他们能够熟练地处理跨多个领域的不同任务，包括自然语言处理（NLP）、计算机视觉（CV）等。在 NLP 领域，大型语言模型（LLM）在各种任务上取得了显着的进步，包括文本生成、翻译、个性化聊天机器人和摘要生成，展现出出色的熟练程度。

早期的研究【Language models are few-shot learners】表明 LLM 表现出高水平的泛化能力，**使他们能够应用所学知识到在原始训练未包含的新任务，这种能力通常称为零样本学习。**尽管如此，微调对于在新用户数据集和任务上进一步增强 LLM 性能仍然重要。由于其规模，广泛采用的微调 LLM 的策略主要为**参数高效微调（PEFT），这有选择地调整一小部分参数，同时保持其余参数不变。**此外，PEFT 的应用超出了 NLP 领域，并迅速引起了 CV 社区的兴趣，用于微调具有大量参数视觉模型，例如 Vision Transformer 和扩散模型，以及诸如视觉语言模型（VLM）等学科模型。

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711867142711-2c1a1e7a-8dcc-46fb-9d3b-5b9a1b063214.png#averageHue=%23dfdcdb&clientId=u6331460c-e958-4&from=paste&height=316&id=u5f8e99d8&originHeight=631&originWidth=1595&originalType=binary&ratio=2&rotation=0&showTitle=false&size=161632&status=done&style=none&taskId=ueaac124e-e0a3-4875-b2eb-65428cbb02a&title=&width=797.5)

这份综述系统回顾和分类 PEFT 算法最新进展，以及不同场景下各种 PEFT 算法相关的系统实施成本。图 1 概述了本文内容。

## LLM 和 PEFT 的一些基本概念

### PEFT 的背景知识

微调对于提高未见过的用户数据集和任务上的 LLM 性能仍然至关重要。随着模型规模的不断增长（例如，GPT-2 中的 1.5B 到 GPT-3 中的 175B），标准的完全微调范式需要数千个 GPU 并行工作，这是非常低效且不可持续的。人们提出参数高效微调（PEFT）来调整最小参数，以在下游任务的全面调整上获得更好的性能。

在并行发展中，视觉和多模态领域的大规模预训练模型也展示了其有效的表征学习能力，能够通过微调实现从大型数据集到较小数据集的适应或跨各种数据模式的适应。因此，这种能力使 PEFT 对更广泛的研究界越来越有吸引力。

### 常用的数据集和任务

语言方面：

* 通用语言理解评估（GLUE）基准：
   * 它集成了九个句子或句子对语言理解任务（CoLA、SST-2、MRPC、STS-B、QQP、MNLI、QNLI、RTE 和 WNLI），数据集选择过程考虑了数据集大小、文本类型和难度级别的多样性，并建立在现有数据集上。
   * 它还包括专门设计用于评估和分析自然语言中固有的各种语言现象的性能诊断数据集。
   * 它还具有一个公共排行榜来跟踪基准测试的性能，以及一个仪表板来可视化诊断集上的模型性能。
* 最近的 LLM 论文使用的另一类数据集是常识推理：
   * OpenBookQA 旨在促进高级问答领域的研究，深入研究对主题及其表达语言的深刻理解。
   * PIQA 主要强调日常场景，表现出对非常规解决方案的偏爱。
   * Social IQA 作为一种新颖的问答基准而出现，专门用于衡量社会常识智力。
   * HellaSwag 作为一个数据集，其本质是确定机器恰当地总结句子的能力。
   * BoolQ 是一个专用于问答的数据集，特别是二元响应（是或否的查询）。
   * WinoGrande 作为新的集合引入，包含 44,000 个问题。
   * ARC-easy 是一个新数据集，包含真正的小学水平的多选的科学问题，旨在激发复杂问答的研究。
   * ARC-challenges 只包含那些基于检索的算法和单词共现算法都不能准确解决的问题。

视觉方面：

* 图像识别，例如细粒度视觉分类（FGVC）和视觉任务适应基准（VTAB）。
* 视频动作识别，涉及 Kinetics-400、SSv2 和 HMDB51 等数据集。
* 此外 MSCOCO、ADE20K 和 PASCAL VOC 等密集预测任务数据集也被关注。

## 根据计算流程分类 PEFT 算法

根据操作将 PEFT 算法分为加性、选择性、重新参数化和混合四种类型。

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711871880245-dd205c4f-180f-4caf-bc3b-dd0a1d573469.png#averageHue=%233bfb31&clientId=u6331460c-e958-4&from=paste&height=527&id=zo1Lc&originHeight=1053&originWidth=2313&originalType=binary&ratio=2&rotation=0&showTitle=false&size=391134&status=done&style=none&taskId=ue4f69c04-fac3-4009-b49f-bacaefd3e64&title=&width=1156.5)

| Transformer 上应用不同类型 PEFT                                                                                                                                                                                                                                                                                                                                                                      | 不同类型的 PEFT 对比                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711874627081-3cde1465-f9dd-487e-8745-fa21bc6f04fb.png#averageHue=%23dcd8d8&clientId=u6331460c-e958-4&from=paste&height=204&id=ue6324fc9&originHeight=601&originWidth=651&originalType=binary&ratio=2&rotation=0&showTitle=false&size=51799&status=done&style=none&taskId=u4687ad44-6969-45b7-8274-d12912cb507&title=&width=221.5) | ![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711873318151-6399e64f-0d01-4ee7-be81-fc97ecde0532.png#averageHue=%23efeeee&clientId=u6331460c-e958-4&from=paste&height=201&id=ueb6acec9&originHeight=401&originWidth=891&originalType=binary&ratio=2&rotation=0&showTitle=false&size=46452&status=done&style=none&taskId=u061657ff-0ecf-49a9-9c44-4b27749b76e&title=&width=445.5)<br> |

### Additive PEFT

通常要么引入额外的权重参数，要么修改激活。在不同的附加可调模块或参数方面彼此不同。

标准的完全微调需要大量的计算费用，并且还可能损害模型的泛化能力。为了缓解这个问题，一种广泛采用的方法是保持预训练主干不变，并仅引入在模型架构中策略性定位的最少数量的可训练参数。在针对特定下游任务进行微调时，仅更新这些附加模块或参数的权重，这会导致存储、内存和计算资源需求的大幅减少。由于其添加参数的特点，这些技术可以称为附加性调整。

大体分为三类：

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711873702941-3b7ec4f4-fdb5-4574-8dea-26549e3e8307.png#averageHue=%23f1efea&clientId=u6331460c-e958-4&from=paste&height=206&id=ue80bc866&originHeight=411&originWidth=1791&originalType=binary&ratio=2&rotation=0&showTitle=false&size=89460&status=done&style=none&taskId=u7da5b171-b952-41b3-b68b-06e32d3a772&title=&width=895.5)

#### Adapter

在 Transformer 块内插入小型适配器层。通常适配器层由降维投影矩阵、非线性激活函数和升维投影矩阵，以及残差框架组成。配置适配器时会将内部的维度变化配置设置为超参数。

* 顺序形式：
   * **Serial Adapter** 中最初提出了 NLP 领域适配器概念。每个 Transformer 块都通过添加两个适配器模块来增强，一个适配器模块分别位于自注意力层之后，另一个位于 FFN 层之后。随后的研究旨在解决与适配器层相关的额外计算成本。
   * **AdapterFusion** 中提出了一种修改后的框架，其中仅在 FFN 层之后的 "Add & Norm" 步骤之后插入适配器层，以提高计算效率。
* 并行形式：这避免前述顺序形式可能会降低模型的并行性，并需要在推理效率和准确性之间进行权衡的问题。
   * **Parallel Adapter (PA)**将传统的顺序适配器层重新组织为与每个 Transformer 子层并行的网络。
   * **CIAT、CoDA 和 KronA**也采用并行适配器设计。
* 稀疏激活：
   * **CoDA**还采用稀疏激活机制来提高推理效率。其使用软 top-k 选择过程识别每层中的 k 个重要标记，这些标记将由冻结的预训练 Transformer 层和适配器分支进行处理，以保持模型的准确性。那些不重要的标记仅由适配器分支处理，同时跳过繁重的预训练层，因此在不影响整体性能的情况下优化了推理效率。

为了提高适配器的性能和泛化能力，各种研究已经实现了多任务学习策略。

* **AdapterFusion** 将所有预训练的适配器保留在模型中，并采用融合模块来合并多任务信息。
***MerA** 通过基于权重和激活的最佳传输将预训练的适配器合并为一个适配器。这种方法避免了引入任何额外的可训练参数，从而提高了计算效率。
* **Hyperformer** 将多任务信息存储在共享的超网络中，该超网络根据任务和层 ID 嵌入生成特定于任务和层的适配器参数。给定一个新任务，只需要学习一个额外的任务嵌入，因此减少了训练参数的数量。

#### Soft Prompt

人们普遍认为，**软提示的连续嵌入空间本质上包含更多信息，而不是通过上下文学习来优化离散 token 表示**【When do prompting and prefix-tuning work? a theory of capabilities and limitations】。受到这个概念的启发，研究人员直接将可调整向量（称为软提示）附加到输入序列的开头。这可以表示如下：

* **Prefix-tuning** 将可学习向量添加到所有 Transformer 层中的 k 和 v 序列之前。为了确保优化过程中的稳定性，Prefix-tuning 采用了重参数化策略，利用 MLP 层来生成这些前缀向量，而不是直接对其进行优化。微调后，仅保存前缀向量以供推理。该技术在多项研究中得到了调整和改进。
* **P-tuning v2**删除了重参数化并将其用途扩展到更广泛的模型规模和 NLP 任务。
* **APT (Adaptive Prefix Tuning)** 通过引入自适应门机制来控制每层中的前缀重要性来增强前缀调整。
* 同期的工作 P-tuning 和 Prompt-tuning 仅在初始词嵌入层,而不是所有层应用可学习向量，以提高训练和推理效率。需要强调的是，后者主要在大型模型中证明了其有效性，特别是那些拥有超过 110 亿个参数的模型。
* **Xprompt** 作为补充，通过分层结构修剪消除了负面提示标记，从而缩小了较小模型规模的性能差距。 并且 Universality and limitations of prompt tuning 中提供了一些针对即时调整的理论分析，证明了其在有限深度 Transformer 中的普遍性和局限性。
* **IDPG (InstanceDependent Prompt Generation)** 通过使用轻量级提示生成器根据每个输入句子生成提示来改进提示调整。
* **LPT (Late Prompt Tuning)** 还利用提示生成器来获取实例感知提示。与之前的工作不同，LPT 仅在中间层之后添加这些提示，而不是在初始层或所有层。这种策略性的布局消除了中间层以下的梯度计算，从而显着加快了训练速度。同时，LPT 可以提高整体性能，因为较短的反向传播路径保留了更多的任务相关信息。
* **SPT (Selective Prompt Tuning)** 受 LPT 的启发，更深入地研究了提示插入策略的重要性。它在每一层中引入一个可学习的概率门控，来确定是使用从前一层传播的提示还是注入新生成的提示。
* **APrompt** 采用了另一种提示插入策略。除了在每个 Transformer 层的输入序列开头插入输入提示之外，APrompt 还为自注意力模块中的相应的 Q、K、V 矩阵添加额外的可学习的 prompt，以学习新的注意力模式。此外，APrompt 还结合了任务特定头的学习。

软提示的概念已被用于各种下游任务，尽管它们的训练可能容易不稳定且收敛缓慢。

* **SPoT** 为了解决这个问题，使用从一个或多个任务中学习到的源提示来初始化新任务的提示。
* **TPT (transferable prompt tuning)** 提出将 Soft Prompt 从一个任务迁移来初始化另一个任务，这表明更好的提示初始化会带来很大的训练收敛加速。
* **InfoPrompt** 开发了两种基于互信息的损失函数，即头损失和表示损失，以找到更好的提示初始化并学习足够的任务相关信息，从而也加速收敛。
* **PTP** 深入研究了训练不稳定的根本原因。它识别了传统即时调整中损失情况的陡峭性质，其中输入数据的微小变化可能导致显着的损失波动。为了缓解这个问题，PTP 引入了基于扰动的正则化器来平滑损失情况，从而稳定训练过程。
* **DePT** 将软提示分解为带有一对低秩矩阵的较短的软提示，并使用两种不同的学习率进行优化。该策略不仅提高了性能，还提高了训练和推理效率。
* **SMoP (Sparse Mixture-of-Prompts)** 通过利用简短的软提示来减少训练和推理成本。在训练过程中，训练多个简短的软提示，每个提示都针对数据集的特定子集进行定制。在推理过程中，SMoP 集成了一种门控机制，将每个输入实例路由到适当的简短提示。该技术不仅提高了训练和推理阶段的效率，而且还保持了与较长软提示所实现的性能相当的性能。
* **IPT (Intrinsic Prompt Tuning)** 为了进一步减少软提示参数的数量，通过在多个任务上训练自动编码器来识别内在任务子空间。然后，调整新任务只需调整该子空间内的几个参数，从而显着减少训练参数的数量。

#### 其他的一些方案

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711875664229-4e59cc72-93ab-458a-ade2-93b2d9a1a811.png#averageHue=%23eeede8&clientId=u6331460c-e958-4&from=paste&height=250&id=u88e6c0d4&originHeight=499&originWidth=1021&originalType=binary&ratio=2&rotation=0&showTitle=false&size=72691&status=done&style=none&taskId=u7ae5d66a-5324-4191-b0f9-2c2e8356e90&title=&width=510.5)

除了上面提到的方法之外，还出现了其他在微调过程中策略性地合并附加参数的方法。

* **(IA)$^3$** 引入了三个一维的可学习重缩放向量，分别重新缩放 K、V 和 FFN 的激活。而 Q 和 K 的尺度向量可以无缝地集成到 Q 和 K 的权重矩阵中。这种集成有效地消除了推理过程中的额外计算成本。
* **SSF** 与之类似，也对模型激活执行线性变换。在预训练模型中的每个操作（即 MSA、FFN 和层归一化）之后，注入 SSF-ADA 层，该层对操作生成的特征执行缩放和移位。在微调过程中，只有 SSF-ADA 层可以更新。而在推理过程中，与 (IA)3 类似，这些 SSF-ADA 层可以合并到模型权重中，因此不会产生额外的推理开销。
* **IPA (InferenceTime Policy Adapters)** 提供了一种新颖的方法来使 LLM（例如 GPT-4）与用户特定的要求保持一致，而无需修改基本模型的参数。当处理参数非常大且通常无法直接访问的模型时，这一点尤其重要。IPA 通过在解码阶段将基本 LLM（基本策略）的输出分布与较小规模模型（适配器策略）的输出分布相结合（通过乘法和归一化）来实现这一目标。在训练过程中，策略适配器的参数使用强化学习进行微调，而基本策略的参数保持固定。在推理过程中，IPA 使用基本模型和经过训练的策略适配器的组合分布进行解码，对其进行定制以满足特定的用户定义标准。

### Selective PEFT

专门需要对现有参数进行微调的算法。不需要任何额外的参数，它从主干模型中选择一小部分参数（就像是乘上了了一个二值掩码一样），仅使它们可学习，同时在下游任务的微调过程中保持大多数参数不变。根据所选参数的分组可以分类为非结构化掩码和结构化掩码。

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711876861227-c025e4c6-1e13-45ed-9360-b3ce47f721f0.png#averageHue=%23eae7de&clientId=u6331460c-e958-4&from=paste&height=213&id=uac0bbf90&originHeight=425&originWidth=1013&originalType=binary&ratio=2&rotation=0&showTitle=false&size=50411&status=done&style=none&taskId=u0566aa6b-8d04-401d-a1bb-af1486dc604&title=&width=506.5)

* 非结构化掩码
   * **Diff pruning** 是一项代表性工作，它在微调过程中将可学习的二进制掩码应用于模型权重。为了实现参数效率，掩模通过 L0 范数惩罚的可微近似进行正则化。
   * **PaFi** 只需选择具有最小绝对量级的模型参数作为可训练的。
   * **FishMask** 使用近似 Fisher 信息确定参数重要性。然后它根据此信息选择前 k 个参数以形成掩码。
   * **Fish-Dip** 也使用 Fisher 信息来计算掩码，但掩码将在每个训练周期动态重新计算。
   * **LT-SFT** 引入了另一种技术来确定参数重要性，该技术受到彩票假设的启发，其中选择在初始微调阶段变化最大的参数子集来形成掩码。
   * **SAM**【On the effectiveness of parameter-efficient fine-tuning】提出了一种二阶近似方法，该方法用可分析求解的优化函数来近似原始问题，以帮助确定参数掩码。
   * **Child-tuning** 提出了两种在每次训练迭代期间选择子网络的方法，其中仅可以更新该子网络内的参数。
* 结构化掩码：上述非结构化参数掩码会导致非零掩码分布不均匀，并在实现 PEFT 时降低硬件效率。以规则模式组织参数掩码可以提高训练期间的计算和硬件效率。因此各种结构化选择性 PEFT 技术得到了广泛的研究。
   * **Diff pruning**提出了一种结构化剪枝策略，将权重参数划分为局部组并策略性地将它们一起消除。
   * **FAR** 通过将 Transformer 块中 FFN 的权重分组为节点来微调 BERT 模型，然后使用 L1 范数对学习器节点进行排序和选择。为了进一步降低内存访问频率，他们还通过将学习器节点分组在一起来重新配置 FFN。
   * **Bitfit** 仅仅调整每个 DNN 层的 bias 参数，并在小模型上取得有竞争力的结果。然而，这种方法无法处理大型模型。
   * **S-BitFit**【Neural architecture search for parameter-efficient fine-tuning of large pre-trained language models】将 NAS 应用到 Bitfit，保留了 Bitfit 中的结构化性质，限制 NAS 算法必须为每个 bias 模块选择是否倒数为的。
   * **Xattn Tuning** 其仅微调交叉注意层。
   * **SPT (sensitivity-aware visual parameter-efficient fine-tuning)** 首先识别调整时通过损失的减少测量的敏感参数。该灵敏度是使用一阶泰勒展开式计算的，该展开式是在单次微调之前从单个前向和后向传递中导出的。接下来，SPT 找到敏感参数数量超过预定义阈值的权重矩阵，然后将 PEFT（例如 LoRA 和 Adapter）应用于这些目标权重，以实现结构调整。
   * **LayerNorm Tuning** 只调整每个注意力块中的 LayerNorm 的权重。这种简单的技术可以实现与微调相当甚至更好的性能，同时提供比 LoRA 高约 10 倍的参数效率。

### Reparameterized PEFT

这通常意味着构建低秩参数化以在训练期间实现参数效率的目标。重新参数化微调在训练期间引入了额外的低秩可训练参数，然后将其与原始模型集成来推理以保持推理速度。该方法分为低秩分解和 LoRA 衍生形式两大类。

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711876879150-9e62e395-850d-49a7-a18e-40eaf8762e70.png#averageHue=%23efebe1&clientId=u6331460c-e958-4&from=paste&height=278&id=ua3a6fb02&originHeight=555&originWidth=2061&originalType=binary&ratio=2&rotation=0&showTitle=false&size=129113&status=done&style=none&taskId=u46185b3c-b226-4aac-8423-9041702cf70&title=&width=1030.5)

早期的研究**Intrinsic SAID**【Intrinsic dimensionality explains the effectiveness of language model finetuning】表明，常见的预训练模型表现出极低的内在维度。换句话说，可以找到对整个参数空间进行有效微调的低维重新参数化。 **Intrinsic SAID** 是在 LLM 微调过程中研究内在维度特征的开创性工作。然而，最广泛认可的重新参数化技术是**LoRA (Low Rank Adaptation)**。

对于给定的预训练权重矩阵，如图 8(a)，LoRA 引入了两个可训练的权重矩阵（其中秩 $r \ll min(d,k)$）与预训练权重并行操作，从而实现结果对预训练组件输出的增量更新，从而封装了特定于任务的知识。在训练开始时，使用随机高斯分布对降维矩阵进行初始化，而升维矩阵初始化为零，确保增量最初保持为零值。微调完成后，LoRA 的自适应权重将与预先训练的主干权重无缝集成。这种集成确保 LoRA 保持模型的效率，在推理过程中不会增加额外的负担。

在 LoRA 训练中，选择合适的 rank 一直是一个具有挑战性的问题。为了解决这个问题，出现了一些工作：

* **DyLoRA**在预定义的训练预算内训练了一系列的具有不同秩的 LoRA 模块。DyLoRA 在训练过程的每次迭代中动态选择一个秩。则两个矩阵针对所选的秩定制，从而产生两个空间截取的版本，并且本次迭代期间后续的前向和反向传播将被限制在选定位置，而不是完整权重。通过这种动态且免搜索的方法，DyLoRA 显着减少了为特定任务找到最佳且固定的 LoRA 秩所需的训练时间。
* **AdaLoRA**使用奇异值分解 (SVD) 重新表述整个增量变换，表示为 $\Delta W = P \Lambda Q$，三个矩阵都设置可学习，其中 $P \in \mathbb{R}^{d \times r}$ 和 $Q \in \mathbb{R}^{r \times k}$ 正交，$\Lambda \in \mathbb{R}^{r \times r}$ 是包含奇异值的对角矩阵。训练过程中，奇异值被根据其重要性分数进行迭代修剪，这些重要性分数是根据梯度权重乘积大小的移动平均值构建的。并构建额外的正则化项确保 $P,Q$ 之间的正交性。这种自适应方法使模型能够动态调整每个 LoRA 模块内的秩，根据权重矩阵的重要性有效管理其参数计数。
* **SoRA**中认为 AdaLoRA 中使用的重要性分数是启发式构建的，缺乏严格的理论动机。此外，移动平均运算和额外的正则项的计算在训练期间引入了额外的计算成本。为了解决这个问题，SoRA 消除正交性前提，直接应用和优化在降维输出后插入的门控向量 $g \in \mathbb{R}^{r}$，其通过 L1 损失的近端梯度迭代的变体进行更新，这具有明确的数学意义并且不需要启发式前提。训练后，通过删除降维和升维权重中对应于门向量中 0 的列和行。

随后的几项研究旨在提高 LoRA 各方面的性能。

* **Laplace-LoRA** 注意到经过微调的 LLM 常常表现出过度自信。为了增强微调 LLM 的校准，Laplace-LoRA 采用贝叶斯方法，特别是对 LoRA 参数的后验拉普拉斯近似（post-hoc Laplace approximation）。
* **LoRA+** 建议为 LoRA 的两个权重矩阵设置不同的学习率，以至于升维的学习率大于降维的。
* **LoRAHub** 聚合了针对不同任务进行训练的各种 LoRA 模块。给定一些新任务的示例，LoRAHub 可以通过无梯度方法 Shiwa 自主构建兼容的 LoRA 模块，而无需人工干预。
* **MOELoRA** 采用专家混合 (MOE) 方法在多任务设置中训练 LoRA，从而产生多个专家 LoRA 模块。为了检索特定任务的参数，MOELoRA 利用任务驱动的门函数，根据任务 ID 为每个专家分配贡献权重，并通过所有专家的加权和计算最终参数。

除了 LoRA 之外，其他几种具有巨大潜力的重新参数化技术正在兴起。

* **Compacter** 将降维和升维权重进一步简化为 $W = \sum^n_{i=1}A_i \otimes B_i$，这里 $A_i \in \mathbb{R}^{n \times n}, B_i \in \mathbb{R}^{\frac{r}{n} \times \frac{d}{n}}$，并二者使用 Kronecker 积组合。通过将 $A_i$ 指定为共享参数并使用两个低秩矩阵的乘积重新参数化 $B_i$ 来进一步减少参数数量，从而有效地将参数复杂度从 $O(rd)$ 降低到 $O(r+d)$。
* **KronA** 和**KAdaptation** 也采用 Kronecker 乘积来重新参数化适配器权重，旨在实现参数减少。
* **HiWi** 提出了一种适配器微调方法，该方法将适配器直接应用于预训练参数，而不是隐藏表征上 $W' = W + \sigma(WW_{down})W_{up}$，这里的 $W$ 表示 Transformer 块 FFN 的权重或者偏置参数。推理期间，$W'$ 会先计算，确保模型位置推理延时不变。
* **DoRA (Weight-Decomposed Low-Rank Adaptation)** 将模型权重分解为幅度向量 m 和方向矩阵 V 的组合。随后 DoRA 对 m 和 V 采用独特的微调策略。虽然两者都是可调的，但实际只有 V 进行 LoRA 形式的重参数化，对其加上基于降维升维组合的附加权重。DoRA 在各种任务和模型中始终优于 LoRA。

### Hybrid PEFT

各种 PEFT 方法的功效在不同的任务中可能存在显着差异。因此，许多研究旨在结合不同 PEFT 方法的优点，或通过分析这些方法之间的相似性来寻求建立统一的视角。

* **UniPELT**将 LoRA, prefix-tuning, 和 adapters 集成到每个 Transformer 块中。为了控制哪些 PEFT 子模块应该被激活，他们还引入了门控机制。该机制由三个小 FFN 组成，每个 FFN 产生一个 0~1 的标量值 G，然后分别应用于 LoRA、前缀和适配器矩阵。在各种设置中，UniPELT 始终显示出准确度的提高，范围为 1% 到 4%。
* **S4**探索了几种 PEFT 方法（即 Adapter (A), Prefix (P), BitFit (B), LoRA (L)）的设计空间，以揭示底层设计模式。经过一系列实验，他们发现，对 Transformer 层应用主轴分组划分后得到的四个层组具有如下特点，由此产生的具有最佳性能的设计空间是（G1 : AL, G2 : AP, G3 : APB, G4 : PBL）：
   * 组中的层具有相似的行为，这意味着应该应用相似的 PEFT 策略。
   * 将可训练参数的数量均匀分配到各层。
   * 调整所有组。
   * 在不同组中分配不同的 PEFT 策略。
* **MAM Adapter**探索了三种附加性 PEFT 方法之间的内在相似性：adapters, prefix-tuning, LoRA，这导致了如下三种变体的开发，广泛实验表明最有效的配置包含在 SA 层中使用 prefix-tuning，并在 FFN 层中使用 Scaled Parallel Adapter，称为 MAM Adapter。
   * Parallel Adapter 将适配器层放置在特定层（SA 或 FFN）旁边而不是他们后面；
   * Multi-head Parallel Adapter 将并行适配器分为多个头，都会影响 SA 中的头注意力输出；
   * Scaled Parallel Adapter 在并行适配器层之后添加了一个缩放项，类似于 LoRA。
* **LLM-Adapters** 构建了一个易于使用的框架，将各种 PEFT 技术合并到 LLM 中。通过跨多个数据集的全面基准测试，该研究揭示了几个关键见解：
   * series adapters, parallel adapters, LoRA 最有效的位置分别是在 MLP 层之后、MLP 层旁边，和同时跟随注意力层和 MLP 层。
   * 与规模较大的 LLM 相比，利用 PEFT 的规模较小的 LLM 可以在某些任务上取得有竞争力甚至更好的结果。
   * 通过适当的分布内数据微调，较小的模型能够在特定任务的性能上超越较大的模型。
* **NOAH** 发现不同的 PEFT 配置是专门针对不同的任务而定制的。为了解决这个问题，NOAH 使用 NAS 来识别每个数据集最有效的 PEFT 配置。具体来说，NOAH 的搜索空间包含三种 PEFT 方法：Adapter、LoRA 和 Visual Prompt Tuning (VPT)。它利用 AutoFormer （一种 one-shot NAS 算法）来有效发现最佳 prompt 模块。
* **AUTOPEFT** 首先建立一个搜索空间，其中包括 serial adapters, parallel adapters, prefix tuning。之后提出了一种基于高维多维贝叶斯优化的有效 NAS 方法。

## 进一步降低 PEFT 算法计算复杂性的策略

从计算的角度来看，处理延迟 latency 和峰值内存开销 peak memory overhead 是需要考虑的关键因素（pivotal factor）。以下几种策略都旨在最小化模型资源消耗的同时增强模型性能。由于量化方法的独特性，将其从内存高效的 PEFT 内容中独立出来单独讨论。

### KV 缓存管理

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1711946249914-6065c052-e856-4e75-aa5a-566853220d66.png#averageHue=%23ecebea&clientId=uce0d62d6-ada8-4&from=paste&height=236&id=u52326c01&originHeight=489&originWidth=930&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=56598&status=done&style=none&taskId=u47c22575-4363-4f8d-ac0c-e28a01b05dd&title=&width=448)

LLM 模型的核心在于自回归 Transformer 模型。自回归特性成为设计推理系统的一个主要挑战。因为每次生成一个新的令牌时，整个 LLM 模型必须将所有权重从不同的内存转移到图形处理器的内存中，这对于单用户任务调度或多用户工作负载平衡非常不友好。

服务自回归范式的挑战性部分是所有先前的序列都必须被缓存并保存以供下一次迭代使用，由先前序列生成的缓存激活被存储为键值缓存（KV-cache）。KV-cache 的存储将消耗内存空间和 IO 性能，导致工作负载内存有限 (workload memory-bounded)，并且系统的计算能力利用率不足 (under-utilizing the computation power)。

之前的工作提出了一系列解决方案，例如 KV-cache 控制管理【Efficient Memory Management for Large Language Model Serving with PagedAttention】或 KV-cache 压缩【High-throughput Generative Inference of Large Language Model with a Single GPU】，以提高吞吐量或减少延迟。

在设计 PEFT 方法时，考虑 KV-cache 的特性以补充其功能至关重要。例如，当在推理阶段应用 soft prompt 时，有效利用 KV-cache 来处理这些附加输入可以通过确保 prompt 相关的数据易于访问从而帮助加快响应时间。

### 剪枝

这可以大大提高 PEFT 方法的效率。特

* **AdapterDrop**探索了从 AdapterFusion 中删除浅层 Transformer 层适配器和多任务适配器，这表明剪枝可以提高训练和推理效率，同时性能下降最小。
* **SparseAdapter**研究了不同的修剪方法，发现高稀疏率（80％）可以优于标准适配器。此外，大稀疏配置在增加瓶颈维度的同时保持恒定的参数预算（例如，以 50% 的稀疏度加倍维度），大大增强了模型的容量，从而提高了性能。
* **SPLoRA**对 LoRA 中降维和升维的权重采用基于通道的剪枝。这种修剪不仅影响源权重，而且影响 LoRA 的这两个权重。
* **LoRAPruning** 不仅对预训练模型权重采用结构化剪枝，而且对 LoRA 权重也采用结构化剪枝。非结构化 LoRA 剪枝方法主要侧重于稀疏模型权重，同时保持 LoRA 权重的密集性，从而使权重合并难以实现，与此相反，LoRAPruning 可以轻松合并权重。此外，这项工作还引入了一种新颖的标准，利用 LoRA 梯度作为预训练权重梯度的近似值，从而能够估计权重重要性。
* **ProPETL**跨层和任务构建单个共享原型（例如 adapter, prefix, LoRA）。此外，ProPETL 学习二进制掩码来修剪不同层和任务中的不同子网络。因此，参数可以在跨层和任务中重用，大大提高了参数效率。

### 量化

这是另一种提高计算效率和减少内存使用的流行技术。

* **BI-Adapter**通过调查适配器的损耗情况，发现适配器对参数空间中的噪声具有抵抗力。基于这一见解，作者引入了一种基于聚类的量化方法。值得注意的是，**他们证明了适配器的 1-bit 量化不仅可以最大限度地减少存储需求，而且可以在所有精度设置中实现卓越的性能**。
* **PEQA (ParameterEfficient and Quantization-aware Adaptation)** 使用两阶段管道来实现参数高效和量化感知的微调。第一阶段，预训练的 FFN 权重矩阵被量化为一个通道放缩量构成的向量与量化权重之间的乘积。第二阶段，量化权重保持固定，仅对通道放缩向量微调。这种方法不仅保证了内存效率，而且有利于参数效率。
* **QLoRA** 提出了几种新技术，包括 4-bit NormalFloat、双量化和分页优化器，将 4-bit 量化预训练语言模型反向传播到 LoRA 中。这些技术可以在单个 48GB GPU 上对 65B 语言模型进行微调，同时保持与完整 16-bit 微调类似的性能。与原始 LoRA 类似，QLoRA 将固定的零初始化 LoRA 权重附加到量化的预训练模型作为训练起点。

然而，当应用极低 bit（例如 2-bit）量化时，巨大的量化误差会对 LoRA 微调的初始化产生负面影响，即 $\text{quantization}(W_0)+W_{down}W_{up} \ne W_0$（$W_{down}=0$），如【Make Your Pre-trained Model Reversible: From Parameter to Memory Efficient Fine-Tuning】中对初始化的研究所示（“在初始化 PEFT 方法时保持 PLM 的起点是至关重要的”）。为了解决这个问题，提出了几种量化策略来消除量化误差。

* **LoftQ (LoRA-Fine-Tuningaware Quantization)** 提出了一种创新框架，为后续的 LoRA 微调提供了量化主干权重和 LoRA 权重的优越初始化点。该方法通过在网络初始化期间优化 Frobenius 范数目标来解决由量化引起的差异，该目标考虑了 LoRA 权重和量化的预训练骨干网络。LoftQ 在 2-bit 量化方面表现出优于 QLoRA 的性能，并且对下游任务具有更强的泛化能力。
* **LQ-LoRA** 使用一种受稳健主成分分析启发的迭代算法，该算法近似分解预训练权重 $W_0$ 为 $Q + L_1L_2$ 来解决由量化误差引起的不准确性，其中 $Q$ 是保持固定的量化分量，$L_1, L_2$ 是可训练的低秩分量。此外，该方法利用整数线性规划来确定混合量化策略，从而为每个权重矩阵启用动态量化配置，同时遵守预定的总比特率限制。
* **QA-LoRA** 解决了 QLoRA 的另一个限制，即在微调后难以保留其量化属性。在 QLoRA 中，量化的预训练权重（NF4）必须恢复为 FP16，以在权重合并期间匹配 LoRA 权重精度（FP16）。相反，QA-LoRA 使用 INT4 量化并引入分组运算符以在推理阶段实现量化，因此与 QLoRA 相比提高了效率和准确性。
* **BitDelta** 引入了一种新颖的 1-bit 训练后量化方法，该方法作用于微调模型与底层预训练模型之间的权重增量。具体来说，给定分别来自微调模型和基础模型的权重矩阵，二者之间的权重增量 $\Delta = W_{fine} - W_{base}$ 被二值化为 $\alpha \odot \text{Sign}(\Delta)$。这里高精度缩放标量 $\alpha$ 根据增量的平均绝对增量值初始化。BitDelta 通过在紧凑校准数据集上的蒸馏进一步校准缩放因子，而二进制矩阵保持不变。这种方法通过利用单个全精度基本模型以及高效批处理的 1-bit 增量，显着简化了共享服务器上多个微调模型的部署。

### 内存优化

由于其规模相当大，微调完整的 LLM 需要大量的训练内存。虽然大多数 PEFT 方法主要以参数效率为目标，但它们在训练期间仍然会产生大量内存开销，因为梯度计算和反向传播对于这些方法仍然是必要的。例如，根据一些文献【LST: Ladder Side-Tuning for Parameter and Memory Efficient Transfer Learning，Parameter-efficient Tuning for Large Language Model without Calculating Its Gradients】，与完整模型微调相比，**流行的 PEFT 技术（例如适配器和 LoRA）只能将内存使用量减少到大约 70%**。从计算的角度来看，内存效率仍然是一个不容忽视的关键因素。

为了提高内存效率，人们开发了各种技术来最大限度地减少微调期间整个 LLM 缓存梯度的需要，从而减少内存使用。

* **Side-Tuning**和**LST(Ladder-Side Tuning)** 都引入了与主干模型并行的可学习网络分支。通过专门通过该并行分支引导反向传播，它避免了存储主模型权重的梯度信息的需要，从而显着减少了训练期间的内存需求。
* **Res-Tuning**将 PEFT 调整组件（例如，prompt tuning, adapter）与骨干模型解耦，提出了一种名为 Res-Tuning-Bypass 的内存高效微调框架，该框架通过删除从解耦的调整组件到主干的数据流，来生成与主干模型并行的旁路网络。这消除了反向传播期间骨干模型内梯度缓存的要求。
* **MEFT(Memory-efficient fine-tuning)** 是一种受可逆模型【The Reversible Residual Network: Backpropagation Without Storing Activations】启发的方法。在可逆模型的训练过程中，中间激活不需要缓存在前向传递中。在反向传播期间，可以根据最终输出重新计算它们。为了在微调过程中节省内存，MEFT 研究了如何将 LLM 转换为其可逆的对应项，而无需额外的预训练。**这种转换的一个关键方面是在预训练模型中仔细初始化新引入的参数。** MEFT 论证了参数初始化的重要性，并建议这些参数必须以保留预训练模型起点的方式进行初始化，确保修改后模型的微调达到与完全微调模型相当的性能方法。考虑到这一关键因素，MEFT 引入了三种不同的方法，每种方法都显着减少了传统上存储激活的内存需求。
* **LoRA-FA**解决了 LoRA 微调中内存开销的限制。**在训练过程中，LoRA 模块仍然需要较高的激活内存消耗。这是因为，在反向传播期间，必须在前向传播期间存储大量输入激活来计算梯度。** LoRA-FA 通过冻结预训练权重和 LoRA 中降维权重并仅更新 LoRA 中升维权重来解决这个问题。因此，不再需要存储输入激活，因为降维权重输出的中间激活足以用于升维权重的梯度计算。所以 LoRA-FA 中激活的内存需求可以显着降低。

为了进一步减少微调期间的内存使用，一些方法尝试规避 LLM 内的反向传播来解决此问题。

* **HyperTuning** 采用超模型仅使用少数样本来生成 PEFT 参数。这种方法展示的结果与通过完整模型微调获得的结果相当。
* **PEFT Plug-in** 首先在小型语言模型上训练 PEFT 模块，与在大型语言模型上训练相比，它的内存效率更高。随后，该研究引入了一套技术，用于在推理过程中将这些经过训练的 PEFT 模块无缝集成到 LLM 中。这种策略有效地避免了直接在较大模型上进行基于梯度的优化的必要性，从而节省了大量的内存。**但需要注意的是，HyperModel 和 PEFT Plug-in 仍然需要额外的模型训练，而且这个训练成本不能完全忽视。**
* **MeZO** 为 LLM 引入了一种内存高效的零阶 (zeroth-order, ZO) 优化器。传统的 PEFT 技术依靠反向传播来计算梯度来更新模型参数，而 MeZO 与此不同，MeZO 仅通过前向传递来微调 LLM。它通过使用 ZO 梯度估计器来计算梯度来实现这一点。值得注意的是，MeZO 为经典 ZO 梯度估计器实现了 in-place 解决方案，有效减轻了内存占用推理执行期间的消耗。这种创新方法允许在具有 80GB 内存的单个 GPU 上对包含 300 亿个参数的 LLM 进行高效微调，同时保持与使用反向传播进行微调相当的性能。此外，与 LoRA 和 Adapter 等传统 PEFT 方法相比，它可以大大减少存储需求。

## 应用 PEFT 到不同模型架构

主要包括 LLM、Vision Transformer、VLM、扩散模型，以适用于各种下游任务，强调 PEFT 在各种场景中的多功能性和适用性。

### 针对 LLM 的应用

#### Visual Instruct Following

* **VL-Adapter** 直接应用了几种 PEFT 方法（Adapter、Hyperformer 和 Compacter），在 VL-BART 基准上几个图像文本和视频文本任务上对它们进行测试。结果表明，简单的适配器最好，它可以实现与完全微调相当的性能。然而，考虑到 VL-BART 中编码器和解码器之间的功能差异，直接分配相同的模块修改将导致性能不佳。
* **VL-PET**选择性地将 PEFT 模块集成到编码器和解码器的不同组件中。还引入了粒度控制机制以实现更细粒度的控制。
* **LLaMA-Adapter** 在 LLaMA 更高的 Transformer 层中的输入标记前添加一组可学习的提示（类似于 prefix tuning）。为了避免在早期训练阶段出现较大损失值的不稳定微调，LLaMA-Adapter 采用零初始化注意力机制，而不是其他 PEFT 方法的随机初始化权重，该机制学习零初始化的门控因子来自适应地调整权重，控制提示对单词标记的贡献。这可以保持微调起点与原始模型相同，并逐步向模型注入新的知识，类似的想法可以在前面讨论的 MEFT 和 LoftQ 中找到。为了表示视觉信息，LLaMA-Adapter 使用 CLIP 图像编码器提取多尺度全局图像特征，然后将它们投影到语言嵌入空间。之后，该功能会按元素添加到所有插入的 Transformer 层的 adaptation prompt 中。仅在 LLaMA-7B 中引入了 120 万个可学习参数，在 8 个 A100GPU 上进行微调的成本不到一小时。
* **LLaMA-Adapter V2** 表明 LLaMA-Adapter 中的简单多模态融合不能推广到更具挑战性的开放式多模态推理任务，其中**视觉提示往往比语言指令数据更能主导 adaptation prompt**。为了解决这个问题，LLaMA-Adapter V2 将指令遵循（instruction-following）能力的学习（以生成长语言响应）和视觉语言对齐解耦，以避免视觉和语言微调之间的干扰。具体来说，LLaMA-AdapterV2 设置了不相交的参数组，这些参数组分别从图像文本对和语言指令数据中学习。视觉适应提示是在 LLM 的早期阶段插入的，而语言适应提示则保留在与 LLaMA-Adapter 类似的更高 Transformer 层。此外，LLaMA-Adapter V2 引入了更多可学习参数和多个专家系统（例如生成描述、检测和 OCR）来增强多模式性能。

#### Continual Learning (CL)

CL 的目标是在一个模型中随着时间的推移学习一系列新任务，该模型在对话系统、信息提取系统和问答系统等场景中具有广泛应用。CL 的主要挑战是灾难性遗忘。

一种流行的做法，称为基于架构的方法，通过维护特定于任务的参数来解决 CL 模型中每个新任务的输入。因此，很自然地利用 PEFT 方法来执行 CL 任务。

* **AdapterCL** 使用 residual adapter 参数化每个新任务。在测试过程中，由于未提供任务 ID，AdapterCL 使用基于熵的分类器来选择使用哪个适配器来完成特定任务。
* **CPT (Continual Prompt Tuning)** 为每个任务训练软提示。CPT 没有从头开始训练软提示，而是提出了一系列技术（continual prompt initialization, query fusion, memory replay, a memory-guided technique）来实现前后任务的知识迁移。
* **O-LoRA (orthogonal lowrank adaptation)** 采用一种在单独的低秩向量子空间内学习不同任务的策略，这些子空间保持彼此正交，以最大限度地减少干扰。这种方法可以有效减少习得新任务过程中的灾难性遗忘。

#### Context Window Extension

LLM 通常使用预定义的上下文大小进行训练。如 LLaMA 和 LLaMA2 的预定义上下文大小分别为 2048 和 4096 个 token。位置编码 RoPE 具有较弱的外推属性，这意味着在输入长度超过预定义上下文长度的情况下，性能明显下降。为了解决这个问题，一个简单的解决方案是将预训练的 LLM 微调到更长的上下文。然而，这会导致计算成本随上下文大小呈二次方上升，从而导致内存和处理资源紧张。

为了解决这个问题：

* **LongLoRA** 建议使用 LoRA 微调预训练的 LLM 以扩大上下文大小。为了减少 LoRA 调优和完全微调之间的困惑度差距，LongLoRA 还**放开了嵌入层和归一化层进行训练**。为了进一步提高长上下文场景下的训练效率，LongLoRA 进一步引入了一种新颖的转移稀疏注意力（S2-Attn）作为训练期间标准自注意力的有效替代品。
* **LongQLoRA** 将 LongLoRA 与 QLoRA 和 Position Interpolation【Extending Context Window of Large Language Models via Positional Interpolation】的优点结合起来，以节省 GPU 内存。这项工作成功地将 LLaMA2-13B 在具有 32GB 内存的单个 V100 上的上下文长度从 4096 扩展到 8192。

除了有限的训练阶段序列长度之外，现实世界的系统内存限制还给上下文窗口带来了另一个关键瓶颈。具体来说，KV 缓存的容量受到可用系统内存的限制。例如，以输入长度 1024 和批量大小 128 运行的 30B 参数 LLM 可能需要高达 180GB 的 KV 缓存【H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models】，从而限制了上下文窗口的可行大小。针对这一点，一些策略诉诸于量化 KV 缓存，但量化肯定会损害性能。为了在不造成重大损失的情况下有效地解决这个问题，最近一些工作展开了探索：

* **GEAR**提出了一种新颖的方法，通过采用低秩矩阵来捕获量化误差的大部分相干基，并辅以稀疏矩阵来解决异常条目（outlier entry）的误差，从而有效地最小化近似误差。

### 针对 Vision Transformer（ViT）的应用

#### 图像分类

视觉数据集上的图像分类是一种非常常见的需求，并且具有广泛的应用，而预训练然后微调范式是一种广泛的策略。多种方法利用 PEFT 技术来实现高效的模型调整。

* **AdaptFormer** 将适配器模块与原始 ViT 模型的 FFN 并行插入，以执行视觉识别任务。
* **VPT (Visual Prompt Tuning)** 将少量特定于任务的参数添加到每个 Transformer 层的输入序列中。当将 ViT 应用于下游任务时，只有这些添加的参数和分类头被设置为可训练。
* **GatedPromptTuning**【Improving Visual Prompt Tuning for Self-supervised Vision Transformers】注意到，与有监督的 ViT 相比，VPT 在自监督 ViT 中的表现通常较差。进一步的分析表明，不同的预训练方法和下游任务对不同位置的变压器块有不同程度的依赖。为了解决这个问题，研究引入了 ViT 块的自适应门控。这些门动态地调节提示 token 对 ViT 块的贡献，从而使模型更有针对性地适应手头的任务。

#### 视频识别

一些工作考虑了更具挑战性的适应问题，将 ViT 转移到具有更大域隔阂的下游任务。

* **ST-Adapter (Spatio-Temporal Adapter)** 和 **AIM**都将适配器层插入到预训练的 ViT 块中。主要目标是对时空信息进行建模，从而实现从图像模型到视频任务的 ViT 的高效适应。值得注意的是，这两种方法都表现出了超越传统全模型微调方法的性能。

### 针对 Vision-Language Alignment 模型（VLA）的应用

VLA 如 CLIP、ALIGN、DeCLIP 和 FLAVA，旨在学习可以在统一表示中对齐的良好图像和文本特征空间。每个 VLA 通常由提取各自特征的单独图像和文本编码器组成。这些模型利用对比学习来有效地对齐图像和文本特征。利用微调来提高 VLA 在特定数据集或任务上的性能。

* 但微调整个模型需要大量计算。例如，微调 CLIP-RN50x64 需要 32,768 的批大小以及在 592 V100 GPU 上进行 18 天的训练【Learning Transferable Visual Models From Natural Language Supervision】。
* 此外，对较小数据集的全面微调通常会导致灾难性的遗忘。

为了应对这些挑战，并从 PEFT 技术在 NLP 中的成功中汲取灵感，一系列 PEFT 策略被提出并在 VLA 模型中实现，例如语义分割、点云理解、视频理解、视觉推理、时间动作检测等。本节将重点介绍一项使用 VLA 的常见任务：开放词汇图像分类。

#### 开放词汇图像分类

早期工作为每个类别设计特定于类别的提示，例如 `a photo of a [CLASS]`，并根据图像与这些文本描述的相似度对图像进行排序。

* **CoOp (Context Optimization)** 用可学习的向量替换手工制作的文本提示，同时在训练期间保留整个 VLA 固定。
* **CoCoOp (Conditional Context Optimization)** 在此基础上解决了 CoOp 在泛化到未见过的类方面的局限性。它引入了一个轻量级神经网络，可以生成特定于输入的上下文标记，根据每个图像动态调整提示，从而增强通用性，但代价是由于实例感知操作而增加了计算需求。
* **ProGrad** 通过正则化梯度与一般知识对齐的 soft prompt 的更新，仅更新梯度与所提供的一般知识对齐（或不冲突）的提示按原来的提示。
* **MaPLe** 指出，现有方法要么在 CLIP 的语言中要么在视觉分支中学习提示，这不能有效地利用 VLA 的多模态性质。为了解决这个问题，MaPLe 提出了分支感知分层提示，可以同时调整语言和视觉分支，并实现卓越的性能。
* **TPT (test-time prompt tuning)** 研究动态提示调整，无需额外训练样本。具体来说，在推理过程中，TPT 首先将输入图像增强到各种视图中，然后利用这些视图来调整可学习的提示。主要训练目标是确保 VLA 在面对这些不同观点时能够做出一致的反应。
* **DiffTPT** 通过扩散模型进一步增强了测试样本的数据多样性。

另一方面，一些研究探索了 VLA 中 adapter 的使用。

* **CLIP-Adapter** 在 CLIP 文本和视觉编码器之后集成了残差式适配器。因此，与 CoOp 和 CoCoOp 不同，CLIP-Adapter 避免了通过 CLIP 编码器进行梯度反向传播，从而减少了训练内存和时间方面的计算要求。
* **Tip-Adapter** 采用与 CLIP-Adapter 相同的设计。与 CLIP-Adapter 不同，adapter 权重是从以非参数方式从少样本监督构建的 query-key cache 模型中以免训练的方式获得的。结果，Tip-Adapter 相较于 CLIP-Adapter 的 SGD 训练过程表现出了更高的效率。

### 针对扩散模型的应用

这是一类生成模型，通过渐进式去噪过程将随机噪声转换为结构化输出来学习生成数据。在训练过程中，扩散模型学习使用去噪网络反转添加到训练数据中的噪声，而在推理过程中，它们从噪声开始，使用去噪网络迭代创建反映与训练示例相同分布的数据。扩散模型各种应用中最值得注意的是 stable diffusion，它以其强大的生成能力弥合了文本和图像之间的差距。直接从文本描述中获得连贯且上下文相关的图像。许多研究利用 PEFT 技术来适应下游任务的预训练扩散模型，包括加快采样速度、文本到视频的适应、文本到 3D 适应等。这里主要关注两种场景：集成超出单纯基于文本的条件的附加输入模式，以及基于预训练扩散模型的定制化内容生成。

#### Additional Input Control

* **GLIGEN** 为了合并附加输入模式（例如布局、关键点），同时保留预训练模型中的广泛知识，引入了一种新颖方法，保持原始模型权重的完整，并集成新的、可训练的接受新的 grounding 输入门控 Transformer 层【Flamingo: a Visual Language Model for Few-Shot Learning】。所得模型不仅可以准确地表示 grounding 条件，而且可以生成高质量的图像。值得注意的是，该模型还可以在推理过程中很好地推广到未见过的对象。
* **ControlNet** 微调来自 stabel diffusion 的编码层的可训练副本，同时锁定其预训练的参数权重。固定的原始模型和可训练的副本通过零卷积层桥接。这些层从零初始化权重开始，旨在在训练过程中逐步适配，确保有害噪声不会影响训练开始时稳定扩散的预训练特征。这个细化的模型能够使用各种输入作为条件，例如 Canny edges, Hough lines, user scribbles, human key points, segmentation maps, shape normals, depths 等。
* **Concept Sliders** 引入了一种即插即用的 LoRA 适配器来在扩散模型中精确编辑概念（例如年龄、微笑）。
* **T2I-Adapter** 引入了一种轻量级适配器模型来对齐外部控制信号与文本到图像扩散模型的内部知识。该适配器可以通过 structural control (e.g., sketch, depth map, semantic segmentation map, and keypose), color control (e.g., hue and color distribution) 以及通过组合多个适配器来集成各种控制来，从而实现精确操作。

#### Customized Generation

**文本到图像扩散模型的有效性受到用户通过文本阐明所需目标的能力的限制。**
例如，很难描述一个大规模模型训练中不会遇到的创新玩具车的精确特征。因此，定制生成的目标是使模型能够从用户提供的最小图像集中掌握新概念。

* **Textual Inversion** 通过找到一个新的伪词（类似于 soft prompt）来解决这个问题，该伪词代表预训练文本到图像扩散的文本嵌入空间中的新的特定概念。伪词通过扩散模型中的原始优化目标进行优化，给定描述概念的小图像集（通常为 3-5 个图像），并且预训练模型保持不变（untouched）。在推理过程中，该伪词可以像任何其他单词一样对待，并与其他文本查询组成（例如，"<伪词>在海滩上的照片 "）。
* **Custom Diffusion** 解决了更具挑战性的设置：多个概念的组合微调。它仅微调从文本到注意层中的 K 和 Q 的映射权重，这在多概念学习场景中产生了卓越的性能。此外，在微调过程中，自定义扩散通过引入一小组带有与目标类似描述的真实图像来防止模型遗忘，同时采用增强来加快收敛速度并改进结果。
* **IP-Adapter** 确定了当前方法（例如 ControlNet 和 T2I-Adapter）的局限性，**这些方法将条件信号投射到交叉注意模块中。当处理旨在控制内容的图像条件时，这些方法无法生成忠实于提示图像的图像。该问题源于在交叉注意层中合并图像特征和文本特征会丢失图像特定信息，导致仅产生粗粒度的可控生成，例如图像风格而不是图像内容。** 为了克服这个问题，IP-Adapter 引入了一种新颖的解耦交叉注意力机制来区分文本和图像特征。IP-Adapter 在每个交叉注意层中添加了专门针对图像特征的额外交叉注意层，并且仅训练新交叉注意层的参数。

## PEFT 方法的系统设计挑战

这里主要涉及到系统设计，偏工程化的内容。所以简短摘录一下。

这里提出了三种预期的使用 ：

![image.png](https://cdn.nlark.com/yuque/0/2024/png/192314/1712046704514-aff4a752-7213-45e9-a4f0-75a0534c80aa.png#averageHue=%23f2f1f0&clientId=u1ee96119-af40-4&from=paste&height=263&id=ue21611a6&originHeight=329&originWidth=719&originalType=binary&ratio=1.25&rotation=0&showTitle=false&size=47555&status=done&style=none&taskId=uec58450f-1a44-40f8-8cfe-eb1c449c9db&title=&width=575.2)

* **Centralized PEFT Query Serving**：云提供商通过 API 提供用户应用程序，从而有助于将许多 ML 功能无缝集成到应用程序中。通过 API 收到针对一项特定下游任务的 query 后，云服务器会使用特化的 LLM 模型处理。此时提出的用于处理多个 PEFT 查询的云解决方案涉及仅存储 LLM 的单个副本和多个 PEFT 模块。该单个副本维护 PEFT 模块的多个分支，每个分支与不同的 PEFT 查询相关联。图 10b 中说明了多 query 的 PEFT 推理计算模式。此时需要关注与四个性能指标：System throughput、Run-time memory footprint during query serving, the memory utilization comes from both model parameters and KV-cache、Accuracy performance with variation context length、Quality of services associated with latency requirements and deadline missing rates。
* **Distributed System for PEFT**：当代的 LLM 预训练模型并不完全支持个性化任务，因此需要使用前面提到的方法进行额外微调。然而，当考虑将私人数据集提供给云提供商时，会出现一个很大的问题，因为这些数据集是个性化的。出于这个考虑，可以假设计算遵循模型集中式和 PEFT 分布式范式，即主干 LLM 存储在云设备中，而个人 PEFT 权重以及数据集存储在用户自己的设备中。如图 10(a) 所示。性能评估主要关注与三个指标：Accuracy performance over the downstream tasks、Compute cost on edge devices、Communication cost between the edge device and the cloud.
* **Multi-PEFT Training**：与多 PEFT 服务不同，多个定制 PEFT 的调整总是涉及不同的骨干 LLM。当考虑 LLM 在各种下游任务中使用时，预训练模型通常表现出低于标准的性能。使 LLM 适应不同任务的一种流行方法是精心微调 PEFT。然而，同时调整多个 PEFT 可能会带来相当大的挑战。如何管理内存梯度和模型权重存储，以及如何设计用于批处理 PEFT 训练的高效内核等挑战仍未解决。PEFT 将根据其 PEFT 算法和骨干 LLM 模型进行分类。**设计挑战涉及如何同时整合具有相同 LLM 主干和多个不同 LLM 主干的多个 PEFT。**

## 总结

在当前以大型模型和大型数据集为主导的时代，PEFT 作为一种非常有吸引力的方法脱颖而出，可以有效地使模型适应下游任务。该技术通过解决传统全模型微调带来的重大挑战而获得吸引力，传统全模型微调通常对普通用户提出难以满足的计算和数据需求。对于 LEFT 的进一步研究，这里从算法和系统的角度提出了一系列可能的方向，希望能够启发更多的研究人员在这些领域进行进一步的研究：

1. 简化超参数调整：**PEFT 的有效性通常对其超参数敏感**，例如适配器瓶颈尺寸、LoRA 秩以及不同附加性 PEFT 层的放置。手动调整这些超参数将花费大量精力。因此，未来的努力可以集中在开发更少依赖手动调整这些参数的方法，或者自动找到最佳的超参数设置。多项研究已经开始解决这个问题，但需要更简单、更有效的解决方案来优化这些超参数。
2. 建立统一的基准：尽管存在像 HuggingFace 的 PEFT 和 AdapterHub 这样的库，但仍然缺乏全面的 PEFT 基准。这种差距阻碍了公平比较不同 PEFT 方法的性能和效率的能力。类似于 MMDetection 的广泛接受的最新目标检测基准将使研究人员能够根据任务和指标的标准集来验证他们的方法，促进社区内的创新和协作。
3. 提升训练效率：**PEFT 的假定参数效率并不总是与训练期间的计算和内存节省一致。**鉴于可训练参数在预训练模型架构中交织在一起，因此在微调期间通常需要计算和存储完整模型的梯度。这种疏忽要求重新思考什么构成了效率。潜在的解决方案在于集成模型压缩技术，例如修剪和量化，以及专门设计用于在 PEFT 调整期间优化内存的创新。进一步提高 PEFT 方法的计算效率的研究势在必行。
4. 探索缩放定律：**最初为较小的 Transformer 模型开发的 PEFT 方法的设计和有效性不一定适用于较大的模型。** 随着基础模型规模的增加，识别和调整保持有效的 PEFT 策略至关重要。这一探索将有助于根据大型模型结构的发展前景（evolving landscape）定制（tailor）PEFT 方法。
5. 服务更多模型和任务：跨领域大型基础模型的兴起为 PEFT 带来了新的机遇。**根据模型的独特特征设计定制的 PEFT 方法，例如 Sora、Mamba 和 LVM，可以解锁新的应用场景和机会。**
6. 加强数据隐私：**信任中心化系统来服务或微调个性化 PEFT 模块是系统开发人员面临的另一个问题。** 信道侧攻击者已成功部署通过劫持中间结果来重建用户数据。未来值得信赖的 LLM 系统设计的一个视角涉及为个人数据以及中间训练和推理结果开发加密协议。
7. 带模型压缩的 PEFT：模型压缩是使 LLM 在资源有限的设备上可执行的最有效方法之一。然而，**模型压缩技术对硬件上运行的 PEFT 算法性能的影响仍然是另一个系统性挑战。** 量化和剪枝等常见的压缩技术需要专用的硬件平台来加快这一过程，而为压缩模型构建这样的硬件平台是研究人员的另一个方向。
