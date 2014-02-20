%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name:		instantclient	
Version:	12.1
Release:	1%{?dist}
Summary:	Oracle instantclient

Group:		libs
License:	GNU
URL:		http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
%{summary}

%prep
%setup -q


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}/oracle/12.1/client64
cp -a * %{buildroot}%{_libdir}/oracle/12.1/client64
cd %{buildroot}%{_libdir}/oracle/12.1/client64
ln -sf  libclntsh.so.12.1 libclntsh.so
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc
/%{_libdir}/oracle/12.1/client64/*


%changelog
* Tue Sep 24 2013 Jesper Kihlberg <jekih@gst.dk> 12.1-1
- First build
