Name:		mapserver
Version:	6.4.0
Release:	1%{?dist}
Summary:	Environment for building spatially-enabled internet applications

Group:		Development/Tools
License:	BSD
URL:		http://mapserver.gis.umn.edu
Source0:	http://download.osgeo.org/mapserver/mapserver-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:	httpd
Requires:	instantclient
Requires:	mod_fcgid

BuildRequires:  libXpm-devel readline-devel
BuildRequires:  httpd-devel php-devel libxslt-devel pam-devel fcgi-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  postgresql-devel mysql-devel java-devel
BuildRequires:  swig > 1.3.24 java
BuildRequires:  geos-devel proj-devel gdal-devel cairo-devel
BuildRequires:  php-devel freetype-devel gd-devel >= 2.0.16
BuildRequires:  python-devel curl-devel zlib-devel libxml2-devel
BuildRequires:  libjpeg-devel libpng-devel fribidi-devel giflib-devel

%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages,
Mapserver can provide an interactive internet map based on
custom GIS data.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc



%changelog

