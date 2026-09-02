from django.db import migrations


def create_subjects(apps, schema_editor):
    Subject = apps.get_model("tutors", "Subject")

    subjects = [
        "Math",
        "Science",
        "Social",
        "English",
        "Nepali",
        "Account",
        "NepalBhasa",
        "Computer",
        "Health",
    ]

    for name in subjects:
        Subject.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("tutors", "0002_review"),
    ]

    operations = [
        migrations.RunPython(create_subjects),
    ]