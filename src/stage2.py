import os
import MeCab
import numpy as np
import json


os.environ["MECABRC"] = "/etc/mecabrc"


# print(ii)

# mecab = MeCab.Tagger("-Owakati")
mecab = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
mecab.parse('')
def wakachi(text):
    node = mecab.parseToNode(text)
    nouns = []
    while node:
        features =  node.feature.split(',')
        term = node.surface
        if features[0] == '名詞' and features[1] == '固有名詞':
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

    n = len(documents)
    docs = np.array(documents)
    vectorizer = TfidfVectorizer(analyzer=wakachi, max_df=0.8)
    X = vectorizer.fit_transform(docs)

    # DEBUG:
    # words = vectorizer.get_feature_names()
    # for doc_id, vec in zip(range(len(docs)), X.toarray()):
    #     f = open(f"/out/stage2/{doc_id}", 'w')
    #     for w_id, tfidf in sorted(enumerate(vec), key=lambda x: x[1], reverse=True):
    #         lemma = words[w_id]
    #         f.write('{0:s}: {1:f}\n'.format(lemma, tfidf))
    #     f.close()

    return X.toarray()

if __name__ == '__main__':
    from sklearn.metrics.pairwise import cosine_similarity

    os.makedirs("/out/stage2", exist_ok=True)

    ii = []
    for i in os.listdir("/out/stage1"):
        ii.append(int(i))

    docs = ["" for i in range(len(ii))]
    # docs = []
    for i in ii:
        inp = f"/out/stage1/{i}"
        f = open(inp, "r")
        data = f.read()
        docs[i] = data
        f.close()
        # print(wakachi(data))

    #類似度行列作成
    #小数点3桁まで計算
    cs_array = np.round(cosine_similarity(vecs_array(docs)), 3)
    print(cs_array)

    n = len(docs)
    mat = [[0.0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            mat[i][j] = cs_array[i,j]

    f = open(f"/out/stage2/out.json", 'w')
    json.dump(mat, f)
    f.close()
    
