#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
# _without_x		- without XFree and gtk+
#
# TODO: UP/SMP for kernel-pcmcia-wavelan2?
%define	_rel	1
Summary:	Daemon and utilities for using PCMCIA adapters
Summary(pl):	ObsЁuga kart PCMCIA
Summary(ru):	Демон и утилиты для пользования PCMCIA-адаптерами
Summary(uk):	Демон та утил╕ти для користування PCMCIA-адаптерами
Name:		pcmcia-cs
Version:	3.2.4
Release:	%{_rel}
License:	MPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/pcmcia-cs/%{name}-%{version}.tar.gz
# Source0-md5:	126e2d87e7a8a12e283db37ae82e9e4c
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
URL:		http://pcmcia-cs.sourceforge.net/
%{!?_without_x:BuildRequires:	XFree86-devel}
%{!?_without_x:BuildRequires:	gtk+-devel}
%{!?_without_dist_kernel:Requires:	kernel-pcmcia-cs}
%{!?_without_dist_kernel:BuildRequires:	kernel-source}
BuildRequires:	%{kgcc_package}
BuildRequires:	modutils
BuildRequires:	rpmbuild(macros) >= 1.118
Requires(post,preun):	/sbin/chkconfig
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	pcmcia-cs-cardinfo

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

%description -l pl
Pakiet pcmcia-cs zawiera programy wspieraj╠ce obsЁugЙ kart PCMCIA w
Twoim PLD-Linuksie. SkЁada siЙ on z demona oraz kilku programСw
narzЙdziowych. Demon ten potrafi reagowaФ na wkЁadanie i wyjmowanie
kart PCMCIA, dodaj╠c i usuwaj╠c odpowiednie drivery (moduЁy kernela),
tak i© karty mog╠ byФ wkЁadane i wyjmowane w dowolnym momencie. ModuЁy
kernela obsЁuguj╠ce sloty kart i same karty zawarte s╠ w innych
pakietach, ktСre musz╠ byФ zainstalowane aby mСc korzystaФ z kart.
Je╤li posiadasz laptopa albo te© TwСj system wykorzystuje karty
PCMCIA, ten pakiet bЙdzie Ci niezbЙdny.

%description -l ru
Многие лаптопы, ноутбуки и другие машины поддерживают расширение при
помощи PCMCIA-карт. Известные также как "credit card adapters",
PCMCIA-карты - это маленькие карточки, включающие все, что угодно, от
поддержки SCSI до модемов. Они довольно удобны тем, что могут быть
подключены и отключены без перезагрузки машины. Настоящий пакет
содержит поддержку разнообразных PCMCIA-карт всех разновидностей и
демон, который позволяет подключать и отключать такие карты "на ходу".

%description -l uk
Багато лаптоп╕в, ноутбук╕в та ╕нших машин п╕дтримують розширення за
допомогою PCMCIA-карт. В╕дом╕ також як "credit card adapters",
PCMCIA-карти - це маленьк╕ карточки, що м╕стять що завгодно, в╕д
п╕дтримки SCSI до модем╕в. Вони досить зручн╕ тим, що можуть бути
п╕дключен╕ та в╕дключен╕ без перезагрузки машини. Цей пакет м╕стить
п╕дтримку р╕зноман╕тних PCMCIA-карт вс╕х вид╕в та демон, що дозволя╓
п╕дключати та в╕дключати так╕ карти "на ходу".

%package -n kernel-pcmcia-wavelan2
Summary:	Avaya Wireless PC Card - Drivers
Summary(pl):	Bezprzewodowe karty PC firmy Avaya - Sterowniki
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-pcmcia-wavelan2
wavelan2 driver for Avaya Wireless PC Card (Silver and Gold).

%description -n kernel-pcmcia-wavelan2 -l pl
Sterownik wavelan2 do kart Bezprzewodowych PC firmy Avaya (modele
Silver oraz Gold).

%package X11
Summary:	X11 Status Monitor
Summary(pl):	Monitor dla X11
Release:	%{_rel}
Group:		X11/Applications

%description X11
X11 Monitor for PCMCIA.

%description X11
Monitorowanie PCMCIA pod X Window.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%ifarch %{ix86}
tar xzvf %{SOURCE4}
%patch2 -p1
%endif
tar xzvf %{SOURCE5}
%patch3 -p1
%patch4 -p1
%patch5	-p1

%build
./Configure \
	--noprompt \
	--trust \
	--cardbus \
	--current \
	--pnp \
	--apm \
	--srctree \
	--kernel=%{_kernelsrcdir} \
	--target=$RPM_BUILD_ROOT

%{__make} all \
	CFLAGS="%{rpmcflags} -Wall -Wstrict-prototypes -pipe" \
	LDFLAGS="%{rpmldflags}" \
	CC="%{kgcc}" \
	CONFIG_PCMCIA=1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/var/lib/pcmcia}

%{__make} install \
	MODDIR=/lib/modules/%{_kernel_ver} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	CONFIG_PCMCIA=1 \

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

%post   -n kernel-pcmcia-wavelan2
%depmod %{_kernel_ver}

%postun -n kernel-pcmcia-wavelan2
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc SUPPORTED.CARDS CHANGES COPYING README{,-2.4}
%doc LICENSE doc/PCMCIA-HOWTO doc/PCMCIA-PROG
%dir /var/lib/pcmcia
%attr(755,root,root) /sbin/*
%attr(754,root,root) /etc/rc.d/init.d/pcmcia
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/pcmcia
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/config.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/cs89x0.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/ftl.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/ide.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/ieee1394.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/memory.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/network.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/parport.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/scsi.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/serial.opts
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wireless.opts
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
%ifnarch alpha ppc
%{_datadir}/pnp.ids
%endif
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%if %{!?_without_x:1}0
%files X11
%defattr(644,root,root,755)
%{_bindir}/gpccard
%{_bindir}/xcardinfo
%endif

%ifarch %{ix86}
%files -n kernel-pcmcia-wavelan2
%defattr(644,root,root,755)
%doc *wavelan2*
/lib/modules/%{_kernel_ver}/pcmcia/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pcmcia/wavelan2*
%endif
