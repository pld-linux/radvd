Summary:	Router Advertisement Daemon
Summary(pl):	Demon og³aszania routerów
Name:		radvd
Version:	0.7.1
Release:	1
License:	GPL
Group:		Networking
Source0:	http://v6web.litech.org/radvd/dist/%{name}-%{version}.tar.gz
Source1:	%{name}.conf
Source2:	%{name}.init
Patch0:		%{name}-am_fix.patch
URL:		http://v6web.litech.org/radvd/
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	automake
BuildRequires:	autoconf
Prereq:		rc-scripts >= 0.2.0
Prereq:		/sbin/chkconfig
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

%description -l pl
Demon ten nas³uchuje komunikatów "router solicitations" (RS) i
odpowiada komunikatami "router adverisement" (RA).

W ten sposób pomaga hostom w sieci konfigurowaæ swoje interfejsy
sieciowe.

Og³aszanie routerów dzia³a tylko w sieciach IPv6.

%prep
%setup  -q
%patch0 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c -f
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man{5,8},/etc/rc.d/init.d,}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/radvd.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radvd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README TODO CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add radvd
if [ -f /var/lock/subsys/radvd ]; then
	/etc/rc.d/init.d/radvd restart >&2
else
	echo "Type \"/etc/rc.d/init.d/radvd start\" to start radvd server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/radvd ]; then
		/etc/rc.d/init.d/radvd stop >&2
	fi
	/sbin/chkconfig --del radvd
fi

%files
%defattr(644,root,root,755)
%doc *.gz INTRO.html
%attr(754,root,root) /etc/rc.d/init.d/radvd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/radvd.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
