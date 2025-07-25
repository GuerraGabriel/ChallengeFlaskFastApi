import pytest


@pytest.fixture
def user_data_from_external_service():
    return {
        "nome": "Filomeno",
        "nome_social": "Astrucio",
        "profissao": "Vendedor de sonhos",
        "email": "none@example.com",
        "idade": 99,
        "cep": "00000000",
        "numero": "100",
        "rua": "Rua A",
        "bairro": "Bairro B",
        "cidade": "Cidade C",
        "estado": "SP",
        "pais": "Brasil",
    }
