import time
from typing import List

from fastapi import UploadFile
from pypdf import PdfReader

from function.get_questoes import get_questoes


def get_identificadas(input_upload: UploadFile) -> dict:
    read_content = input_upload.file.read()
    current_timestamp = time.time()
    full_file_name: str = 'file/' + str(current_timestamp) + '_' + input_upload.filename
    with open(full_file_name, 'wb') as f:
        f.write(read_content)

    reader = PdfReader(full_file_name)
    questoes: List[dict] = get_questoes()
    identificadas = __get_from_pages(reader.pages, questoes)

    return {'identificadas': identificadas}


def __get_from_pages(pages, questoes) -> List[dict]:
    titulos = []
    for page in pages:
        extracted = page.extract_text()
        non_new_lines = extracted.replace('\n', '').replace('\r', '')
        non_double_spaces = non_new_lines.replace('  ', '')
        __add_titulos(non_double_spaces, questoes, titulos)

    return titulos


def __add_titulos(content, questoes, target) -> None:
    for questao in questoes:
        if questao['trechoCaracteristico'] in content:
            target.append(questao)