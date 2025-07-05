from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_remove_ticket_ticket_file_ticket_image'),  # or your latest migration file here
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='image',
            field=models.ImageField(upload_to='ticket_images/', null=True, blank=True),
        ),
    ]
