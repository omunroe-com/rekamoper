# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-05 18:01
from __future__ import unicode_literals

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import maker.models.sshstorage
import maker.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Apk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(blank=True, max_length=255)),
                ('file', models.FileField(storage=maker.storage.RepoStorage(), upload_to='')),
                ('version_name', models.CharField(blank=True, max_length=128)),
                ('version_code', models.PositiveIntegerField(default=0)),
                ('size', models.PositiveIntegerField(default=0)),
                ('signature', models.CharField(blank=True, max_length=512)),
                ('hash', models.CharField(blank=True, max_length=512)),
                ('hash_type', models.CharField(blank=True, max_length=32)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_downloading', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ApkPointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=maker.storage.RepoStorage(), upload_to=maker.storage.get_apk_file_path)),
                ('apk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maker.Apk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('summary', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('website', models.URLField(blank=True, max_length=2048)),
                ('icon', models.ImageField(default='fdroid-icon.png', upload_to=maker.storage.get_media_file_path_for_app)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='RemoteApkPointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=maker.storage.RepoStorage(), upload_to=maker.storage.get_apk_file_path)),
                ('url', models.URLField(max_length=2048)),
                ('apk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maker.Apk')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoteApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_id', models.CharField(blank=True, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('summary', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('website', models.URLField(blank=True, max_length=2048)),
                ('icon', models.ImageField(default='fdroid-icon.png', upload_to=maker.storage.get_media_file_path_for_app)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('icon_etag', models.CharField(blank=True, max_length=128)),
                ('last_updated_date', models.DateTimeField(blank=True)),
                ('category', models.ManyToManyField(blank=True, to='maker.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RemoteRepository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField(max_length=2048)),
                ('icon', models.ImageField(default='fdroid-icon.png', upload_to=maker.storage.get_media_file_path)),
                ('public_key', models.TextField(blank=True)),
                ('fingerprint', models.CharField(blank=True, max_length=512)),
                ('update_scheduled', models.BooleanField(default=False)),
                ('is_updating', models.BooleanField(default=False)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('pre_installed', models.BooleanField(default=False)),
                ('last_change_date', models.DateTimeField(auto_now=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Remote Repositories',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.URLField(max_length=2048)),
                ('icon', models.ImageField(default='fdroid-icon.png', upload_to=maker.storage.get_media_file_path)),
                ('public_key', models.TextField(blank=True)),
                ('fingerprint', models.CharField(blank=True, max_length=512)),
                ('update_scheduled', models.BooleanField(default=False)),
                ('is_updating', models.BooleanField(default=False)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('qrcode', models.ImageField(blank=True, upload_to=maker.storage.get_media_file_path)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_publication_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Repositories',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='S3Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(choices=[('s3', 'US Standard')], default='s3', max_length=32)),
                ('bucket', models.CharField(max_length=128)),
                ('accesskeyid', models.CharField(max_length=128)),
                ('secretkey', models.CharField(max_length=255)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maker.Repository')),
            ],
        ),
        migrations.CreateModel(
            name='SshStorage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, validators=[maker.models.sshstorage.UsernameValidator()])),
                ('host', models.CharField(max_length=256, validators=[maker.models.sshstorage.HostnameValidator()])),
                ('path', models.CharField(max_length=512, validators=[maker.models.sshstorage.PathValidator()])),
                ('identity_file', models.FileField(blank=True, storage=maker.storage.RepoStorage(), upload_to=maker.storage.get_identity_file_path)),
                ('repo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maker.Repository')),
            ],
        ),
        migrations.AddField(
            model_name='remoteapp',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maker.RemoteRepository'),
        ),
        migrations.AddField(
            model_name='remoteapkpointer',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maker.RemoteApp'),
        ),
        migrations.AddField(
            model_name='app',
            name='category',
            field=models.ManyToManyField(blank=True, to='maker.Category'),
        ),
        migrations.AddField(
            model_name='app',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maker.Repository'),
        ),
        migrations.AddField(
            model_name='apkpointer',
            name='app',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='maker.App'),
        ),
        migrations.AddField(
            model_name='apkpointer',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maker.Repository'),
        ),
        migrations.AlterUniqueTogether(
            name='apk',
            unique_together=set([('package_id', 'hash')]),
        ),
        migrations.AlterUniqueTogether(
            name='repository',
            unique_together=set([('url', 'fingerprint')]),
        ),
        migrations.AlterUniqueTogether(
            name='remoterepository',
            unique_together=set([('url', 'fingerprint')]),
        ),
        migrations.AlterUniqueTogether(
            name='remoteapp',
            unique_together=set([('package_id', 'repo')]),
        ),
        migrations.AlterUniqueTogether(
            name='remoteapkpointer',
            unique_together=set([('apk', 'app')]),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('user', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='app',
            unique_together=set([('package_id', 'repo')]),
        ),
        migrations.AlterUniqueTogether(
            name='apkpointer',
            unique_together=set([('apk', 'app')]),
        ),
    ]
