import cloudinary.api
from django.core.management.base import BaseCommand
from core.models import GalleryItem

FOLDER_TO_CATEGORY = {
    'srissnehidi-website/certificates': 'certificates',
    'srissnehidi-website/classes': 'classes',
    'srissnehidi-website/aari-students-work': 'aari_work',
}


def fetch_all_resources():
    resources = []
    result = cloudinary.api.resources(type='upload', max_results=500)
    resources.extend(result.get('resources', []))
    while 'next_cursor' in result:
        result = cloudinary.api.resources(
            type='upload',
            max_results=500,
            next_cursor=result['next_cursor'],
        )
        resources.extend(result.get('resources', []))
    return resources


class Command(BaseCommand):
    help = 'Sync images from Cloudinary folders into the GalleryItem database'

    def handle(self, *args, **options):
        existing_public_ids = set(
            GalleryItem.objects.filter(image__isnull=False)
            .values_list('image', flat=True)
        )

        self.stdout.write('Fetching all Cloudinary resources...')
        all_resources = fetch_all_resources()
        self.stdout.write(f'Found {len(all_resources)} total resources')

        counts = {cat: 0 for cat in FOLDER_TO_CATEGORY.values()}

        for resource in all_resources:
            asset_folder = resource.get('asset_folder', '')
            category = FOLDER_TO_CATEGORY.get(asset_folder)
            if not category:
                continue

            public_id = resource['public_id']
            if public_id in existing_public_ids:
                continue

            filename = public_id.split('/')[-1]
            title = filename.replace('_', ' ').replace('-', ' ').title()
            GalleryItem.objects.create(
                title=title,
                category=category,
                media_type='image',
                image=public_id,
            )
            existing_public_ids.add(public_id)
            counts[category] += 1

        for folder, category in FOLDER_TO_CATEGORY.items():
            folder_name = folder.split('/')[-1]
            self.stdout.write(
                self.style.SUCCESS(f'  {folder_name}: added {counts[category]} images [{category}]')
            )

        total = sum(counts.values())
        self.stdout.write(self.style.SUCCESS(f'\nDone. Total new entries: {total}'))
