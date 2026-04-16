# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Recopilar módulos completos
django_datas, django_binaries, django_hiddenimports = collect_all('django')
whitenoise_datas, whitenoise_binaries, whitenoise_hiddenimports = collect_all('whitenoise')

# Recopilar datos de crispy_forms y crispy_bootstrap4 (incluye templates)
crispy_datas = collect_data_files('crispy_forms')
crispy_bootstrap4_datas = collect_data_files('crispy_bootstrap4')

# Recopilar submodulos
crispy_submodulos = collect_submodules('crispy_forms')
crispy_bootstrap4_submodulos = collect_submodules('crispy_bootstrap4')

a = Analysis(
    ['run_local.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('Jovenes_Aventureros', 'Jovenes_Aventureros'),
        ('Inicio', 'Inicio'),
        ('Socios', 'Socios'),
        ('data', 'data'),
    ] + django_datas + whitenoise_datas + crispy_datas + crispy_bootstrap4_datas,
    hiddenimports=[
        'django',
        'whitenoise',
        'crispy_forms',
        'crispy_bootstrap4',
        'widget_tweaks',
        'tailwind',
        'Inicio',
        'Socios',
        'csv',
        'datetime',
        # Templatetags de crispy_forms
        'crispy_forms.templatetags',
        'crispy_forms.templatetags.crispy_forms_filters',
        'crispy_forms.templatetags.crispy_forms_tags',
        'crispy_bootstrap4.templatetags',
        'crispy_bootstrap4.templatetags.crispy_bootstrap4',
        # Template loaders
        'django.template.loaders.app_directories',
        'django.template.backends.django',
    ] + django_hiddenimports + whitenoise_hiddenimports + crispy_submodulos + crispy_bootstrap4_submodulos,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'psycopg2',
        'psycopg2_binary',
        'dj_database_url',
        'tkinter',
        'unittest',
        'pdb',
        'doctest',
        'distutils.tests',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='JovenesAventureros',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Cambia a False cuando todo funcione
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)