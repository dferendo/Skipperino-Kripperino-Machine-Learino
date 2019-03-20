import tensorflow as tf


def load_graph(graph_location):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(graph_location, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()

    for l in proto_as_ascii_lines:
        label.append(l.rstrip())

    return label


def predict_image(config):