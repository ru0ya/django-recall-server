from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter", "0012_alter_voter_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$720000$gEWZZ5ffbVlBurRcKUS4bC$Y6reTL5BQi1gCeu18dj8BfiD2WkqkiRYGElpJjvMOS8=', max_length=128),
        ),
    ]
