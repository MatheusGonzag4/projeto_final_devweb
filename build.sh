#!/usr/bin/env bash
set -o errexit

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

# O painel Django depende destes arquivos; falhar aqui evita um deploy
# aparentemente bem-sucedido, mas com o /admin/ sem CSS.
test -f staticfiles/admin/css/base.css
test -f staticfiles/admin/css/login.css
