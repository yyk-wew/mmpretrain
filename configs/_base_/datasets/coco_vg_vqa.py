# data settings
data_preprocessor = dict(
    type='MultiModalDataPreprocessor',
    mean=[122.770938, 116.7460125, 104.09373615],
    std=[68.5005327, 66.6321579, 70.32316305],
    to_rgb=True,
)

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='RandomResizedCrop',
        scale=(480, 480),
        crop_ratio_range=(0.5, 1.0),
        interpolation='bicubic',
        backend='pillow'),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(
        type='RandAugment',
        policies='simple_increasing',  # slightly different from LAVIS
        num_policies=2,
        magnitude_level=5),
    dict(type='CleanCaption', keys=['question', 'gt_answer']),
    dict(
        type='PackInputs',
        algorithm_keys=[
            'question', 'gt_answer', 'gt_answer_weight', 'dataset'
        ]),
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='Resize',
        scale=(480, 480),
        interpolation='bicubic',
        backend='pillow'),
    dict(type='CleanCaption', keys=['question', 'gt_answer']),
    dict(
        type='PackInputs',
        algorithm_keys=[
            'question', 'gt_answer', 'gt_answer_weight', 'dataset'
        ]),
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='Resize',
        scale=(480, 480),
        interpolation='bicubic',
        backend='pillow'),
    dict(type='CleanCaption', keys=['question']),
    dict(
        type='PackInputs',
        algorithm_keys=['question'],
        meta_keys=['question_id']),
]

train_dataloader = dict(
    batch_size=32,
    num_workers=8,
    dataset=dict(
        type='ConcatDataset',
        datasets=[
            dict(
                type='COCOVQA',
                data_root='data/coco',
                ann_file='annotations/vqa_train.json',
                pipeline=train_pipeline),
            dict(
                type='COCOVQA',
                data_root='data/coco',
                ann_file='annotations/vqa_val.json',
                pipeline=train_pipeline),
            dict(
                type='COCOVQA',
                data_root='data/coco',
                ann_file='annotations/vg_qa.json',
                pipeline=train_pipeline),
        ]),
    sampler=dict(type='DefaultSampler', shuffle=True),
    persistent_workers=True,
    drop_last=True,
)

val_dataloader = dict(
    batch_size=32,
    num_workers=8,
    dataset=dict(
        type='COCOVQA',
        data_root='data/coco',
        ann_file='annotations/vqa_val.json',
        pipeline=val_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=False),
    persistent_workers=True,
)

test_dataloader = dict(
    batch_size=32,
    num_workers=8,
    dataset=dict(
        type='COCOVQA',
        data_root='data/coco',
        ann_file='annotations/vqa_test.json',
        pipeline=test_pipeline),
    sampler=dict(type='DefaultSampler', shuffle=False),
    persistent_workers=True,
)

val_evaluator = dict(type='VQAAcc')