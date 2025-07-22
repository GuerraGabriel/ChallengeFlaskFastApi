import pytest


@pytest.fixture
def csv_content():
    content = """nome,nome social,email,idade,cep,numero,rua,bairro,cidade,estado,país,profissão
Gabriel,Gabe,gabriel@example.com,30,Developer,12345,100,Rua A,Bairro X,Cidade Y,SP,Brasil
Ana,Ana S,ana@example.com,25,Designer,54321,200,Rua B,Bairro Y,Cidade Z,RJ,Brasil
"""
    return content
