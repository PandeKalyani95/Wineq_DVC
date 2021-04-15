- Create Env
```bash
conda create -n wineq python=3.7 -y
```
- Activate Env
```bash
conda activate wineq
```
- Create req. file
- install req. file by using following command
```bash
pip install -r requirements.txt
```
- create template files for creating base project setup 
   neccessary folders and files.
```bash
git init
```
```bash
dvc init
```
```bash
dvc add data_given/winequality.csv
```
```bash
git add . && git commit -m "first commit"
```
- creatr github accout for project if it is already created then simply push
```bash
git remote add origin https://github.com/PandeKalyani95/Wineq_DVC.git
```
```bash
git branch -M main
```
```bash
git push -u origin main
```
#### update gitub repo if we do any changes in code.
```bash
git add . && git commit -m "update commit"
```
```bash
git push -u origin main
```