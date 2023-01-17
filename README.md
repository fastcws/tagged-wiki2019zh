
## [下载语料库](https://github.com/fastcws/tagged-wiki2019zh/releases/download/v1.0.0/cn-wiki-wseg.7z)

# 进行了分词标注的2019中文维基语料库

基于经过清洗和切分的2019年中文wiki语料库[wiki2019zh.zip](https://github.com/brightmart/nlp_chinese_corpus#1%E7%BB%B4%E5%9F%BA%E7%99%BE%E7%A7%91json%E7%89%88wiki2019zh)，使用[hanlp](https://github.com/hankcs/HanLP)中的[COARSE_ELECTRA_SMALL_ZH](https://hanlp.hankcs.com/docs/api/hanlp/pretrained/tok.html)模型进行了分词。

分词结果采用4-tag BMES标注法进行了序列标注，格式如下：

假设被分词的语料是：`你好Tom。我喜欢吃羊肉串。`，标注结果为：

```
你 B
好 E
T B
o M
m E
。 S
SENTENCE END
我 S
喜 B
欢 E
吃 S
羊 B
肉 M
串 E
。 S
SENTENCE END
TEXT END
```
使用中可能需要注意嵌入（embeddings）和标点符号的处理方式，以及语句和语料结束的标志`SENTENCE END`和`TEXT END`。

分词使用的脚本是[process_wiki_data.py](process_wiki_data.py)。

运行此脚本需要花费大量的时间：

* CPU型号：Intel Xeon(Cascade Lake) Platinum 8269CY
* CPU主频：2.5Ghz/3.2Ghz
* 花费时间：7天11小时2分钟

