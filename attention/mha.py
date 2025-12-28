import torch
import torch.nn as nn
import torch.nn.functional as F


class MultiHeadAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super(MultiHeadAttention, self).__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads  # 每个头的维度

        # 为 Q, K, V 定义线性变换
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)

        # 最终输出投影
        self.out_proj = nn.Linear(embed_dim, embed_dim)

    def forward(self, x, mask=None):
        B, S, E = x.shape  # B: batch_size, S: seq_len, E: embed_dim

        # [B, S, E] -> [B, S, num_heads, head_dim] -> [B, num_heads, S, head_dim]
        Q = self.q_proj(x).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_proj(x).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_proj(x).view(B, S, self.num_heads, self.head_dim).transpose(1, 2)
        # 现在 Q, K, V 形状都是 [B, num_heads, S, head_dim]

        # 计算缩放点积注意力
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.head_dim ** 0.5)
        # 归一化为注意力权重 [B, num_heads, S, S]
        attn_weights = F.softmax(attn_scores, dim=-1)
        # 加权求和 V -> [B, num_heads, S, head_dim]
        attn_output = torch.matmul(attn_weights, V)

        # 多头合并: [B, num_heads, S, head_dim] -> [B, S, E]
        attn_output = attn_output.transpose(1, 2).contiguous().view(B, S, E)

        # 最终线性映射
        out = self.out_proj(attn_output)  # [B, S, E]
        return out


mha = MultiHeadAttention(embed_dim=64, num_heads=8)
x = torch.randn(2, 10, 64)  # B=2, S=10, E=64
out = mha(x)
print(out.shape)  # 应该输出 [2, 10, 64]