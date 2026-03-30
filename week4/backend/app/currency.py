"""
Modul konversi mata uang dari Rupiah ke USD, SGD, dan Yen.
Kurs statis:
- USD: 1 USD = 15_000 IDR
- SGD: 1 SGD = 11_000 IDR
- JPY: 1 JPY = 110 IDR
"""

def rupiah_to_usd(amount_idr: float) -> float:
    """Konversi Rupiah ke USD."""
    if amount_idr < 0:
        raise ValueError("Jumlah Rupiah tidak boleh negatif")
    return round(amount_idr / 15000, 2)

def rupiah_to_sgd(amount_idr: float) -> float:
    """Konversi Rupiah ke SGD."""
    if amount_idr < 0:
        raise ValueError("Jumlah Rupiah tidak boleh negatif")
    return round(amount_idr / 11000, 2)

def rupiah_to_yen(amount_idr: float) -> float:
    """Konversi Rupiah ke Yen."""
    if amount_idr < 0:
        raise ValueError("Jumlah Rupiah tidak boleh negatif")
    return round(amount_idr / 110, 2)
