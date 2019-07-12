# eToroBot

###### A Python bot that analyses stocks on Xignite and posts a new status message with the report.

Example of a status message that gets automatically posted on eToro:
```
>> 🇬🇧  DAILY performance of LONDON's stocks 🇬🇧  <<
After analysing 343 stocks in the London Stock Exchange, the following are the TOP 5 traded stocks by volume for TODAY Friday 12 July:
1. $TCG.L 277.13 Million // 2. $LLOY.L 81.18 Million // 3. $SXX.L 72.30 Million // 4. $VOD.L 23.12 Million // 5. $GLEN.L 21.70 Million.

In addition, the following are the 5 BEST GAINERS:
1. $GFTU.L 787.00 (+5.14%) // 2. $SXX.L 16.69 (+5.04%) // 3. $SOPH.L 430.80 (+4.39%) // 4. $PSN.L 1,982.00 (+4.15%) // 5. $SAGA.L 42.58 (+4.11%).

Finally, here are the 5 WORST LOSERS:
1. $TCG.L 5.40 (-59.34%) // 2. $KIE.L 83.35 (-7.03%) // 3. $IPO.L 69.70 (-3.60%) // 4. $ACA.L 179.30 (-2.71%) // 5. $INDV.L 46.22 (-2.24%).
```

## Requirements
- Python 3.7
- An eToro account **without** the two-factor authentication enabled (not supported yet).
- Xignite API credentials

## Installation
- `git clone git@github.com:GiacomoP/eToroBot.git`
- `cd eToroBot`
- `pip install -r requirements.txt`

After you've installed the required modules:
- `mkdir bin`
- Download [chromedriver](http://chromedriver.chromium.org/) and put the binary file in the `bin` folder just created.
- Create an `.env` file based on `.example.env`
- Run `python main.py`

You can create a cron job that runs main.py every time you'd like to publish a status message.

The code has been tested with ChromeDriver 75.0.3770.90, and also with [PhantomJS 2.1.1](https://phantomjs.org/download.html) even though it's deprecated in the chosen version of Selenium. Other web drivers might work, too.

## Working example
Feel free to follow me at https://www.etoro.com/people/jackheuston to see a working example with stocks from the London Stock Exchange!

## Caveats
I've filled `settings.py` with all the stocks I could find in eToro via some network requests scraping. However, some of those stocks don't seem to actually be in eToro and tagging them in the status message with `$STK_NAME` won't work.

I'll remove them from the list as soon as I detect them all. You're also free to open a pull request.