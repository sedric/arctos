use strict;
use vars qw($VERSION %IRSSI);
use HTTP::Request::Common qw(POST);
use LWP::UserAgent;

use Irssi;
$VERSION = '0.0.1';
%IRSSI = (
    authors     => 'Benjamin "sedric" Boudoir',
    contact     => 'sedric+github@sedric.fr',
    name        => 'arctos notifier',
    description => 'Write a notification in an arctos channel.',
    url         => 'https://github.com/sedric/arctos/tree/master/clients/irssi_plugin',
    license     => 'GNU General Public License',
    changed     => '$Date: 2014-08-11 19:57:00 +0200 (Mon, 11 Aug 2014) $'
);

#--------------------------------------------------------------------
# Based on fnotify.pl 0.0.3 by Thorsten Leemhuis
# http://www.leemhuis.info/files/fnotify/fnotify
# Which as the following credits :
#
# ===================================================================
# In parts based on knotify.pl 0.1.1 by Hugo Haas
# http://larve.net/people/hugo/2005/01/knotify.pl
# which is based on osd.pl 0.3.3 by Jeroen Coekaerts, Koenraad Heijlen
# http://www.irssi.org/scripts/scripts/osd.pl
#
# Other parts based on notify.pl from Luke Macken
# http://fedora.feedjack.org/user/918/
# ===================================================================
#
# I'll thank all these peoples, because I don't know perl (yet), and
# a simple code is a good start.
#
#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Private message parsing
#--------------------------------------------------------------------

sub priv_msg {
    my ($server,$msg,$nick,$address,$target) = @_;
    arctos_send("Private message from " .$nick );
}

#--------------------------------------------------------------------
# Printing hilight's
#--------------------------------------------------------------------

sub hilight {
    my ($dest, $text, $stripped, $nick) = @_;
    my $message = "Hilight from";
    if ($dest->{level} & MSGLEVEL_HILIGHT) {
        arctos_send("Hilighted in " .$dest->{target});
    }
}

#--------------------------------------------------------------------
# Send to the server
#--------------------------------------------------------------------

sub arctos_send {
    my $server  = "localhost";
    my $port    = "8080";
    my $channel = "irssinotifications";

    my $endpoint = "http://$server:$port/$channel";
    my ($text) = @_;
    my $ua = LWP::UserAgent->new;
    my $req = POST $endpoint, Content => "$text" ;

    $ua->request($req)->as_string;
}

#--------------------------------------------------------------------
# Irssi::signal_add_last / Irssi::command_bind
#--------------------------------------------------------------------

Irssi::signal_add_last("message private", "priv_msg");
Irssi::signal_add_last("print text", "hilight");

#- end
