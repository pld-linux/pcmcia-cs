Summary:	PCMCIA card services
Summary(pl):	Obs³uga kart PCMCIA
Name:		pcmcia-cs
Version:	3.1.21
Release:	1
Group:		Applications/System
Group(pl):	Aplikacje/System
Group(de):	Applikationen/System
License:	MPL (Mozilla Public License)
Source0:	ftp://projects.sourceforge.net/pub/pcmcia-cs/%{name}-%{version}.tar.gz
Source1:	%{name}-network.script
Source2:	pcmcia.sysconfig
Source3:	pcmcia.init
URL:		http://hyper.stanford.edu/HyperNews/get/pcmcia/home.html
BuildRequires:	kernel-source
BuildRequires:	xforms-static
BuildRequires:	xforms-devel
Prereq:		chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pcmcia-cs package adds PCMCIA cards handling support for your
PLD-Linux ystem and contains of a card manager daemon and some
utilities. PCMCIA daemon can respond to card insertion and removal
events by loading and unloading proper drivers on demand (with hot
swap support), so that the cards can be safely inserted and ejected at
any time. This package does not contain kernel modules (ie. socket and
card drivers) that come with another package that must be installed
for full PCMCIA support. If you own a laptop or your system uses
PCMCIA cards this package is a must.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj±ce obs³ugê kart PCMCIA w
Twoim PLD-Linuxie. Sk³ada siê on z demona oraz kilku programów
narzêdziowych. Demon ten potrafi reagowaæ na wk³adanie i wyjmowanie
kart PCMCIA, dodaj±c i usuwaj±c odpowiednie drivery (modu³y kernela),
tak i¿ karty mog± byæ wk³adane i wyjmowane w dowolnym momencie. Modu³y
kernela obs³uguj±ce sloty kart i same karty zawarte s± w innych
pakietach, które musz± byæ zainstalowane aby móc korzystaæ kart. Je¶li
posiadasz laptopa albo te¿ Twój system wykorzystuje karty PCMCIA, ten
pakiet bêdzie Ci niezbêdny.

%package cardinfo
Summary:	PCMCIA card monitor and control utility for X
Summary(pl):	Monitor i narzêdzie kontroluj±ce kart PCMCIA dla Xów
Group:		Applications/System
Group(pl):	Aplikacje/System
Group(de):	Applikationen/System
Requires:	xforms

%description cardinfo
PCMCIA card monitor and control utility for X.

%description cardinfo -l pl
Monitor i narzêdzie kontroluj±ce kart PCMCIA dla Xów.

%prep
%setup -q

%build
LDFLAGS="-s"; export LDFLAGS

./Configure \
	--noprompt \
	--trust \
	--cardbus \
	--current \
	--pnp \
	--apm \
	--srctree \
	--kernel=%{_prefix}/src/linux \
	--target=$RPM_BUILD_ROOT

%{__make} all \
	CFLAGS="$RPM_OPT_FLAGS -Wall -Wstrict-prototypes -pipe" \
	CONFIG_PCMCIA=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{rc.d/init.d,sysconfig},/var/lib/pcmcia}

%{__make} install \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	CONFIG_PCMCIA=1

# Install our own network up/down script
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network.orig
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/pcmcia
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/pcmcia

gzip -9nf $RPM_BUILD_ROOT/{%{_mandir}/man*/*,usr/X11R6/man/man1/*} \
	SUPPORTED.CARDS CHANGES COPYING README LICENSE \
	doc/PCMCIA-HOWTO doc/PCMCIA-PROG

mv -f $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1/cardinfo.1.gz \
  $RPM_BUILD_ROOT%{_prefix}/X11R6/man/man1/cardinfo.1x.gz

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add pcmcia
if [ -f /var/lock/subsys/pcmcia ]; then
	/rc.d/init.d/pcmcia restart 2> /dev/null
else
	echo "Run \"/rc.d/init.d/pcmcia start\" to start pcmcia cardbus daemon."
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/state/run/pcmcia ]; then
		/rc.d/init.d/pcmcia stop 2> /dev/null
	fi
	/sbin/chkconfig --del pcmcia
fi

%files
%defattr(644,root,root,755)
%doc SUPPORTED.CARDS.gz CHANGES.gz COPYING.gz README.gz LICENSE.gz
%doc doc/PCMCIA-HOWTO.gz doc/PCMCIA-PROG.gz
%dir /var/lib/pcmcia
%attr(755,root,root) /sbin/*

%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/pcmcia
%config %verify(not size mtime md5) %{_sysconfdir}/sysconfig/pcmcia
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/config.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/ftl.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/ide.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/memory.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/parport.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/scsi.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/serial.opts
%config %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wireless.opts
%attr(754,root,root) %{_sysconfdir}/pcmcia/ftl
%attr(754,root,root) %{_sysconfdir}/pcmcia/ide
%attr(754,root,root) %{_sysconfdir}/pcmcia/memory
%attr(754,root,root) %{_sysconfdir}/pcmcia/network
%attr(754,root,root) %{_sysconfdir}/pcmcia/parport
%attr(754,root,root) %{_sysconfdir}/pcmcia/scsi
%attr(754,root,root) %{_sysconfdir}/pcmcia/serial
%attr(754,root,root) %{_sysconfdir}/pcmcia/wireless
%{_sysconfdir}/pcmcia/cis
%{_sysconfdir}/pcmcia/config
%{_sysconfdir}/pcmcia/network.orig
%{_sysconfdir}/pcmcia/shared
%{_datadir}/pnp.ids
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files cardinfo
%defattr(644,root,root,755)
%attr(755,root,root) %{_prefix}/X11R6/bin/cardinfo
%{_prefix}/X11R6/man/man1/*
