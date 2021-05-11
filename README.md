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
- create template files for creating base project setup neccessary folders and files.
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
- in dvc.yaml write all the stages that we done while model creation after creating dvc.yaml file this command will excecute that stages and create dvc.lock file this file start tracking that code whichever we write on dvc.yaml file if we make certain changes in any file for example in get_data.py we do some changes in code and after that if i run "dvc repro" commad so it will sence that change and it will runs the same process and track the code.

```bash
dvc metrics show
```
- as we maintion in the dvc.yaml file in metrics section where we gonna store scores and params of the model using above commnd we can see scores and params of the model which is stored in  "report/scores.json" & "report/params.json

```bash
dvc metrics diff
```
- it will show the old and new and change values from metrics (scores & paramms) in short it will track the model params/scores
     - "for example if i do change hyper-parameter and then i run my model so using above command we can compare previous and current model after the change"

### we install two library
```bash
pip install tox 
pip install pytest
```
#### what is tox?
- tox is a generic "virtual env" managemnt and test command line tool you can use for:
   - checking that your package installs correctly with different Python version and interpreters
   - running your tests in each of the environments, configuring your test tool of choice
   - acting as a frontend to continuous integration servers, greatly reducing boilerplate and merging CI and shell-based testing

```bash
tox
```
- this command will create virtual env and checking that your package installs correctly with different Python version and interpreters as we mention
- it will create virtual env in .tox dir

```bash 
tox -r
```
- for reload `tox.ini` and for reload the complete experiment

```bash
pytest -v
```
- "PyTest is a testing framework that allows users to write test codes using Python programming language. It helps you to write simple and scalable test cases for databases, 
APIs, or UI. PyTest is mainly used for writing tests for APIs. It helps to write tests from simple unit tests to complex functional tests."
- it will test codes

```bash
pip install -e .
```
- this install the packages which are present in your local dir and it will run "setup.py" file as well

```bash
pip freeze
```
- this command will shows all the packages which is present in your env "setup.py" file which contain "src" pakages in src there are (get_data.py, load_data.py etc)

```bash
python setup.py sdist bdist_wheel
```
- this command will create "dist dir" in which we have "zip" file which contain all the packages and it will easy for share
 
### handel range of features for correct result
- here main motive is that sometimes variables could be in some specific range
    - for ex:
        - our dataset have `blood presure" variable as we know blood presure never be '0' but some how by mistakly someone enter is 0 and after that model works but as we know blood presure could not be 0
- so in this case we set a `min` and `max` value so model will perform correctly form our data set we take `min` and `max` values for the perticular `features` and store that min and max values in `schema_in.json` file. and using this `schema_in.json` file if feature value are outof the range then we will rise an `customized error(NotInRange)` which is present in `tests/test_config.py`
- we need only indenpendent variables in `schema_in.json` file

    - note: now app is deployed successfully if we do chances in code and then push it into the git we don't have to so changes in anything
- just check `github/action/"whatever we commit"` and see wether it will build successfully or not

## mlflow
- once we start the mlflow server using below command it will shows link once we click on that link it will redirect to server page and it will show default folder run an expreriment using command `dvc repro` and refresh mlflow server and see it will create new artifats for present experimant.
- we can do some changes in model ex: if model is not performing well so we can do some changes in hyper-parameter or change algorithm and after that run again experiment using  `dvc repro` now again refresh mlflow server it will create another artifacts which contain present experiment information
- we can compare models(experiment) which one is performing well

- as many time we runs an experiemnt it will create an unique id artifats(folder which store model file)
- as many time we run an model it will create artifacts that many times and mlflow.db sqlite database
#### command for run the mlflow server

- before run mlflow server command create an artifcats folder
```mkdir artifacts```

- mlflow server command -
```bash
mlflow server
--backend-store-uri sqlite:///mlflow.db
--default-artifact-root ./artifacts
--host 0.0.0.0 -p 1234
```
- `backend-store-uri sqlite:///mlflow.db` we are telling tham so what is my backend store uri that means i am going to store all my data into "mlflow" database and this will create an "sqlite database" for us
- `default-artifact-root ./artifacts` and there is default artifact root that means where i am going to save my artifacts(model parts/model information) which store in `artifacts` folder that's why we create `artifacts` dir before the mlflow server command
- `1234` is the port no. that we 

#### Note:
- if in case above mlflow server command gives an error then use
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
```
- it will runs on default port

```bash
dvc repro
```
- it will runs experiment / model

#### git Action
- once we push all the code into the github `main-mlflow` branch so it will not performing action in git because in `ci-cd.yaml` file which is in(/.github/workflows/ci-cd.yaml) we maintion `main` branch so it will search for main brance if we want to perform action in main-mlfow brance we have to do changes in `ci-cd.yaml` file


### App Link 
[App link](https://wineqwithmlpos.herokuapp.com/)

### Wine Quality Project with MLOps present in `main` branch
[main branch link](https://github.com/PandeKalyani95/Wineq_DVC/blob/main/README.md)
