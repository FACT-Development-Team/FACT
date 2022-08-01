import os
directory = os.path.join("/","absolute","path","to","your","local","folder")

parameters = {
    # general parameters
    "directory" : directory,
    "seq_length": 50,
    "debug": False,
    "wandb": False,
    "test_immediately": True,
    "encoding": "text",
    "embedding_dim": 14,
    "optimizer": "adam",
    "train_test_fraction": 0.1,
    "validation_split": 0.1,
    "epochs": 20,
    # Models parameters
    # dense
    "dense_depth_layout": [64,32,16],
    "dense_regularizer_l1": 0.001,
    "dense_regularizer_l2": 0.0001,
    # rnn
    "rnn_dropout": 0,
    "rnn_depth_layout": [32,16,8],
    "rnn_regularizer_l1": 0.001,
    "rnn_regularizer_l2": 0.0001,
    # transformer
    "transformer_embedding_dim": 6,
    "attention_heads": 10,
    # cnn
    "cnn_depth_layout": [(2,2), (2,2)], # (pooling_size, pooling_strides)
    "cnn_regularizer_l1": 0.001,
    "cnn_regularizer_l2": 0.0001,
    "cnn_filters": 10,
    "cnn_kernel_size": 1,
    # Tasks parameters
    # similarity
    "similarity_embedding_dim": 5,
    "margin_distance": 1,
    "siamese_fraction": 0.01,
    "siamese_upper_limit": 10,
    "siamese_lower_limit": 5,
    "similarity_seq_len": 10,
    # continuation
    "continuation_split": 10,
    # generation
    "generation_embedding_dim": 10,
    "generation_seq_len": 10,
    # unmasking
    "unmasking_embedding_dim": 10,
    "unmasking_seq_len": 10,
    "unmasking_masks_per_batch": 5,
    
}

def get_hyperparameters(parameters, hyperparameters):
    p = {}
    result = hyperparameters.copy()
    # reshape to wandb-format
    for key, value in parameters.items():
        p[key] = {
            "value": value
        }
    result["parameters"] = p # append parameters to result
    # override hyperparameters
    for key, value in hyperparameters["parameters"].items():
        result["parameters"][key] = value

    return result