# Experiment Results

| experiment                          | model            | loss       |   val_iou |   test_iou |   test_f1 |   precision |   recall |   epochs |   training_time_min |
|:------------------------------------|:-----------------|:-----------|----------:|-----------:|----------:|------------:|---------:|---------:|--------------------:|
| unet_resnet34_dice_seed_42          | unet_resnet34    | dice       |    0.8013 |     0.7923 |    0.8841 |      0.8908 |   0.8776 |       40 |              7.7691 |
| unet_resnet34_dice_focal_seed_42    | unet_resnet34    | dice_focal |    0.7958 |     0.7866 |    0.8805 |      0.8939 |   0.8676 |       30 |              5.7854 |
| unet_resnet34_focal_seed_42         | unet_resnet34    | focal      |    0.7887 |     0.7755 |    0.8736 |      0.8961 |   0.8522 |       40 |              7.7089 |
| unet_mit_b0_dice_focal_seed_42      | unet_mit_b0      | dice_focal |    0.7884 |     0.7792 |    0.8759 |      0.8819 |   0.8701 |       26 |              4.7599 |
| segformer_mit_b0_dice_focal_seed_42 | segformer_mit_b0 | dice_focal |    0.7856 |     0.7801 |    0.8765 |      0.8591 |   0.8946 |       40 |             13.4803 |
| unet_resnet34_bce_seed_42           | unet_resnet34    | bce        |    0.7832 |     0.7744 |    0.8729 |      0.8854 |   0.8607 |       30 |              5.8749 |