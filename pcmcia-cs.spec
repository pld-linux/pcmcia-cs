Summary:	PCMCIA card services
Summary(pl):	Obs³uga kart PCMCIA
Name:		pcmcia-cs
Version:	3.1.27
Release:	1
License:	MPL (Mozilla Public License)
Group:		Applications/System
Group(pl):	Aplikacje/System
Group(de):	Applikationen/System
Source0:	ftp://projects.sourceforge.net/pub/pcmcia-cs/%{name}-%{version}.tar.gz
Source1:	%{name}-network.script
Source2:	pcmcia.sysconfig
Source3:	pcmcia.init
URL:		http://hyper.stanford.edu/HyperNews/get/pcmcia/home.html
BuildRequires:	kernel-source
Prereq:		chkconfig
ExcludeArch:	sparc sparc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	pcmcia-cs-cardinfo
%if %{?BOOT:1}%{!?BOOT:0}
BuildRequires:	glibc-static
BuildRequires:	uClibc-BOOT
%endif


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
Pakiet pcmcia-cs zawiera programy wspieraj±ce obs³ugê kart PCMCIA w
Twoim PLD-Linuxie. Sk³ada siê on z demona oraz kilku programów
narzêdziowych. Demon ten potrafi reagowaæ na wk³adanie i wyjmowanie
kart PCMCIA, dodaj±c i usuwaj±c odpowiednie drivery (modu³y kernela),
tak i¿ karty mog± byæ wk³adane i wyjmowane w dowolnym momencie. Modu³y
kernela obs³uguj±ce sloty kart i same karty zawarte s± w innych
pakietach, które musz± byæ zainstalowane aby móc korzystaæ z kart. Je¶li
posiadasz laptopa albo te¿ Twój system wykorzystuje karty PCMCIA, ten
pakiet bêdzie Ci niezbêdny.

%if %{?BOOT:1}%{!?BOOT:0}
%package BOOT
Summary:	%{name} for bootdisk
Group:		Applications/System
%description BOOT
%endif


%prep
%setup -q

%build

%if %{?BOOT:1}%{!?BOOT:0}
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

%{__make} -C cardmgr cardmgr CONFIG_PCMCIA=1 \
	CPPFLAGS="-Os -I../include -I%{_kernelsrcdir}/include -I%{_libdir}/bootdisk%{_includedir}" \
	LDFLAGS="-nostdlib -static -s" \
	LDLIBS="%{_libdir}/bootdisk%{_libdir}/crt0.o %{_libdir}/bootdisk%{_libdir}/libc.a -lgcc"

## uClibc lacks outb and family required by probe
## TODO: support for other arch than intel
cat <<EOF >cardmgr/io.c
inline void 
outb (unsigned char value, unsigned short int port) { 
  asm volatile ("outb %b0,%w1": :"a" (value), "Nd" (port)); 
}
inline void 
outw (unsigned short int value, unsigned short int port) {
  asm volatile ("outw %w0,%w1": :"a" (value), "Nd" (port));
}

inline unsigned char 
inb (unsigned short int port) {
  unsigned char _v;
  asm volatile ("inb %w1,%0":"=a" (_v):"Nd" (port));
  return _v;
}

inline unsigned short int 
inw (unsigned short int port) {
  unsigned short _v;
  asm volatile ("inw %w1,%0":"=a" (_v):"Nd" (port));
  return _v;
}
EOF

( cd cardmgr; gcc -c io.c )

%{__make} -C cardmgr probe   CONFIG_PCMCIA=1 \
	CFLAGS="-Os -I%{_kernelsrcdir}/include -I%{_libdir}/bootdisk%{_includedir}" \
	LDFLAGS="-nostdlib -static -s" \
	LDLIBS="%{_libdir}/bootdisk%{_libdir}/crt0.o %{_libdir}/bootdisk%{_libdir}/libc.a -lgcc io.o"

%{__make} -C cardmgr cardctl ide_info scsi_info pcinitrd ifport ifuser  CONFIG_PCMCIA=1 \
	CFLAGS="-Os -I%{_kernelsrcdir}/include -I%{_libdir}/bootdisk%{_includedir}" \
	LDFLAGS="-nostdlib -static -s" \
	LDLIBS="%{_libdir}/bootdisk%{_libdir}/crt0.o %{_libdir}/bootdisk%{_libdir}/libc.a -lgcc"

mv -f cardmgr/cardmgr cardmgr-BOOT
mv -f cardmgr/probe probe-BOOT
mv -f cardmgr/ifuser ifuser-BOOT
mv -f cardmgr/ifport ifport-BOOT
mv -f cardmgr/ide_info ide_info-BOOT
mv -f cardmgr/scsi_info scsi_info-BOOT
mv -f cardmgr/cardctl cardctl-BOOT
#mv -f cardmgr/pcinitrd pcinitrd-BOOT
%{__make} clean
%endif


LDFLAGS="%{rpmldflags}"; export LDFLAGS
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
	CONFIG_PCMCIA=1

%install
rm -rf $RPM_BUILD_ROOT

%if %{?BOOT:1}%{!?BOOT:0}
install -d $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin
for i in *-BOOT; do 
  install -s $i $RPM_BUILD_ROOT/usr/lib/bootdisk/sbin/`basename $i -BOOT`
done

install -d $RPM_BUILD_ROOT/usr/lib/bootdisk/etc/pcmcia
cp -a etc/* $RPM_BUILD_ROOT/usr/lib/bootdisk/etc/pcmcia
install %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/bootdisk/etc/pcmcia/network
%endif

install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/etc/sysconfig,/var/lib/pcmcia}

%{__make} install \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	CONFIG_PCMCIA=1 \

# Install our own network up/down script
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network.orig
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pcmcia/network
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pcmcia
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/pcmcia

gzip -9nf SUPPORTED.CARDS CHANGES COPYING README LICENSE \
	doc/PCMCIA-HOWTO doc/PCMCIA-PROG

%clean
rm -rf $RPM_BUILD_ROOT

%post
chkconfig --add pcmcia
if [ -f /var/lock/subsys/pcmcia ]; then
	/etc/rc.d/init.d/pcmcia restart 2> /dev/null
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
%doc SUPPORTED.CARDS.gz CHANGES.gz COPYING.gz README.gz LICENSE.gz
%doc doc/PCMCIA-HOWTO.gz doc/PCMCIA-PROG.gz
%dir /var/lib/pcmcia
%attr(755,root,root) /sbin/*
%attr(754,root,root) /etc/rc.d/init.d/pcmcia
%config %verify(not size mtime md5) /etc/sysconfig/pcmcia
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
%ifnarch alpha
%{_datadir}/pnp.ids
%endif
%{_mandir}/man4/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%if %{?BOOT:1}%{!?BOOT:0}
%files BOOT
%defattr(644,root,root,755)
%attr(755,root,root) /usr/lib/bootdisk/sbin/*
/usr/lib/bootdisk/%{_sysconfdir}/pcmcia
%endif
