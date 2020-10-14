![nps-logo](./nps-logo.jpg)

# [@natl_park_pics](https://twitter.com/natl_park_pics)
A small Twitter bot written in Python that posts a random picture of a random national park every couple of hours.

Prettify your hellsite feed by following!

# Installation
If you want to run this locally, clone this repository.

Navigate to the `natl_park_pics_twitterbot` directory and run:
```
pip install -r requirements.txt
```

### Twitter Developer Account
To use the Twitter API, you'll need to apply for [access](https://developer.twitter.com/en/apply-for-access). Once that's granted, you'll be able to see an `API key` and `API secret` as well as generate an `access token` and `access secret`. Copy those and replace these placeholders with them:
```
main.py:7:
twitter_api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
```

### NPS API Key
Similarly, you'll need access to the [NPS API](https://www.nps.gov/subjects/developer/get-started.htm), which should happen pretty quickly.

Replace `YOUR_API_KEY` with your unique NPS API key:
```
main.py:8:
nps_url = 'https://developer.nps.gov/api/v1/parks?api_key=[YOUR_API_KEY]&limit=500'
```

Also, be sure to change `IMAGE_PATH` on lines `28` and `35` with the path that you want your random park image to save to.

# Running and Scheduling
To run the program, simply:
```
python3 main.py
```

Two brief `Success` or verbose `Error` messages will show depending on the responses that `upload()` or `reference()` gets.

To schedule, you can use something like cron or launchd. Sine I'm on a Mac, I opted for launchd:
```
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>michaelkopsho.twit</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/michaelkopsho/.pyenv/shims/python3</string>
        <string>/Users/michaelkopsho/natl_park_pics_twitterbot/main.py</string>
    </array>
    <key>StartInterval</key>
    <integer>7200</integer>
    <key>StandardOutPath</key>
    <string>/Users/michaelkopsho/out.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/michaelkopsho/error.log</string>
</dict>
</plist>
```

As you can see, I post a new pic every 2 hours.
