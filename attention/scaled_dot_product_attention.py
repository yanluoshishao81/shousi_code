from math import sqrt
import torch
import torch.nn.functional as F
def scaled_dot_product_attention(query,key,value,query_mask=None,key_mask=None,mask=None):
    dim_k=query.size(-1)
    scores=torch.bmm(query,key.transpose(1,2))/sqrt(dim_k)

    # 1. 先处理通用的、已经计算好的 mask (通常是因果掩码或外部传入的复杂掩码)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -float("inf"))

    # 2. 如果没有传入通用 mask，才尝试用 query_mask 和 key_mask 组合
    # 这里增加了对单个 mask 的支持
    elif query_mask is not None or key_mask is not None:

        # 如果只传了 query_mask，用它去屏蔽 scores 的行
        if query_mask is not None and key_mask is None:
            # query_mask: (B, Lq) -> 调整形状: (B, Lq, 1)
            q_mask = query_mask.unsqueeze(-1)
            scores = scores.masked_fill(q_mask == 0, -float("inf"))
            # 这里用的是 *运算* 而不是 bmm，因为只需要屏蔽行
            # 但更常见的做法是生成一个全1的 key_mask，或者直接用 masked_fill
            # 实际上，单独的 query_mask 很少见，通常是通过 mask 参数处理

        # 如果只传了 key_mask，用它去屏蔽 scores 的列 (这是最常见的 Padding Mask)
        elif key_mask is not None and query_mask is None:
            # key_mask: (B, Lk) -> 调整形状: (B, 1, Lk)
            k_mask = key_mask.unsqueeze(1)
            # 这里直接用 masked_fill
            scores = scores.masked_fill(k_mask == 0, -float("inf"))

        # 如果两个都传了，就用你原来的 bmm 方式 (生成二维矩阵)
        else:
            combined_mask = torch.bmm(query_mask.unsqueeze(-1), key_mask.unsqueeze(1))
            scores = scores.masked_fill(combined_mask == 0, -float("inf"))

    weights=F.softmax(scores,dim=-1)
    return torch.bmm(weights,value)


if __name__ == "__main__":
    # 模拟输入：batch_size=2，query/key序列长度=3，value序列长度=3，维度dk=4，dv=5
    batch_size = 2
    seq_len = 3
    dim_k = 4
    dim_v = 5

    query = torch.randn(batch_size, seq_len, dim_k)  # [2, 3, 4]
    key = torch.randn(batch_size, seq_len, dim_k)  # [2, 3, 4]
    value = torch.randn(batch_size, seq_len, dim_v)  # [2, 3, 5]

    # 模拟掩码：第一个样本保留前2个位置，第二个样本保留全部
    query_mask = torch.tensor([[1, 1, 0], [1, 1, 1]])  # [2, 3]
    key_mask = torch.tensor([[1, 1, 0], [1, 1, 1]])  # [2, 3]

    # 执行注意力计算
    output = scaled_dot_product_attention(query, key, value, query_mask, key_mask)
    print("输出形状:", output.shape)  # 输出：torch.Size([2, 3, 5])
