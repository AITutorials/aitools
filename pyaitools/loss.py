import torch
import torch.nn as nn

class LabelSmoothingCELoss(nn.Module):
    def __init__(self, classes, smoothing=0.0, dim=-1):
        super(LabelSmoothingCELoss, self).__init__()
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.cls = classes
        self.dim = dim

    def forward(self, pred, target):
        pred = pred.log_softmax(dim=self.dim)
        with torch.no_grad():
            true_dist = pred.data.clone()
            true_dist = torch.zeros_like(pred)
            true_dist.fill_(self.smoothing / (self.cls - 1))
            # .scatter_也是一种数据填充方法，目的仍然是将self.confidence填充到true_dist中
            # 第一个参数0/1代表填充的轴，大多数情况下使用scatter_都使用纵轴（1）填充
            # 第二个参数就是self.confidence的填充规则，即填充到第几列里面，如[[1], [2]]代表填充到第二列和第三列里面
            # 第三个参数就是填充的数值，int/float
            true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        return torch.mean(torch.sum(-true_dist * pred, dim=self.dim))




if __name__ == "__main__":
    predict = torch.FloatTensor([[1, 1, 1, 1, 1]])
    target = torch.LongTensor([2])
    LSL = LabelSmoothingCELoss(3, 0.03)
    print(LSL(predict, target))
