
make spacy datasets -> python3 create_spacy_bin.py --output_path datasets/training.spacy --input_path anno.json --input_type json
make experiment folder -> mkdir <folder name> + cd
create config file -> !python3 -m spacy init fill-config base_config.cfg config.cfg
train model ->!python3 -m spacy train config.cfg --output ./ --paths.train ./training_data.spacy --paths.dev ./training_data.spacy

