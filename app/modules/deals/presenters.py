"""Presentation of money for the deals screens - formatting never reaches the domain."""

from decimal import Decimal

#: Symbol and separators per locale; amounts are stored as cents plus ISO 4217.
_SYMBOLS = {"BRL": "R$", "USD": "US$", "EUR": "€"}
_SEPARATORS = {"en": (",", "."), "pt-BR": (".", ","), "es": (".", ",")}


def money(amount_cents: int, currency: str, locale: str) -> str:
    """Render `amount_cents` of `currency` the way `locale` writes numbers."""
    thousands, decimal = _SEPARATORS.get(locale, _SEPARATORS["en"])
    whole = f"{Decimal(int(amount_cents or 0)) / 100:,.2f}"
    localized = whole.replace(",", "\u0000").replace(".", decimal).replace("\u0000", thousands)
    return f"{_SYMBOLS.get(currency, currency)} {localized}"
