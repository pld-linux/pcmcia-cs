%define KERNEL_VERSION 2.0.35
%define PCMCIA_VERSION 3.0.3

Summary     	: PCMCIA card services.
Name        	: pcmcia-cs
Version     	: %{PCMCIA_VERSION}
Release     	: 2
Group       	: System/Tools

Copyright   	: distributable
Packager    	: rf@lst.de (Ralf Flaxa)
URL         	: http://hyper.stanford.edu/HyperNews/get/pcmcia/home.html

BuildRoot   	: /tmp/pcmcia-cs-%{PCMCIA_VERSION}

Source0: ftp://hyper.stanford.edu/pub/pcmcia/pcmcia-cs-%{PCMCIA_VERSION}.tar.gz
Source1: pcmcia-cs-network.script
Patch0: pcmcia-cs-COL.patch


%Description
PCMCIA card services


%Prep
if [ ! -d /usr/src/linux-%{KERNEL_VERSION} ]; then
  echo "no matching kernel sources (%{KERNEL_VERSION}) installed" >&2
  exit 1
fi

%setup
%patch -P 0 -p1


%Build
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
touch config.auto
make config
make all


%Install
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
[ -n "`echo $DESTDIR | sed -n 's:^/tmp/[^.].*$:OK:p'`" ] && rm -rf $DESTDIR ||
(echo "Invalid BuildRoot: '$DESTDIR'! Check this .spec ..."; exit 1) || exit 1
make install

# Install our own network up/down script
mv ${DESTDIR}/etc/pcmcia/network ${DESTDIR}/etc/pcmcia/network.orig
install -m755 $RPM_SOURCE_DIR/pcmcia-cs-network.script \
       ${DESTDIR}/etc/pcmcia/network

# Fix sysconfig options
sed '/^CARDMGR_OPTS=/!b;s/="*\(.*\)"*/="-f \1"/' \
	< ${DESTDIR}/etc/sysconfig/pcmcia \
	> ${DESTDIR}/etc/sysconfig/pcmcia.new
mv ${DESTDIR}/etc/sysconfig/pcmcia{.new,}

# gzip man pages and fix sym-links
MANPATHS=`find $DESTDIR -type d -name "man[1-9n]" -print`
if [ -n "$MANPATHS" ]; then
  chown -Rvc root.root $MANPATHS
  find $MANPATHS -type l -print |
    perl -lne '($f=readlink($_))&&unlink($_)&&symlink("$f.gz","$_.gz")||die;'
  find $MANPATHS -type f -print |
    xargs -r gzip -v9nf
fi


%Clean
DESTDIR=$RPM_BUILD_ROOT;export DESTDIR;[ -n "$UID" ]&&[ "$UID" -gt 0 ]&&exit 0
[ -n "`echo $DESTDIR | sed -n 's:^/tmp/[^.].*$:OK:p'`" ] && rm -rf $DESTDIR ||
(echo "Invalid BuildRoot: '$DESTDIR'! Check this .spec ..."; exit 1) || exit 1


%Post
lisa --SysV-init install pcmcia S01 1:2:3:4:5 K98 0:6


%PostUn
lisa --SysV-init remove pcmcia $1


%Files
%doc SUPPORTED.CARDS CHANGES COPYING README
%doc doc/PCMCIA-HOWTO doc/PCMCIA-PROG
/lib/modules/%{KERNEL_VERSION}/pcmcia

/sbin/cardctl
/sbin/cardmgr
/sbin/ftl_check
/sbin/ftl_format
/sbin/ide_info
/sbin/ifport
/sbin/ifuser
/sbin/pcinitrd
/sbin/probe
/sbin/scsi_info

/usr/X11R6/bin/cardinfo

%{_mandir}/man1/*
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%config /etc/rc.d/init.d/pcmcia
%config /etc/sysconfig/pcmcia
%dir /etc/pcmcia
/etc/pcmcia/cdrom
/etc/pcmcia/cis
/etc/pcmcia/config
/etc/pcmcia/ftl
/etc/pcmcia/ide
/etc/pcmcia/memory
/etc/pcmcia/network
/etc/pcmcia/network.orig
/etc/pcmcia/scsi
/etc/pcmcia/serial
/etc/pcmcia/shared

%config /etc/pcmcia/cdrom.opts
%config /etc/pcmcia/config.opts
%config /etc/pcmcia/ftl.opts
%config /etc/pcmcia/ide.opts
%config /etc/pcmcia/memory.opts
%config /etc/pcmcia/network.opts
%config /etc/pcmcia/scsi.opts
%config /etc/pcmcia/serial.opts


%ChangeLog
* Mon Jan 01 1997 ...

$Id: pcmcia-cs.spec,v 1.2 1999-05-17 10:23:24 kloczek Exp $
