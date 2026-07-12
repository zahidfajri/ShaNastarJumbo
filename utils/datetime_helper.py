from datetime import datetime, timezone
from zoneinfo import ZoneInfo


# =====================================
# TIMEZONE
# =====================================

JAKARTA_TZ = ZoneInfo("Asia/Jakarta")


# =====================================
# CONVERT UTC -> JAKARTA
# =====================================

def to_jakarta_datetime(
    timestamp: str
):

    dt = datetime.fromisoformat(
        timestamp
    )

    # Supabase timestamps are UTC
    if dt.tzinfo is None:

        dt = dt.replace(
            tzinfo=timezone.utc
        )

    return dt.astimezone(
        JAKARTA_TZ
    )


# =====================================
# FORMAT DATETIME
# =====================================

def format_jakarta_datetime(
    timestamp: str,
    show_timezone: bool = True
):

    jakarta_time = to_jakarta_datetime(
        timestamp
    )

    if show_timezone:

        return jakarta_time.strftime(
            "%d %b %Y, %H:%M WIB"
        )

    return jakarta_time.strftime(
        "%d %b %Y, %H:%M"
    )


# =====================================
# TODAY IN JAKARTA
# =====================================

def get_jakarta_today():

    return datetime.now(
        JAKARTA_TZ
    ).date()
    
# =====================================
# CURRENT JAKARTA DATETIME
# =====================================

def get_jakarta_now():

    return datetime.now(
        JAKARTA_TZ
    )