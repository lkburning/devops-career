from certbot import main as certbot


"certbot certonly  -d *.copylife.fun --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory --config-dir=/opt/acm/config/ --work-dir=/opt/acm/work/ --logs-dir=/opt/acm/logs"

"""
Please deploy a DNS TXT record under the name:

_acme-challenge.copylife.fun.

with the following value:

pXI_eRWHQSSghtvtu2gTMVJS3Tt3Oz9-tukGDDe2BTY
"""

"""
https://eff-certbot.readthedocs.io/en/stable/using.html#certbot-commands
The manual plugin can use either the http or the dns challenge. You can use the --preferred-challenges option to choose the challenge of your preference.

The http challenge will ask you to place a file with a specific name and specific content in the /.well-known/acme-challenge/ directory directly in the top-level directory (“web root”) containing the files served by your webserver. In essence it’s the same as the webroot plugin, but not automated.

When using the dns challenge, certbot will ask you to place a TXT DNS record with specific contents under the domain name consisting of the hostname for which you want a certificate issued, prepended by _acme-challenge.
"""