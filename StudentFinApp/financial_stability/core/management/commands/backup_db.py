import os
import datetime
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup MySQL database to a file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            default='backups',
            help='Directory where backups will be stored',
        )
        
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Compress the backup file with gzip',
        )

    def handle(self, *args, **options):
        # Create backup directory if it doesn't exist
        output_dir = options['output_dir']
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Generate backup filename with timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"bachatbuddy_{timestamp}.sql"
        filepath = os.path.join(output_dir, filename)
        
        # Get database credentials from settings
        db_settings = settings.DATABASES['default']
        user = db_settings['USER']
        password = db_settings['PASSWORD']
        database = db_settings['NAME']
        host = db_settings['HOST']
        port = db_settings['PORT']
        
        # MySQL dump command
        cmd = [
            'mysqldump',
            f'--user={user}',
            f'--password={password}',
            f'--host={host}',
            f'--port={port}',
            '--single-transaction',
            '--quick',
            '--lock-tables=false',
            database
        ]
        
        # Execute the backup
        try:
            with open(filepath, 'w') as f:
                self.stdout.write(self.style.SUCCESS('Starting database backup...'))
                subprocess.run(cmd, stdout=f, check=True)
            
            # Compress if requested
            if options['compress']:
                compress_cmd = ['gzip', filepath]
                subprocess.run(compress_cmd, check=True)
                filepath = f"{filepath}.gz"
                self.stdout.write(self.style.SUCCESS(f'Backup compressed to {filepath}'))
            
            self.stdout.write(self.style.SUCCESS(f'Database backup completed: {filepath}'))
            
        except subprocess.CalledProcessError as e:
            raise CommandError(f'Database backup failed: {e}')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}') 