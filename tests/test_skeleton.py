import os

__author__ = "hanyanbo"
__copyright__ = "hanyanbo"
__license__ = "MIT"
TEST_PATH = os.path.abspath(os.path.dirname(__name__))
# def test_fib():
#     """API Tests"""
#     assert fib(1) == 1
#     assert fib(2) == 1
#     assert fib(7) == 13
#     with pytest.raises(AssertionError):
#         fib(-10)
#
#
# def test_main(capsys):
#     """CLI Tests"""
#     # capsys is a pytest fixture that allows asserts agains stdout/stderr
#     # https://docs.pytest.org/en/stable/capture.html
#     main(["7"])
#     captured = capsys.readouterr()
#     assert "The 7-th Fibonacci number is 13" in captured.out
#
#
# def test_cli():
#     res = os.popen("fibonacci 7")
#     assert "The 7-th Fibonacci number is 13" in res.read()
def test_cli():
    if not os.path.exists(os.path.join(TEST_PATH, r"files/ADJ/test")):
        os.mkdir(os.path.join(TEST_PATH, r"files/ADJ/test"))
    res = os.popen("Fullertool spiralIO --atom files/ADJ/atomadj --circle files/ADJ/circleadj -o files/ADJ/test")
    assert "error" not in res.read()
    [os.remove(os.path.abspath(os.path.join(TEST_PATH, r"files/ADJ/test", item))) for item in os.listdir(os.path.join(TEST_PATH, r"files/ADJ/test"))]

#
#
# def test_main_python():
#     res = os.popen("python -m fullerenedatapraser.skeleton 7")
#     assert "The 7-th Fibonacci number is 13" in res.read()
