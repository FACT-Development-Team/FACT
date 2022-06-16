hyperparameters_Transformer = {
    "name": "Transformer",
    "method": "grid",
    "metric": {
        "name": "val_accuracy",
        "goal": "maximize",
    },
    "parameters": {
        "attention_heads": {
            "values": [5,10,20,40],
        },
        "transformer_embedding_dim": {
            "values": [3,6,12,24],
        },
    }
}