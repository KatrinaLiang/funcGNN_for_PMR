"""funcGNN runner."""

from utils import tab_printer
from funcgnn import funcGNNTrainer
from param_parser import parameter_parser
import argparse


def main():
    """
    Parsing command line parameters, reading data.
    Fitting and scoring a funcGNN model.
    """
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--training_graphs', default='dataset/train', help='Dataset name')
    # parser.add_argument('--testing_graphs', default='dataset/test', help='Dataset name')
    # parser.add_argument('--batch_size', default='100', help='Dataset name')
    # parser.add_argument('--learning_rate', default='0.001', help='Dataset name')
    # parser.add_argument('--weight_decay', default='0.1', help='Dataset name')
    # parser.add_argument('--epochs', default='1', help='Dataset name')
    # args = parser.parse_args()

    args = parameter_parser()
    tab_printer(args)
    trainer = funcGNNTrainer(args)
    trainer.fit()
    # trainer.start_parallel()
    # trainer.load_model()


if __name__ == "__main__":
    main()
