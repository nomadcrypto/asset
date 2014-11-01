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
http://localhost:8000/charts/btce/btc_usd/1d?display_periods=60
```

the url format is:
```
http://localhost:8000/charts/{market}/{pair}/{step}?display_periods=x
```

if no display periods are given all results will be returned. The asset data shown below the chart will reflect averages for the given display periods. *this data does not yet reflect the asset variance.

The available steps are: 1min, 5min, 15min, 30min, 1hr, and 1d


This data is taken from bitcoinwisdom for the given step and should work for tracked pairs and markets on bitcoinwisdom
