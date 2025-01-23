## eval.json
处理后符合标准格式并完成筛错的数据

## test.json
用于测试 evaluation&metrics 的数据

## evaluation.py
主程序

## metrics.py
评分工具

## eval_standard_Verx.0 
未合并未筛错的数据

## wrong_list.json
`eval_standard_Verx.0`中有问题的文件的列表

# TODO

> For Multi-Turn Scenarios (M-S & M-M). In multi-turn dialogues, the following metrics are intro- duced: (1) Success Rate (SR): A binary metric where the entire dialogue is considered successful for tool-use: (=1) only if there are no errors throughout all turns; otherwise, it is considered unsuccessful (=0). (2) Averaged Turn Success Rate (ATS): We first evaluate each dialogue turn with the tool-use success rate (where each turn is marked as either 0 or 1), then average the binary scores with the total dialogue turns of a dialogue session. This score takes into account the finer-grained success rate of tool-use at the turn level. (3) Soft Averaged Turn Success Rate (SATS): This metric adjusts the ATS based on the proximity of errors to the current turn. Specifically: If a turn is incorrect, the score is 0. If a turn is correct, given j as the index of this turn and i as the index of the last incorrect turn,
the score is 1 when j < i and 1 − e−(j−i) when j > i. This design is based on the intuition that a
closer incorrect turn can negatively impact subsequent turns. Moreover, the closer the turn becomes incorrect, the lower the overall accumulated score, even if the remaining turns are correct. (4) Task Process Rate (TPR): This is calculated as the ratio of the first incorrect turn to the total number of turns. This metric is included to capture how early in the dialogue the first mistake occurs, as earlier errors tend to disrupt the overall task flow more significantly.

> For Multi-Tool Scenarios (S-M & M-M). For scenarios involving multiple tools, the following metrics are introduced: (1) Tool Number Accuracy (TN): Denote the predicted tool list as “Pred”
and the ground truth tool list as “GT”, TN =| Pred ∩ GT | / | Pred ∪ GT |, where || denotes the number of tools. (2) Tool Order Accuracy (TO): This metric evaluates the correctness of the tool sequence, adjusted by a decay factor: TO = t× | LCR(GT, Pred) | / | GT |, where LCR is the
longest common subsequence, and t is a decay coefficient calculated as: t = cos((π/2) × (i/|Pred|), where i is the starting position of the longest common subsequence. The value of t ranges from 0 to 1, with a faster decay for positions later in the sequence.