# whisper-eval

用Whisper不同的模型，在不同语种、不同测试集上的效果。

## Preparation

- 安装[`whisper`](https://github.com/openai/whisper)

  ```shell
  pip install -U whisper
  ```

## Languages Evaluation

1. 波兰语/Polish/pl-PL

   - 数据集

     | name                  | Duration/Utterances | WER  |
     | --------------------- | ------------------- | ---- |
     | common vioce/test     | 0.424573/300        |      |
     | King-ASR-212/Internal | 0.505855/300        |      |
     | M_AILABS              | 0.551745/263        |      |
     | mls_polish            | 2.14412/520         |      |

     

