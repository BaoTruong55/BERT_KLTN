```bash
python3 train.py --fold 0 \
--train_path ./Data/train.csv \
--dict_path ./PhoBERT/PhoBERT_base_transformers/dict.txt \
--config_path ./PhoBERT/PhoBERT_base_transformers/config.json \
--bpe-codes ./PhoBERT/PhoBERT_base_transformers/bpe.codes \
--pretrained_path ./PhoBERT/PhoBERT_base_transformers/model.bin \
--ckpt_path ./Models \
--rdrsegmenter_path ./VnCoreNLP/VnCoreNLP-1.1.1.jar
```

```bash
python3 infer.py  --test_path ./Data/test.csv \
--dict_path ./PhoBERT/PhoBERT_base_transformers/dict.txt \
--config_path ./PhoBERT/PhoBERT_base_transformers/config.json \
--bpe-codes ./PhoBERT/PhoBERT_base_transformers/bpe.codes \
--pretrained_path .PhoBERT/PhoBERT_base_transformers/model.bin \
--ckpt_path ./Data \
--rdrsegmenter_path ./VnCoreNLP/VnCoreNLP-1.1.1.jar 
```
