import pandas as pd
from typing import Iterable


def validate_input_dataframe(data: pd.DataFrame) -> None:
    """
    Ensure `data` is a non-empty pandas DataFrame.

    Raises
    ------
    TypeError  — if data is not a DataFrame
    ValueError — if data is empty
    """
    if not isinstance(data, pd.DataFrame):
        raise TypeError(f"Expected a pandas DataFrame, got {type(data).__name__}")
    if data.empty:
        raise ValueError("Input DataFrame is empty")


def check_required_columns(data: pd.DataFrame, required: Iterable[str]) -> None:
    """
    Verify that all required columns exist in `data`.

    Parameters
    ----------
    data     : pd.DataFrame
    required : iterable of column name strings

    Raises
    ------
    KeyError — listing every missing column
    """
    missing = [col for col in required if col not in data.columns]
    if missing:
        raise KeyError(
            f"Missing required column(s): {missing}. "
            f"Available columns: {list(data.columns)}"
        )


def handle_missing_values(
    series: pd.Series,
    strategy: str = "drop",
) -> pd.Series:
    """
    Handle NaN values in a Series produced by an indicator.

    Parameters
    ----------
    series   : pd.Series
    strategy : str
        'drop'    — remove NaN rows (default)
        'ffill'   — forward-fill
        'bfill'   — backward-fill
        'zero'    — fill with 0
        'keep'    — do nothing

    Returns
    -------
    pd.Series — cleaned series (copy, never modifies input)
    """
    s = series.copy()
    if strategy == "drop":
        return s.dropna()
    if strategy == "ffill":
        return s.ffill()
    if strategy == "bfill":
        return s.bfill()
    if strategy == "zero":
        return s.fillna(0)
    if strategy == "keep":
        return s
    raise ValueError(
        f"Unknown strategy '{strategy}'. "
        "Choose from: 'drop', 'ffill', 'bfill', 'zero', 'keep'"
    )


def rolling_mean(series: pd.Series, period: int, min_periods: int | None = None) -> pd.Series:
    """
    Simple rolling mean wrapper — keeps naming and min_periods consistent.

    Parameters
    ----------
    series      : pd.Series
    period      : int
    min_periods : int | None — defaults to `period` (no partial windows)

    Returns
    -------
    pd.Series
    """
    if not isinstance(period, int) or period <= 0:
        raise ValueError(f"period must be a positive int, got {period!r}")
    if min_periods is None:
        min_periods = period
    return series.rolling(window=period, min_periods=min_periods).mean()


def normalize_column_names(data: pd.DataFrame) -> pd.DataFrame:
    """
    Lowercase all column names and strip whitespace.
    Returns a copy — original DataFrame is never modified.

    Useful for harmonising feeds that may mix 'Close' / 'close' / ' Close'.
    """
    df = data.copy()
    df.columns = [col.strip().lower() for col in df.columns]
    return df
