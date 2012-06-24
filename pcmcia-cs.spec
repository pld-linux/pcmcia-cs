Summary:	PCMCIA card services.
Summary(pl):	Obs�uga kart PCMCIA.
Name:		pcmcia-cs
Version:	3.1.14
Release:	1
Group:		Utilities/System
Group(pl):	Narz�dzia/System
Copyright:	MPL (Mozilla Public License)
URL:		http://hyper.stanford.edu/HyperNews/get/pcmcia/home.html
BuildRequires:	kernel-source
BuildRequires:	xforms-static
BuildRequires:	xforms-devel
Prereq:		chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Source0:	ftp://sourceforge.org/pcmcia/%{name}-%{version}.tar.gz
Source1:	pcmcia-cs-network.script
Source2:	pcmcia.sysconfig
Source3:	pcmcia.init

%description
The pcmcia-cs package adds PCMCIA cards handling support for your PLD-Linux
ystem and contains of a card manager daemon and some utilities. PCMCIA
daemon can respond to card insertion and removal events by loading and
unloading proper drivers on demand (with hot swap support), so that the
cards can be safely  inserted and ejected at any time. This package does
not contain kernel modules (ie. socket and card drivers) that come with
another package that must be installed for full PCMCIA support. If you own
a laptop or your system uses PCMCIA cards this package is a must.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj�ce obs�ug� kart PCMCIA w Twoim
PLD-Linuxie. Sk�ada si� on z demona oraz kilku program�w narz�dziowych.
Demon ten potrafi reagowa� na wk�adanie i wyjmowanie kart PCMCIA, dodaj�c i
usuwaj�c odpowiednie drivery (modu�y kernela), tak i� karty mog� by�
wk�adane i wyjmowane w dowolnym momencie. Modu�y kernela obs�uguj�ce sloty
kart i same karty zawarte s� w innych pakietach, kt�re musz� by�
zainstalowane aby m�c korzysta� kart. Je�li posiadasz laptopa albo te� Tw�j
system wykorzystuje karty PCMCIA, ten pakiet b�dzie Ci niezb�dny.

%package cardinfo
Summary:	PCMCIA card monitor and control utility for X
Summary(pl):	Monitor i narz�dzie kontroluj�ce kart PCMCIA dla X�w
Group:		X11/Utilities/System
Group(pl):	X11/Narz�dzia/System
Requires:	xforms

%description cardinfo
PCMCIA card monitor and control utility for X.

%description cardinfo -l pl
Monitor i narz�dzie kontroluj�ce kart PCMCIA dla X�w.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS

./Configure -n --trust --cardbus --current --target=$RPM_BUILD_ROOT \
    --pnp --srctree --kernel=%{_prefix}/src/linux
make CFLAGS="$RPM_OPT_FLAGS -Wall -Wstrict-prototypes -pipe " \
    XFLAGS="$RPM_OPT_FLAGS -O -pipe " \
    all

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT; export DESTDIR
make MANDIR=${RPM_BUILD_ROOT}%{_mandir} install

# Install our own network up/down script
mv $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network.orig
install -m755 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
mv $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc.pcmcia $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pcmcia
install -d $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
cp -f %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/pcmcia

install -m754 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pcmcia
install -d $RPM_BUILD_ROOT/var/state/pcmcia

gzip -9nf $RPM_BUILD_ROOT/{%{_mandir}/man*/*,usr/X11R6/man/man1/*}
gzip -9nf ${RPM_BUILD_DIR}/%{name}-%{version}/{SUPPORTED.CARDS,\
CHANGES,COPYING,README,LICENSE,doc/PCMCIA-HOWTO,doc/PCMCIA-PROG}

mv $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1/cardinfo.1.gz \
  $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1/cardinfo.1x.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add pcmcia

%postun
[ "$1" = 0 ] && chkconfig --del pcmcia

%files
%defattr(644,root,root,755)
%doc SUPPORTED.CARDS.gz CHANGES.gz COPYING.gz
%doc README.gz LICENSE.gz
%doc doc/PCMCIA-HOWTO.gz doc/PCMCIA-PROG.gz
/sbin/*
#%{_datadir}/pnp.ids

%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

#%{_sysconfdir}/pcmcia/cdrom
%{_sysconfdir}/pcmcia/config
%{_sysconfdir}/pcmcia/ftl
%{_sysconfdir}/pcmcia/ide
%{_sysconfdir}/pcmcia/memory
%{_sysconfdir}/pcmcia/network
%{_sysconfdir}/pcmcia/network.orig
%{_sysconfdir}/pcmcia/scsi
%{_sysconfdir}/pcmcia/serial
%{_sysconfdir}/pcmcia/shared

%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/pcmcia
%config %{_sysconfdir}/sysconfig/pcmcia

#%config %attr(644,root,root) %{_sysconfdir}/pcmcia/cdrom.opts
%config %{_sysconfdir}/pcmcia/config.opts
%config %{_sysconfdir}/pcmcia/ftl.opts
%config %{_sysconfdir}/pcmcia/ide.opts

%files cardinfo
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/cardinfo
%{_prefix}/X11R6/man/man*/*
