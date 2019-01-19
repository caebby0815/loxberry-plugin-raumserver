#!/bin/sh

# Bashscript which is executed by bash *AFTER* complete installation is done
# (but *BEFORE* postupdate). Use with caution and remember, that all systems
# may be different! Better to do this in your own Pluginscript if possible.
#
# Exit code must be 0 if executed successfull.
#
# Will be executed as user "loxberry".
#
# We add 5 arguments when executing the script:
# command <TEMPFOLDER> <NAME> <FOLDER> <VERSION> <BASEFOLDER>
#
# For logging, print to STDOUT. You can use the following tags for showing
# different colorized information during plugin installation:
#
# <OK> This was ok!"
# <INFO> This is just for your information."
# <WARNING> This is a warning!"
# <ERROR> This is an error!"
# <FAIL> This is a fail!"

echo "<INFO> Copy config file to raumserver config folder"
echo "<INF0> from $ARGV5/config/$ARGV3/ to $ARGV5/data/plugins/raumserver/node_modules/node-raumserver/config"
cp -p -v -r  $ARGV5/config/$ARGV3/* $ARGV5/data/plugins/raumserver/node_modules/node-raumserver/config

echo "<WARN> You need to reboot Loxberry in order to complete the installation"
echo "<WARN> Loxberry muss neu gestartet werden um die Installation abzuschliessen."

# Exit with Status 0
exit 0
