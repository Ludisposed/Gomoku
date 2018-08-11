# Generated by Django 2.1 on 2018-08-11 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='game',
            name='name',
        ),
        migrations.AddField(
            model_name='game',
            name='end_timestamp',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='game',
            name='start_timestamp',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='result',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_r_g_id', to='game.Game'),
        ),
        migrations.AddField(
            model_name='result',
            name='loser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_r_l_id', to='game.User'),
        ),
        migrations.AddField(
            model_name='result',
            name='winner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_r_w_id', to='game.User'),
        ),
        migrations.AddField(
            model_name='record',
            name='game',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_re_g_id', to='game.Game'),
        ),
        migrations.AddField(
            model_name='record',
            name='step',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_re_s_id', to='game.Step'),
        ),
        migrations.AddField(
            model_name='game',
            name='player1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_g_p1_id', to='game.User'),
        ),
        migrations.AddField(
            model_name='game',
            name='player2',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fk_g_p2_id', to='game.User'),
        ),
    ]