#!/usr/bin/bash

YN="yn"
AMSURE=

while [ "yn" = "${YN#*$AMSURE}" ] ; do
    read -p "Confirm y/n: " AMSURE
done

cd ../../client

# update
msgmerge --update locale/en/LC_MESSAGES/net-ctrl-pc-client.po locale/net-ctrl-pc-client.pot
msgmerge --update locale/uk/LC_MESSAGES/net-ctrl-pc-client.po locale/net-ctrl-pc-client.pot
