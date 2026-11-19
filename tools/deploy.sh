#!/bin/zsh
# Deploy daria-lash.com: push main to GitHub, then make cPanel (account lbdaria) pull and run .cpanel.yml.
# Never upload files to public_html directly: the next git deploy overwrites them.
set -e
source ~/.openclaw/secrets/daria-lash/cpanel.env
cd "${0:A:h}/.."
git push -q origin main
A="Authorization: cpanel $CPANEL_USER:$CPANEL_TOKEN"; H=https://s040.cubrad.eu:2083/execute; R=/home/lbdaria/repositories/beauty-by-daria
curl -sf -H "$A" --get "$H/VersionControl/update" --data-urlencode repository_root=$R --data-urlencode branch=main >/dev/null
curl -sf -H "$A" --get "$H/VersionControlDeployment/create" --data-urlencode repository_root=$R \
  | python3 -c "import sys,json;d=json.load(sys.stdin);print('deploy', 'queued' if d['status']==1 else d['errors'])"
