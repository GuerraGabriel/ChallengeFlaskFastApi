# Requisitado
Desenvolver uma solução para **persistir os dados de uma planilha em um banco relacional**.

A planilha deve ter **no mínimo 10 registros** e o seu conteúdo deve ser:

- Nome
- Nome social
- Email
- Idade
- Endereço:
  - CEP
  - Número
  - Rua
  - Bairro
  - Cidade
  - Estado
  - País
- Profissão

---

## Requisitos Técnicos

### API 1 – Flask (obrigatório)

- Responsável por receber o **arquivo CSV** (com a lista de usuários).
- Processa o conteúdo e salva os dados no banco relacional.
- Implementa um CRUD básico:
  - **Criar**: Inserir dados do arquivo.
  - **Ler**: Consultar registros.
  - **Atualizar e Deletar**: Opcional.
- Expõe endpoint para retornar dados em **JSON**.

---

### API 2 – Framework à escolha  
*(Ex: FastAPI, Django REST Framework, Spring Boot)*

- Realiza consultas rápidas nos dados já salvos pelo Flask.
- A comunicação entre as APIs pode ser feita via **HTTP** ou por chamadas internas.
- Deve receber parâmetros via **GET/POST** e retornar dados em **JSON**.

---

### Banco de Dados

- Pode ser **PostgreSQL**, **MySQL** ou **SQLite**.
- Tabelas estruturadas de forma **simples e clara**.

---

### Especificações do Arquivo de Entrada

- Arquivo enviado via **multipart/form-data**.
- Dados estruturados (conforme lista de campos acima).
- **Validação** e **tratamento de erros** são obrigatórios.

---

### Integração entre APIs

- Um endpoint na **API 2** deve chamar a **API Flask**, buscar os dados e retornar o resultado.

---

### Observações

- Realizar **testes unitários** nas duas APIs.

---

### Desafio Extra (opcional)

- Autenticação via **Token** entre APIs.
- **Logs** de operação em cada API.
- **Deploy local com Docker**.
