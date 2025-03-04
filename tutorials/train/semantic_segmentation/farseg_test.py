import sys

sys.path.append("E:/dataFiles/github/PaddleRS")

import paddlers as pdrs
from paddlers import transforms as T

# 下载和解压视盘分割数据集
optic_dataset = 'https://bj.bcebos.com/paddlex/datasets/optic_disc_seg.tar.gz'
pdrs.utils.download_and_decompress(optic_dataset, path='./')

# 定义训练和验证时的transforms
# API说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/apis/transforms/transforms.md
train_transforms = T.Compose([
    T.Resize(target_size=512),
    T.RandomHorizontalFlip(),
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

eval_transforms = T.Compose([
    T.Resize(target_size=512),
    T.Normalize(
        mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

# 定义训练和验证所用的数据集
# API说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/apis/datasets.md
train_dataset = pdrs.datasets.SegDataset(
    data_dir='optic_disc_seg',
    file_list='optic_disc_seg/train_list.txt',
    label_list='optic_disc_seg/labels.txt',
    transforms=train_transforms,
    num_workers=0,
    shuffle=True)

eval_dataset = pdrs.datasets.SegDataset(
    data_dir='optic_disc_seg',
    file_list='optic_disc_seg/val_list.txt',
    label_list='optic_disc_seg/labels.txt',
    transforms=eval_transforms,
    num_workers=0,
    shuffle=False)

# 初始化模型，并进行训练
# 可使用VisualDL查看训练指标，参考https://github.com/PaddlePaddle/paddlers/blob/develop/docs/visualdl.md
num_classes = len(train_dataset.labels)
model = pdrs.tasks.FarSeg(num_classes=num_classes)

# API说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/apis/models/semantic_segmentation.md
# 各参数介绍与调整说明：https://github.com/PaddlePaddle/paddlers/blob/develop/docs/parameters.md
model.train(
    num_epochs=10,
    train_dataset=train_dataset,
    train_batch_size=4,
    eval_dataset=eval_dataset,
    learning_rate=0.01,
    pretrain_weights=None,
    save_dir='output/farseg')
