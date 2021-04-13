import os
import tempfile
from pathlib import Path

from fullerenedatapraser.data.spiral import read_spiral_output

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"

TEST_PATH = os.path.dirname(__file__)


def test_read_spiral_output():
    """spiral output file combination Tests"""
    with tempfile.TemporaryDirectory(prefix=r"testspiral_", dir=os.path.join(TEST_PATH, Path(r"files/ADJ"))) as f:
        read_spiral_output(atomdir=os.path.join(TEST_PATH, Path(r"files\ADJ/atomadj")), circledir=os.path.join(TEST_PATH, Path(r"files/ADJ/circleadj")), storedir=Path(f))
