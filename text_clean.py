import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import re

import warnings
warnings.filterwarnings('ignore') 

nltk.data.path.append('nltk_data/')

# freshely installed nltk requires few additional download , so commenting it for now
# nltk.download('stopwords')
# nltk.download('punkt')



def TextClean(all_text):
    '''
    helper function to clean text
    '''
    assert type(all_text)==list
    all_clean = []
    for text in all_text:
        text = text.lower()
        text = re.sub(r'#',' # ',text)
        text = re.sub(r'@',' @ ',text)
        text = re.sub(r'_','  ',text)
        text = re.sub(r'-','  ',text)
        # how to remove full stop and " -> findout ??
        re.sub(r"[,.;@#?!&$]+\ *"," ",text, flags=re.VERBOSE)
        text = word_tokenize(text)
        stopword_all =  list(set(stopwords.words('english'))) 
        stopword_all.extend(list(string.punctuation))
        # print(text)
        text = [word for word in text if word not in stopword_all]
        text = ' '.join(text)
        all_clean.append(text)
    return all_clean


if __name__=='__main__':
    text = 'RT @ReshadRahman_: Barça couldn’t renew Messi due to financial issues, we know that — but relaying in public (and private) that the renewal…'
    clean_text = TextClean([text])
    print(clean_text)