# Generated by Django 2.1 on 2018-08-12 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_game_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_g_c_id', to='game.User'),
        ),
        migrations.AddField(
            model_name='game',
            name='next_player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_g_n_id', to='game.User'),
        ),
    ]