%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:		instantclient	
Version:	12.1
Release:	3%{?dist}
Summary:	Oracle instantclient

Group:		libs
License:	GNU
URL:		http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Oracle Instantclient


%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/oracle/12.1/client64
cp -a * %{buildroot}%{_libdir}/oracle/12.1/client64
cd %{buildroot}%{_libdir}/oracle/12.1/client64
###since gdal seems to insist on the "lib" postfix when searching for libs
ln -sf %{buildroot}%{_libdir}/oracle/12.1/client64 lib
ln -sf libclntsh.so.12.1 libclntsh.so
ln -sf libocci.so.12.1 libocci.so
ln -sf libclntshcore.so.12.1 libclntshcore.so
echo '%{buildroot}%{_libdir}/oracle/12.1/client64/' > instantclient.conf
cp instantclient.conf /etc/ld.so.conf.d/instantclient.conf
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
/%{_libdir}/oracle/12.1/client64/*
/etc/ld.so.conf.d/instantclient.conf


%changelog
* Tue Feb 5 2019 Jonas Lund Nielsen <jolni@sdfe.dk> 12.1-3
- Added /etc/ld.so.conf.d/instantclient.conf, containing '/usr/lib64/oracle/12.1/client64/',
-  may still require running ldconfig 
-   (could be added in %post: https://stackoverflow.com/questions/4823757/centos-5-5-symbolic-link-creation-into-rpm-spec-file)

* Fri Jan 25 2019 Jonas Lund Nielsen <jolni@sdfe.dk> 12.1-2
- First build for RHEL7
- Added symlink to libocci.so.12.1, libclntshcore.so.12.1

* Tue Sep 24 2013 Jesper Kihlberg <jekih@gst.dk> 12.1-1
- First build
