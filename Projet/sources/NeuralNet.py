import tensorflow as tf
import os


class NeuralNetwork:
    def __init__(self):
        print("Neural Network Initialized")
        self.main()
        print("test")
    def main(self):
        os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
        var = tf.constant("Hey there")
        session = tf.Session()

        session.run(var)

