Name:           mapserver
Version:        6.4.0
Release:        1%{?dist}
Summary:        Environment for building spatially-enabled internet applications
Group:          Development/Tools
License:        BSD
URL:            http://mapserver.gis.umn.edu
Source:         http://download.osgeo.org/mapserver/mapserver-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:       httpd
Requires:       instantclient
Requires:       mod_fcgid
# Requires:       bitstream-vera-sans-fonts

BuildRequires:  libXpm-devel readline-devel
BuildRequires:  httpd-devel php-devel libxslt-devel pam-devel fcgi-devel
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  postgresql-devel mysql-devel java-devel
BuildRequires:  swig > 1.3.24 java 
BuildRequires:  geos-devel proj-devel gdal-devel cairo-devel
BuildRequires:  php-devel freetype-devel gd-devel >= 2.0.16
BuildRequires:  python-devel curl-devel zlib-devel libxml2-devel
BuildRequires:  libjpeg-devel libpng-devel fribidi-devel giflib-devel


%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

# description is not very up to date, anymore
%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages, 
Mapserver can provide an interactive internet map based on 
custom GIS data.

%package -n php-mapserver
Summary:        PHP/Mapscript map making extensions to PHP
Group:          Development/Languages
Requires:       httpd php-gd

%description -n php-mapserver
The PHP/Mapscript extension provides full map customization capabilities within
the PHP scripting language.


%package perl
Summary:        Perl/Mapscript map making extensions to Perl
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description perl
The Perl/Mapscript extension provides full map customization capabilities
within the Perl programming language.

%package python
Summary:        Python/Mapscript map making extensions to Python
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description python
The Python/Mapscript extension provides full map customization capabilities
within the Python programming language.

%package java
Summary:        Java/Mapscript map making extensions to Java
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Requires:       java-gcj-compat 

%description java
The Java/Mapscript extension provides full map customization capabilities
within the Java programming language.

%prep
%setup -q -n mapserver-%{version}
# %setup -q
# fix spurious perm bits
chmod -x mapscript/python/tests/rundoctests.dist
chmod -x mapscript/perl/examples/*.pl


# remove fonts
# alias as symlinks
rm -rf tests/vera/Vera.ttf
rm -rf tests/vera/VeraBd.ttf
pushd tests/vera/
ln -sf /usr/share/fonts/bitstream-vera/Vera.ttf Vera.ttf
ln -sf /usr/share/fonts/bitstream-vera/VeraBd.ttf VeraBd.ttf
popd

%build

CFLAGS="${CFLAGS} -ldl" ; export CFLAGS

mkdir build
cd build
cmake .. 
make
# temporary hack!
#make mapscriptvars
# build perl
#cd mapscript/perl
#perl Makefile.PL
#make

# build python
# is this obsolete?
# cd ../python
# python setup.py build

# build java
#cd ../java
# not needed with 6.2
# make interface
#make

%install
#rm -rf %{buildroot}
# make install
#make    DESTDIR=%{buildroot} \
#        install
pwd
cd build
mkdir -p %{buildroot}/%{_libexecdir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_var}/www/cgi-bin

#mv %{buildroot}/%{_bindir}/mapserv %{buildroot}/%{_libexecdir}/
#install -p -m 755 mapserv %{buildroot}/%{_var}/www/cgi-bin

mv mapserv %{buildroot}/%{_var}/www/cgi-bin
mv libmapserver*.so %{buildroot}/%{_libdir}

#mkdir -p %{buildroot}/%{_sbindir}
#mkdir -p %{buildroot}/%{_sysconfdir}/php.d
#mkdir -p %{buildroot}%{_libdir}/php/modules
#mkdir -p %{buildroot}/%{_bindir}
#install -p -m 755 mapserv %{buildroot}/%{_sbindir}
#install -p -m 755 shp2img %{buildroot}/%{_bindir}
#install -p -m 755 shptree %{buildroot}/%{_bindir}
#install -p -m 755 sortshp %{buildroot}/%{_bindir}
#install -p -m 755 tile4ms %{buildroot}/%{_bindir}

#install -p -m 755 mapscript/php/.libs/php_mapscript.so.0.0.0 %{buildroot}/%{_libdir}/php/modules/
# install -p -m 755 mapscript/php/php_mapscript.so %{buildroot}/%{_libdir}/php/modules/

# install perl module
#pushd mapscript/perl
#make DESTDIR=%{buildroot} pure_vendor_install
#popd

# install python module
#pushd mapscript/python
#python setup.py install --root %{buildroot}
#popd

# install java
#mkdir -p %{buildroot}%{_javadir}
#install -p -m 644 mapscript/java/mapscript.jar %{buildroot}%{_javadir}/

# install php config file
#mkdir -p %{buildroot}%{_sysconfdir}/php.d/
#cat > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini <<EOF
#; Enable %{name} extension module
#extension=php_mapscript.so
#EOF

# cleanup junks
#for junk in {'*.la',*.pod,*.bs,.packlist} ; do
#find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
#done

# fix some exec bits
#chmod 755 %{buildroot}/%{perl_vendorarch}/auto/mapscript/mapscript.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README COMMITERS GD-COPYING HISTORY.TXT  
%doc INSTALL MIGRATION_GUIDE.txt
%doc symbols tests
%doc fonts
#%{_bindir}/*
#%{_bindir}/shptree
#%{_bindir}/sortshp
#%{_bindir}/tile4ms
%{_libdir}/libmapserver*.so
%{_var}/www/cgi-bin/mapserv

#%files -n php-mapserver
#%defattr(-,root,root)
#%doc mapscript/php/README
#%doc mapscript/php/examples
#%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
#%{_libdir}/php/modules/php_mapscript.so*
#%{_libdir}/php/modules/php_mapscript-%{version}.so

#%files perl
#%defattr(-,root,root)
#%doc mapscript/perl/examples
#%dir %{perl_vendorarch}/auto/mapscript
#%{perl_vendorarch}/auto/mapscript/*
#%{perl_vendorarch}/mapscript.pm

#%files python
#%defattr(-,root,root)
#%doc mapscript/python/README
#%doc mapscript/python/examples
#%doc mapscript/python/tests
#%{python_sitearch}/*

#%files java
#%defattr(-,root,root)
#%doc mapscript/java/README
#%doc mapscript/java/examples
#%doc mapscript/java/tests
#%{_javadir}/*.jar

%changelog
