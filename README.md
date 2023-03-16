# whisper-eval

用Whisper不同的模型，在不同语种、不同测试集上的效果。

## Preparation

- 安装[`whisper`](https://github.com/openai/whisper)

  ```shell
  pip install -U whisper
  ```

## Information

- 模型大小

  | model               | size |
  | ------------------- | ---- |
  | tiny                | 73M  |
  | base                | 139M |
  | small               | 462M |
  | medium              | 1.5G |
  | large-v1            | 2.9G |
  | large-v2            | 2.9G |
  | speechocean[Polish] | 165M |

## Languages Evaluation

1. 波兰语/Polish/pl-PL

   - 数据集

     | name                  | Dur/Utt  | tiny | base | small | medium | large-v1 | large-v2 | so    |
     | --------------------- | -------- | ---- | ---- | ----- | ------ | -------- | -------- | ----- |
     | common vioce/test     | 0.42/300 | 53.5 | 40.8 | 20.1  | 11.5   | 11.1     | 9.2      | 10.48 |
     | King-ASR-212/Internal | 0.50/300 | 27.7 | 16.1 | 6.0   | 3.4    | 3.2      | 2.3      | 0.47  |
     | M_AILABS/test         | 0.55/263 | 45.0 | 29.2 | 16.1  | 10.8   | 10.2     | 10.5     | 3.14  |

     

