from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('request', 'New Tutor Request'), ('accepted', 'Request Accepted'), ('rejected', 'Request Rejected'), ('registered', 'New Registration'), ('review', 'New Review')], max_length=20),
        ),
    ]