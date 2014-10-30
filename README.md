asset
=====

This is a chop out of my running bot and if you access to this you are granted personal or professional(trading) use from this code. The only thing I ask is that you do not give this code to anyone else for any reason unless you ask me first

You will need the following python packages
```
numpy - sudo pip install numpy
```

```
requests - sudo pip install requests
```

Then you:

```
python asset.py btce btc_usd 1hr
```

The response will be a json list with the following fields: [open, close, low, high, volume, time_close(unix timestamp), 12ema]

This data is taken from bitcoinwisdom for the given step and dumps a json list with the 12 period ma in it.
it works for tracked pairs and markets on bitcoinwisdom


If you you look at the priceInfo and statInfo class you will see lots of useful data