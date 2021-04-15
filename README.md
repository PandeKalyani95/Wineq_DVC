# Create Env
conda create -n wineq python=3.7 -y
# Activate Env
conda activate wineq
- Create req. file
- install req. file by using following command
- pip install -r requirements.txt
- create template files for creating base project setup 
   neccessary folders and files.
git init
dvc init
dvc add data_given/winequality.csv
git add .