#!/usr/bin/bash

YN="yn"
AMSURE=

while [ "yn" = "${YN#*$AMSURE}" ] ; do
    read -p "Confirm y/n: " AMSURE
done

if [ "${AMSURE}" = "y" ] ; then
   cd ../..//
   msgfmt server/locale/en/LC_MESSAGES/net-ctrl-pc-server.po -o server/locale/en/LC_MESSAGES/net-ctrl-pc-server.mo
   msgfmt server/locale/uk/LC_MESSAGES/net-ctrl-pc-server.po -o server/locale/uk/LC_MESSAGES/net-ctrl-pc-server.mo
fi
