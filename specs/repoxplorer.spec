Name:           repoxplorer
Version:        1.1.1
Release:        1%{?dist}
Summary:        RepoXplorer is a stats and charts utility for Git repositories

License:        ASL 2.0
URL:            https://github.com/morucci/repoxplorer
Source0:        https://github.com/morucci/%{name}/archive/%{version}.tar.gz

Source1:        %{name}.service
Source2:        %{name}-webui.service
Source3:        index.yaml
Source4:        config.py

BuildArch:      noarch

Requires:       PyYAML
Requires:       python-pecan
Requires:       python-crypto
Requires:       python-urllib3
Requires:       python-elasticsearch
Requires:       python-requests
Requires:       python-jsonschema
Requires:       python-gunicorn
Requires:       pytz
Requires:       git

BuildRequires:  systemd
Buildrequires:  python2-devel

%description
RepoXplorer is a stats and charts utility for Git repositories.
Its main purpose is to ease visualization of statistics for projects
composed of one or multiple Git repositories. Indeed lot of projects
are splitted and have a Git repository by component (server, client, library A, ...)
but unfortunately most of the existing Git statistic tools does not
handle that.

RepoXplorer let's you describe how a project is composed and then computes stats
across them. RepoXplorer provides a Web UI to browse statistics easily.
RepoXplorer relies on ElasticSearch for its data backend.

%prep
%autosetup -n %{name}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/repoxplorer
mkdir -p %{buildroot}/%{_sysconfdir}/repoxplorer
mkdir -p %{buildroot}/%{_var}/lib/repoxplorer
mkdir -p %{buildroot}/%{_var}/log/repoxplorer
mv %{buildroot}/usr/local/share/repoxplorer %{buildroot}/%{_datadir}/
rm %{buildroot}/%{_datadir}/repoxplorer/*.yaml
rm %{buildroot}/%{_datadir}/repoxplorer/config.*
rm %{buildroot}/%{_datadir}/repoxplorer/repoxplorer.service
rm %{buildroot}/%{_datadir}/repoxplorer/repoxplorer-webui.service
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}/%{name}.service
install -p -D -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/%{name}-webui.service
install -p -D -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/%{name}/index.yaml
install -p -D -m 644 %{SOURCE4} %{buildroot}/%{_sysconfdir}/%{name}/config.py

%check
#%{__python2} setup.py nosetests

%pre
getent group repoxplorer >/dev/null || groupadd -r repoxplorer
getent passwd repoxplorer >/dev/null || \
useradd -r -g repoxplorer -G repoxplorer -d /usr/share/repoxplorer -s /sbin/nologin \
-c "Repoxplorer daemons" repoxplorer
exit 0

%post
%systemd_post %{name}.service
%systemd_post %{name}-webui.service

%preun
%systemd_preun %{name}.service
%systemd_preun %{name}-webui.service

%postun
%systemd_postun %{name}.service
%systemd_postun %{name}-webui.service

%files
%{python2_sitelib}/*
%{_datadir}/*
%{_bindir}/*
%{_unitdir}/*
%config(noreplace) %{_sysconfdir}/*
%attr(-, repoxplorer, repoxplorer) %{_var}/lib/repoxplorer
%attr(-, repoxplorer, repoxplorer) %{_var}/log/repoxplorer

%changelog
* Mon Oct 09 2017 Fa
