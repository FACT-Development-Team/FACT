hyperparameters_Dense = {
    "name": "DENSE",
    "method": "bayes",
    "metric": {
        "name": "val_accuracy",
        "goal": "maximize",
    },
    "parameters": {
        "epochs": {
            "values": [10, 20, 40],
        },
        "batch_size": {
            "values": [32, 64, 128, 256],
        },
        "regularizer_l1": {
            "values": [0.01, 0.02, 0.005],
        },
        "regularizer_l2": {
            "values": [0.01, 0.02, 0.005],
        },
        "dense_depth_layout": {
            "values": [
                [16,16,16,16],
                [32,16,8,4],
                [64,32,16,8,4],
            ],
        },
    }
}