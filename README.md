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
```bash
dvc repro
```
- in dvc.yaml write all the stages that we done while model creation
- after creating dvc.yaml file this command will excecute that stages
- and create dvc.lock file this file start tracking that code whichever we write on dvc.yaml file
if we make certain changes in any file for example in get_data.py we do some changes in code
and after that if i run "dvc repro" commad so it will sence that change
and it will runs the same process and track the code.