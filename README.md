# Live-Landings-Notifier
Notification of landing predictions within Xkm and X hours of a specified 'home' location.

Use https://pushover.net/ and https://github.com/dschep/ntfy to send notifications to android.

## Cron examples

\# Get Live Balloon predictions

40      7       *       *       *       /usr/local/live_sonde_predict/getLiveLandings.py 52.322844 -0.7079209 300 86400 | mail --exec 'set nonullbody' -s "Live Landing Predictions" email@blah.org

55      7-20    *       *       *       /usr/local/live_sonde_predict/getLiveLandings.py 52.322844 -0.7079209 200 7200 | xargs --null --no-run-if-empty ntfy -b pushover -o user_key blahblahkey -t "Live Balloon Prediction" send
