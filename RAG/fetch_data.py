import os
import argparse
import requests
import pandas as pd
from io import StringIO


DEFAULT_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY', 'DEM38RUWFXNK6LFA')


def get_weekly_adjusted(symbol: str, api_key: str = DEFAULT_API_KEY, datatype: str = 'json') -> pd.DataFrame:
	"""Fetch TIME_SERIES_WEEKLY_ADJUSTED for `symbol` from AlphaVantage and return a DataFrame.

	Returns DataFrame indexed by date (last trading day of week) with numeric columns.
	"""
	base_url = 'https://www.alphavantage.co/query'
	params = {
		'function': 'TIME_SERIES_WEEKLY_ADJUSTED',
		'symbol': symbol,
		'apikey': api_key,
		'datatype': datatype,
	}

	r = requests.get(base_url, params=params, timeout=30)
	r.raise_for_status()

	if datatype == 'csv':
		df = pd.read_csv(StringIO(r.text), index_col=0, parse_dates=True)
		return df.sort_index()

	data = r.json()
	# Rate-limit or errors
	if not isinstance(data, dict):
		raise ValueError('Unexpected response format from API')
	if 'Error Message' in data:
		raise ValueError(data['Error Message'])
	if 'Note' in data:
		raise RuntimeError(data['Note'])

	ts = data.get('Weekly Adjusted Time Series') or data.get('Weekly Time Series')
	if not ts:
		raise ValueError('Time series not found in API response')

	df = pd.DataFrame.from_dict(ts, orient='index')
	# Normalize column names like '1. open' -> 'open'
	def clean_col(c):
		return c.split('. ', 1)[1] if '. ' in c else c

	df.columns = [clean_col(c) for c in df.columns]
	# convert types
	df = df.apply(pd.to_numeric, errors='coerce')
	df.index = pd.to_datetime(df.index)
	df = df.sort_index()
	return df


def main():
	parser = argparse.ArgumentParser(description='Fetch Weekly Adjusted Time Series from AlphaVantage')
	parser.add_argument('symbol', help='Equity symbol, e.g. IBM')
	parser.add_argument('--apikey', help='AlphaVantage API key (or set ALPHAVANTAGE_API_KEY env var)')
	parser.add_argument('--datatype', choices=['json', 'csv'], default='json')
	parser.add_argument('--save', action='store_true', help='Save CSV to data/processed')
	parser.add_argument('--outdir', default=os.path.join('data', 'processed'), help='Output directory for CSV')

	args = parser.parse_args()
	api_key = args.apikey or DEFAULT_API_KEY

	try:
		df = get_weekly_adjusted(args.symbol, api_key=api_key, datatype=args.datatype)
	except Exception as e:
		print('Error fetching data:', e)
		return

	print(df.tail())

	if args.save:
		os.makedirs(args.outdir, exist_ok=True)
		out_path = os.path.join(args.outdir, f'{args.symbol}_weekly_adjusted.csv')
		df.to_csv(out_path)
		print('Saved CSV to', out_path)


if __name__ == '__main__':
	main()