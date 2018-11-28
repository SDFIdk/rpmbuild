%define PACKAGE_NAME proj
%define PACKAGE_VERSION 4.9.3
%define PACKAGE_URL http://trac.osgeo.org/proj
%define _prefix /usr


Summary: Cartographic projection software
Name: %PACKAGE_NAME
Version: %PACKAGE_VERSION
Release: 1
Source0: proj-4.9.3.tar.gz
License: MIT License, Copyright (c) 2000, Frank Warmerdam
Group: Applications/GIS
Vendor: Intevation GmbH <http://intevation.net>
Distribution: FreeGIS CD

BuildRoot: %{_builddir}/%{name}-root
Prefix: %{_prefix}

Conflicts: PROJ.4

%description
This package offers commandline tools and a library for performing respective
forward and inverse transformation of cartographic data to or from cartesian
data with a wide range of selectable projection functions.

%package devel
Summary:	Development files for PROJ.4
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.


%prep
%setup -D -n proj-4.9.3
%configure

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%post
cd /usr/lib64/    #Changes diretory to lib64 
ln -sf libproj.so.12.0.0 libproj.so.0 #Creates symbolic link libproj.so.0 from libproj.so.12.0.0 

%clean
rm -rf %{_builddir}/proj-4.9.3
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
%{_includedir}/*
%{_datadir}/proj/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*.3*
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%exclude %{_libdir}/libproj.la

%doc AUTHORS COPYING ChangeLog NEWS README
