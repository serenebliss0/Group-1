# Required Extensions

- [ ] Python for VSCode
- [ ] Code Spell Checker
- [ ] CSV
- [ ] Figma for VS Code
- [ ] Git Extension Pack
- [ ] Git History
- [ ] Live Share
- [ ] Path Intellisense
- [ ] Python Extension Pack
- [ ] SQLTools
- [ ] Git Extension Pack
- [ ] SQLTools SQLite

## Get use to these commands

```bash
git push origin main
//pushes to the main branch of our repo
//use this one every time you need to push


git push origin branch-name
//pushes to a specified branch


git branch
//check the current branch you're in

```

### Core Git Commands

```bash

git status
// check current state

git branch
// see all branches

git switch -c branch-name
// create + switch branch

git add .
git commit -m "message"
// save changes

git push -u origin branch-name
// first push

git push
// future pushes

git pull
// get latest updates

```

### Stuff

- Setting up a python virtual environment (venv)

```bash
python -m venv venv
```

- CustomTkinkter
-Pillow

```bash
git checkout your-branch
git pull origin main
```

```python
pip freeze > requirements.txt
```

## How to run the code

[![Watch the video]](external/how_to_run.mp4)

By now you should've tried running the code by clicking that shiny run button up in VSCode just to be hit with `Error: Module not found`. Due to our repo being structured as a python package for later, you'll need to run it a bit differently:

- If you haven't already, create your python virtual environment (venv)

``` Powershell
python -m venv venv
```

- Make sure you're in the correct directory

```Powershell
cd the-app/src/the-app-name
```

- Now ensure you've installed all the dependencies in requirements.txt

```Powershell
pip install -r requirements.txt
```

- Now you can run code by specifying its filename

```python
python -m main
```

This runs main.py

```python
python -m backend.database
```

This runs database.py

```python
python -m frontend.login
```

This displays the login page

---

p.s the `-m` means run as module
