import os 
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
from tensorflow.keras.models import save_model
from dataset import data_loader
from dataset import tokenizer
from network import network_architecture
from model import train_model
from visualization import utils
#import inference

#print(config.list_physical_devices("GPU"))
#print(config.list_physical_devices("CPU"))


DATA_PATH = "src/dataset/spa.txt"
MAX_TOKEN = 15000
SEQUENCE_LENGTH = 20
BATCH_SIZE = 64
EPOCHS = 15
EMBED_DIM = 128
#LATENT_DIM = 1024


def main():
    doc = data_loader.load_doc(DATA_PATH)
    pairs = data_loader.make_pairs(doc)
    train, validation, test = data_loader.train_test_split_data(pairs)
    train_dataset, validation_dataset, test_dataset, spanish_tokenizer = tokenizer.vectorize(train, validation, test, MAX_TOKEN, SEQUENCE_LENGTH, BATCH_SIZE)
    vocabs = spanish_tokenizer.get_vocabulary() # to reverse predictions from numbers to words
    # print(vocabs)
    

    for batch in train_dataset.take(1):
        print(batch)  # Print a sample batch

    # print(len(train))
    for inputs, targets in train_dataset.take(1):
        print(f"english input: {inputs['English'].shape}")
        print(inputs['English'][6])
        print(f"Spanish input: {inputs['Spanish'].shape}")
        print(inputs['Spanish'][6])
        print(f"Spanish output: {targets.shape}")
   
    # for inputs in test_dataset.take(1):
    #     print(f"english test input: {inputs['English'].shape}")

    #Run this for train
    seq2seq = network_architecture.Transformers(10, 5, 4, n_encoders=4, n_decoders=2)
    model = seq2seq()
    print(f"model is: {model}")
    H = train_model.train(model, train_dataset, validation_dataset, BATCH_SIZE, EPOCHS)
    utils.plot_metrics(H)
    

if __name__ == "__main__":
    main()
