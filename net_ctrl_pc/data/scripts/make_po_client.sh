#!/usr/bin/bash

YN="yn"
AMSURE=

while [ "yn" = "${YN#*$AMSURE}" ] ; do
    read -p "Confirm y/n: " AMSURE
done

cd ../../client

# make
if [ -f locale/net-ctrl-pc-client.pot ]; then
  mv locale/net-ctrl-pc-client.pot locale/net-ctrl-pc-client.pot_old
fi
xgettext --language=Python --keyword=_ --package-name=net-ctrl-pc-client --msgid-bugs-address=khvalera@ukr.net --from-code=UTF-8 --output=locale/net-ctrl-pc-client.pot $(find . -name "*.py")
mv client/locale/uk/LC_MESSAGES/net-ctrl-pc-client.po client/locale/uk/LC_MESSAGES/net-ctrl-pc-client.po_old
msginit --locale=en_US.UTF-8 --no-translator --input=locale/net-ctrl-pc-client.pot --output-file=locale/en/LC_MESSAGES/net-ctrl-pc-client.po
msginit --locale=uk_UA.UTF-8 --no-translator --input=locale/net-ctrl-pc-client.pot --output-file=locale/uk/LC_MESSAGES/net-ctrl-pc-client.po

