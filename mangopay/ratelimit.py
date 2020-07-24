class RateLimit:

    interval_minutes = 0
    calls_made = 0
    calls_remaining = 0
    reset_time_millis = 0

    def __init__(self, interval_minutes):
        self.interval_minutes = interval_minutes

