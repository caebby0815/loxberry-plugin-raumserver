#!/usr/bin/perl

# Copyright 2019 Markus Keppeler, m@keppeler.de
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##########################################################################
# Modules
##########################################################################
# Einbinden der LoxBerry-Module
use CGI;
use LoxBerry::System;
use LoxBerry::Web;

#Einbinden weiterer Module
use File::HomeDir;
use Config::Simple;
use warnings;
use strict;
no strict "refs"; # we need it for template system
### Module für das Handling der JSON config
use JSON;
use utf8;

##########################################################################
# Variables
##########################################################################

#Loxberry Home Verzeichnis, normalerweise /_opt/loxberry
my  $home = File::HomeDir->my_home;
#Pfad zur Raumserver config, normalerweise /_opt/loxberry/data/plugins/raumserver/node_modules/node-raumserver/config
my  $raumserverCfgFilePath = "$home/data/plugins/raumserver/node_modules/node-raumserver/config";

# Mit dieser Konstruktion lesen wir uns alle POST-Parameter in den Namespace R.
my $cgi = CGI->new;
$cgi->import_names('R');

##########################################################################
# SubRoutinen
##########################################################################
#Read Raumserver Config file
sub extract_json{
	my $file = shift;
	local $/;
	open my $fh, "<", $file or die "Can't load file '$file' [$!]\n";
	my $json = <$fh>;
	$json = decode_json($json);
	close $fh;
	return $json;
}
#Write JSON Object to Config File
sub write_jsonfile{
	my $fh;
	my $json = shift;
	my $file = shift;
	open ($fh, ">$file") or die "Can't write to file '$file' [$!]\n";
	print $fh encode_json($json);
	close $fh;
  print "Konfiguration gespeichert<br>"
}

##########################################################################
# Read Settings
##########################################################################
# Die Version des Plugins wird direkt aus der Plugin-Datenbank gelesen.
my $version = LoxBerry::System::pluginversion();
my $rsconfig = extract_json("$raumserverCfgFilePath/default.json");

##########################################################################
# Main program
##########################################################################
# Header
LoxBerry::Web::lbheader("Raumserver Plugin V$version", "https://www.loxwiki.eu/display/LOXBERRY/Raumserver", "help.html");

# Template
my $template = HTML::Template->new(
    filename => "$lbptemplatedir/index.html",
    global_vars => 1,
    loop_context_vars => 1,
    die_on_bad_params => 0,
	associate => $cgi,
);

# -------------------------------------------------------------------------
# Load Language file
# -------------------------------------------------------------------------
my %L = LoxBerry::System::readlanguage($template, "language.ini");
# -------------------------------------------------------------------------
# Labels, diese können später über die Sprachdatei gesteuert werden
# -------------------------------------------------------------------------
$template->param( lblRaumserverPort => "Raumserver Port");
$template->param( lblRaumserverLoglevel => "Raumserver Loglevel");
$template->param( lblraumfeldHost => "Raumfeld Host");
$template->param( lblraumfeldRequestPort => "Raumfeld Request Port");
$template->param( lblPluginEnabled => "Plugin aktivieren");


# ---------------------------------------------------
# Control for "frmStart" Form
# ---------------------------------------------------
my $frmStart = $cgi->start_form(
     -name    => 'Raumserver Plugin',
     -method => 'POST',
 );
$template->param( frmStart => $frmStart );

# ---------------------------------------------------
# Control for "frmEnd" Form
# ---------------------------------------------------
my $frmEnd = $cgi->end_form();
$template->param( frmEnd => $frmEnd );

# ---------------------------------------------------
# Control for "btnSave" Button
# ---------------------------------------------------
my $btnSave = $cgi->submit(
     -name    => 'btnSave',
     -value => "Speichern",
 );
$template->param( btnSave => $btnSave );

# ---------------------------------------------------
# Control for "raumserverPort" Textfield
# ---------------------------------------------------
my $raumserverPort = $cgi->textfield(
     -name    => 'raumserverPort',
     -default => $rsconfig->{'raumserver'}->{'port'},
 );
$template->param( raumserverPort => $raumserverPort );

# ---------------------------------------------------
# Control for "raumserverPort" Textfield
# ---------------------------------------------------
my $raumserverLoglevel = $cgi->textfield(
     -name    => 'raumserverLoglevel',
     -default => $rsconfig->{'raumserver'}->{'loglevel'},
 );
$template->param( raumserverLoglevel => $raumserverLoglevel );

# ---------------------------------------------------
# Control for "raumfeldHost" Textfield
# ---------------------------------------------------
my $raumfeldHost = $cgi->textfield(
     -name    => 'raumfeldHost',
     -default => $rsconfig->{'raumfeld'}->{'raumfeldHost'},
 );
$template->param( raumfeldHost => $raumfeldHost );

# ---------------------------------------------------
# Control for "raumfeldHostRequestPort" Textfield
# ---------------------------------------------------
my $raumfeldHostRequestPort = $cgi->textfield(
     -name    => 'raumfeldHostRequestPort',
     -default => $rsconfig->{'raumfeld'}->{'raumfeldHostRequestPort'},
 );
$template->param( raumfeldHostRequestPort => $raumfeldHostRequestPort );


# ---------------------------------------------------
# Control for "pluginEnabled" Flipswitch
# ---------------------------------------------------
my @values = ('1', '0' );
my %labels = (
     '1' => 'On',
     '0' => 'Off',
 );
my $pluginEnabled = $cgi->popup_menu(
     -name    => 'pluginEnabled',
     -values  => \@values,
     -labels  => \%labels,
     -default => '1',
 );
$template->param( pluginEnabled => $pluginEnabled );


# ---------------------------------------------------
# Save settings to config file
# ---------------------------------------------------
if ($R::btnSave)
{
 $rsconfig->{'raumserver'}->{'port'} = $R::raumserverPort;
 $rsconfig->{'raumserver'}->{'loglevel'} = $R::raumserverLoglevel;
 $rsconfig->{'raumfeld'}->{'raumfeldHost'} = $R::raumfeldHost;
 $rsconfig->{'raumfeld'}->{'raumfeldHostRequestPort'} = $R::raumfeldHostRequestPort;
 write_jsonfile($rsconfig, "$raumserverCfgFilePath/default.json");
}

# Nun wird das Template ausgegeben.
print $template->output();

# Schlussendlich lassen wir noch den Footer ausgeben.
LoxBerry::Web::lbfooter();
