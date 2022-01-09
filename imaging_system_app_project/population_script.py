import os

local_files = os.listdir()

if "sample_data.json" in local_files and "manage.py" in local_files:
	print("importing data from sample_data.json into the database")
	os.system("python manage.py loaddata sample_data.json")
else:
	print("manage.py or sample_data.json not found - are you running this in the same directory as manage.py and sample_data.json?")