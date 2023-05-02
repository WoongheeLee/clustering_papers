import requests
from lxml import etree
from bs4 import BeautifulSoup
from tqdm.auto import tqdm
import pickle
from pathlib import Path

def crawling_pmlr(url, pkl_path):
    '''
    Given a URL of a proceeding in PMLR, save the corresponding title and abstract as a pickle file to the specified file path.

    Args:
        url (str): The URL of the proceeding in PMLR. For example, for ICML 2020, url='https://proceedings.mlr.press/v162/'
        path (str): The file path where the pickle file will be saved.

    Returns:
        None
    '''
    
    if Path(pkl_path).exists():
        raise ValueError(f"Pickle already exists at {pkl_path}!")
    
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    urls = [] # for each paper
    for a in soup.find_all('a'):
        if "abs" in a.text:
            a = str(a).split("\"")
            urls.append(a[1])
    
    title_abs = dict()
    for u in tqdm(urls):
        resp_abs = requests.get(u)
        if resp_abs.status_code == 200:
            soup_abs = BeautifulSoup(resp_abs.text, 'lxml')
            t = soup_abs.find_all('title')[0].text.strip()
            a = soup_abs.find_all('div', {"class":"abstract"})[0].text.strip()
            title_abs[t] = a        
            
    with open(pkl_path, 'wb') as f:
        pickle.dump(title_abs, f)
        
        
def crawling_emnlp(url, pkl_path):
    """
    Args:
        url (str): The URL of the webpage to crawl.
            for example: "https://aclanthology.org/volumes/2022.emnlp-main/"
        pkl_path (str): The path to save the resulting pickle file.

    Returns:
        None
    """

    if Path(pkl_path).exists():
        raise ValueError(f"Pickle already exists at {pkl_path}!")

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    
    titles, abstracts = [], []
    for i, item in enumerate(soup.find_all()):
        if item.get('class') is not None and len(item.get('class'))==1 and "align-middle" in item.get('class'):
            titles.append(item.text)

        # abstract is not provided some times.
        if len(titles) - len(abstracts) == 2:
            del titles[-2]

        if item.get('class') is not None and len(item.get('class'))==3 and {'card-body', 'p-3', 'small'} == set(item.get('class')):
            abstracts.append(item.text)
    
    title_abs = dict()
    for t, a in tqdm(zip(titles, abstracts)):
        title_abs[t] = a

    with open(pkl_path, 'wb') as f:
        pickle.dump(title_abs, f)