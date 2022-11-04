#!/usr/bin/env python3
"""
ceps.py

 URL: viacep.com.br/ws/01001000/json/
    {
      "cep": "01001-000",
      "logradouro": "Praça da Sé",
      "complemento": "lado ímpar",
      "bairro": "Sé",
      "localidade": "São Paulo",
      "uf": "SP",
      "ibge": "3550308",
      "gia": "1004",
      "ddd": "11",
      "siafi": "7107"
    }
"""
import requests
import json
from db.ceps_fetcher_sqlalch import Cep
from db.ceps_fetcher_sqlalch import get_session
BASE_INTERPOL_API_URL = 'https://viacep.com.br/ws/{cep}/json/'
CEP_EXAMPLE = '20260020'


def fetch_data_from_viacep_api(cep=None):
  if cep is None:
    cep = CEP_EXAMPLE
  url = BASE_INTERPOL_API_URL.format(cep=cep)
  print('Accessing', url)
  req = requests.get(url)
  json_data = json.loads(req.content)
  print(str(json_data))
  # record_cepdata_into_db()


def fetch_cep_if_exists_in_local_db(cep=None):
  if cep is None:
    cep = CEP_EXAMPLE
  # sqlalch.
  session = get_session()
  res = session.query(Cep).filter(Cep.cep == cep).first()
  if res:
    print(cep, 'Found')
    print(res)
    return res
  return None
  

def fetch_data_from_viacep_api_or_cached(cep=None):
  go_api = fetch_cep_if_exists_in_local_db()
  if go_api is None:
    fetch_data_from_viacep_api(cep)


def process():
  fetch_data_from_viacep_api_or_cached()


if __name__ == '__main__':
  process()
