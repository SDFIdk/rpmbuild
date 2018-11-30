%define %{name} proj
%define %{version} 5.2.0
%define PACKAGE_URL https://proj4.org/index.html
%define _prefix /usr


Summary: Cartographic projection software
Name: %{name}
Version: %{version}
Release: 1
Source0: %{name}-%{version}.tar.gz
License: MIT License, Copyright (c) 2000, Frank Warmerdam
Group: Applications/GIS
Provides: %{name} = %{version}

BuildRoot: %{_builddir}/%{name}-root
Prefix: %{_prefix}

Obsoletes: %{name} < %{version}
Conflicts: %{name} < %{version}

%description
This package offers commandline tools and a library for performing respective
forward and inverse transformation of cartographic data to or from cartesian
data with a wide range of selectable projection functions.

%package devel
Summary:	Development files for PROJ
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains libproj and the appropriate header files and man pages.


%prep
%setup -D -n proj-5.2.0
%configure

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%post
cd /usr/lib64/    					  #Changes diretory to lib64 
ln -sf libproj.so.12.0.0 libproj.so.0 #Creates symbolic link libproj.so.0 from libproj.so.12.0.0
 

%clean
rm -rf %{_builddir}/proj-5.2.0
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

%changelog
* Wed Nov 28 2018 Jonas Lund Nielsen <jolni@sdfe.dk> 2.0.0
- Proj 5.2.0 to be built on RHEL7