# This client represents one device/institution/organization
import flwr as fl
import tensorflow as tf

# Define model
print("Defining model ...")
model = tf.keras.applications.MobileNetV2(
    (32, 32, 3),
    classes=10,
    weights=None
)
model.compile("adam", 
              "sparse_categorical_crossentropy",
              metrics=['accuracy']
              )

# Load CIFAR-10 dataset
print("Loading data ...")
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

class CifarClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()
    
    def fit(self, parameters, config):
        model.set_weights(parameters)
        model.fit(x_train, y_train, epochs=1, batch_size=32)
        return model.get_weights(), len(x_train), {}
    
    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test)
        return loss, len(x_test), {"accuracy": accuracy} 
    
# Start Flower client
fl.client.start_numpy_client(
    server_address="127.0.0.1:8080",
    client=CifarClient())