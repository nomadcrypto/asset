asset
=====

This is a chop out of my running bot and if you access to this you are granted personal or professional(trading) use from this code. The only thing I ask is that you do not give this code to anyone else for any reason unless you ask me first

You will need the following python packages
numpy
```
sudo pip install numpy
```

requests
```
sudo pip install requests
```

django
```
sudo pip install django
```



Then you:

```
cd asset_web
python manage.py runserver
```

Then open your browser and go to(example)
```
http://localhost:8000/charts/
```
For right now you must manually enter the market/pair and they must be valid. I do absolutely no validation yet. You can now add as many charts on the page as you want.


This data is taken from bitcoinwisdom for the given step and should work for tracked pairs and markets on bitcoinwisdom
