import os
import MeCab
import numpy as np
import json

os.environ["MECABRC"] = "/etc/mecabrc"

os.makedirs("/out/stage2", exist_ok=True)

ii = []
for i in os.listdir("/out/stage1"):
    ii.append(int(i))

# print(ii)

# mecab = MeCab.Tagger("-Owakati")
mecab = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
mecab.parse('')
def wakachi(text):
    node = mecab.parseToNode(text)
    nouns = []
    while node:
        hinshi =  node.feature.split(',')[0]
        term = node.surface
        if hinshi == '名詞':
            nouns.append(term)
        node = node.next
    # print(nouns)
    return nouns

# from janome.tokenizer import Tokenizer
# janome = Tokenizer()
# def wakachi(text):
#     tokens = janome.tokenize(text)
#     docs=[]
#     for token in tokens:
#         docs.append(token.surface)
#     return docs

def vecs_array(documents):
    from sklearn.feature_extraction.text import TfidfVectorizer
 
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi)
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

    n = len(docs)
    mat = [[0.0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            mat[i][j] = cs_array[i,j]

    f = open(f"/out/stage2/out.json", 'w')
    json.dump(mat, f)
    f.close()
    
