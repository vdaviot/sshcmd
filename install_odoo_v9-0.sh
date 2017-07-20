#!/bin/bash

sudo apt-get install postgresql zsh
zsh
sudo su
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/9.0/nightly/deb/ ./" >> /etc/apt/sources.list
apt-get update && apt-get install odoo

export ODOO_ADDON_PATH="/usr/lib/python2.7/dist-packages/openerp/addons/"

echo "alias odoo=\"odoo.py start " >> ~/.zshrc
echo "alias restart=\"odoo.py restart" >> ~/.zshrc
echo "alias scaffold=\"odoo.py scaffold " >> ~/.zshrc

echo "alias addon=\"scaffold $ODOO_ADDON_PATH"