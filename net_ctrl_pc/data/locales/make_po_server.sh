#!/usr/bin/bash

YN="yn"
AMSURE=

while [ "yn" = "${YN#*$AMSURE}" ] ; do
    read -p "Confirm y/n: " AMSURE
done

cd ../../

# make
#mv server/locale/net-ctrl-pc-server.pot server/locale/net-ctrl-pc-server.pot_old
#xgettext --language=Python --keyword=_ --package-name=net-ctrl-pc-server --msgid-bugs-address=khvalera@ukr.net --from-code=UTF-8 --output=server/locale/net-ctrl-pc-server.pot $(find . -name "*.py")
#mv server/locale/uk/LC_MESSAGES/net-ctrl-pc-server.po server/locale/uk/LC_MESSAGES/net-ctrl-pc-server.po_old
#msginit --locale=en_US.UTF-8 --no-translator --input=server/locale/net-ctrl-pc-server.pot --output-file=server/locale/en/LC_MESSAGES/net-ctrl-pc-server.po
#msginit --locale=uk_UA.UTF-8 --no-translator --input=server/locale/net-ctrl-pc-server.pot --output-file=server/locale/uk/LC_MESSAGES/net-ctrl-pc-server.po

# update
msgmerge --update ./server/locale/en/LC_MESSAGES/net-ctrl-pc-server.po ./server/locale/net-ctrl-pc-server.pot
msgmerge --update ./server/locale/uk/LC_MESSAGES/net-ctrl-pc-server.po ./server/locale/net-ctrl-pc-server.pot
