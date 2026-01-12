from django.core.management.base import BaseCommand
from users.models import User
from shops.models import Shop


class Command(BaseCommand):
    help = "Create default shop and manager"

    def handle(self, *args, **kwargs):
        shop, _ = Shop.objects.get_or_create(
            name="DG Makeover Studio – Main Branch"
        )

        if User.objects.filter(username="manager").exists():
            self.stdout.write(self.style.WARNING("Manager already exists"))
            return

        User.objects.create_user(
            username="manager",
            password="manager123",
            role="MANAGER",
            shop=shop
        )

        self.stdout.write(
            self.style.SUCCESS("Manager created successfully")
        )
