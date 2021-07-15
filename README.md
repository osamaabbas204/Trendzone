# Trendzone is a website that shows trends about devices(Laptop, Mobile...). This website will extract the reviews and rating and latest market trends of product from different
websites and show the user on our websites.
This website also show the market prices of a product from different websites like Telemart, daraz, shophive, etc
This website help the user to choose the best device according to his/her specifiction

STEP 1
First install anaconda for create enviorment
Run the following Command and make sure you in the Trendzone Directory
conda env create -f trendzone.yml 
This Command create the enviorment with the required packages for project
........................................................................................

STEP 2
Setup the database for Project
Install MySQL, MySQL Workbench(Optional)
Create the database in MySQL Workbench
write the Database Name and Password in Trendzone->settings.py DatabaseDictionary
Activate your Enviorment in commandPrompt by run this Command
conda activate myenv
Run the following command in commandPrompt
python manage.py makemigrations
python manage.py migrate
After this all tables create in your Database
..............................................................................................

STEP 3
Make Sure Run the scheduler before run the Project.
Set the time for Scheduler according to your Requirement in Trendz->scheduleData.py
Run this command in commandPrompt
python manage.py runserver --noreload
Make Sure Run all the Schedule in Trendz->scheduleData.py
..............................................................................................

STEP 4
Run this command for run the Project and also make sure you connected to the internet
python manage.py runserver
Run http://127.0.0.1:8000/ this link in Browser
