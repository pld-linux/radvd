# $Revision: 1.1 $
Summary:	Router Advertisement Daemon
Summary(pl):	Demon og³aszania routerów
Name:		radvd
Version:	0.5.0
Release:	1
Group:		Networking
Group(pl):	Sieciowe
Copyright:	GPL
Source0:	ftp://ftp.cityline.net/pub/systems/linux/network/ipv6/%{name}/%{name}-%{version}.tar.gz
Source1:	radvd.conf
Source2:	radvd.init
URL:		http://bugs.pld.org.pl
Requires:	rc-scripts >= 0.1.3	
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
This daemon listens to router solicitations (RS) and answers with router
advertisement (RA). Furthermore unsolicited RAs are also send from time
to time.

These RAs contain information, which is used by hosts to configure
their interfaces. This information includes address prefixes, the
MTU of the link and information about default routers.

Router solicitations and router advertisement works only on IPv6
networks.

	 
%description -l pl
Demon ten nas³uchuje komunikatów "router solicitations" (RS) i odpowiada
komunikatami "router adverisement" (RA).

W ten sposób pomaga hostom w sieci konfigurowaæ swoje interfejsy
sieciowe.

Og³aszanie routerów dzia³a tylko w sieciach IPv6


%prep
%setup  -q

%build
LDFLAGS="-s" ; export LDFLAGS
%configure  

make

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/{man5,man8},%{_sysconfdir}/rc.d/init.d}

install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/radvd.conf 
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/radvd

make install \
	prefix=$RPM_BUILD_ROOT/%{_prefix} \
	exec_prefix=$RPM_BUILD_ROOT/%{_exe_prefix}\
        libdir=$RPM_BUILD_ROOT/%{_libdir} \
        sbindir=$RPM_BUILD_ROOT/%{_sbindir} \
        sysconfdir=$RPM_BUILD_ROOT/%{_sysconfdir} \
        mandir=$RPM_BUILD_ROOT/%{_mandir} 

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README TODO CHANGES COPYRIGHT 

%pre

%post
/sbin/chkconfig --add radvd

if [ -f /var/lock/subsys/radvd ]; then
	/etc/rc.d/init.d/radvd restart >&2
fi

%preun
if [ "$1" = 0 ]; then
	/etc/rc.d/init.d/radvd stop >&2
	/sbin/chkconfig --del radvd
fi

%postun

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz TODO.gz CHANGES.gz COPYRIGHT.gz INTRO.html 
%attr(755,root,root) %config /etc/rc.d/init.d/radvd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/radvd.conf
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man5/*
%{_mandir}/man8/*
