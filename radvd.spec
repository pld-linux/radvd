Summary:	Router Advertisement Daemon
Summary(pl.UTF-8):	Demon ogłaszania routerów
Name:		radvd
Version:	1.8.5
Release:	2
License:	GPL
Group:		Networking
Source0:	http://v6web.litech.org/radvd/dist/%{name}-%{version}.tar.gz
# Source0-md5:	bdeca76d976282c306f3c454d6ff1f67
Source1:	%{name}.conf
Source2:	%{name}.init
Source3:	%{name}.tmpfiles
URL:		http://v6web.litech.org/radvd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.2.0
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/usr/sbin/useradd
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
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

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

%preun
if [ "$1" = "0" ]; then
	%service radvd stop
	/sbin/chkconfig --del radvd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove radvd
fi

%triggerpostun -- %{name} < 1.8.3-2
chmod 0644 /etc/radvd.conf

%files
%defattr(644,root,root,755)
%doc README TODO CHANGES INTRO.html
%attr(754,root,root) /etc/rc.d/init.d/radvd
/usr/lib/tmpfiles.d/%{name}.conf
%attr(755,radvd,root) %dir /var/run/radvd
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radvd.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
