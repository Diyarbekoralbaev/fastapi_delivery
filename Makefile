init:
	python3 init_db.py

run:
	uvicorn main:app --reload