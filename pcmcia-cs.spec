#
# Conditional build:
%bcond_without x11		# without X11-based utilities
#
Summary:	Daemon and utilities for using PCMCIA adapters
Summary(es):	Demonio y herramientas para usar adaptadores PCMCIA
Summary(pl):	ObsЁuga kart PCMCIA
Summary(ru):	Демон и утилиты для пользования PCMCIA-адаптерами
Summary(uk):	Демон та утил╕ти для користування PCMCIA-адаптерами
Name:		pcmcia-cs
Version:	3.2.8
Release:	4
License:	MPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/pcmcia-cs/%{name}-%{version}.tar.gz
# Source0-md5:	0d6d65be8896eff081aee996049afaa5
Source1:	%{name}-network.script
Source2:	pcmcia.sysconfig
Source3:	pcmcia.init
Patch0:		%{name}-path.patch
Patch1:		%{name}-LDFLAGS.patch
Patch2:		%{name}-llh.patch
Patch3:		%{name}-man.patch
Patch4:		%{name}-realtek_cb-support.patch
Patch5:		%{name}-major.patch
Patch6:		%{name}-original-config.patch
Patch7:		%{name}-build.patch
URL:		http://pcmcia-cs.sourceforge.net/
%{?with_x11:BuildRequires:	gtk+2-devel}
%{?with_x11:BuildRequires:	pkgconfig}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_x11:BuildRequires:	xforms-devel}
Requires(post,preun):	/sbin/chkconfig
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/
%define		_bindir		/bin

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
El paquete pcmcia-cs aЯade el soporte de tarjetas PCMCIA a su sistema
PLD-Linux y consiste de un demonio de manejador de tarjetas y unas
herramientas. El demonio PCMCIA responde a los eventos de inserciСn y
extracciСn cargando y descargando los drivers adecuados (con soporte
de "hot swap") asМ, que las tarjetas se pueden insertar y extraer en
cualquier momento. Este paquete no contiene mСdulos de nЗcleo, los que
estАn incluidos en otro paquete que tiene que estar instalado para
obtener soporte completo de PCMCIA. Si posee un portАtil o su sistema
usa tarjetas PCMCIA, este paquete serА indispensable.

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

%package X11
Summary:	X11 Status Monitor
Summary(es):	Monitor del estado para X11
Summary(pl):	Monitor dla X11
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Obsoletes:	pcmcia-cs-cardinfo

%description X11
X11 Monitor for PCMCIA.

%description X11 -l es
Monitador de PCMCIA para X11.

%description X11 -l pl
Monitorowanie PCMCIA pod X Window.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
chmod -R u+rwX .
cat <<EOF > config.mk
LINUX=/usr
PREFIX=%{_prefix}
UCC=%{__cc}
LD=ld
UFLAGS=
CPPFLAGS=-I../include
SYSV_INIT=y
RC_DIR=/etc/rc.d
MANDIR=%{_mandir}
%if %{with x11}
GTK_CFLAGS=`pkg-config --cflags gtk+-2.0`
GTK_LIBS=`pkg-config --libs gtk+-2.0`
FLIBS=-L/usr/X11R6/%{_lib} -lforms -lm
HAS_XAW=y
HAS_GTK=y
HAS_FORMS=y
%endif
CONFIG_INET=y
CONFIG_SCSI=y
DO_IDE=y
CONFIG_ISA=y
EOF
ln -s config.mk config.out

cat <<EOF > include/pcmcia/config.h
#ifndef _PCMCIA_CONFIG_H
#define _PCMCIA_CONFIG_H
#define AUTOCONF_INCLUDED
#define __IN_PCMCIA_PACKAGE__
#define LINUX "/usr/include"
#define PREFIX ""
#define KCC "%{__cc}"
#define UCC "%{__cc}"
#define LD "ld"
#define UFLAGS ""
#define SYSV_INIT 1
#define RC_DIR "%{_sysconfdir}/rc.d"
#define MANDIR "%{_mandir}"
#endif /* _PCMCIA_CONFIG_H */
EOF

%{__make} all \
	CFLAGS="%{rpmcflags} -Wall -Wstrict-prototypes -pipe" \
	LDFLAGS="%{rpmldflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/var/lib/pcmcia,%{_bindir},/usr/bin}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}

%if %{with x11}
mv -f $RPM_BUILD_ROOT/usr/X11R6/bin/{,x}cardinfo $RPM_BUILD_ROOT/usr/bin
%endif

# The files that we don't want installed
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/rc.pcmcia
%ifarch %{ix86}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/config.orig
%endif

# Install our own network up/down script
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network.orig
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcmcia
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcmcia

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add pcmcia
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
%{_mandir}/man*/*

%if %{with x11}
%files X11
%defattr(644,root,root,755)
%attr(755,root,root) /usr/bin/*
%endif
