%define MS_REL %{nil}
Name:           mapserver%{MS_REL}
Version:        7.2.1
Release:        1%{?dist}
Summary:        Environment for building spatially-enabled internet applications

Group:          Development/Tools
License:        BSD
URL:            http://www.mapserver.org
Source0:        http://download.osgeo.org/mapserver/mapserver-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       dejavu-sans-fonts
Requires:       fcgi
Requires:       gdal
Requires:       geos
Requires:       httpd
Requires:       freetype >= 2.8
Requires:       instantclient 
Requires:       cairo >= 1.15


BuildRequires:  cairo-devel >= 1.15
BuildRequires:  cmake
BuildRequires:  curl-devel
BuildRequires:  fcgi-devel
BuildRequires:  freetype-devel
BuildRequires:  gd-devel >= 2.0.16
BuildRequires:  gdal-devel
BuildRequires:  httpd-devel
BuildRequires:  geos-devel
BuildRequires:  giflib-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  mysql-devel
BuildRequires:  pam-devel
BuildRequires:  postgresql-devel
BuildRequires:  proj-devel
BuildRequires:  swig > 1.3.24
BuildRequires:  zlib-devel
#BuildRequires:  libXpm-devel readline-devel librsvg2-devel
#BuildRequires:  perl(ExtUtils::MakeMaker) python-devel
#BuildRequires: java-1.7.0-openjdk-devel php-devel
#BuildRequires:  fribidi-devel harfbuzz-devel cairo-devel

# %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages, 
Mapserver can provide an interactive internet map based on 
custom GIS data.

######
#PHP
######
#%package -n php-%{name}
#Summary:        PHP/Mapscript map making extensions to PHP
#Group:          Development/Languages
#BuildRequires:  php-devel
#Requires:       php-gd%{?_isa}
#Requires:       php(zend-abi) = %{php_zend_api}
#Requires:       php(api) = %{php_core_api}
#
#%description -n php-%{name}
#The PHP/Mapscript extension provides full map customization capabilities within
#the PHP scripting language.

######
#PERL
######
#%package perl
#Summary:        Perl/Mapscript map making extensions to Perl
#Group:          Development/Languages
#Requires:       %{name} = %{version}-%{release}
#Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
#
#%description perl
#The Perl/Mapscript extension provides full map customization capabilities
#within the Perl programming language.

#%package python
#Summary:        Python/Mapscript map making extensions to Python
#Group:          Development/Languages
#Requires:       %{name} = %{version}-%{release}
#
#%description python
#The Python/Mapscript extension provides full map customization capabilities
#within the Python programming language.

######
#JAVA
######
#%package java
#Summary:        Java/Mapscript map making extensions to Java
#Group:          Development/Languages
#Requires:       %{name} = %{version}-%{release}
#
#%description java
#The Java/Mapscript extension provides full map customization capabilities
#within the Java programming language.

%prep
%setup -q -n mapserver-%{version}

# fix spurious perm bits
#chmod -x mapscript/python/examples/*.py
#chmod -x mapscript/python/tests/rundoctests.dist
#chmod -x mapscript/perl/examples/*.pl

## replace fonts for tests with symlinks
#rm -rf tests/vera/Vera.ttf
#rm -rf tests/vera/VeraBd.ttf
#pushd tests/vera/
#ln -sf /usr/share/fonts/dejavu/DejaVuSans.ttf Vera.ttf
#ln -sf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf VeraBd.ttf
#popd

%build
mkdir build
pushd build
export ORACLE_HOME="/usr/lib64/oracle/12.1/client64"

##Please note: Comments not to be mixed with active -D cmake-directives. It is a one-liner :-)
#-DINSTALL_LIB_DIR:PATH=/usr/lib64 \	#necessary for cmake to install into lib64 as RHEL expects
                                        #'autodetect' seems not to work in this particular case, although included from https://github.com/mapserver/mapserver/pull/4791
										#possibly caused by non-Intel 64-bit architecture
%cmake -DINSTALL_LIB_DIR:PATH=/usr/lib64 \
       -DCMAKE_PREFIX_PATH="/usr/lib64/oracle/12.1/client64;/usr/lib64/oracle/12.1/client64/sdk/include" \
       -DWITH_WMS=ON \
	   -DWITH_WFS=ON \
	   -DWITH_WCS=ON \
	   -DWITH_SOS=ON \
	   -DWITH_KML=ON \
	   -DWITH_CLIENT_WFS=ON \
       -DWITH_CLIENT_WMS=ON \
	   -DWITH_CURL=ON \
	   -DWITH_PROJ=ON \
	   -DWITH_GEOS=ON \
	   -DWITH_ICONV=ON \
	   -DWITH_LIBXML2=ON \
	   -DWITH_OGR=ON \
	   -DWITH_GDAL=ON \
	   -DWITH_GIF=ON \
	   -DWITH_CAIRO=OFF \
       -DWITH_RSVG=OFF\
       -DWITH_POSTGIS=ON \
       -DWITH_ORACLESPATIAL=ON \
       -DWITH_FCGI=ON \
       -DWITH_THREAD_SAFETY=ON \
	   -DWITH_PYTHON=OFF \
       -DWITH_PERL=OFF \
       -DWITH_JAVA=OFF \
       -DWITH_PHP=OFF \
	   -DWITH_APACHE_MODULE=OFF \
	   -DWITH_FRIBIDI=OFF \
	   -DWITH_HARFBUZZ=OFF ..
	   
make
popd

%install
pushd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
popd

#mkdir -p %{buildroot}%{_libexecdir}			#for old placement of mapserv
mkdir -p %{buildroot}/%{_var}/www/cgi-bin		#for direct apache-placement of mapserv
mkdir -p %{buildroot}%{_sysconfdir}/php.d
mkdir -p %{buildroot}%{_libdir}/php/modules
mkdir -p %{buildroot}%{_datadir}/%{name}

# destination adjusted to include version, hoping for smoother transition with multiple working instances in cgi-bin
#mv %{buildroot}%{_bindir}/mapserv %{buildroot}%{_libexecdir}/mapserv-%{version}			#for old placement of mapserv
#cp %{buildroot}%{_bindir}/mapserv %{buildroot}/%{_var}/www/cgi-bin/mapserv-%{version}		#for direct apache-placement of mapserv
#cp %{buildroot}%{_bindir}/mapserv %{buildroot}/%{_var}/www/cgi-bin/mapserv-%{version}.fcgi	#for direct apache-placement of mapserv fcgi
cp %{buildroot}%{_bindir}/mapserv %{buildroot}/%{_var}/www/cgi-bin/mapserv-7				#for direct apache-placement of mapserv
cp %{buildroot}%{_bindir}/mapserv %{buildroot}/%{_var}/www/cgi-bin/mapserv-7.fcgi			#for direct apache-placement of mapserv fcgi

install -p -m 644 xmlmapfile/mapfile.xsd %{buildroot}%{_datadir}/%{name}
install -p -m 644 xmlmapfile/mapfile.xsl %{buildroot}%{_datadir}/%{name}

######
#PHP
######
## install php config file
#mkdir -p %{buildroot}%{_sysconfdir}/php.d/
#cat > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini <<EOF
#; Enable %{name} extension module
#extension=php_mapscript%{MS_REL}.so
#EOF

# cleanup junks
for junk in {*.pod,*.bs,.packlist} ; do
find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done

######
#PERL
######
## move perl stuff into perl_vendorarch
## things get installed in /usr/local erroneously, so move the to the right place
#mkdir -p %{buildroot}%{perl_vendorarch}
#mv  %{buildroot}/usr/local/lib64/perl5/* %{buildroot}%{perl_vendorarch} 

%files
%defattr(-,root,root)
#%doc README COMMITERS HISTORY.TXT  #COMMITERS makes build fail and is omitted
%doc README HISTORY.TXT  
%doc INSTALL MIGRATION_GUIDE.txt
%doc symbols tests
%doc fonts
%{_bindir}/legend%{MS_REL}
%{_bindir}/msencrypt%{MS_REL}
%{_bindir}/scalebar%{MS_REL}
%{_bindir}/shp2img%{MS_REL}
%{_bindir}/shptree%{MS_REL}
%{_bindir}/shptreetst%{MS_REL}
%{_bindir}/shptreevis%{MS_REL}
%{_bindir}/sortshp%{MS_REL}
%{_bindir}/tile4ms%{MS_REL}
%{_bindir}/mapserv
%{_libdir}/libmapserver.so
%{_libdir}/libmapserver.so.2
%{_libdir}/libmapserver.so.%{version}
#%{_var}/www/cgi-bin/mapserv-%{version}
%{_var}/www/cgi-bin/mapserv-7
%{_var}/www/cgi-bin/mapserv-7.fcgi
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
#%exclude %{buildroot}
%exclude /usr/include/mapserver/*

#%{_libexecdir}/mapserv-%{version}		#for old placement of mapserv
#%{_var}/www/cgi-bin/mapserv-%{version}	#for direct apache-placement of mapserv

######
#PHP
######
#%files -n php-%{name}
#%defattr(-,root,root)
#%doc mapscript/php/README
#%doc mapscript/php/examples
#%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
#%{_libdir}/php/modules/php_mapscript%{MS_REL}.so

######
#PERL
######
#%files perl
#%defattr(-,root,root)
#%doc mapscript/perl/examples
#%dir %{perl_vendorarch}/auto/mapscript%{MS_REL}
#%{perl_vendorarch}/auto/mapscript%{MS_REL}/*
#%{perl_vendorarch}/mapscript%{MS_REL}.pm

######
#PYTHON
######
#%files python
#%defattr(-,root,root)
#%doc mapscript/python/README
#%doc mapscript/python/examples
#%doc mapscript/python/tests
#%{python_sitearch}/*

######
#JAVA
######
#%files java
#%defattr(-,root,root)
#%doc mapscript/java/README
#%doc mapscript/java/examples
#%doc mapscript/java/tests
#%{_libdir}/libjavamapscript.so

%changelog
* Thu Dec 20 2018 Jonas Lund Nielsen <jolni@sdfe.dk> 
- MapServer 7.2.1 to be built on RHEL7 (preliminary version)

* Wed Jun 25 2017 Jonas Lund Nielsen <jolni@sdfe.dk> 0.6.0
- Reverted to MapServer 7.0.4

* Tue Jan 25 2017 Jonas Lund Nielsen <jolni@sdfe.dk> 0.4.0
- Updated to MapServer 7.0.4
- Name of binary only includes major version (no longer uses macro %{version})
- Mapserv left in-place at %{buildroot}%{_bindir}/mapserv (cp instead of mv)
- Create copy of binary as mapserv-7.fcgi

* Tue Dec 06 2016 Jonas Lund Nielsen <jolni@sdfe.dk> 0.3.0
- Updated to MapServer 7.0.3
- Deactivated some remaining python

* Thu Oct 20 2016 Jonas Lund Nielsen <jolni@sdfe.dk> 0.2.0
- Initial version
- Originally from: https://github.com/mapserver/packaging/blob/master/el/mapserver-7.0.spec
