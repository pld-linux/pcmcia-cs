
%bcond_without dist_kernel	# without kernel from distribution
%bcond_without x		# without XFree and GTK+
%bcond_without xforms		# don't build the XForms version of cardinfo
%bcond_without smp		# don't build the SMP modules

%define	_rel	1
Summary:	Daemon and utilities for using PCMCIA adapters
Summary(es):	Demonio y herramientas para usar adaptadores PCMCIA
Summary(pl):	Obs³uga kart PCMCIA
Summary(ru):	äÅÍÏÎ É ÕÔÉÌÉÔÙ ÄÌÑ ÐÏÌØÚÏ×ÁÎÉÑ PCMCIA-ÁÄÁÐÔÅÒÁÍÉ
Summary(uk):	äÅÍÏÎ ÔÁ ÕÔÉÌ¦ÔÉ ÄÌÑ ËÏÒÉÓÔÕ×ÁÎÎÑ PCMCIA-ÁÄÁÐÔÅÒÁÍÉ
Name:		pcmcia-cs
Version:	3.2.5
Release:	%{_rel}
License:	MPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/pcmcia-cs/%{name}-%{version}.tar.gz
# Source0-md5:	44dbc0a8978fe618eee242b0bd25392c
Source1:	%{name}-network.script
Source2:	pcmcia.sysconfig
Source3:	pcmcia.init
Source4:	ftp://ftp.avaya.com/incoming/Up1cku9/tsoweb/avayawireless/wavelan2_cs-6.16Avaya.tar.gz
# Source4-md5:	8b1829e3554ba15d400ab367e6851437
Source5:	http://pcmcia-cs.sourceforge.net/ftp/contrib/cs89x0_cs.tar.gz
# Source5-md5:	7ef76ff6b798e426f62efac7f4abf636

Patch0:		%{name}-path.patch
Patch1:		%{name}-LDFLAGS.patch
Patch2:		%{name}-wavelan2.patch
Patch3:		%{name}-man.patch
Patch4:		%{name}-realtek_cb-support.patch
# based on http://airsnort.shmoo.com/pcmcia-cs-3.2.1-orinoco-patch.diff
Patch5:		%{name}-orinoco.patch
Patch7:		%{name}-major.patch
Patch8:		%{name}-smp-up.patch
Patch9:		%{name}-no-lib-detect.patch
URL:		http://pcmcia-cs.sourceforge.net/
%{?with_x:BuildRequires:	gtk+-devel}
%{?with_xforms:BuildRequires:	xforms-devel}
%if %{with dist_kernel}
Requires:	kernel(pcmcia)
BuildRequires:	kernel-source
%endif
BuildRequires:	%{kgcc_package}
BuildRequires:	modutils
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post,preun):	/sbin/chkconfig
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pcmcia-cs package adds PCMCIA cards handling support for your
PLD-Linux system and contains of a card manager daemon and some
utilities. PCMCIA daemon can respond to card insertion and removal
events by loading and unloading proper drivers on demand (with hot
swap support), so that the cards can be safely inserted and ejected at
any time. This package does not contain kernel modules (ie. socket and
card drivers) that come with another package that must be installed
for full PCMCIA support. If you own a laptop or your system uses
PCMCIA cards this package is a must.

%description -l es
El paquete pcmcia-cs añade el soporte de tarjetas PCMCIA a su sistema
PLD-Linux y consiste de un demonio de manejador de tarjetas y unas
herramientas. El demonio PCMCIA responde a los eventos de inserción
y extracción cargando y descargando los drivers adecuados (con soporte
de "hot swap") así, que las tarjetas se pueden insertar y extraer en
cualquier momento. Este paquete no contiene módulos de núcleo, los que
están incluidos en otro paquete que tiene que estar instalado para
obtener soporte completo de PCMCIA. Si posee un portátil o su sistema
usa tarjetas PCMCIA, este paquete será indispensable.

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj±ce obs³ugê kart PCMCIA w
Twoim PLD-Linuksie. Sk³ada siê on z demona oraz kilku programów
narzêdziowych. Demon ten potrafi reagowaæ na wk³adanie i wyjmowanie
kart PCMCIA, dodaj±c i usuwaj±c odpowiednie drivery (modu³y kernela),
tak i¿ karty mog± byæ wk³adane i wyjmowane w dowolnym momencie. Modu³y
kernela obs³uguj±ce sloty kart i same karty zawarte s± w innych
pakietach, które musz± byæ zainstalowane aby móc korzystaæ z kart.
Je¶li posiadasz laptopa albo te¿ Twój system wykorzystuje karty
PCMCIA, ten pakiet bêdzie Ci niezbêdny.

%description -l ru
íÎÏÇÉÅ ÌÁÐÔÏÐÙ, ÎÏÕÔÂÕËÉ É ÄÒÕÇÉÅ ÍÁÛÉÎÙ ÐÏÄÄÅÒÖÉ×ÁÀÔ ÒÁÓÛÉÒÅÎÉÅ ÐÒÉ
ÐÏÍÏÝÉ PCMCIA-ËÁÒÔ. éÚ×ÅÓÔÎÙÅ ÔÁËÖÅ ËÁË "credit card adapters",
PCMCIA-ËÁÒÔÙ - ÜÔÏ ÍÁÌÅÎØËÉÅ ËÁÒÔÏÞËÉ, ×ËÌÀÞÁÀÝÉÅ ×ÓÅ, ÞÔÏ ÕÇÏÄÎÏ, ÏÔ
ÐÏÄÄÅÒÖËÉ SCSI ÄÏ ÍÏÄÅÍÏ×. ïÎÉ ÄÏ×ÏÌØÎÏ ÕÄÏÂÎÙ ÔÅÍ, ÞÔÏ ÍÏÇÕÔ ÂÙÔØ
ÐÏÄËÌÀÞÅÎÙ É ÏÔËÌÀÞÅÎÙ ÂÅÚ ÐÅÒÅÚÁÇÒÕÚËÉ ÍÁÛÉÎÙ. îÁÓÔÏÑÝÉÊ ÐÁËÅÔ
ÓÏÄÅÒÖÉÔ ÐÏÄÄÅÒÖËÕ ÒÁÚÎÏÏÂÒÁÚÎÙÈ PCMCIA-ËÁÒÔ ×ÓÅÈ ÒÁÚÎÏ×ÉÄÎÏÓÔÅÊ É
ÄÅÍÏÎ, ËÏÔÏÒÙÊ ÐÏÚ×ÏÌÑÅÔ ÐÏÄËÌÀÞÁÔØ É ÏÔËÌÀÞÁÔØ ÔÁËÉÅ ËÁÒÔÙ "ÎÁ ÈÏÄÕ".

%description -l uk
âÁÇÁÔÏ ÌÁÐÔÏÐ¦×, ÎÏÕÔÂÕË¦× ÔÁ ¦ÎÛÉÈ ÍÁÛÉÎ Ð¦ÄÔÒÉÍÕÀÔØ ÒÏÚÛÉÒÅÎÎÑ ÚÁ
ÄÏÐÏÍÏÇÏÀ PCMCIA-ËÁÒÔ. ÷¦ÄÏÍ¦ ÔÁËÏÖ ÑË "credit card adapters",
PCMCIA-ËÁÒÔÉ - ÃÅ ÍÁÌÅÎØË¦ ËÁÒÔÏÞËÉ, ÝÏ Í¦ÓÔÑÔØ ÝÏ ÚÁ×ÇÏÄÎÏ, ×¦Ä
Ð¦ÄÔÒÉÍËÉ SCSI ÄÏ ÍÏÄÅÍ¦×. ÷ÏÎÉ ÄÏÓÉÔØ ÚÒÕÞÎ¦ ÔÉÍ, ÝÏ ÍÏÖÕÔØ ÂÕÔÉ
Ð¦ÄËÌÀÞÅÎ¦ ÔÁ ×¦ÄËÌÀÞÅÎ¦ ÂÅÚ ÐÅÒÅÚÁÇÒÕÚËÉ ÍÁÛÉÎÉ. ãÅÊ ÐÁËÅÔ Í¦ÓÔÉÔØ
Ð¦ÄÔÒÉÍËÕ Ò¦ÚÎÏÍÁÎ¦ÔÎÉÈ PCMCIA-ËÁÒÔ ×Ó¦È ×ÉÄ¦× ÔÁ ÄÅÍÏÎ, ÝÏ ÄÏÚ×ÏÌÑ¤
Ð¦ÄËÌÀÞÁÔÉ ÔÁ ×¦ÄËÌÀÞÁÔÉ ÔÁË¦ ËÁÒÔÉ "ÎÁ ÈÏÄÕ".

%package -n kernel-pcmcia-cs
Summary:	PCMCIA Card Services kernel modules
Summary(es):	Módulos del núcleo de PCMCIA Card Services
Summary(pl):	Modu³y j±dra PCMCIA Card Services
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(pcmcia)
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-pcmcia-cs
Kernel modules for PCMCIA cards from the Card Services package.

%description -n kernel-pcmcia-cs -l es
Módulos del núcleo para tarjetas PCMCIA del paquete Card Services.

%description -n kernel-pcmcia-cs -l pl
Modu³y j±dra dla kart PCMCIA z pakietu Card Services.

%package -n kernel-pcmcia-wavelan2
Summary:	Avaya Wireless PC Card - Drivers
Summary(es):	Tarjetas PCMCIA inalámbricas de Avaya - Drivers
Summary(pl):	Bezprzewodowe karty PC firmy Avaya - Sterowniki
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires:	kernel(pcmcia)
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel-pcmcia-wavelan2
wavelan2 driver for Avaya Wireless PC Card (Silver and Gold).

%description -n kernel-pcmcia-wavelan2 -l es
El driver wavelan2 para tarjetas PCMCIA inalámbricas Avaya (Silver y
Gold).

%description -n kernel-pcmcia-wavelan2 -l pl
Sterownik wavelan2 do kart Bezprzewodowych PC firmy Avaya (modele
Silver oraz Gold).

%package -n kernel-smp-pcmcia-cs
Summary:	PCMCIA Card Services kernel modules
Summary(es):	Módulos del núcleo de PCMCIA Card Services
Summary(pl):	Modu³y j±dra SMP PCMCIA Card Services
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Provides:	kernel(pcmcia)
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-pcmcia-cs
SMP kernel modules for PCMCIA cards from the Card Services package.

%description -n kernel-smp-pcmcia-cs -l es
Módulos del núcleo SMP para tarjetas PCMCIA del paquete Card Services.

%description -n kernel-smp-pcmcia-cs -l pl
Modu³y j±dra SMP dla kart PCMCIA z pakietu Card Services.

%package -n kernel-smp-pcmcia-wavelan2
Summary:	Avaya Wireless PC Card - Drivers
Summary(es):	Tarjetas PCMCIA inalámbricas de Avaya - Drivers
Summary(pl):	Bezprzewodowe karty PC firmy Avaya - Sterowniki
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires:	kernel(pcmcia)
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-pcmcia-wavelan2
wavelan2 driver for Avaya Wireless PC Card (Silver and Gold).

%description -n kernel-pcmcia-wavelan2 -l es
El driver wavelan2 para tarjetas PCMCIA inalámbricas Avaya (Silver y
Gold).

%description -n kernel-smp-pcmcia-wavelan2 -l pl
Sterownik wavelan2 do kart Bezprzewodowych PC firmy Avaya (modele
Silver oraz Gold).

%package X11
Summary:	X11 Status Monitor
Summary(es):	Monitor del estado para X11
Summary(pl):	Monitor dla X11
Release:	%{_rel}
Group:		X11/Applications
Requires:	%{name} = %{version}-%{_rel}

%description X11
X11 Monitor for PCMCIA.

%description X11 -l es
Monitador de PCMCIA para X11.

%description X11 -l pl
Monitorowanie PCMCIA pod X Window.

%package cardinfo
Summary:	PCMCIA cardinfo utility
Summary(es):	Herramienta de PCMCIA cardinfo
Summary(pl):	Narzêdzie PCMCIA cardinfo
Release:	%{_rel}
Group:		X11/Applications
Requires:	%{name} = %{version}-%{_rel}

%description cardinfo
This package contains the XForms version of the cardinfo utility (whose
basic version is contained in the %{name}-X11 package).

%description cardinfo -l es
Este paquete contiene la versión XForms de la herramienta cardinfo (cuya
versión básica se encuentra en el paquete %{name}-X11).

%description cardinfo -l pl
Ten pakiet zawiera wersjê XForms narzêdzia cardinfo (jego podstawowa
wersja znajduje siê w pakiecie %{name}-X11).

%prep
%setup -q

%patch1 -p1
%ifarch %{ix86}
tar xzvf %{SOURCE4}
%patch2 -p1
%endif
#tar xzvf %{SOURCE5}
%patch3 -p1
%patch4 -p1
#%patch5	-p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

%build
CONFIGOPTS="--noprompt --trust --cardbus --current --pnp --apm --srctree --force"
%if %{with x}
CONFIGOPTS="$CONFIGOPTS --has-xaw --has-gtk"
%endif
%if %{with xforms}
CONFIGOPTS="$CONFIGOPTS --has-forms"
%endif
%if %{with smp}
./Configure \
	$CONFIGOPTS \
	--kernel=%{_kernelsrcdir} \
	--target=$RPM_BUILD_ROOT \
	--smp

%{__make} all \
	CFLAGS="%{rpmcflags} -Wall -Wstrict-prototypes -pipe" \
	LDFLAGS="%{rpmldflags}" \
	CC="%{kgcc}"
	
mkdir modules-smp
mv -f {clients,modules,wireless}/*.o modules-smp
%endif

./Configure \
	$CONFIGOPTS \
	--kernel=%{_kernelsrcdir} \
	--target=$RPM_BUILD_ROOT \
	--up

%{__make} all \
	CFLAGS="%{rpmcflags} -Wall -Wstrict-prototypes -pipe" \
	LDFLAGS="%{rpmldflags}" \
	CC="%{kgcc}" 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/var/lib/pcmcia}

%{__make} install \
	MODDIR=/lib/modules/%{_kernel_ver} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} 
# Move the X11 binaries, if any
mv $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT/usr/X11R6/bin || :

%if %{with smp}
SMPMODDIR=$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/pcmcia
mkdir -p $SMPMODDIR
install modules-smp/*.o $SMPMODDIR
%endif

# The files that we don't want installed
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc.pcmcia
rm -f $RPM_BUILD_ROOT/lib/modules/*/*/8390.o  # it's in the kernel anyway
%ifarch %{ix86}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/config.orig
%endif

# Install our own network up/down script
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network.orig
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcmcia
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcmcia

%ifarch %{ix86}
gzip -9nf *.wavelan2_cs
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add pcmcia
if [ -f /var/lock/subsys/pcmcia ]; then
	echo "You may run \"/etc/rc.d/init.d/pcmcia restart\" to restart with new version"
	echo "of pcmcia cardbus daemon. Note that if you changed your kernel, restarting"
	echo "pcmcia subsystem may cause problems if not rebooted before."
else
	echo "Run \"/etc/rc.d/init.d/pcmcia start\" to start pcmcia cardbus daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/state/run/pcmcia ]; then
		/etc/rc.d/init.d/pcmcia stop 2> /dev/null
	fi
	/sbin/chkconfig --del pcmcia
fi

%post -n kernel-pcmcia-cs
%depmod %{_kernel_ver}

%postun -n kernel-pcmcia-cs
%depmod %{_kernel_ver}

%post -n kernel-smp-pcmcia-cs
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-pcmcia-cs
%depmod %{_kernel_ver}smp

%post -n kernel-pcmcia-wavelan2
%depmod %{_kernel_ver}

%postun -n kernel-pcmcia-wavelan2
%depmod %{_kernel_ver}

%post -n kernel-smp-pcmcia-wavelan2
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-pcmcia-wavelan2
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc SUPPORTED.CARDS CHANGES COPYING README{,-2.4}
%doc LICENSE doc/PCMCIA-HOWTO doc/PCMCIA-PROG
%dir /var/lib/pcmcia
%attr(755,root,root) /sbin/*
%attr(754,root,root) /etc/rc.d/init.d/pcmcia
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/pcmcia
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/*.opts
%attr(754,root,root) %{_sysconfdir}/pcmcia/ftl
%attr(754,root,root) %{_sysconfdir}/pcmcia/ide
%attr(754,root,root) %{_sysconfdir}/pcmcia/ieee1394
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
%ifnarch alpha ppc
%{_datadir}/pnp.ids
%endif
%{_mandir}/man*/*

%if %{with x}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/bin/*
%exclude /usr/X11R6/bin/cardinfo
%endif

%if %{with xforms}
%files cardinfo
%defattr(644,root,root,755)
%attr(755,root,root) /usr/X11R6/bin/cardinfo
%endif

%files -n kernel-pcmcia-cs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/pcmcia/*
%exclude /lib/modules/%{_kernel_ver}/pcmcia/wavelan2*

%if %{with smp}
%files -n kernel-smp-pcmcia-cs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/pcmcia/*
%exclude /lib/modules/%{_kernel_ver}smp/pcmcia/wavelan2*
%endif

%ifarch %{ix86}
%files -n kernel-pcmcia-wavelan2
%doc *wavelan2*
/lib/modules/%{_kernel_ver}/pcmcia/wavelan2*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wavelan2*
%endif

%if %{with smp}
%ifarch %{ix86}
%files -n kernel-smp-pcmcia-wavelan2
%doc *wavelan2*
/lib/modules/%{_kernel_ver}smp/pcmcia/wavelan2*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wavelan2*
%endif
%endif
