#!/usr/bin/bash

YN="yn"
AMSURE=

while [ "yn" = "${YN#*$AMSURE}" ] ; do
    read -p "Confirm y/n: " AMSURE
done

if [ "${AMSURE}" = "y" ] ; then
   cd ../../
   msgfmt client/locale/en/LC_MESSAGES/net-ctrl-pc-client.po -o client/locale/en/LC_MESSAGES/net-ctrl-pc-client.mo
   msgfmt client/locale/uk/LC_MESSAGES/net-ctrl-pc-client.po -o client/locale/uk/LC_MESSAGES/net-ctrl-pc-client.mo
fi
