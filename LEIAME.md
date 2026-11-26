# CompraAi - WEB III, Projeto Django

## Como rodar

    python -m venv venv
    venv\Scripts\activate          (Linux/Mac: source venv/bin/activate)
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

Abra http://127.0.0.1:8000/

Para desenvolvimento, copie `.env.example` para `.env` e preencha `SUPABASE_URL` e
`SUPABASE_ANON_KEY` com os valores do projeto Supabase. `SUPABASE_KEY` continua aceito
para compatibilidade com o deploy antigo.

No Render, cadastre essas variáveis em **Environment**. Também configure
`DJANGO_SECRET_KEY` com uma chave nova e `DJANGO_DEBUG=False`. O build deve executar
`./build.sh` e o start pode usar o `Procfile` ou
`gunicorn projeto.wsgi:application --bind 0.0.0.0:$PORT`.

## Rotas principais

- `/` Home | `/quem-somos/` | `/produtos/` | `/contato/` | `/login/`
- `/login/dashboard/` (cliente) ou `/admin/` (administrador)
- `/servicos/`, `/integrantes/` (equipe), `/pedidos/`, `/relatorios/`, `/contato/contatos/`

## Observações

- O e-mail de "Esqueceu a senha" aparece no terminal onde o servidor está rodando (EMAIL_BACKEND de console).
- Para um usuário ser administrador, crie/edite o Perfil dele no painel admin com tipo "Administrador".

- Logo, ícone e fontes ficam em `app/static/img` e `app/static/fonts` (tudo local, não depende de internet para carregar o visual).
- As cores da marca estão no começo de `app/static/css/style.css` (variáveis `--azul` e `--laranja`).
