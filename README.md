asset
=====

This is a chop out of my running bot. If you find it useful and feel like making a monetary donation please make a donation to seans outpost(http://seansoutpost.com) or bitcoin not bombs(http://www.bitcoinnotbombs.com). 

You will need the following python packages


numpy
```
sudo pip install numpy
```

requests
```
sudo pip install requests
```

simplejson
```
sudo pip install simplejson
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

Then open your browser and go to
```
http://localhost:8000/charts/
```

![Screenshot](/screenshot.png?raw=true "Screenshot")
For right now you must manually enter the market/pair and they must be valid. I do absolutely no validation yet.


This data is taken from bitcoinwisdom for the given step and should work for tracked pairs and markets on bitcoinwisdom
