# QTitan
QTitan is built with Python3 and uses the Django web framework. Read up on the [Django Documentation](https://docs.djangoproject.com/en/1.10/). If you need a quick rundown on using Python, check out [this tutorial](https://docs.python.org/3/tutorial/).

#### Getting Up and Running

Python3, Pip, and Git

[Python3](https://www.python.org/downloads/)
[Pip](https://pip.pypa.io/en/stable/installing/)
[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

###### Clone this repo
```git clone https://github.com/rdespoiu/QTitan.git```

###### Install required packages
In the directory where you've clone QTitan, run this command:
```pip install -r requirements.txt```

###### Run the server
```cd``` into QTitan (the subdirectory inside the main repository directory)
```python manage.py runserver```
You should see something like:
```
Performing system checks...

System check identified no issues (0 silenced).
January 12, 2017 - 18:47:54
Django version 1.10.5, using settings 'QTitan.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Then simply visit ```http://127.0.0.1:8000/QTSurvey``` in a web browser and you'll get to the application's index page.

#### Making Changes
When you start working on a feature, make sure you first pull (in case there have been changes) and then create a new git branch. These are run on the command line.
```
git checkout master
git pull
git checkout -b SomeFeature
```

When you've finished your feature:
```
git add .
git commit -m "Your commit message here"
git push                # NOTE: You may have to do git push --set upstream origin SomeFeature
```

Once you've pushed your new branch, go on the repository's GitHub page, and under ```Pull Requests```, select ```Create a pull request```. You'll want to request to merge your branch into either the ```dev``` or ```master``` branch (we'll figure this out later). Once you've created the PR, just go into our Discord channel and ask someone to do a quick code review to check for issues, and once someone's looked it over, go ahead and merge/close your PR. This will be a good way to avoid little errors down the road as the project grows in size.
