#!/bin/zsh
# Deploy daria-lash.com: push main to GitHub, then over SSH make the server repo pull and run the .cpanel.yml tasks.
# Never upload files to public_html directly: the next git deploy overwrites them.
# SSH: lbdaria@s040.cubrad.eu:22022, key ~/.ssh/daria-lash-deploy (cPanel API on :2083 sits behind Imunify WebShield).
set -e
cd "${0:A:h}/.."
git push -q origin main
ssh -p 22022 -i ~/.ssh/daria-lash-deploy -o BatchMode=yes -o IdentitiesOnly=yes lbdaria@s040.cubrad.eu 'bash -s' <<'REMOTE'
set -e
cd ~/repositories/beauty-by-daria
git pull -q --ff-only origin main
sed -n 's/^ *- //p' .cpanel.yml | grep -v '^deployment:' > /tmp/daria-deploy-tasks.sh
bash -e /tmp/daria-deploy-tasks.sh
rm -f /tmp/daria-deploy-tasks.sh
echo "deployed $(git log --oneline -1)"
REMOTE
