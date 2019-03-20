%define MS_REL %{nil}
Name:           mapserver%{MS_REL}
Version:        7.2.2
Release:        2%{?dist}
Summary:        Environment for building spatially-enabled internet applications
Group:          Development/Tools
License:        BSD
URL:            http://www.mapserver.org
Source0:        http://download.osgeo.org/mapserver/mapserver-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       curl
Requires:       dejavu-sans-fonts
Requires:       fcgi
Requires:       gdal
Requires:       giflib
Requires:       geos
Requires:       httpd
Requires:       freetype >= 2.8
Requires:       instantclient
#Requires:       cairo >= 1.15
Requires:       libxml2
Requires:       mod_fcgid
Requires:       postgresql11-libs       
##x86_64             11.1-1PGDG.rhel7             pgdg11
Requires:       proj >= 5.0
Requires:       protobuf-c

#BuildRequires:  cairo-devel >= 1.15
BuildRequires:  cmake3
BuildRequires:  curl-devel
BuildRequires:  fcgi-devel
BuildRequires:  freetype-devel
#BuildRequires:  gd-devel >= 2.0.16     #should be unnecessary since longtime
BuildRequires:  gdal-devel
#BuildRequires:  giflib-devel
BuildRequires:  geos-devel
BuildRequires:  giflib-devel
#BuildRequires:  httpd-devel
BuildRequires:  instantclient
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
#BuildRequires:  mysql-devel
#BuildRequires:  pam-devel              #what does this even do?
BuildRequires:  postgresql11-devel
##x86_64             11.1-1PGDG.rhel7             pgdg11
BuildRequires:  proj-devel >= 5.0
BuildRequires:  protobuf-c-devel
#BuildRequires:  swig > 1.3.24          #for mapscript?
BuildRequires:  zlib-devel
#BuildRequires:  libXpm-devel readline-devel librsvg2-devel
#BuildRequires:  perl(ExtUtils::MakeMaker) python-devel
#BuildRequires: java-1.7.0-openjdk-devel php-devel
#BuildRequires:  fribidi-devel harfbuzz-devel cairo-devel

%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages, 
Mapserver can provide an interactive internet map based on 
custom GIS data.


%prep
%setup -q -n mapserver-%{version}

# fix spurious perm bits
#chmod -x mapscript/python/examples/*.py
#chmod -x mapscript/python/tests/rundoctests.dist
#chmod -x mapscript/perl/examples/*.pl

## replace fonts for tests with symlinks
rm -rf tests/vera/Vera.ttf
rm -rf tests/vera/VeraBd.ttf
pushd tests/vera/
ln -sf /usr/share/fonts/dejavu/DejaVuSans.ttf Vera.ttf
ln -sf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf VeraBd.ttf
popd


%build
mkdir build
pushd build

#-DCMAKE_PREFIX_PATH="/usr/lib64/oracle/12.1/client64;/usr/lib64/oracle/12.1/client64/sdk/include" \

#-DINSTALL_LIB_DIR:PATH=/usr/lib64 \	#necessary for cmake to install into lib64 as RHEL expects
                                        #'autodetect' seems not to work in this particular case, although included from https://github.com/mapserver/mapserver/pull/4791
										#possibly caused by non-Intel 64-bit architecture

export ORACLE_HOME="/usr/lib64/oracle/12.1/client64"

%cmake3 -DINSTALL_LIB_DIR:PATH=/usr/lib64 \
        -DCMAKE_PREFIX_PATH="/usr/lib64;/usr/pgsql-11;/usr/lib64/oracle/12.1/client64/sdk/include" \
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
        -DWITH_THREAD_SAFETY=OFF \
        -DWITH_PYTHON=OFF \
        -DWITH_PERL=OFF \
        -DWITH_JAVA=OFF \
        -DWITH_PHP=OFF \
        -DWITH_APACHE_MODULE=OFF \
        -DWITH_FRIBIDI=OFF \
        -DWITH_HARFBUZZ=OFF \
        -DWITH_PROTOBUFC=ON ..
	   
make -j 2 %{?_smp_mflags}
#?make -j 4
popd

%install
pushd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
popd

#mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_includedir}/%{name}/
install -p -m 644 xmlmapfile/mapfile.xsd %{buildroot}%{_datadir}/%{name}
install -p -m 644 xmlmapfile/mapfile.xsl %{buildroot}%{_datadir}/%{name}
install -p -m 644 *.h %{buildroot}%{_includedir}/%{name}/
cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}


#mkdir -p %{buildroot}%{_libexecdir}			    #for old placement of mapserv
mkdir -p %{buildroot}/%{_var}/www/cgi-bin		#for direct apache-placement of mapserv
#?mkdir -p %{buildroot}%{_sysconfdir}/php.d
#?mkdir -p %{buildroot}%{_libdir}/php/modules
#?mkdir -p %{buildroot}%{_datadir}/%{name}

cp %{buildroot}%{_bindir}/mapserv %{buildroot}%{_var}/www/cgi-bin/mapserv-%{version}		#for direct apache-placement of mapserv
cp %{buildroot}%{_bindir}/mapserv %{buildroot}%{_var}/www/cgi-bin/mapserv-%{version}.fcgi	#for direct apache-placement of mapserv fcgi
#mv %{buildroot}%{_bindir}/mapserv %{buildroot}%{_libexecdir}/mapserv-%{version} 			#for old placement of mapserv

# cleanup junks
for junk in {*.pod,*.bs,.packlist} ; do
    find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done


%files
%defattr(-,root,root)
#%doc README COMMITERS HISTORY.TXT  #COMMITERS makes build fail and is omitted
#%doc README
%{_bindir}/legend
%{_bindir}/mapserv
%{_var}/www/cgi-bin/mapserv-%{version}
%{_var}/www/cgi-bin/mapserv-%{version}.fcgi
#%{_libexecdir}/mapserv-%{version}
%{_bindir}/msencrypt
%{_bindir}/scalebar
%{_bindir}/shp2img
%{_bindir}/shptree
%{_bindir}/shptreetst
%{_bindir}/shptreevis
%{_bindir}/sortshp
%{_bindir}/tile4ms
%{_libdir}/libmapserver.so
%{_libdir}/libmapserver.so.2
%{_libdir}/libmapserver.so.%{version}
%{_datadir}/%{name}
#%exclude %{buildroot}
%exclude /usr/include/mapserver/*


%changelog
* Wed Feb 20 2019 Jonas Lund Nielsen <jolni@sdfe.dk> 1.0.2
- added Requires: mod_fcgid

* Thu Feb 02 2019 Jonas Lund Nielsen <jolni@sdfe.dk> 1.0.1
- Upgraded to MapServer 7.2.2

* Mon Jan 28 2019 Jonas Lund Nielsen <jolni@sdfe.dk> 1.0.0
- MapServer 7.2.1 to built on RHEL7
- Name of binary again includes minor version (uses macro %{version})
- including self-built instantclient

* Wed Jun 28 2017 Jonas Lund Nielsen <jolni@sdfe.dk> 0.6.0
- Reverted to MapServer 7.0.4

* Wed Jan 25 2017 Jonas Lund Nielsen <jolni@sdfe.dk> 0.4.0
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
