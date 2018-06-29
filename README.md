self-replicative-stupidity
==========================

The GitHub repository which replicates itself

Installation
------------

Clone the repository:

```bash
git clone https://github.com/hlibvel/self-replicative-stupidity.git
cd self-replicative-stupidity
```


Create a virtual environment:

```bash
mkvirtualenv srr --python=`which python3`
```

From this moment each time you work with the application switch to that environment:

```bash
workon ssr
```

Install requirements:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Deploy
------

Add the remote Heroku repository:

```bash
heroku git:remote -a self-replicative-stupidity
```

Push code to the Heroku:

```bash
git push heroku master
```

If you are deploying to the fresh Heroku application enable the web worker:

```bash
heroku ps:scale web=1 -a self-replicative-stupidity
```
