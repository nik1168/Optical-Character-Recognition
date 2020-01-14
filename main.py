from data_loader.conv_emnist_data_loader import ConvEMnistDataLoader
from data_loader.conv_mnist_data_loader import ConvMnistDataLoader
from data_loader.simple_mnist_data_loader import SimpleMnistDataLoader
from data_visualizer.simple_mnist_data_visualizer import SimpleMnistDataVisualizer
from evaluater.conv_mnist_data_predictor import ConvMnistDataPredictor
from models.conv_emnist_model import ConvEMnistModel
from models.conv_mnist_model import ConvMnistModel
from models.simple_mnist_model import SimpleMnistModel
from trainers.conv_mnist_trainer import ConvMnistModelTrainer
from trainers.simple_mnist_trainer import SimpleMnistModelTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
import numpy as np
import sklearn.metrics as metrics
from flask import Flask, render_template, request, redirect

app = Flask(__name__,
            static_url_path='/test_images',
            static_folder='test_images', )


def main():
    # capture the config path from the run arguments
    # then process the json configuration file
    try:
        args = get_args()
        config = process_config(args.config)
    except:
        print("missing or invalid arguments")
        exit(0)

    # create the experiments dirs
    create_dirs([config.callbacks.tensorboard_log_dir, config.callbacks.checkpoint_dir, config.callbacks.history_dir])

    print('Create the data generator.')
    data_loader = ConvEMnistDataLoader(config)

    print('Some data visualization')
    X_train, y_train = data_loader.get_train_data()
    print("ytrain")
    print(y_train.shape)
    mapp = data_loader.get_map()
    data_visualizer = SimpleMnistDataVisualizer(X_train, y_train, mapp)
    data_visualizer.plot_first_digit()
    data_visualizer.plot_range()

    print('Create the model.')
    model = ConvEMnistModel(config)

    print("Model Summary")
    model.model.summary()

    print('Create the trainer')
    # trainer = ConvMnistModelTrainer(model.model, data_loader.get_train_data(), config)

    print('Start training the model.')
    # if not config.evaluator.custom_weight:
    # trainer.train()

    print("Plot loss and accuracy in training model")
    data_visualizer.plot_loss_acc()

    print("Finish training")
    print("Predict")
    weight = './experiments/2019-12-15/conv_emnist_from_config/checkpoints/conv_emnist_from_config-10-0.35.hdf5'

    predictor = ConvMnistDataPredictor(model.model, data_loader.get_test_data(), mapp, config, weight)
    predicted_values = predictor.ocr('./test_images/clau/clau.png')
    print("Predicted values")
    print(predicted_values)
    # predictor.predict3('./test_images/h/1.png')
    # predictor.predict_from_data_set()

    """
    Evaluate model with test set
    """
    # predictor.evaluate_model()
    #
    # predictor.confusion_matrix()


@app.route('/')
def hello_world():
    return render_template('index.html', name="name")


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":

        if request.files:
            image = request.files["image"]
            print("Fine")

            print(image)

            return redirect(request.url)

    return render_template('index.html', name="name")


if __name__ == '__main__':
    main()
    # app.run()
