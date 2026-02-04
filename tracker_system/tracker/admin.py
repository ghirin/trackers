from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
try:
    from import_export import resources
    from import_export.admin import ImportExportModelAdmin
    from import_export.formats import base_formats
except Exception:
    resources = None
    ImportExportModelAdmin = admin.ModelAdmin
    base_formats = []

from django.db.models import Q
from .models import Car, Tracker, InstallationHistory, OrderDocument, Location, ActionLog

# Ресурсы для импорта-экспорта
class CarResource(resources.ModelResource):
    class Meta:
        model = Car
        fields = (
            'id', 'board_number', 'model', 'location', 
            'comment', 'is_active', 'created_at'
        )
        export_order = fields

class TrackerResource(resources.ModelResource):
    class Meta:
        model = Tracker
        fields = (
            'id', 'imei', 'serial_number', 'inventory_number_tracker',
            'inventory_number_antenna', 'model', 'protocol', 'holder_number',
            'sim_old', 'n_card', 'sim_new', 'comment', 'is_active', 'created_at'
        )
        export_order = fields

# Inline для документов
class OrderDocumentInline(admin.TabularInline):
    model = OrderDocument
    extra = 1
    fields = ('document', 'document_type', 'document_number', 'issue_date', 'comment')
    readonly_fields = ('uploaded_at',)

# Inline для истории установки
class InstallationHistoryInline(admin.TabularInline):
    model = InstallationHistory
    extra = 1
    fields = ('tracker', 'installation_date', 'removal_date', 'is_active', 'comment')
    readonly_fields = ('created_at',)

# Админ-класс для Car
@admin.register(Car)
class CarAdmin(ImportExportModelAdmin):
    resource_class = CarResource
    formats = [base_formats.XLSX, base_formats.CSV]
    
    list_display = (
        'board_number', 'model', 'location', 
        'is_active', 'created_at', 'documents_link',
        'installation_history_link'
    )
    
    list_filter = ('model', 'is_active', 'created_at')
    search_fields = ('board_number', 'location', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('board_number', 'model', 'is_active')
        }),
        ('Дополнительная информация', {
            'fields': ('location', 'comment'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [OrderDocumentInline, InstallationHistoryInline]
    
    def documents_link(self, obj):
        count = obj.order_documents.count()
        url = reverse('admin:tracker_orderdocument_changelist') + f'?car__id__exact={obj.id}'
        return format_html('<a href="{}">Документы ({})</a>', url, count)
    documents_link.short_description = 'Документы'
    
    def installation_history_link(self, obj):
        count = obj.installations.count()
        url = reverse('admin:tracker_installationhistory_changelist') + f'?car__id__exact={obj.id}'
        return format_html('<a href="{}">Установки ({})</a>', url, count)
    installation_history_link.short_description = 'История установок'

# Админ-класс для Tracker
@admin.register(Tracker)
class TrackerAdmin(ImportExportModelAdmin):
    resource_class = TrackerResource
    formats = [base_formats.XLSX, base_formats.CSV]
    
    list_display = (
        'serial_number', 'imei', 'model', 'protocol',
        'inventory_number_tracker', 'is_active', 'created_at',
        'installation_history_link'
    )
    
    list_filter = ('protocol', 'is_active', 'created_at')
    search_fields = (
        'serial_number', 'imei', 'inventory_number_tracker',
        'inventory_number_antenna', 'comment'
    )
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'serial_number', 'imei', 'model', 'protocol',
                'inventory_number_tracker', 'inventory_number_antenna'
            )
        }),
        ('SIM карты', {
            'fields': ('holder_number', 'sim_old', 'n_card', 'sim_new'),
            'classes': ('collapse',)
        }),
        ('Дополнительная информация', {
            'fields': ('comment', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def installation_history_link(self, obj):
        count = obj.installations.count()
        url = reverse('admin:tracker_installationhistory_changelist') + f'?tracker__id__exact={obj.id}'
        return format_html('<a href="{}">Установки ({})</a>', url, count)
    installation_history_link.short_description = 'История установок'

# Админ-класс для InstallationHistory
@admin.register(InstallationHistory)
class InstallationHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'car', 'tracker', 'installation_date', 
        'removal_date', 'is_active', 'created_at'
    )
    
    list_filter = ('is_active', 'installation_date', 'created_at')
    search_fields = (
        'car__board_number', 'tracker__serial_number',
        'tracker__imei', 'comment'
    )
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('car', 'tracker', 'is_active')
        }),
        ('Даты', {
            'fields': ('installation_date', 'removal_date')
        }),
        ('Дополнительная информация', {
            'fields': ('comment', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('car', 'tracker')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Админ-класс для OrderDocument
@admin.register(OrderDocument)
class OrderDocumentAdmin(admin.ModelAdmin):
    list_display = (
        'car', 'document_type', 'document_number',
        'issue_date', 'uploaded_at', 'document_link'
    )
    
    list_filter = ('document_type', 'issue_date', 'uploaded_at')
    search_fields = (
        'car__board_number', 'document_type',
        'document_number', 'comment'
    )
    readonly_fields = ('uploaded_at', 'filename')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('car', 'document')
        }),
        ('Информация о документе', {
            'fields': ('document_type', 'document_number', 'issue_date')
        }),
        ('Дополнительная информация', {
            'fields': ('comment', 'uploaded_at', 'filename'),
            'classes': ('collapse',)
        })
    )
    
    def document_link(self, obj):
        if obj.document:
            return format_html(
                '<a href="{}" target="_blank">Просмотреть</a>',
                obj.document.url
            )
        return "-"
    document_link.short_description = 'Документ'
    
    def filename(self, obj):
        return obj.filename()
    filename.short_description = 'Имя файла'


# ------------------------
# ActionLog admin + export
# ------------------------
import csv
import json
from django.http import HttpResponse

@admin.action(description='Export selected logs as CSV')
def export_logs_csv(modeladmin, request, queryset):
    fieldnames = ['timestamp', 'user', 'action', 'object_repr', 'content_type', 'object_id', 'changes', 'request_path', 'ip_address']
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="action_logs.csv"'
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for log in queryset:
        writer.writerow({
            'timestamp': log.timestamp.isoformat(),
            'user': log.user.username if log.user else '',
            'action': log.action,
            'object_repr': log.object_repr,
            'content_type': str(log.content_type),
            'object_id': log.object_id,
            'changes': json.dumps(log.changes, ensure_ascii=False),
            'request_path': log.request_path or '',
            'ip_address': log.ip_address or '',
        })
    return response

@admin.action(description='Export selected logs as JSON')
def export_logs_json(modeladmin, request, queryset):
    data = []
    for log in queryset:
        data.append({
            'timestamp': log.timestamp.isoformat(),
            'user': log.user.username if log.user else None,
            'action': log.action,
            'object_repr': log.object_repr,
            'content_type': str(log.content_type),
            'object_id': log.object_id,
            'changes': log.changes,
            'request_path': log.request_path or '',
            'ip_address': log.ip_address or '',
        })
    response = HttpResponse(json.dumps(data, ensure_ascii=False, indent=2), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="action_logs.json"'
    return response


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'object_repr', 'content_type', 'object_id')
    list_filter = ('action', 'content_type', 'timestamp')
    search_fields = ('user__username', 'object_repr', 'changes')
    readonly_fields = ('timestamp', 'user', 'action', 'object_repr', 'content_type', 'object_id', 'changes', 'request_path', 'ip_address')
    actions = [export_logs_csv, export_logs_json]
