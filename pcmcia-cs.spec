Summary: 	PCMCIA card services.
Summary(pl):	Obs�uga kart PCMCIA.
Name:		pcmcia-cs
Version:	3.0.14
Release:	1
Group:		Utilities/System
Group(pl):	Narz�dzie/System
Copyright:	MPL (Mozilla Public License)
URL:		http://hyper.stanford.edu/HyperNews/get/pcmcia/home.html
Requires:	xforms
BuildPrereq:	xforms-static, kernel-source
BuildPrereq:	xforms-devel
BuildPrereq:	kernel-source
Prereq:		chkconfig
BuildRoot:	/tmp/%{name}-%{version}-root
Source0: 	ftp://csb.stanford.edu/pub/pcmcia/pcmcia-cs-%{version}.tar.gz
Source1: 	pcmcia-cs-network.script
Source2: 	pcmcia.sysconfig
Patch0:		pcmcia-nokernelmod.patch
Patch1:		pcmcia-chkconfig-pld.patch

%description
The pcmcia-cs package adds PCMCIA cards handling support for your PLD-Linux 
system and contains of a card manager daemon and some utilities. PCMCIA 
daemon can respond to card insertion and removal events by loading and unloading
proper drivers on demand (with hot swap support), so that the cards can be safely 
inserted and ejected at any time. 

This package does not contain kernel modules (ie. socket and card drivers) 
that come with another package that must be installed for full PCMCIA
support.

If you own a laptop or your system uses PCMCIA cards this package is a must.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj�ce obs�ug� kart PCMCIA w twoim
PLD-Linuxie. Sk�ada si� on z demona oraz kilku program�w narz�dziowych.
Demon ten potrafi reagowa� na wk�adanie i wyjmowanie kart PCMCIA, �aduj�c i
usuwaj�c odpowiednie drivery (modu�y kernela), tak i� karty mog� by�
wk�adane i wyjmowane w dowolnym momencie.

Modu�y kernela obs�uguj�ce sloty kart i same karty zawarte s� w innym
pakiecie, kt�ry musi by� zainstalowany aby m�c korzysta� z kart.

Je�li posiadasz laptopa lub tw�j system wykorzystuje karty PCMCIA ten pakiet
jest niezb�dny.

%prep

%setup -q
%patch0 -p0 
%patch1 -p0

%build
LDFLAGS="-s"; export LDFLAGS

./Configure -n --trust --cardbus --current --target=$RPM_BUILD_ROOT \
    --srctree --kernel=/usr/src/linux
make CFLAGS="$RPM_OPT_FLAGS -Wall -Wstrict-prototypes -pipe " \
    XFLAGS="$RPM_OPT_FLAGS -O -pipe " \
    all

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
make MANDIR=${RPM_BUILD_ROOT}%{_mandir} install

# Install our own network up/down script
mv $RPM_BUILD_ROOT/etc/pcmcia/network $RPM_BUILD_ROOT/etc/pcmcia/network.orig
install -m755 %{SOURCE1} $RPM_BUILD_ROOT/etc/pcmcia/network
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
mv $RPM_BUILD_ROOT/etc/rc.d/rc.pcmcia $RPM_BUILD_ROOT/etc/rc.d/init.d/pcmcia
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
cp -f %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcmcia

gzip -9nr $RPM_BUILD_ROOT/{%{_mandir}/man*/*,usr/X11R6/man/man1/*}
gzip -9nr ${RPM_BUILD_DIR}/%{name}-%{version}/{SUPPORTED.CARDS,\
CHANGES,COPYING,README,LICENSE,doc/PCMCIA-HOWTO,doc/PCMCIA-PROG}

mv $RPM_BUILD_ROOT/usr/X11R6/man/man1/cardinfo.1.gz \
  $RPM_BUILD_ROOT/usr/X11R6/man/man1/cardinfo.1x.gz

#MANPATHS=`find $DESTDIR -type d -name "man[1-9n]" -print`
#if [ -n "$MANPATHS" ]; then
#  chown -Rvc root.root $MANPATHS
#  find $MANPATHS -type l -print |
#    perl -lne '($f=readlink($_))&&unlink($_)&&symlink("$f.gz","$_.gz")||die;'
#  find $MANPATHS -type f -print |
#    xargs -r gzip -v9nf
#fi


%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add pcmcia

%postun
[ "$1" = 0 ] && chkconfig --del pcmcia

%files
%defattr(755,root,root,755)
%doc %attr(644,root,root) SUPPORTED.CARDS.gz CHANGES.gz COPYING.gz
%doc %attr(644,root,root) README.gz LICENSE.gz
%doc %attr(644,root,root) doc/PCMCIA-HOWTO.gz doc/PCMCIA-PROG.gz
/sbin/cardctl
/sbin/cardmgr
/sbin/ftl_check
/sbin/ftl_format
/sbin/ide_info
/sbin/ifport
/sbin/ifuser
/sbin/pcinitrd
/sbin/probe
/sbin/dump_cis
/sbin/pack_cis
/usr/X11R6/bin/cardinfo

%attr(644,root,root) %{_mandir}/man4/*
%attr(644,root,root) %{_mandir}/man5/*
%attr(644,root,root) %{_mandir}/man8/*
%attr(644,root,root) /usr/X11R6/man/man*/*

/etc/pcmcia/cdrom
/etc/pcmcia/config
/etc/pcmcia/ftl
/etc/pcmcia/ide
/etc/pcmcia/memory
/etc/pcmcia/network
/etc/pcmcia/network.orig
/etc/pcmcia/scsi
/etc/pcmcia/serial
/etc/pcmcia/shared

/etc/rc.d/init.d/pcmcia
%config %attr(644,root,root) /etc/sysconfig/pcmcia

%config %attr(644,root,root) /etc/pcmcia/cdrom.opts
%config %attr(644,root,root) /etc/pcmcia/config.opts
%config %attr(644,root,root) /etc/pcmcia/ftl.opts
%config %attr(644,root,root) /etc/pcmcia/ide.opts
%config %attr(644,root,root) /etc/pcmcia/memory.opts
%config %attr(644,root,root) /etc/pcmcia/network.opts
%config %attr(644,root,root) /etc/pcmcia/scsi.opts
%config %attr(644,root,root) /etc/pcmcia/serial.opts

%attr(644,root,root) /etc/pcmcia/cis/*
