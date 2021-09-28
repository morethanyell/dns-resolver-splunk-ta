# DNS Resolver
### A custom Splunk command that translate or resolves a URL/DNS into IPv4 address.
by morethanyell (daniel.l.astillero@gmail.com) <--- accepts beer
\
&nbsp;
## Usage
### The search below shows a pretend index and sourcetype about VPN logs. The events don't have (natively) the IP address resolution of the URLs. Splunk engineer Chloe is interested in the ip address equivalent of the URLs. Thankfully, the `dnsresolver` command solves her problem. She pipes it in and gets the ip address out of the URL!
&nbsp;
```
index=vpn sourcetype=vpn:urls
| stats sparkline as visits_over_time dc(user) as total_users by url
| dnsresolver inpf=url outf=ip
| sort 10 - total_users
| table url ip visits_over_time total_users
```
&nbsp;
## Installation
- Step 1: Download the Splunk app
    - Option 1: Splunkbase. Download the app from Splunkbase https://splunkbase.splunk.com/app/6114/
    - Option 2: Github. Download the app from Github https://github.com/morethanyell/dns-resolver-splunk-ta
- Step 2: Download the Splunk SDK Python from Github https://github.com/splunk/splunk-sdk-python
- Step 3: Copy the directory `splunklib` from Splunk SDK Python and then paste it in the `/bin` folder of DNS Resolver app (TA-dnsresolver)
    - E.g.: `$ [sudo] cp -R ~/splunk-sdk-python/splunklib $SPLUNK_HOME/etc/apps/TA-dnsresolver/bin/`
    - Where `$SPLUNK_HOME` is the install-location of your Splunk isntance, e.g. normally in `/opt/splunk/` for Linux boxes
- Step 4: Ensure the permission and ownership of the entirety of the app / directory `TA-dnsresolver`
    - E.g.: `$ [sudo] chown -R splunk:splunk $SPLUNK_HOME/etc/apps/TA-dnsresolver/`
    - Or whatever user is preferred over `splunk:splunk`
- Step 5: Restart your Splunk instance
    - E.g.: `$ ~/bin/splunk restart`
\
&nbsp;
\
&nbsp;
### Disclaimer
This is not a "WhoIs" app. There are probably other solutions out there that address the problem and already work. I built this app to keep myself from rusting. Also, when I searched about similar solutions, I eventually realized that most of the existing ones are "lookup table dependent". I wanted to come up with a solution that is live—ad-hoc—searching the DNS resolution provided by the local machine's DNS provider using Python library `socket`. With that, it is safe to say that this could be a lot slower than other a lookup-based DNS resolution Splunk apps. I tested this against a 1000-row CSV file and got around 18 seconds in average.

Thank you for using this app and have a nice day.