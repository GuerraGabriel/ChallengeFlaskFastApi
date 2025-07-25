from typing import List
from pydantic import BaseModel, Field


class UserAddressExternalSchema(BaseModel):
    nome: str
    nome_social: str | None
    profissao: str
    email: str
    idade: int
    cep: str = Field(max_length=8)
    numero: str
    rua: str
    bairro: str
    cidade: str
    estado: str
    pais: str


class UserAddressResponseSchema(BaseModel):
    data: List[UserAddressExternalSchema]
    message: str
