```bash
python3 train.py --fold 0 \
--train_path ./data/train.csv \
--dict_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBert-Sentiment-Classification/PhoBERT_base_transformers/dict.txt \
--config_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBert-Sentiment-Classification/PhoBERT_base_transformers/config.json \
--bpe-codes /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBert-Sentiment-Classification/PhoBERT_base_transformers/bpe.codes \
--pretrained_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBert-Sentiment-Classification/PhoBERT_base_transformers/model.bin \
--ckpt_path ./models \
--rdrsegmenter_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBert-Sentiment-Classification/VnCoreNLP/VnCoreNLP-1.1.1.jar
```

```bash
python3 infer.py  --test_path ./data2/data/test.csv \
--dict_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBERT_base_transformers/dict.txt \
--config_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBERT_base_transformers/config.json \
--bpe-codes /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBERT_base_transformers/bpe.codes \
--pretrained_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/PhoBERT_base_transformers/model.bin \
--ckpt_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/train_and_sub_20k \
--rdrsegmenter_path /media/henry/HENRY/Finally-16-20/suicao/suicao.raw/BERT_KLTN/VnCoreNLP/VnCoreNLP-1.1.1.jar 
```