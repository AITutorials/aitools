import torch
import torch.nn as nn

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def _get_slices(token_type_ids):
    """由token_type_ids获取切片组"""
    slices_list = []
    for slices in token_type_ids:
        slices_ = list(map(lambda x: x.tolist(), slices))
        start_index = slices_.index(1)
        slices_.remove(0)
        end_index = start_index + len(slices_)
        slices_list.append([start_index, end_index])
    return slices_list


def _get_sentence_tensor(T):
    mT = nn.AvgPool2d((len(T), 1))
    return mT(T.unsqueeze(0))[0]


def get_output(sample, token_type_ids, weight=0.8):
    output = []
    slices = _get_slices(token_type_ids)
    for i, batch in enumerate(sample):
        A = batch[0 : slices[i][0]]
        B = batch[slices[i][0] : slices[i][1]]
        # 进行平均池化
        A = _get_sentence_tensor(A)
        B = _get_sentence_tensor(B)
        C = weight * B + (1 - weight) * A
        output.append(C.tolist())
    return torch.tensor(output).squeeze(1).to(device)


if __name__ == "__main__":
    sample = torch.rand(8, 70, 768)
    token_type_ids = torch.tensor([[0, 0, 0, 0, 0, 1, 1, 1, 1]] * 8)
    res = get_output(sample, token_type_ids, weight=0.8)
    print(res)
    print(res.shape)
