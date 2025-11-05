from django.core.management.base import BaseCommand, CommandError

from ip_tracking.models import BlockedIP


class Command(BaseCommand):
    help = "Blocks a specific IP address by adding it to the BlockedIP table"

    def add_arguments(self, parser):
        # Expect one argument: the IP address
        parser.add_argument('ip_address', type=str, help='IP address to block')

    def handle(self, *args, **options):
        ip_address = options['ip_address']

        # Check if already blocked
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f'IP {ip_address} is already blocked.'))
        else:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
