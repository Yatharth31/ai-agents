"""Utility checks for Chroma DB contents.

Run this module to print whether the local Chroma vectorstore contains any
documents and a short summary (counts or a sample peek).
"""
import sys
import traceback
import vectorstore


def check_chroma(collection_name: str = "market_docs") -> None:
	"""Connect to local Chroma and print whether it has stored documents."""
	try:
		client = vectorstore._get_client()
		col = vectorstore._get_collection(client, name=collection_name)
	except Exception as exc:
		print("Error connecting to Chroma:", exc)
		traceback.print_exc()
		return

	# Try collection.count(), fallback to peek()
	try:
		cnt = col.count()
		print(f"Chroma collection '{collection_name}' document count: {cnt}")
		if cnt == 0:
			print("Chroma is empty.")
		else:
			try:
				peek = col.peek()
				print("Sample documents/metadata:")
				print(peek)
			except Exception:
				print("Collection has documents but peek() failed to return sample.")
	except Exception:
		try:
			peek = col.peek()
			# peek may return a dict with 'documents' key
			if not peek:
				print(f"Chroma collection '{collection_name}' appears empty (peek returned no data).")
			else:
				print(f"Chroma collection '{collection_name}' has some data (peek returned):")
				print(peek)
		except Exception as exc:
			print("Unable to determine Chroma contents:", exc)
			traceback.print_exc()


if __name__ == "__main__":
	name = "market_docs"
	if len(sys.argv) > 1:
		name = sys.argv[1]
	check_chroma(collection_name=name)

