from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_categoria_servico_categoria'),
        ('contato', '0001_initial'),
    ]

    operations = [
        # o Contato agora pertence ao app "contato"; a tabela não pode ser apagada
        migrations.SeparateDatabaseAndState(
            state_operations=[migrations.DeleteModel(name='Contato')],
            database_operations=[],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pedidos', to='app.servico')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-criado_em'],
            },
        ),
    ]
