import json
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from .models import ActionLog
from .middleware import get_current_user, get_current_request

def _serialize_value(value):
    try:
        if hasattr(value, 'isoformat'):
            return value.isoformat()
        return str(value)
    except Exception:
        return str(value)

@receiver(pre_save)
def _pre_save(sender, instance, **kwargs):
    # Ignore our ActionLog model to prevent recursion
    if sender is ActionLog:
        return
    if not hasattr(instance, 'pk') or instance.pk is None:
        instance._pre_save_snapshot = None
        return
    try:
        old = sender.objects.filter(pk=instance.pk).values().first()
        instance._pre_save_snapshot = old
    except Exception:
        instance._pre_save_snapshot = None

@receiver(post_save)
def _post_save(sender, instance, created, **kwargs):
    if sender is ActionLog:
        return
    user = get_current_user()
    request = get_current_request()
    try:
        ct = ContentType.objects.get_for_model(sender)
    except Exception:
        # ContentType table may not be ready during migrations/tests; skip logging
        return
    # Ensure ActionLog table exists before attempting to write to it (migrations may be running)
    from django.db import connection
    if ActionLog._meta.db_table not in connection.introspection.table_names():
        return
    object_repr = str(instance)
    request_path = request.path if request is not None else ''
    ip = ''
    if request is not None:
        ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR', '')
    changes = None
    if created:
        # Record all fields
        data = {}
        for f in instance._meta.fields:
            name = f.name
            data[name] = _serialize_value(getattr(instance, name, None))
        changes = data
        action = 'create'
    else:
        old = getattr(instance, '_pre_save_snapshot', None)
        new = {}
        diffs = {}
        for f in instance._meta.fields:
            name = f.name
            new_val = getattr(instance, name, None)
            new[name] = _serialize_value(new_val)
            old_val = None
            if old:
                old_val = old.get(name)
            if _serialize_value(old_val) != _serialize_value(new_val):
                diffs[name] = {'old': _serialize_value(old_val), 'new': _serialize_value(new_val)}
        if diffs:
            changes = diffs
            action = 'update'
        else:
            # nothing changed; skip logging
            return

    # Save ActionLog
    try:
        ActionLog.objects.create(
            user=user if getattr(user, 'is_authenticated', False) else None,
            content_type=ct,
            object_id=str(getattr(instance, 'pk', '')),
            object_repr=object_repr,
            action=action,
            changes=changes,
            request_path=request_path,
            ip_address=ip
        )
        # After creating a log, ensure storage doesn't grow beyond threshold
        try:
            ActionLog.trim_logs()
        except Exception:
            # Never let trimming break user request
            pass
    except Exception as e:
        # avoid failing the request because logging failed
        print('ActionLog save error:', e)

@receiver(pre_delete)
def _pre_delete(sender, instance, **kwargs):
    if sender is ActionLog:
        return
    try:
        data = {}
        for f in instance._meta.fields:
            name = f.name
            data[name] = _serialize_value(getattr(instance, name, None))
        instance._pre_delete_snapshot = data
    except Exception:
        instance._pre_delete_snapshot = None

@receiver(post_delete)
def _post_delete(sender, instance, **kwargs):
    if sender is ActionLog:
        return
    user = get_current_user()
    request = get_current_request()
    try:
        ct = ContentType.objects.get_for_model(sender)
    except Exception:
        # ContentType table may not be ready during migrations/tests; skip logging
        return
    # Ensure ActionLog table exists before attempting to write to it (migrations may be running)
    from django.db import connection
    if ActionLog._meta.db_table not in connection.introspection.table_names():
        return
    object_repr = str(instance)
    request_path = request.path if request is not None else ''
    ip = ''
    if request is not None:
        ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR', '')
    changes = getattr(instance, '_pre_delete_snapshot', None)
    try:
        ActionLog.objects.create(
            user=user if getattr(user, 'is_authenticated', False) else None,
            content_type=ct,
            object_id=str(getattr(instance, 'pk', '')),
            object_repr=object_repr,
            action='delete',
            changes=changes,
            request_path=request_path,
            ip_address=ip
        )
        # Trim logs after delete event as well
        try:
            ActionLog.trim_logs()
        except Exception:
            pass
    except Exception as e:
        print('ActionLog save error (delete):', e)
