import os
from ursa_major import settings

for dir in [settings.SRC_DIR, settings.DEST_DIR]:
    if not os.path.isdir(dir):
        os.makedirs(dir)
