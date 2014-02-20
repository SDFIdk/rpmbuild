Name:           mapcache
Version:        1.2.0
Release:        1%{?dist}
Summary:        Caching server for WMS layers
Group:          Development/Tools
License:        MIT
URL:            http://mapserver.org/trunk/en/mapcache/
Source:         mapcache-rel-1-2-0.tar.gz
#Obtain source using git archive available at https://github.com/mapserver/mapcache:
#git archive --format=tar --prefix=mapcache-1.1dev/ master | gzip > mapcache-1.1dev.tar.gz
#or adjust archive available at: https://github.com/mapserver/mapcache/archive/master.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       webserver, berkeleydb, apr-util

BuildRequires:  httpd-devel fcgi-devel libcurl-devel
BuildRequires:  geos-devel proj-devel gdal-devel libjpeg-turbo-devel
BuildRequires:  libpng-devel libtiff-devel pixman-devel sqlite-devel


%description
MapCache is a server that implements tile caching to speed up access to WMS layers. 
The primary objectives are to be fast and easily deployable, while offering the 
essential features (and more!) expected from a tile caching solution.

%prep
%setup -q -n %{name}-rel-1-2-0

%build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_PREFIX_PATH="/usr/local/berkeleydb" -DWITH_BERKELEY_DB=1 -DWITH_MEMCACHE=1 -DWITH_GEOTIFF=1 .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} \
    install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc INSTALL README* LICENSE 
%{_bindir}/*
%{_libdir}/*
/usr/lib/libmapcache.so

%changelog
