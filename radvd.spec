Summary:	Router Advertisement Daemon
Summary(pl.UTF-8):	Demon ogłaszania routerów
Name:		radvd
Version:	2.21
Release:	3
License:	BSD
Group:		Networking
Source0:	https://github.com/radvd-project/radvd/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	44b1883c193afd55d396ab76556d6f66
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.tmpfiles
URL:		https://github.com/radvd-project/radvd
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1.2
BuildRequires:	bison
BuildRequires:	flex
# or glibc-devel>=2.17 + libbsd-devel (for strlcpy)
BuildRequires:	glibc-devel >= 6:2.38
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.2.0
Requires:	systemd-units >= 38
Provides:	user(radvd)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This daemon listens to router solicitations (RS) and answers with
router advertisement (RA). Furthermore unsolicited RAs are also send
from time to time.

These RAs contain information, which is used by hosts to configure
their interfaces. This information includes address prefixes, the MTU
of the link and information about default routers.

Router solicitations and router advertisement works only on IPv6
networks.

%description -l pl.UTF-8
Demon ten nasłuchuje komunikatów "router solicitations" (RS) i
odpowiada komunikatami "router adverisement" (RA).

W ten sposób pomaga hostom w sieci konfigurować swoje interfejsy
sieciowe.

Ogłaszanie routerów działa tylko w sieciach IPv6.

%prep
%setup  -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-systemdsystemunitdir=%{systemdunitdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/rc.d/init.d,/var/run/radvd} \
	$RPM_BUILD_ROOT/usr/lib/tmpfiles.d

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/radvd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radvd
install %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 260 -d /usr/share/empty -s /bin/false -c "radvd" -g proc radvd

%post
/sbin/chkconfig --add radvd
%service radvd restart "radvd server"
%systemd_post radvd.service

%preun
if [ "$1" = "0" ]; then
	%service radvd stop
	/sbin/chkconfig --del radvd
fi
%systemd_preun radvd.service

%postun
if [ "$1" = "0" ]; then
	%userremove radvd
fi
%systemd_reload

%triggerpostun -- %{name} < 2.21-3
%systemd_trigger radvd.service

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYRIGHT README.md SECURITY.md TODO INTRO.html
%attr(754,root,root) /etc/rc.d/init.d/radvd
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/radvd.service
%attr(755,radvd,root) %dir /var/run/radvd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radvd.conf
%attr(755,root,root) %{_sbindir}/radvd
%attr(755,root,root) %{_sbindir}/radvdump
%{_mandir}/man5/radvd.conf.5*
%{_mandir}/man8/radvd.8*
%{_mandir}/man8/radvdump.8*
