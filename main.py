from data_loader.conv_emnist_data_loader import ConvEMnistDataLoader
from data_loader.conv_mnist_data_loader import ConvMnistDataLoader
from data_loader.simple_mnist_data_loader import SimpleMnistDataLoader
from data_visualizer.simple_mnist_data_visualizer import SimpleMnistDataVisualizer
from evaluater.conv_mnist_data_predictor import ConvMnistDataPredictor
from models.conv_mnist_model import ConvMnistModel
from models.simple_mnist_model import SimpleMnistModel
from trainers.conv_mnist_trainer import ConvMnistModelTrainer
from trainers.simple_mnist_trainer import SimpleMnistModelTrainer
from utils.config import process_config
from utils.dirs import create_dirs
from utils.utils import get_args
import numpy as np


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
    create_dirs([config.callbacks.tensorboard_log_dir, config.callbacks.checkpoint_dir])

    print('Create the data generator.')
    data_loader = ConvEMnistDataLoader(config)

    # print('Some data visualization')
    X_train, y_train = data_loader.get_train_data()
    # print("ytrain")
    # print(y_train)
    mapp = data_loader.get_map()
    data_visualizer = SimpleMnistDataVisualizer(X_train, y_train, mapp)
    data_visualizer.plot_first_digit()
    data_visualizer.plot_range()

    print('Create the model.')
    model = ConvMnistModel(config)

    print("Model Summary")
    model.model.summary()

    print('Create the trainer')
    trainer = ConvMnistModelTrainer(model.model, data_loader.get_train_data(), config)

    print('Start training the model.')
    # trainer.train()

    print("Finish training")
    print("Predict")
    # weight = './experiments/2019-11-18/conv_mnist_from_config/checkpoints/conv_mnist_from_config-03-0.01.hdf5'
    # # weight = ''
    # predictor = ConvMnistDataPredictor(model.model, data_loader.get_test_data(), weight)
    # predictor.predict3('./test_images/9/1.png')


if __name__ == '__main__':
    main()
