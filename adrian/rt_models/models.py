import os
import inspect
import importlib
from django.apps import apps
from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import models


def get_sourcecode_filename():
    return getattr(settings, 'RT_MODELS_PATH', 'rt_models.py')


def get_sourcecode_path(app_name):
    """
    Place to store runtime generated models
    :param app_name:
    :return:
    """
    filename = get_sourcecode_filename()
    return os.path.join(
        os.path.dirname(os.path.normpath(os.sys.modules[app_name].__file__)),
        filename)


def apply_to_db():
    """
    Apply registered models to db (generate migrations and apply them)
    :return:
    """
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])


def reg_model_python(model, touch_db=False):
    """
    Register new model using created type object
    :param model: Model to register
    :param touch_db: If true database will be changed immediately
    :return:
    """
    try:
        apps.get_registered_model(model._meta.app_label, model._meta.object_name)
    except LookupError:
        apps.register_model(model._meta.app_label, model)
    with open(get_sourcecode_path(model._meta.app_label), 'a') as f:
        f.writelines(inspect.getsource(model))
    if touch_db:
        apply_to_db()


def reg_model_attrs(model_name, app_label, attrs, base_models=(models.Model,)):
    """
    Register new model using dict of attrs.
    Example:
        reg_model_from_attrs(
            'Person',
            {
                'name': models.CharField(max_length=32),
                '__module__': 'myapp.models'
            }
        )

    :param model_name: Name of model class
    :param base_model: Base model for new runtime model.
    :param attrs: Info about model.
    :return:
    """
    model = type(model_name, (base_models,), attrs)
    model._meta.app_label = app_label
    reg_model_python(model)


def get_rt_model(app_label, model_name):
    return apps.get_model(app_label, model_name)


def import_rt_models():
    raise NotImplementedError
    # This will return a list of frame records, [1] is the frame
    # record of the caller.
    frame_records = inspect.stack()[1]
    # Index 1 of frame_records is the full path of the module,
    # we can then use inspect.getmodulename() to get the
    # module name from this path.
    calling_module = inspect.getmodulename(frame_records[1])
    importlib.import_module('.{0}'.format(get_sourcecode_filename()), calling_module)
