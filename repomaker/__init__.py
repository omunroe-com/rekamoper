import os
import sys

from django.core.checks import Error, register
from fdroidserver import common
from fdroidserver.exception import FDroidException

# The name of the default user. Please DO NOT CHANGE
DEFAULT_USER_NAME = 'user'


def runserver():
    execute([sys.argv[0], 'migrate'])  # TODO move into package hook?
    if len(sys.argv) <= 1 or sys.argv[1] != 'runserver':
        sys.argv = sys.argv[:1] + ['runserver'] + sys.argv[1:]
    sys.argv.append('--noreload')
    execute(sys.argv)


def process_tasks():
    if len(sys.argv) <= 1 or sys.argv[1] != 'process_tasks':
        sys.argv = sys.argv[:1] + ['process_tasks'] + sys.argv[1:]
    execute(sys.argv)


def execute(params):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repomaker.settings_desktop")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    # create DATA_DIR if it doesn't exist
    from django.conf import settings
    if not os.path.isdir(settings.DATA_DIR):
        os.makedirs(settings.DATA_DIR)

    # execute pending command
    execute_from_command_line(params)


@register()
def requirements_check(app_configs, **kwargs):  # pylint: disable=unused-argument
    errors = []
    config = {}
    common.fill_config_defaults(config)
    common.config = config
    if 'keytool' not in config:
        errors.append(
            Error(
                'Could not find `keytool` program.',
                hint='This program usually comes with Java. Try to install JRE. '
                     'On Debian-based system you can try to run '
                     '`apt install openjdk-8-jre-headless`.',
            )
        )
    if 'jarsigner' not in config and not common.set_command_in_config('apksigner'):
        errors.append(
            Error(
                'Could not find `jarsigner` or `apksigner`. At least one of them is required.',
                hint='Please install the missing tool. On Debian-based systems you can try to run '
                     '`apt install apksigner`.',
            )
        )
    try:
        common.SdkToolsPopen(['aapt', 'version'], output=False)
    except FDroidException:
        errors.append(
            Error(
                'Could not find `aapt` program.',
                hint='This program can be found in the Android SDK. '
                     'On Debian-based systems you can also try to run `apt install aapt` '
                     'to install it.',
            )
        )
    return errors
