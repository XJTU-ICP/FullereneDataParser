import tempfile

from fullerenedatapraser.data.spiral import read_spiral_output

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"


def test_read_spiral_output():
    """spiral output file combination Tests"""
    with tempfile.TemporaryDirectory(prefix=f"testspiral_", dir="files\ADJ") as f:
        read_spiral_output(atomdir=r"files\ADJ\atomadj", circledir=r"files\ADJ\circleadj", storedir=f)
