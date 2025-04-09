import time
from typing import List

import nltk
from fastapi import UploadFile
from nltk import sent_tokenize
from nltk.corpus import stopwords
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from function.get_questoes import get_questoes

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')


def get_identificadas(input_upload: UploadFile) -> dict:
    read_content = input_upload.file.read()
    current_timestamp = time.time()
    full_file_name: str = 'file/' + str(current_timestamp) + '_' + input_upload.filename
    with open(full_file_name, 'wb') as f:
        f.write(read_content)

    reader = PdfReader(full_file_name)
    questoes: List[dict] = get_questoes()
    stop_words_pt = stopwords.words('portuguese')
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt)
    identificadas = __get_from_pages(reader.pages, questoes, vectorizer)

    return {'identificadas': identificadas}


def __get_from_pages(pages, questoes, vectorizer) -> List[dict]:
    titulos = []
    for page in pages:
        extracted = page.extract_text()
        __add_titulos(extracted, questoes, titulos, vectorizer)

    return titulos


def __add_titulos(content, questoes, target, vectorizer) -> None:
    for questao in questoes:
        trecho_caracteristico = questao['trechoCaracteristico']
        frases: List[str] = sent_tokenize(content)
        frases.append(trecho_caracteristico)
        tfidf_matrix = vectorizer.fit_transform(frases)
        similaridades = __get_similaridades(tfidf_matrix)
        limiar = 0.3

        frases_similares: List = [(frases[i], similaridades[i]) for i in range(len(similaridades)) if similaridades[i]
                                  >= limiar]

        [__add_questao(target, questao, frase_similar, similaridade) for frase_similar, similaridade in
         frases_similares]


def __get_similaridades(tfidf_matrix):
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    return cosine_similarities.flatten()

def __add_questao(target, questao, frase_similar, porcentagem) -> None:
    questao['frase_similar'] = frase_similar
    questao['porcentagem'] = porcentagem
    target.append(questao)