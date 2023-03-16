import os
import re
import sys
import argparse
import whisper
import torch
import shutil

from collections import defaultdict
from pydub import AudioSegment
from tqdm import tqdm

def color_log(information):
    return f"\033[1;31;40m{information}\033[0m"

def read_inputs_info(data_dir, is_long=False, temp_short_dir=None):
    wavscp_file = os.path.join(data_dir, "wav.scp")
    text_file = os.path.join(data_dir, "text")
    assert os.path.exists(wavscp_file)
    assert os.path.exists(text_file)
    
    # Get name to text dict
    name2text = {}
    with open(text_file, encoding='utf-8') as f:
        text_contents = f.readlines()    
    for line in text_contents:
        name, text = line.strip().split(" ", 1)
        if not is_long:
            name = name.split("--")[0]
        text = text.lower().strip()
        name2text[name] = text
    
    # Get name to path dict
    name2wavp = {}
    with open(wavscp_file, encoding='utf-8') as f:
        wavp_contents = f.readlines()
    for line in wavp_contents:
        name, wavp = line.strip().split()
        name2wavp[name] = wavp

    # if original wav file is long type
    # then cut them into short    
    if is_long:
        segments_file = os.path.join(data_dir, "segments")
        assert temp_short_dir is not None
        os.makedirs(temp_short_dir, exist_ok=True)
        with open(segments_file, encoding='utf-8') as f:
            seg_contents = f.readlines()
        name2subinfo = defaultdict(list)
        for line in tqdm(seg_contents):
            subname, name, start, end = line.strip().split()
            start, end = int(float(start) * 1000), int(float(end) * 1000)
            name2subinfo[name].append([subname, start, end])
        subname2wavp = {}
        for name, subinfo in name2subinfo.items():
            sound = AudioSegment.from_wav(name2wavp[name])
            for (subname, start, end) in subinfo:
                subfile = os.path.join(temp_short_dir, f"{subname}.wav")
                piece = sound[start:end]
                piece.export(subfile, format="wav")
                subname2wavp[subname] = subfile
        name2wavp = subname2wavp
    
    data_info = []
    for name, text in name2text.items():
        if name in name2wavp.keys():
            wavp = name2wavp[name]
        else:
            print(f"The wav path of {name} is not existed!")
            sys.exit()
        data_info.append(
            {
                "name": name,
                "wav_path": wavp,
                "text": text
            }
        )
    return data_info
    

def main(args):
    # Loading whisper model
    model = whisper.load_model(args.model_type)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    # get the wavfile and corresponding text
    exp_dir = os.path.join(args.exp_dir, args.setname, args.model_type)
    os.makedirs(exp_dir, exist_ok=True)
    
    temp_short_dir = os.path.join(exp_dir, "shorts")
    data_info = read_inputs_info(args.data_dir, args.is_long, temp_short_dir)
    
    ref_file = os.path.join(exp_dir, f"{args.setname}_{args.model_type}_ref.text")
    hyp_file = os.path.join(exp_dir, f"{args.setname}_{args.model_type}_hyp.text")
    
    print("="*40)
    print(f"     Model     : {color_log(args.model_type)}")
    print(f"     Dataset   : {color_log(args.setname)}")
    print(f"     Language  : {color_log(args.language)}")
    print("="*40)
    
    with open(ref_file, 'w', encoding='utf-8') as fr, \
        open(hyp_file, 'w', encoding='utf-8') as fh:
        print(f"Start to do the recognition for [{args.setname}] with {args.model_type}.")
        for one in tqdm(data_info):
            name, wavp, raw_text = one["name"], one["wav_path"], one["text"]
            result = model.transcribe(wavp, language=args.language)
            rec_text = result["text"].lower()
            rec_text = re.sub("[.–?!,]", "", rec_text).strip()
            fr.write(f"{raw_text}({name})\n")
            fh.write(f"{rec_text}({name})\n")

    # remove the directory for temp wav
    if os.path.isdir(temp_short_dir):
        shutil.rmtree(temp_short_dir)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--language",
                        default="Polish",
                        type=str,
                        help="the language to do the recognition")
    parser.add_argument("--model-type",
                        default="base",
                        type=str,
                        choices=["tiny", "base", "small", "medium", "large-v1", "large-v2"],
                        help="which model of whisper to do the recognition")
    parser.add_argument("--exp-dir",
                        default="exp",
                        type=str,
                        help="directory to save the recoginised results")
    parser.add_argument("--is-long",
                        action='store_true',
                        help="if the original wav is long type.")
    parser.add_argument("--data-dir",
                        default=None,
                        type=str,
                        help="directory for the data with wav.scp and text")
    parser.add_argument("--setname",
                        default=None,
                        type=str,
                        required=True,
                        help="what kind of testset")
    args = parser.parse_args()
    print(args)
    main(args)