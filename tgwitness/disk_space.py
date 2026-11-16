import shutil

RECORD_BYTES = 1024
WORKING_COPIES = 5
DISK_SHORT = "Not enough free disk space for this export. Free up space or choose a shorter period."


def disk_check(root, messages, min_free_mb):
    needed = max(0, messages) * RECORD_BYTES * WORKING_COPIES + min_free_mb * 1024**2
    free = shutil.disk_usage(root).free
    return {"estimated_messages": messages, "needed_bytes": needed, "free_bytes": free, "disk_ok": free >= needed}
