#! /bin/sh
# see http://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4 for more information

I18NDOMAIN="collective.twofactor"

# find the source, as it should be in the src directory
SOURCE=`find . -type d | grep -m 1 "collective/twofactor"`
LOCALES="$SOURCE/locales";

# rebuild pot file for package's domain and merge it with any manual translations needed
i18ndude rebuild-pot --pot $LOCALES/$I18NDOMAIN.pot --merge $LOCALES/manual.pot --create $I18NDOMAIN $SOURCE

# synchronise translations for package's domain
for po in $LOCALES/*/LC_MESSAGES/$I18NDOMAIN.po; do
    i18ndude sync --pot $LOCALES/$I18NDOMAIN.pot $po
done

# rebuild pot file for Plone's domain
i18ndude rebuild-pot --pot $LOCALES/plone.pot --create plone $SOURCE/configure.zcml $SOURCE/profiles/default

# synchronise translations for Plone's domain
for po in $LOCALES/*/LC_MESSAGES/plone.po; do
    i18ndude sync --pot $LOCALES/plone.pot $po
done
