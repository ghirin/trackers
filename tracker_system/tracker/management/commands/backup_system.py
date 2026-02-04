# tracker/management/commands/backup_system.py
import os
import zipfile
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
import tempfile

class Command(BaseCommand):
    help = 'Создание полной резервной копии системы'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            help='Путь для сохранения резервной копии',
            default=None
        )
    
    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Создаем временную директорию
        with tempfile.TemporaryDirectory() as tmp_dir:
            backup_files = []
            
            # 1. Бэкап базы данных
            db_backup_path = os.path.join(tmp_dir, f'db_backup_{timestamp}.json')
            self.stdout.write(f'Создание бэкапа базы данных...')
            
            # Используем dumpdata для экспорта всех данных
            with open(db_backup_path, 'w', encoding='utf-8') as f:
                call_command('dumpdata', '--indent', '2', stdout=f)
            backup_files.append(db_backup_path)
            
            # 2. Бэкап медиа файлов
            if os.path.exists(settings.MEDIA_ROOT):
                media_backup_path = os.path.join(tmp_dir, f'media_backup_{timestamp}.zip')
                self.stdout.write(f'Создание бэкапа медиа файлов...')
                
                with zipfile.ZipFile(media_backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(settings.MEDIA_ROOT):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, settings.MEDIA_ROOT)
                            zipf.write(file_path, arcname)
                backup_files.append(media_backup_path)
            
            # 3. Создание файла конфигурации
            config_data = {
                'timestamp': timestamp,
                'django_version': '4.x',
                'project_name': 'tracker_system',
                'backup_type': 'full',
                'included': ['database', 'media_files']
            }
            
            import json
            config_path = os.path.join(tmp_dir, 'backup_info.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            backup_files.append(config_path)
            
            # 4. Создание финального архива
            output_path = options['output'] or os.path.join(
                settings.BASE_DIR, 'backups', f'full_backup_{timestamp}.zip'
            )
            
            # Создаем директорию для бэкапов если её нет
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            self.stdout.write(f'Создание финального архива {output_path}...')
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for backup_file in backup_files:
                    zipf.write(backup_file, os.path.basename(backup_file))
            
            self.stdout.write(self.style.SUCCESS(
                f'Резервная копия успешно создана: {output_path}'
            ))