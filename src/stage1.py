import os
import sys
import requests
from bs4 import BeautifulSoup

print("stage1")

os.makedirs("/out/stage1", exist_ok=True)

doclist = sys.argv[1]
print(doclist)

docs = []
for doc in open(f"/in/{doclist}", 'r'):
    docs.append(doc.strip())

print(docs)

for i,doc in enumerate(docs):
    res = requests.get(doc)

    soup = BeautifulSoup(res.text, 'html.parser')

    f = open(f"/out/stage1/{i}", 'w')
    f.write(soup.text)
    f.close()