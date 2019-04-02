import os
import numpy as np
import tensorflow as tf


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph


def prepare_image_for_tensor_flow(directory_of_images):
    images_normalized = []
    input_height, input_width, input_mean, input_std = 299, 299, 0, 255
    input_name = "file_reader"

    for image_name in os.listdir(directory_of_images):
        image_location = f"{directory_of_images}\\{image_name}"

        file_reader = tf.read_file(image_location, input_name)
        image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        re_sized_image = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        images_normalized.append(tf.divide(tf.subtract(re_sized_image, [input_mean]), [input_std]))

    return tf.Session().run(images_normalized)


def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label


def label_images(model_location, images_dictionary_location, labels_location):
    input_name = "import/Placeholder"
    output_name = "import/final_result"
    graph = load_graph(model_location)
    images_prepared = prepare_image_for_tensor_flow(images_dictionary_location)

    input_operation = graph.get_operation_by_name(input_name)
    output_operation = graph.get_operation_by_name(output_name)

    with tf.Session(graph=graph) as sess:
        # Loop through all the images and first either 
        for t in images_prepared:
            result = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: t
            })

    results = np.squeeze(results)

    top_k = results.argsort()[-5:][::-1]
    labels = load_labels(label_file)
    for i in top_k:
        print(labels[i], results[i])

    results = np.squeeze(results)

    labels = load_labels(labels_location)

    return
