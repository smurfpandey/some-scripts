## update-cloudflare-dns-record.py

This script enables dynamic IP for your domain on cloudflare by updating the DNS record every hour.

### Getting Started

* Install dependencies
  * Sentry SDK: Used for logging errors. `pip3 install --upgrade sentry-sdk==0.9.0 --user`
  * Python Dotenv: Used for loading env vars from .env file during development. `pip3 install python-dotenv --user`

* Setup Environment Variables
  * CLOUDFLARE_API_KEY: API key generated on the "My Account" page of Cloudflare account.
  * CLOUDFLARE_API_EMAIL: Email address associated with the Cloudflare account
  * SENTRY_DSN: DSN for the project on Sentry

* Get [Zone Id](https://api.cloudflare.com/#zone-list-zones), & [DNS Record ID](https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records) of the domain/sub-domain from Cloudflare which you want to update. Set the value in script, `CLOUDFLARE_ZONE_ID` & `CLOUDFLARE_DNS_RECORD_ID`.

* Setup cron for this script
  * Make the script executable: `chmod +x update-cloudflare-dns-record.py`
  * Add cron by creating new file `/etc/cron.d/update-cloudflare-dns` with below content
    * `0 * * * * . /home/pi/.bash_profile; /home/pi/scripts/update-cloudflare-dns-record.py && curl -fsS --retry 3 https://hc-ping.com/your-uuid-here > /dev/null`
    * The above script also loads environment variable before executing the script.