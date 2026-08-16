import os
import shutil
import hashlib
import time


class AtomicFileEngine:

    def __init__(self):

        self.temp_suffix = ".tmp"

    def calculate_checksum(self, file_path):

        if not os.path.exists(file_path):

            return None

        hasher = hashlib.md5()

        with open(file_path, "rb") as f:

            while True:

                chunk = f.read(4096)

                if not chunk:

                    break

                hasher.update(chunk)

        return hasher.hexdigest()

    def atomic_write(self, file_path, content):

        temp_path = file_path + self.temp_suffix

        # SCRITTURA SU FILE TEMPORANEO

        with open(temp_path, "w") as f:

            f.write(content)

        # FORZA DISCO (riduce rischio perdita dati)

        f.flush()

        os.fsync(f.fileno())

        # RINOMINA ATOMICA

        os.replace(temp_path, file_path)

        print(f"[ATOMIC WRITE] {file_path}")

    def safe_copy(self, source, destination):

        if not os.path.exists(source):

            return

        temp_dest = destination + self.temp_suffix

        shutil.copy2(source, temp_dest)

        os.replace(temp_dest, destination)

        print(f"[ATOMIC COPY] {destination}")

    def is_file_valid(self, file_path):

        # controllo base: file non vuoto e leggibile

        if not os.path.exists(file_path):

            return False

        if os.path.getsize(file_path) == 0:

            return False

        try:

            with open(file_path, "r") as f:

                f.read(100)

            return True

        except:

            return False
