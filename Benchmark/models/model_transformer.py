# -----------------------------------------------------------
# Transformer Subclass of Model Class
#
# Released under GNU Public License (GPL)
# @author Flavio Schenker
# @email flaviosc@student.ethz.ch
# -----------------------------------------------------------

from models import Model
import tensorflow
import keras
import numpy

class Transformer(Model):
    """Keras Transformer Model Wrapper
    Attributes
    ----------
    name : str
        Name of the model.
    dependency: str
        Keras or Sklearn, source of the Model wrapper.
    Methods
    -------
    build_model(parameters, input_shape):
        Implementation of the Model wrapper.
    """
    def __init__(self):
        """Inits Transformer Class
        Parameters
        ----------
        none
        """
        self.name = "Transformer"
        self.dependency = "Keras"

    def build_model(self, parameters, input_shape):
        """Implementation of the Model wrapper.
        Parameters
        ----------
        parameters : dict
            Layout blueprint for the models like 'layer_depth', 'units', etc.
        input_shape: tuple
            Shape of the input training data.
        Returns
        -------
        keras.Model()
        """
        if len(input_shape) < 2:
            input_shape += (1,)
        input_layer = keras.layers.Input(name="input", shape=input_shape)
        embedding_layer = EmbeddingBlock(name="embedding", seq_len=input_shape[0], transformer_embedding_dim=parameters["transformer_embedding_dim"], input_shape=input_layer.shape)(input_layer)
        transformer_layer = TransformerBlock(name="transformer", embed_dim=parameters["transformer_embedding_dim"], num_heads=parameters["attention_heads"], ff_dim=parameters["transformer_embedding_dim"])(embedding_layer)
        pooling_layer = keras.layers.GlobalAveragePooling1D(name="pooling")(transformer_layer)
        output_layer = keras.layers.Dense(name="output", units=parameters["last-layer_units"], activation=parameters["last-layer_activation"])(pooling_layer)
        model = keras.models.Model(name="Transformer", inputs=input_layer, outputs=output_layer)
        return model

class TransformerBlock(keras.layers.Layer):
    """Keras Custom Layer Transformer Block
    Attributes
    ----------
    att : keras.layers
        multi head attention layer
    ffn : keras.layers
        feed-forward layer
    layernorm1 : keras.layers
        normalization layer 1
    layernorm2 : keras.layers
        normalization layer 2
    dropout1 : keras.layers
        dropout layer 1
    dropout2 : keras.layers
        dropout layer 2
    Methods
    -------
    call(input_layer):
        Implementation of keras.layers call method
    get_config(input_layer):
        Implementation of keras.layers get_config method
    """
    def __init__(self, name, embed_dim, num_heads, ff_dim, rate=0.1):
        super().__init__(name=name)
        self.att = keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.models.Sequential(
            [keras.layers.Dense(ff_dim, activation="relu"), keras.layers.Dense(embed_dim),]
        )
        self.layernorm1 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = keras.layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = keras.layers.Dropout(rate)
        self.dropout2 = keras.layers.Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

    def get_config(self):
        config = super().get_config().copy()
        return config        

class EmbeddingBlock(keras.layers.Layer):
    """Keras Custom Layer Embedding Block
    Attributes
    ----------
    seq_len : int
        length of the input sequence
    transformer_embedding_dim : int
        size of the transformer embedding space
    input_shape : tuple
        shape of the input tensor        
    Methods
    -------
    call(input_layer):
        Implementation of keras.layers call method
    get_config(input_layer):
        Implementation of keras.layers get_config method
    """
    def __init__(self, name, seq_len, transformer_embedding_dim, input_shape):
        super().__init__(name=name)
        self.seq_len = seq_len
        self.dense_emb = keras.layers.Dense(transformer_embedding_dim, use_bias=False, input_shape=input_shape)
        self.pos_emb = keras.layers.Embedding(input_dim=self.seq_len, output_dim=transformer_embedding_dim)

    def call(self, input_layer):
        positions = tensorflow.range(start=0, limit=self.seq_len, delta=1)
        positions = self.pos_emb(positions)
        return self.dense_emb(input_layer) + positions
    def get_config(self):
        config = super().get_config().copy()
        return config        
