hyperparameters_RNN = {
    "name": "RNN",
    "method": "grid",
    "metric": {
        "name": "val_accuracy",
        "goal": "maximize",
    },
    "parameters": {
        "regularizer_l1": {
            "values": [0,0.001,0.0001],
        },
        "regularizer_l2": {
            "values": [0,0.001,0.0001],
        },
        "rnn_dropout": {
            "values": [0,0.1],
        },
    }
}