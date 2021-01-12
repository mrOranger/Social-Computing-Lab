# Social Computing Assignment
Lab assignment for the Social Computing exam. This project is aimed to create a reproducible pipeline using _Data Version Control_ and the notebook [How clean are San Francisco's restaurants?](https://nbviewer.ipython.org/github/Jay-Oh-eN/happy-healthy-hungry/blob/master/h3.ipynb).

## Setup
1. Download the repository and move to the folder:
```
git clone https://github.com/mrOranger/Social-Computing-Assignment
cd Social-Computing-Assignment
```

2. Install the dependencies usign pip:
```
pip install -r src/requirements.txt
```

3. Pull data from the remote storage:
```
dvc pull
```

## Run
Run the pipeline using the command:
```
dvc repro --force
```

By using the command:
```
dvg dag
```
we can see the how the pipeline is distributed: ![alt text](DAG.png)