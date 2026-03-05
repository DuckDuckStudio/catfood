import catfood.constant


def test_constant():
    assert isinstance(catfood.constant.VERSION, str)
    assert isinstance(catfood.constant.YES, tuple)
    assert isinstance(catfood.constant.NO, tuple)
