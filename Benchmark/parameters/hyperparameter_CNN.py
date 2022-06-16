hyperparameters_CNN = {
    "name": "CNN_exponential",
    "method": "grid",
    "metric": {
        "name": "val_accuracy",
        "goal": "maximize",
    },
    "parameters": {
        "cnn_depth_layout": {
            "values": [ # (pooling_size, pooling_strides)
                [(2,2), (2,2)],
                [(2,2), (2,2), (2,2)],
            ],
        },
        "cnn_kernel_size": {
            "values": [2, 4, 6]
        },
        "cnn_filters": {
            "values": [1, 5, 10]
        },

    },
}