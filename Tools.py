from datetime import datetime, timedelta
import pandas as pd

def generate_date_ranges_days(start_date, end_date, interval_days=30):
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

def generate_date_ranges_months(start, end, months=2):
  date_ranges = []
  current_start = pd.to_datetime(start, format='%d/%m/%Y')
  end = pd.to_datetime(end, format='%d/%m/%Y')

  while current_start <= end:
    # Calculer la fin de l'intervalle (ajouter 2 mois)
    current_end = current_start + pd.DateOffset(months=months) - timedelta(days=1)

    # Si la date de fin dépasse la date finale donnée, on ajuste
    if current_end > end:
      current_end = end
    
    # Ajouter l'intervalle (start, end) à la liste
    date_ranges.append((current_start.strftime('%d/%m/%Y'), current_end.strftime('%d/%m/%Y')))

    # Déplacer la date de début au début du prochain intervalle
    current_start = current_end + timedelta(days=1)

  return date_ranges