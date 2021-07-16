from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def get_img_metadata(fname):
    parser = createParser(fname)
    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            metadata = None
    if not metadata:
        print("Unable to extract metadata")
        return None
    return metadata


def view_img_metadata(f):
    metadata = get_img_metadata(f)
    return "\n".join([line for line in metadata.exportPlaintext()])

