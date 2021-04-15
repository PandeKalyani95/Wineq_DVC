import os

dirs = [
    # if use data/raw this format for creatinf folder
    # so in OS it will create a problem
    # some OS require "/" or some "\"
    # for better we can use "os.path.join()"
    # it will set default "slash" for OS as it need
    # (for screating sub folder)
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    "notebook",    # here we create single folder so here we do not need "slash
    "saved_models",
    "src"
]

for dir_ in dirs:
    os.makedirs(dir_, exist_ok = True)
    with open(os.path.join(dir_, ".gitkeep"), "w") as f:   # each sub folder conatin .gitkeep file
        pass

files = [
    "dvc.yaml",
    "params.yaml",
    ".gitignore",
    os.path.join("src","__init__.py")
]

for file_ in files:
    with open(file_, "w") as f:
        pass

