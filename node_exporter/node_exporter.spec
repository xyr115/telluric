Name:           node_exporter
Version:        0.16.0
Release:        5%{?dist}
Summary:        Prometheus exporter for machine metrics.
License:        ASL 2.0
URL:            https://prometheus.io

Source0:        %{name}-%{version}.linux-amd64.tar.gz
Source1:        %{name}.service
Source2:        logrotate.conf
Source3:        rsyslog.conf

BuildRoot:      %{buildroot}
BuildArch:      x86_64
BuildRequires:  systemd-units
Requires:       systemd, logrotate, rsyslog > 7.2
Requires(pre):  shadow-utils

%description

Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

This package contains binary to export node metrics to prometheus.

%prep
%setup -q -n node_exporter-%{version}.linux-amd64

%install
# Directory for storing log files.
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

# Logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}.conf

# RSyslog config to enable writing to a file.
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rsyslog.d/%{name}.conf

# SystemD unit definition and environment settings to go alongside unit file.
mkdir -p %{buildroot}%{_unitdir}/%{name}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

# Binaries
mkdir -p %{buildroot}%{_bindir}
install -m 755 node_exporter %{buildroot}%{_bindir}/%{name}

# Copy over License and notice
mkdir -p %{buildroot}/usr/share/%{name}
install -m 644 LICENSE %{buildroot}/usr/share/node_exporter/LICENSE
install -m 644 NOTICE %{buildroot}/usr/share/node_exporter/NOTICE

%pre
getent group node_exporter > /dev/null || groupadd -r node_exporter
getent passwd node_exporter >/dev/null || \
  useradd -r -g node_exporter -s /sbin/nologin \
          -c "Node Exporter Service Account" node_exporter

%post
%systemd_post %{name}.service

echo
echo "NOTES ##############################################################################"
echo "Please restart RSyslog so that logs are written to %{_localstatedir}/log/node_exporter"
echo "    systemctl restart rsyslog.service"
echo "To have %{name} start automatically on boot:"
echo "    systemctl enable %{name}.service"
echo "Start %{name}:"
echo "    systemctl daemon-reload"
echo "    systemctl start %{name}.service"
echo "####################################################################################"
echo

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,node_exporter,node_exporter,-)
%{_bindir}/node_exporter
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/rsyslog.d/%{name}.conf
%config(noreplace) %{_unitdir}/%{name}.service

# Log directory
%dir %attr(755, node_exporter, node_exporter) %{_localstatedir}/log/%{name}

/usr/share/node_exporter
/usr/share/node_exporter/NOTICE
/usr/share/node_exporter/LICENSE
