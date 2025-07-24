from dataclasses import dataclass


@dataclass
class UserAddressDTO:
    nome: str
    nome_social: str
    email: str
    idade: int
    cep: str
    numero: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    pais: str 
    profissao: str

