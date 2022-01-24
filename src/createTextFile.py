import argparse
import json
from typing import Tuple, List

import cv2
from path import Path

from dataloader_iam import Batch
from model import Model, DecoderType
from preprocessor import Preprocessor
import os

class FilePaths:
    """Filenames and paths to data."""
    fn_char_list = '../model/charList.txt'
    fn_summary = '../model/summary.json'
    fn_corpus = '../data/corpus.txt'
    save_path = '../output-files/'


def get_img_height() -> int:
    """Fixed height for NN."""
    return 32


def get_img_size(line_mode: bool = False) -> Tuple[int, int]:
    """Height is fixed for NN, width is set according to training mode (single words or text lines)."""
    if line_mode:
        return 256, get_img_height()
    return 128, get_img_height()


def write_summary(char_error_rates: List[float], word_accuracies: List[float]) -> None:
    """Writes training summary file for NN."""
    with open(FilePaths.fn_summary, 'w') as f:
        json.dump({'charErrorRates': char_error_rates, 'wordAccuracies': word_accuracies}, f)

def getText(model: Model, fn_img: Path) -> None:
    """Recognizes text in image provided by file path."""
    img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)
    assert img is not None

    preprocessor = Preprocessor(get_img_size(), dynamic_width=True, padding=16)
    img = preprocessor.process_img(img)

    batch = Batch([img], None, 1)
    recognized, probability = model.infer_batch(batch, True)
    print(f'Recognized: "{recognized[0]}"')
    print(f'Probability: {probability[0]}')
    return recognized[0]

def createTextFromImages(filePath,fileName,outputFolderName):
    parser = argparse.ArgumentParser()
    parser.add_argument('--dump', help='Dump output of NN to CSV file(s).', action='store_true')
    decoder_mapping = {'bestpath': DecoderType.BestPath,
                       'beamsearch': DecoderType.BeamSearch,
                       'wordbeamsearch': DecoderType.WordBeamSearch}
    args = parser.parse_args()
    decoder_type = decoder_mapping['bestpath']
    model = Model(list(open(FilePaths.fn_char_list).read()), decoder_type, must_restore=True, dump=args.dump)
    text = getText(model, filePath+'/'+fileName)
    outputFolderName = FilePaths.save_path + outputFolderName
    if not os.path.exists(outputFolderName):
        os.makedirs(outputFolderName)

    completeName = os.path.join(outputFolderName, fileName.split('.png')[0] + ".txt")
    print('Plag', text)
    txtFile = open(completeName, "w+")
    txtFile.write(text)
    txtFile.close()
    return text