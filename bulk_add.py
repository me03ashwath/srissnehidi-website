import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srissnehidi.settings')
django.setup()

from core.models import GalleryItem

GalleryItem.objects.all().delete()

public_ids = [
    "b2DSC01266_dutjkh",
    "b3DSC01240_wijnll",
    "b4DSC01252_sjy4hf",
    "b1DSC01307_dphuj2",
    "20240831_191434_k3dyls",
    "20240803_084846_v4avpg",
    "20251207_192721_rjzz2x",
    "20251204_123235_nuidy1",
    "IMG-20240804-WA0050_1_otyoed",
    "20240203_190341_qguxru",
    "20240204_180502_s5mott",
    "20220423_115604_amslwj",
    "20230601_184528_mpvpzi",
    "20230905_113959_aueuoh",
    "20240202_155126_si8qc3",
    "20240803_085203_eomcp6",
]

for i, pid in enumerate(public_ids):
    GalleryItem.objects.create(
        title=f"Certificate {i+1}",
        category="Certificates Issued",
        media_type="image",
        image=pid
    )

print(f"Done! Created {len(public_ids)} items.")