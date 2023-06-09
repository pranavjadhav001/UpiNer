# Objective
To classify each entity in a UPI remark into a category,Approaching the problem as a NER problem statement
![alt text](https://github.com/pranavjadhav001/UpiNer/blob/main/images/Image.jpg?raw=true)
# Basic Commands for training NER Spacy Model:

- make spacy datasets -> python3 create_spacy_bin.py --output_path datasets/training.spacy --input_path anno.json --input_type json
- make experiment folder -> mkdir <folder name> + cd
- create config file -> !python3 -m spacy init fill-config base_config.cfg config.cfg
- train model ->!python3 -m spacy train config.cfg --output ./ --paths.train ./training_data.spacy --paths.dev ./training_data.spacy

# About Notebooks

## Data Augmentation
- NER spacy library doesn't have support for data augmentation
- I annotated data from 1 specific bank and augmentated to suit the needs the other
- Model was trained on augmented data and later validated on the other bank which was never a part of the training dataset
- Some Augmentation techniques used were : 
	- Position Augmentation: interchanging positions of NER entities
	- Random Upper/Lower Case augmentation
	- Repetition Augmentation : Randomly repeat 1 or more entity at random places in a sentence
	- Special Chars : Adding Special Characters at random location to random entities
	- Delimiters : some UPI remarks have '/' as delimiter while some have '-'
	- All the above augmentations are later combine with different weights and probabilities to account for as much randomness in data
	- Augmentation Notebook Path : Notebooks/data_augmentation.ipynb

## Training Notebook
- Training Notebook Path : Notebooks/spacy_training.ipynb
