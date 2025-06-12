#!/usr/bin/python3

import sys
import argparse
import zipfile
from io import BytesIO
import tarfile


class SlipperArguments:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-p', '--payload', action='append', nargs=2,
                                 metavar=('filename', 'contents'),
                                 help='add filename with contents to archive')
        self.parser.add_argument('-z', '--zip_filename', default=None,
                                 help='create a zip with given name')
        self.parser.add_argument('-t', '--tar_filename', default=None,
                                 help='create a tar with given name')
        self.parser.add_argument('-i', '--input_filename', default=None,
                                 help='create a tar with given name')

    def parse_arguments(self, args):
        return self.parser.parse_args(args)


class Slipper:
    def __init__(self, parsed):
        self.parsed = parsed

    def create_tar(self):
        with tarfile.TarFile(self.parsed.tar_filename, 'w') as tar:
            for payload in self.parsed.payload:
                tarinfo = tarfile.TarInfo(name=payload[0])
                pl = payload[1].encode('utf8')
                tarinfo.size = len(pl)
                tar.addfile(tarinfo, BytesIO(pl))
            if self.parsed.input_filename:
                with tarfile.TarFile(self.parsed.input_filename, 'r') as existing_tar:
                    for member_name in existing_tar.getmembers():
                        member_data = existing_tar.extractfile(member_name).read()
                        tar.addfile(member_name, BytesIO(member_data))

    def create_zip(self):
        with open(self.parsed.zip_filename, 'wb') as zip:
            rawdata = BytesIO()
            zipinmem = zipfile.ZipFile(rawdata, 'w', zipfile.ZIP_DEFLATED)
            for payload in self.parsed.payload:
                zipinmem.writestr(payload[0], payload[1])
            if self.parsed.input_filename:
                with zipfile.ZipFile(self.parsed.input_filename, 'r') as existing_zip:
                    for member_name in existing_zip.infolist():
                        member_data = existing_zip.read(member_name)
                        zipinmem.writestr(member_name, member_data)

            zipinmem.close()
            zip.write(rawdata.getvalue())


if __name__ == '__main__':
    parsed = SlipperArguments().parse_arguments(sys.argv[1:])
    slipper = Slipper(parsed)

    if parsed.tar_filename:
        slipper.create_tar()

    if parsed.zip_filename:
        slipper.create_zip()
