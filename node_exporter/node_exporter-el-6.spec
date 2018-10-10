%{buildroot}%define debug_package %{nil}

Name:		        node-exporter-init
Version:	      0.16.0
Release:	      1%{?dist}
Summary:	      Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.
Group:		      System Environment/Daemons
License:	      ASL 2.0
URL:		        https://github.com/prometheus/node_exporter
Source0:        node_exporter-%{pkg_version}.linux-amd64.tar.gz
Source1:        node_exporter.init
Source2:        node_exporter.sysconfig
BuildRoot:      %{buildroot}
BuildArch:      x86_64
Requires(pre):  /usr/sbin/useradd
Requires:       daemonize
AutoReqProv:	  No

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n node_exporter-%{version}.linux-amd64

%build
echo

%install
mkdir -vp %{buildroot}/var/log/prometheus/
mkdir -vp %{buildroot}/var/run/prometheus
mkdir -vp %{buildroot}/var/lib/prometheus
mkdir -vp %{buildroot}/usr/bin
mkdir -vp %{buildroot}/etc/init.d
mkdir -vp %{buildroot}/etc/sysconfig
install -m 755 node_exporter-%{version}.linux-amd64/node_exporter %{buildroot}/usr/bin/node_exporter
install -m 755 %{SOURCE1} %{buildroot}/etc/init.d/node_exporter
install -m 644 %{SOURCE2} %{buildroot}/etc/sysconfig/node_exporter

%clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d %{buildroot}/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%files
%defattr(-,root,root,-)
/usr/bin/node_exporter
/etc/init.d/node_exporter
%config(noreplace) /etc/sysconfig/node_exporter
/var/run/prometheus
/var/log/prometheus
