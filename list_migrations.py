# list_migrations.py

import os, time

folder = os.path.join("migrations", "versions")
output = "listado_migrations_versions.txt"
found = False

with open(output, "w", encoding="utf-8") as f:
    if not os.path.isdir(folder):
        f.write("El directorio migrations/versions no existe.\n")
    else:
        for fn in sorted(os.listdir(folder)):
            path = os.path.join(folder, fn)
            if os.path.isfile(path):
                mtime = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime(os.path.getmtime(path))
                )
                f.write(f"{fn}\t{mtime}\n")
                found = True

        if not found:
            f.write("No migration files found in migrations/versions/\n")

print(f"Wrote {output}")
