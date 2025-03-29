import numpy as np


def is_local_min(prices: np.ndarray) -> bool:
    """
    Returns True if the prices array shows a local minimum.
    Checks if the first half of the differences are negative
    and the second half are positive.
    """
    # Account for minimum logical length
    if len(prices) < 3:
        return False
    
    # Calculate differences between consecutive prices
    diffs = np.diff(prices)

    # Take the floor of the length of the array
    half = len(diffs) // 2

    # If the first half differences are less than 0, the trend is negative
    # If the trend is negative and then it changes, it's a bounce
    return (diffs[:half] < 0).all() and (diffs[half:] > 0).all()

def is_local_max(prices: np.ndarray) -> bool:
    """
    Returns True if the prices array shows a local maximum.
    Checks if the first half of the differences are positive
    and the second half are negative.
    """
    # Account for minimum logical length
    if len(prices) < 3:
        return False
    
    # Calculate differences between consecutive prices
    diffs = np.diff(prices)

    # Take the floor of the length of the array
    half = len(diffs) // 2
    
    # If the first half differences are less than 0, the trend is negative
    # If the trend is negative and then it changes, it's a bounce
    return (diffs[:half] > 0).all() and (diffs[half:] < 0).all()