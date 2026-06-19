load:
	python src/etl/loader.py

test:
	pytest tests/etl/

clean:
	del /f db\nifty100.db
	del /f output\*.csv

report:
	jupyter nbconvert --to html notebooks/*.ipynb

dashboard:
	echo "Open dashboard/ folder in Power BI"