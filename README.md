# kite-history
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/mr-karan/kiteHistory/master/LICENSE)
[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/mr-karan)

`kitehistory` is a wrapper around [Kite Historical API](https://kite.trade/docs/connect/v1/#historical-data)


### Installation : 

    pip install kitehistory

[![asciicast](https://asciinema.org/a/.png)](https://asciinema.org/a/)

###Options : 

    --symbol                         Stock symbol of the instrument.
    --interval                       Time interval for the tick data.
    --from_date                      Start date indicating the start of records.
    --to_date                        End date indicating the end of records.
    --exchange                       Exchange Name. (MCX/NSE/BSE/NFO/CDS/BFO/MCXSX)
    --output                         Output path to save `csv`
    --verbose                        Enable verbose logging

### Example Usage : 

    kitehistory -s TCS -i day -f 2017-05-15 -t 2017-06-05 -e NSE -o TCS.csv --verbose 

![img](addlink)

### First Time Setup

`kitehistory` depends on Kite API to fetch instruments master file in `.csv`. You need to create an appllication at
[https://developers.kite.trade/apps](https://developers.kite.trade/apps) and export the following keys in your shell

```
            export KITE_API_KEY='your-kite-api-key'
            export KITE_SECRET='your-kite-secret-key'
            export KITE_REQUEST_TOKEN='your-kite-request-token'

``` 

## Credits

- [pandas](http://pandas.pydata.org/)
- [Kite API](https://developers.kite.trade/apps/)


## Contributing

Feel free to report any issues and/or send PRs for additional features.

### License

MIT © Karan Sharma 
[LICENSE included here](LICENSE)