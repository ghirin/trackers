# tracker/management/commands/restore_system.py
import os
import zipfile
import tempfile
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
from django.core.files.storage import default_storage

class Command(BaseCommand):
    help = 'Восстановление системы из резервной копии'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='Путь к файлу резервной копии'
        )
        parser.add_argument(
            '--no-media',
            action='store_true',
            help='Не восстанавливать медиа файлы'
        )
    
    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        if not os.path.exists(backup_file):
            self.stderr.write(self.style.ERROR(f'Файл не найден: {backup_file}'))
            return
        
        self.stdout.write(f'Восстановление из {backup_file}...')
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Распаковываем архив
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extractall(tmp_dir)
            
            # Читаем информацию о бэкапе
            info_path = os.path.join(tmp_dir, 'backup_info.json')
            if os.path.exists(info_path):
                with open(info_path, 'r', encoding='utf-8') as f:
                    backup_info = json.load(f)
                self.stdout.write(f'Информация о бэкапе: {backup_info}')
            
            # Восстанавливаем базу данных
            db_files = [f for f in os.listdir(tmp_dir) if f.startswith('db_backup_')]
            if db_files:
                db_file = os.path.join(tmp_dir, db_files[0])
                self.stdout.write(f'Восстановление базы данных из {db_file}...')
                
                # Очищаем базу данных
                call_command('flush', '--noinput')
                
                # Загружаем данные
                call_command('loaddata', db_file)
                
                self.stdout.write(self.style.SUCCESS('База данных восстановлена'))
            
            # Восстанавливаем медиа файлы
            if not options['no_media']:
                media_files = [f for f in os.listdir(tmp_dir) if f.startswith('media_backup_')]
                if media_files:
                    media_file = os.path.join(tmp_dir, media_files[0])
                    self.stdout.write(f'Восстановление медиа файлов из {media_file}...')
                    
                    with zipfile.ZipFile(media_file, 'r') as zipf:
                        for file_info in zipf.infolist():
                            # Пропускаем директории
                            if file_info.is_dir():
                                continue
                            
                            # Извлекаем файл
                            file_data = zipf.read(file_info.filename)
                            
                            # Сохраняем в медиа хранилище
                            file_path = os.path.join(settings.MEDIA_ROOT, file_info.filename)
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            
                            with open(file_path, 'wb') as f:
                                f.write(file_data)
                    
                    self.stdout.write(self.style.SUCCESS('Медиа файлы восстановлены'))
            
            self.stdout.write(self.style.SUCCESS('Восстановление завершено!'))