%define debug_package %{nil}

Name:    blackbox_exporter
Version: 0.14.0
Release: 1%{?dist}
Summary: Blackbox exporter
License: ASL 2.0
URL:     https://github.com/prometheus/blackbox_exporter

#Source0: https://github.com/prometheus/blackbox_exporter/releases/download/v%{version}/blackbox_exporter-%{version}.linux-amd64.tar.gz
Source0: %{name}-%{version}.linux-amd64.tar.gz
Source1: blackbox_exporter.service
Source2: blackbox_exporter.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description

The blackbox exporter allows blackbox probing of endpoints over HTTP, HTTPS, DNS, TCP and ICMP.

%prep
%setup -q -n blackbox_exporter-%{version}.linux-amd64

%build
/bin/true

%install
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/usr/lib/systemd/system
mkdir -vp %{buildroot}/etc/default

mkdir -vp %{buildroot}/etc/blackbox_exporter
mkdir -vp %{buildroot}/var/lib/blackbox_exporter

install -m 755 blackbox_exporter %{buildroot}/usr/bin/blackbox_exporter

install -D -m 644 blackbox.yml %{buildroot}%{_sysconfdir}/blackbox_exporter/blackbox.yml
#install -m 644 blackbox.yml %{buildroot}/etc/blackbox_exporter/blackbox.yml

install -D -m 644 %{SOURCE1} %{buildroot}/etc/systemd/system/blackbox_exporter.service
#install -m 644 %{SOURCE1} %{buildroot}/etc/systemd/system/blackbox_exporter.service

install -m 644 %{SOURCE2} %{buildroot}/etc/default/blackbox_exporter

%pre
getent group blackbox_exporter >/dev/null || groupadd -r blackbox_exporter
getent passwd blackbox_exporter >/dev/null || \
  useradd -r -g blackbox_exporter -d /var/lib/blackbox_exporter -s /sbin/nologin \
          -c "Blackbox Exporter Services" blackbox_exporter
exit 0

%post
%systemd_post blackbox_exporter.service

%preun
%systemd_preun blackbox_exporter.service

%postun
%systemd_postun blackbox_exporter.service

%files
%defattr(-,root,root,-)
%{_bindir}/blackbox_exporter
%config(noreplace) /etc/systemd/system/blackbox_exporter.service
%config(noreplace) /etc/blackbox_exporter/blackbox.yml
%config(noreplace) /etc/default/blackbox_exporter
%attr(755, blackbox_exporter, blackbox_exporter) /var/lib/blackbox_exporter
