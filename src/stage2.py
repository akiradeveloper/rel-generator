import os
import MeCab
import numpy as np

os.environ["MECABRC"] = "/etc/mecabrc"

os.makedirs("/out/stage2", exist_ok=True)

ii = []
for i in os.listdir("/out/stage1"):
    ii.append(int(i))

# print(ii)

mecab = MeCab.Tagger("-Owakati")

def wakachi(text):
    node = mecab.parseToNode(text)
    nouns = []
    while node:
        features =  node.feature.split(',')
        if features[0] == '名詞' and features[1] == '一般':
            nouns.append(node.surface)
        node = node.next
    return nouns

def vecs_array(documents):
    from sklearn.feature_extraction.text import TfidfVectorizer
 
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi,binary=True,use_idf=False)
    vecs = vectorizer.fit_transform(docs)
    return vecs.toarray()

if __name__ == '__main__':
    from sklearn.metrics.pairwise import cosine_similarity
    docs = []
    for i in ii:
        inp = f"/out/stage1/{i}"
        f = open(inp, "r")
        data = f.read()
        f.close()
        # print(wakachi(data))
        docs.append(data)

    #類似度行列作成
    #小数点3桁まで計算
    cs_array = np.round(cosine_similarity(vecs_array(docs), vecs_array(docs)), 3)
    print(cs_array)
    

    
