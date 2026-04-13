def normalize_whitespace(s: str) -> str:
    return "".join(s.split())

def getTimeInSec(seconds: float=0,
                 minutes:float=0,
                 hours:float=0,
                 days:float=0,
                 weeks:float=0) -> float:
    result = 0 + seconds
    result += minutes * 60
    result += hours * 60 * 60
    result += days * 24 * 60 * 60
    result += weeks * 7 * 24 * 60 * 60

    return result