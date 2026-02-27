pip install -r requirements.txt

python main.py
python -m pytest tests/ -v
python benchmarks/measure.py
