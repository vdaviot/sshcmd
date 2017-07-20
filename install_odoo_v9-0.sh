#!/bin/bash

sudo apt-get install postgresql zsh git vim
sudo add-apt-repository ppa:webupd8team/sublime-text-3
zsh
sudo su
wget -O - https://nightly.odoo.com/odoo.key | apt-key add -
echo "deb http://nightly.odoo.com/9.0/nightly/deb/ ./" >> /etc/apt/sources.list
apt-get update && apt-get install odoo sublime-text-installer

export ODOO_ADDON_PATH="/usr/lib/python2.7/dist-packages/openerp/addons/"
export ODOO_CONF_PATH="/etc/odoo/openerp-server.conf"

echo "alias odoo=\"sudo odoo.py start " >> ~/.zshrc
echo "alias restart=\"sudo odoo.py restart" >> ~/.zshrc
echo "alias scaffold=\"sudo odoo.py scaffold $ODOO_ADDON_PATH" >> ~/.zshrc
echo "alias conf=\"sudo subl $ODOO_CONF_PATH" >> ~/.zshrc
