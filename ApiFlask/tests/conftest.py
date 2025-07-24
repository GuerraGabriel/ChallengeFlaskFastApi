import pytest


@pytest.fixture
def csv_content():
    content = """Nome,Nome social,Email,Idade,CEP,Número,Rua,Bairro,Cidade,Estado,País,Profissão
Gabriel,,gabriel@example.com,27,00000000,100,Rua A,Bairro B,Cidade C,SP,Brasil,Developer
Filomeno,Astrucio,none@example.com,99,00000000,100,Rua A,Bairro B,Cidade C,SP,Brasil,Vendedor de sonhos
"""
    return content
