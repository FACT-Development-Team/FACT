# -----------------------------------------------------------
# Custom Keras metrics and losses for our tasks
# -----------------------------------------------------------
import tensorflow as tf
import numpy
from keras import backend as kb

# -------------------------
# custom evaluation metrics
# -------------------------
def top_k_multiclass(trained_model, x_train, x_test, y_train, y_test, categories, verbose=False):
    from keras import backend as kb
    import tensorflow

    x_test_embedded = trained_model.predict(x_test) # embedd whole test-set
    group_indices_train = [numpy.squeeze(numpy.argwhere(category)) for category in numpy.transpose(y_train)] # group train-set into categories
    group_indices_test = [numpy.squeeze(numpy.argwhere(category)) for category in numpy.transpose(y_test)] # group test-set into categories

    result = {}

    top_k = [1,3,5]

    for k in top_k:
        for i, group in enumerate(group_indices_test): # go over every category
            group_len = group.size
            if group_len > 0:
                hit = 0
                print("Evaluating category", categories[i], "of length", group_len, "k", k)
                for j in range(group_len):
                    if group_len > 1:
                        index = group[j]
                    else:
                        index = group

                    x = x_test_embedded[index]
                    samples_indexes = [numpy.random.choice(sample_group, size=k, replace=False) for sample_group in group_indices_train] # list of numpy arrays of length k with indices
                    samples_indexes = numpy.ravel(samples_indexes)
                    category_vector = numpy.zeros(len(samples_indexes))
                    category_vector[i*k:(i*k)+k] = 1
                    samples = x_train[samples_indexes]
                    samples_embedded = trained_model.predict(samples)
                    distances = numpy.ravel(euclidean_distance([x, samples_embedded]).numpy())
                    lookup_indices = numpy.argsort(distances)
                    lookup_sum = numpy.sum((category_vector[lookup_indices])[:k])
                    if lookup_sum > 0:
                        hit += 1
                hitrate = hit / group_len
                print("hitrate:", int(hitrate*100), "%")
                result[str(categories[i])+"_"+str(k)] = hitrate
            else:
                print("skipping group", categories[i], ", no test data.")
    return result

def f1_multiclass_metric(y_true, y_pred):
    """
    custom average macro F1 score

    computes batch-wise
    """
    def recall(y_true, y_pred):
        true_positive = kb.sum(kb.round(y_true * y_pred))
        real_positive = kb.sum(kb.round(y_true))

        return true_positive / (real_positive + kb.epsilon())

    def precision(y_true, y_pred):
        true_positive = kb.sum(kb.round(y_true * y_pred))
        predicted_positive = kb.sum(kb.round(y_pred))

        return true_positive / (predicted_positive + kb.epsilon())

    recall = recall(y_true, y_pred)
    precision = precision(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + kb.epsilon()))


# -------------
# custom losses
# -------------
def contrastive_loss(margin_distance):
    """
    custom contrastive loss

    computes batch-wise
    """
    def loss(same_or_different, distance):
        
        non_alignment_distance = kb.square(distance)
        alignment_distance = kb.square(kb.maximum(margin_distance - distance, 0))

        return kb.mean((1 - same_or_different) * alignment_distance + (same_or_different) * non_alignment_distance)

    return loss

# --------------------
# custom lambda layers
# --------------------

def euclidean_distance(batches):
    from keras import backend as kb
    import tensorflow
    x1, x2 = batches
    sum_square = kb.sum(kb.square(x1 - x2), axis=1, keepdims=True)
    return kb.sqrt(kb.maximum(kb.epsilon(), sum_square))