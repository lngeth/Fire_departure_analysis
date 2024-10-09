from datetime import datetime, timedelta

def generate_date_ranges(start_date, end_date, interval_days=30):
  """Split start and end dates into tuples of smaller date interval
  """
  
  start = datetime.strptime(start_date, "%d/%m/%Y")
  end = datetime.strptime(end_date, "%d/%m/%Y")
  date_ranges = []

  while start < end:
    next_date = start + timedelta(days=interval_days)
    if next_date > end:
      next_date = end
    date_ranges.append((start.strftime("%d/%m/%Y"), next_date.strftime("%d/%m/%Y")))
    start = next_date + timedelta(days=1)

  return date_ranges