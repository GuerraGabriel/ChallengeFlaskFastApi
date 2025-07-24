from dataclasses import dataclass
from typing import Optional


@dataclass
class UserAddressDTO:
    nome: str
    nome_social: str
    email: str
    idade: int
    profissao: str

    cep: str
    numero: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    pais: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
