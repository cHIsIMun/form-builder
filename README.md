# form-builder

🇧🇷 Português | 🇺🇸 [English](README.en.md)

> Backend Django REST para construção de formulários dinâmicos multi-etapa, com coleta de respostas tipadas.

## Visão geral

API REST em Django para **montar formulários dinâmicos** organizados em etapas e seções, e coletar respostas com tipos variados. O modelo de dados segue a hierarquia **Step → Section → Field**, e as submissões são vinculadas a usuários.

## Modelo de dados

- **Step** → **Section** → **Field** (com ordenação via `unique_together`).
- Respostas tipadas: `AnswerText`, `AnswerNumber`, `AnswerBoolean`, `AnswerDate`, `AnswerFile`.
- **Submission** associada a usuário e etapa.

## Funcionalidades

- ViewSets CRUD para steps, sections e fields.
- Recuperação da estrutura do formulário (`/form-structure/`, `/step/<id>/`, `/section/<id>/`).
- Coleta de respostas com conversão de tipos.
- Autenticação customizada baseada em email (`AbstractBaseUser`), permissões e grupos.

## Stack

Python · Django · Django REST Framework · SQLite.

## Como executar

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # ou conforme o gerenciador do projeto
python manage.py migrate
python manage.py runserver        # http://localhost:8000
```

## Estado do projeto

Backend bem estruturado, com modelos sólidos. Para produção, faltam: autenticação por token/JWT, configuração de CORS e testes.

## Licença

Este projeto ainda não declara uma licença; até que uma seja adicionada, todos os direitos são reservados ao autor.
