import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Parameter


class Res2Conv1dReluBn(nn.Module):
    def __init__(self, channels, kernel_size=1, stride=1, padding=0, dilation=1, bias=False, scale=4):
        super().__init__()
        assert channels % scale == 0, "{} % {} != 0".format(channels, scale)
        self.scale = scale
        self.width = channels // scale
        self.nums = scale if scale == 1 else scale - 1

        self.convs = []
        self.bns = []
        for i in range(self.nums):
            self.convs.append(nn.Conv1d(self.width, self.width, kernel_size, stride, padding, dilation, bias=bias))
            self.bns.append(nn.BatchNorm1d(self.width))
        self.convs = nn.ModuleList(self.convs)
        self.bns = nn.ModuleList(self.bns)

    def forward(self, x):
        out = []
        spx = torch.split(x, self.width, 1)
        for i in range(self.nums):
            if i == 0:
                sp = spx[i]
            else:
                sp = sp + spx[i]
            # Order: conv -> relu -> bn
            sp = self.convs[i](sp)
            sp = self.bns[i](F.relu(sp))
            out.append(sp)
        if self.scale != 1:
            out.append(spx[self.nums])
        out = torch.cat(out, dim=1)
        return out


class Conv1dReluBn(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1, padding=0, dilation=1, bias=False):
        super().__init__()
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding, dilation, bias=bias)
        self.bn = nn.BatchNorm1d(out_channels)

    def forward(self, x):
        return self.bn(F.relu(self.conv(x)))


class SE_Connect(nn.Module):
    def __init__(self, channels, s=2):
        super().__init__()
        assert channels % s == 0, "{} % {} != 0".format(channels, s)
        self.linear1 = nn.Linear(channels, channels // s)
        self.linear2 = nn.Linear(channels // s, channels)

    def forward(self, x):
        out = x.mean(dim=2)
        out = F.relu(self.linear1(out))
        out = torch.sigmoid(self.linear2(out))
        out = x * out.unsqueeze(2)
        return out


def SE_Res2Block(channels, kernel_size, stride, padding, dilation, scale):
    return nn.Sequential(
        Conv1dReluBn(channels, channels, kernel_size=1, stride=1, padding=0),
        Res2Conv1dReluBn(channels, kernel_size, stride, padding, dilation, scale=scale),
        Conv1dReluBn(channels, channels, kernel_size=1, stride=1, padding=0),
        SE_Connect(channels)
    )


class AttentiveStatsPool(nn.Module):
    def __init__(self, in_dim, bottleneck_dim):
        super().__init__()
        # Use Conv1d with stride == 1 rather than Linear, then we don't need to transpose inputs.
        self.linear1 = nn.Conv1d(in_dim, bottleneck_dim, kernel_size=1)  # equals W and b in the paper
        self.linear2 = nn.Conv1d(bottleneck_dim, in_dim, kernel_size=1)  # equals V and k in the paper

    def forward(self, x):
        # DON'T use ReLU here! In experiments, I find ReLU hard to converge.
        alpha = torch.tanh(self.linear1(x))
        alpha = torch.softmax(self.linear2(alpha), dim=2)
        mean = torch.sum(alpha * x, dim=2)
        residuals = torch.sum(alpha * x ** 2, dim=2) - mean ** 2
        std = torch.sqrt(residuals.clamp(min=1e-9))
        return torch.cat([mean, std], dim=1)


class EcapaTdnn(nn.Module):
    def __init__(self, input_size=80, channels=512, embd_dim=192):
        super().__init__()
        self.layer1 = Conv1dReluBn(input_size, channels, kernel_size=5, padding=2, dilation=1)
        self.layer2 = SE_Res2Block(channels, kernel_size=3, stride=1, padding=2, dilation=2, scale=8)
        self.layer3 = SE_Res2Block(channels, kernel_size=3, stride=1, padding=3, dilation=3, scale=8)
        self.layer4 = SE_Res2Block(channels, kernel_size=3, stride=1, padding=4, dilation=4, scale=8)

        cat_channels = channels * 3
        out_channels = cat_channels * 2
        self.emb_size = embd_dim
        self.conv = nn.Conv1d(cat_channels, cat_channels, kernel_size=1)
        self.pooling = AttentiveStatsPool(cat_channels, 128)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.linear = nn.Linear(out_channels, embd_dim)
        self.bn2 = nn.BatchNorm1d(embd_dim)

    def forward(self, x):
        out1 = self.layer1(x)
        out2 = self.layer2(out1) + out1
        out3 = self.layer3(out1 + out2) + out1 + out2
        out4 = self.layer4(out1 + out2 + out3) + out1 + out2 + out3

        out = torch.cat([out2, out3, out4], dim=1)
        out = F.relu(self.conv(out))
        out = self.bn1(self.pooling(out))
        out = self.bn2(self.linear(out))
        return out


class SpeakerIdetification(nn.Module):
    def __init__(
            self,
            backbone,
            num_class=1,
            lin_blocks=0,
            lin_neurons=192,
            dropout=0.1, ):
        """The speaker identification model, which includes the speaker backbone network
           and the a linear transform to speaker class num in training

        Args:
            backbone (Paddle.nn.Layer class): the speaker identification backbone network model
            num_class (_type_): the speaker class num in the training dataset
            lin_blocks (int, optional): the linear layer transform between the embedding and the final linear layer. Defaults to 0.
            lin_neurons (int, optional): the output dimension of final linear layer. Defaults to 192.
            dropout (float, optional): the dropout factor on the embedding. Defaults to 0.1.
        """
        super(SpeakerIdetification, self).__init__()
        # speaker idenfication backbone network model
        # the output of the backbond network is the target embedding
        self.backbone = backbone
        if dropout > 0:
            self.dropout = nn.Dropout(dropout)
        else:
            self.dropout = None

        # construct the speaker classifer
        input_size = self.backbone.emb_size
        self.blocks = list()
        for i in range(lin_blocks):
            self.blocks.extend([
                nn.BatchNorm1d(input_size),
                nn.Linear(in_features=input_size, out_features=lin_neurons),
            ])
            input_size = lin_neurons

        # the final layer
        self.weight = Parameter(torch.FloatTensor(num_class, input_size), requires_grad=True)
        nn.init.xavier_normal_(self.weight, gain=1)

    def forward(self, x):
        """Do the speaker identification model forwrd,
           including the speaker embedding model and the classifier model network

        Args:
            x (paddle.Tensor): input audio feats,
                               shape=[batch, dimension, times]
            lengths (paddle.Tensor, optional): input audio length.
                                        shape=[batch, times]
                                        Defaults to None.

        Returns:
            paddle.Tensor: return the logits of the feats
        """
        # x.shape: (N, C, L)
        x = self.backbone(x)  # (N, emb_size)
        if self.dropout is not None:
            x = self.dropout(x)

        for fc in self.blocks:
            x = fc(x)

        logits = F.linear(F.normalize(x), F.normalize(self.weight, dim=-1))

        return logits
