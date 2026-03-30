import pytest
from backend.app import currency

def test_rupiah_to_usd():
    assert currency.rupiah_to_usd(15000) == 1.0
    assert currency.rupiah_to_usd(30000) == 2.0
    assert currency.rupiah_to_usd(0) == 0.0
    assert currency.rupiah_to_usd(7500) == 0.5
    
def test_rupiah_to_usd_negative():
    with pytest.raises(ValueError):
        currency.rupiah_to_usd(-1000)

def test_rupiah_to_sgd():
    assert currency.rupiah_to_sgd(11000) == 1.0
    assert currency.rupiah_to_sgd(22000) == 2.0
    assert currency.rupiah_to_sgd(0) == 0.0
    assert currency.rupiah_to_sgd(5500) == 0.5

def test_rupiah_to_sgd_negative():
    with pytest.raises(ValueError):
        currency.rupiah_to_sgd(-500)

def test_rupiah_to_yen():
    assert currency.rupiah_to_yen(110) == 1.0
    assert currency.rupiah_to_yen(220) == 2.0
    assert currency.rupiah_to_yen(0) == 0.0
    assert currency.rupiah_to_yen(55) == 0.5

def test_rupiah_to_yen_negative():
    with pytest.raises(ValueError):
        currency.rupiah_to_yen(-10)
