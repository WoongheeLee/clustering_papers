# crawling proceedings
This function crawls the titles and corresponding abstracts of papers and saves them as a dictionary of {title: abstract} in a pickle file.

## tree
```
└── utils
    └── crawling.py
```
## usage
```
from utils.crawling import *
```

```python
url = 'https://proceedings.mlr.press/v162/
pkl_path = '../data/icml2022.pkl'
crawling_pmlr(url, pkl_path)
```

```python
url = "https://aclanthology.org/volumes/2022.emnlp-main/"
pkl_path = '../data/emnlp2022.pkl'
crawling_emnlp(url, pkl_path)
```