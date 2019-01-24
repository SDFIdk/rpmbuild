# From ECW spec-file: (can hopefully resolve rpaths issue)
# "Needs to be built with:  QA_RPATHS=$[ 0x0001|0x002 ] rpmbuild -bb rpmbuild/SPECS/libecwj2.spec
# otherwise it complains about some rpaths - which we cannot see any problem with.. "
#
Name:           gdal
Version:        2.4.0
Release:        1%{?dist}
Summary:        GDAL

Group:          Libraries
License:        BSD
URL:            http://www.gdal.org/
Source0:        http://download.osgeo.org/gdal/%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  geos-devel
#BuildRequires:  giflib-devel
BuildRequires:  libcurl-devel
#BuildRequires:  libecwj2-devel
#BuildRequires:  libgeotiff
#BuildRequires:  libgeotiff-devel
BuildRequires:  libjpeg-turbo-devel
#BuildRequires:  libpng-devel
#BuildRequires:  libtiff
#BuildRequires:  libtiff-devel
BuildRequires:  libzstd-devel
BuildRequires:  libspatialite-devel
BuildRequires:  openjpeg2-devel
#BuildRequires:  oracle-instantclient11.2-devel
BuildRequires:  postgresql11-devel     
##x86_64             11.1-1PGDG.rhel7             pgdg11 
##https://download.postgresql.org/pub/repos/yum/11/redhat/rhel-7-x86_64/pgdg-redhat11-11-2.noarch.rpm
BuildRequires:  proj-devel
#BuildRequires:  python-devel

Requires:       geos
Requires:       libcurl
#Requires:       libecwj2
Requires:       libjpeg-turbo
#Requires:       libpng 
Requires:       libspatialite
Requires:       libzstd
Requires:       openjpeg2
#Requires:       oracle-instantclient11.2-basic
Requires:       postgresql11-libs
##x86_64             11.1-1PGDG.rhel7             pgdg11
##https://download.postgresql.org/pub/repos/yum/11/redhat/rhel-7-x86_64/pgdg-redhat11-11-2.noarch.rpm
Requires:       proj

%description
GDAL Main files

%package devel
Summary:        GDAL library header files
Group:          Development/libraries
#BuildRequires:  gdal

%description devel
GDAL header files

%prep
%setup -q

#Fix Python installation path
sed -i 's|setup.py install|setup.py install --root=%{buildroot}|' swig/python/GNUmakefile

%build
#fra gdal-rogue spec-fil
#sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' GDALmake.opt.in

#--with-static-proj4 \
#--disable-rpath \
#--with-python 
#--with-ecw=/opt/libecw \

#https://trac.osgeo.org/gdal/wiki/BuildingOnUnix
#export ORACLE_HOME=/home/matt/instantclient_11_2 
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/matt/instantclient_11_2
#export PATH=$PATH:$ORACLE_HOME
#export NLS_LANG=American.America.WE8ISO8859P1 (this may not be essential) 
#--with-oci-include=/home/matt/instantclient_11_2/sdk/include
#--with-oci-lib=/home/matt/instantclient_11_2

%configure --disable-rpath \
        --with-curl \
        --with-ecw=no \
        --with-geos=yes \
        --with-geotiff=internal \
        --with-gif=internal \
        --with-jpeg=/usr/lib64 \
        --with-libtiff=internal \
        --with-oci=no \
        --with-openjpeg \
        --with-pg=/usr/pgsql-11/bin/pg_config \
        --with-png=internal \
        --with-spatialite=yes \
        --with-zstd=yes
        

# -j [number] defines # of simultaneous jobs make will start
make -j 4 %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

#####fra gdal-rogue_minimal
%ifarch x86_64 # 32-bit libs go in /usr/lib while 64-bit libs go in /usr/lib64
%define lib_dir /usr/lib64
%else
%define lib_dir /usr/lib
%endif
mkdir -p %{buildroot}/%{lib_dir}/gdalplugins

# Delete undesired libtool archives 
# copied from libspatialite.spec, since gdal-devel at installation complains about 
# libgdal.la already present from non-devel)
#find %{buildroot} -type f -name "*.la" -delete

%clean
rm -rf %{buildroot}
#rm -f /usr/local/lib/{libgeos*,libltidsdk*,libtbb*,liblti_lidar_dsdk*,liblaslib.so} && rm -f /usr/local/include/*.h && rm -rf /usr/local/include/{lidar,nitf}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_datadir}/gdal*
%{_libdir}/lib*
#%{_libdir}/gdal-%{version}.jar
%{_libdir}/pkgconfig/gdal.pc
%attr(755,root,root) /usr/etc/bash_completion.d/gdal-bash-completion.sh
%attr(755,root,root) /usr/include/gnm.h
%attr(755,root,root) /usr/include/gnm_api.h
%attr(755,root,root) /usr/include/gnmgraph.h
%attr(755,root,root) /usr/share/bag_template.xml
%attr(755,root,root) /usr/share/eedaconf.json
%attr(755,root,root) /usr/share/default.rsc
%attr(755,root,root) /usr/share/esri_epsg.wkt
%attr(755,root,root) /usr/share/gmlasconf.xml
%attr(755,root,root) /usr/share/gmlasconf.xsd
%attr(755,root,root) /usr/share/jpfgdgml_AdmArea.gfs
%attr(755,root,root) /usr/share/jpfgdgml_AdmBdry.gfs
%attr(755,root,root) /usr/share/jpfgdgml_AdmPt.gfs
%attr(755,root,root) /usr/share/jpfgdgml_BldA.gfs
%attr(755,root,root) /usr/share/jpfgdgml_BldL.gfs
%attr(755,root,root) /usr/share/jpfgdgml_Cntr.gfs
%attr(755,root,root) /usr/share/jpfgdgml_CommBdry.gfs
%attr(755,root,root) /usr/share/jpfgdgml_CommPt.gfs
%attr(755,root,root) /usr/share/jpfgdgml_Cstline.gfs
%attr(755,root,root) /usr/share/jpfgdgml_ElevPt.gfs
%attr(755,root,root) /usr/share/jpfgdgml_GCP.gfs
%attr(755,root,root) /usr/share/jpfgdgml_LeveeEdge.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RailCL.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RdASL.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RdArea.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RdCompt.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RdEdg.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RdMgtBdry.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RdSgmtA.gfs
%attr(755,root,root) /usr/share/jpfgdgml_RvrMgtBdry.gfs
%attr(755,root,root) /usr/share/jpfgdgml_SBAPt.gfs
%attr(755,root,root) /usr/share/jpfgdgml_SBArea.gfs
%attr(755,root,root) /usr/share/jpfgdgml_SBBdry.gfs
%attr(755,root,root) /usr/share/jpfgdgml_WA.gfs
%attr(755,root,root) /usr/share/jpfgdgml_WL.gfs
%attr(755,root,root) /usr/share/jpfgdgml_WStrA.gfs
%attr(755,root,root) /usr/share/jpfgdgml_WStrL.gfs
%attr(755,root,root) /usr/share/pds4_template.xml
%attr(755,root,root) /usr/share/plscenesconf.json
%attr(755,root,root) /usr/share/GDALLogoBW.svg
%attr(755,root,root) /usr/share/GDALLogoColor.svg
%attr(755,root,root) /usr/share/GDALLogoGS.svg
%attr(755,root,root) /usr/share/LICENSE.TXT
%attr(755,root,root) /usr/share/compdcs.csv
%attr(755,root,root) /usr/share/coordinate_axis.csv
%attr(755,root,root) /usr/share/cubewerx_extra.wkt
%attr(755,root,root) /usr/share/datum_shift.csv
%attr(755,root,root) /usr/share/ecw_cs.wkt
%attr(755,root,root) /usr/share/ellipsoid.csv
%attr(755,root,root) /usr/share/epsg.wkt
%attr(755,root,root) /usr/share/esri_StatePlane_extra.wkt
%attr(755,root,root) /usr/share/esri_Wisconsin_extra.wkt
%attr(755,root,root) /usr/share/esri_extra.wkt
%attr(755,root,root) /usr/share/gcs.csv
%attr(755,root,root) /usr/share/gcs.override.csv
%attr(755,root,root) /usr/share/geoccs.csv
%attr(755,root,root) /usr/share/gml_registry.xml
%attr(755,root,root) /usr/share/gt_datum.csv
%attr(755,root,root) /usr/share/gt_ellips.csv
%attr(755,root,root) /usr/share/header.dxf
%attr(755,root,root) /usr/share/inspire_cp_BasicPropertyUnit.gfs
%attr(755,root,root) /usr/share/inspire_cp_CadastralBoundary.gfs
%attr(755,root,root) /usr/share/inspire_cp_CadastralParcel.gfs
%attr(755,root,root) /usr/share/inspire_cp_CadastralZoning.gfs
%attr(755,root,root) /usr/share/netcdf_config.xsd
%attr(755,root,root) /usr/share/nitf_spec.xml
%attr(755,root,root) /usr/share/nitf_spec.xsd
%attr(755,root,root) /usr/share/ogrvrt.xsd
%attr(755,root,root) /usr/share/osmconf.ini
%attr(755,root,root) /usr/share/ozi_datum.csv
%attr(755,root,root) /usr/share/ozi_ellips.csv
%attr(755,root,root) /usr/share/pci_datum.txt
%attr(755,root,root) /usr/share/pci_ellips.txt
%attr(755,root,root) /usr/share/pcs.csv
%attr(755,root,root) /usr/share/pcs.override.csv
%attr(755,root,root) /usr/share/prime_meridian.csv
%attr(755,root,root) /usr/share/projop_wparm.csv
%attr(755,root,root) /usr/share/ruian_vf_ob_v1.gfs
%attr(755,root,root) /usr/share/ruian_vf_st_uvoh_v1.gfs
%attr(755,root,root) /usr/share/ruian_vf_st_v1.gfs
%attr(755,root,root) /usr/share/ruian_vf_v1.gfs
%attr(755,root,root) /usr/share/s57agencies.csv
%attr(755,root,root) /usr/share/s57attributes.csv
%attr(755,root,root) /usr/share/s57expectedinput.csv
%attr(755,root,root) /usr/share/s57objectclasses.csv
%attr(755,root,root) /usr/share/seed_2d.dgn
%attr(755,root,root) /usr/share/seed_3d.dgn
%attr(755,root,root) /usr/share/stateplane.csv
%attr(755,root,root) /usr/share/trailer.dxf
%attr(755,root,root) /usr/share/unit_of_measure.csv
%attr(755,root,root) /usr/share/vdv452.xml
%attr(755,root,root) /usr/share/vdv452.xsd
%attr(755,root,root) /usr/share/vertcs.csv
%attr(755,root,root) /usr/share/vertcs.override.csv


%files devel
%defattr(644,root,root,755)
#%doc _html/*
%attr(755,root,root) %{_bindir}/gdal-config
%{_libdir}/libgdal.so
# left out since gdal-devel at installation complains about 
# libgdal.la already present from non-devel)
#%{_libdir}/libgdal.la
%{_includedir}/cpl_*.h
%{_includedir}/cplkeywordparser.h
%{_includedir}/gdal*.h
#%{_includedir}/gvgcpfit.h
%{_includedir}/memdataset.h
%{_includedir}/ogr_*.h
%{_includedir}/ogrsf_frmts.h
%{_includedir}/rawdataset.h
#%{_includedir}/thinplatespline.h
%{_includedir}/vrtdataset.h
#%{_mandir}/man1/gdal-config.1*

%changelog
* Mon Jan 14 2019 Jonas Lund Nielsen <jolni@sdfe.dk> 2.2.0
- Upgrade to GDAL 2.4.0
- leave out libgdal.la from devel

* Fri Dec 14 2018 Jonas Lund Nielsen <jolni@sdfe.dk> 2.1.1
- Upgrade to GDAL 2.3.3

* Wed Feb 08 2017 Jonas Lund Nielsen <jolni@sdfe.dk> 2.1.0
- Upgrade to 2.1.3
- Has unsolved issues with rpath in version 2.1.3
  Relates to configuring --with-ecw=/opt/libecw \

* Tue Nov 08 2016 Jonas Lund Nielsen <jolni@sdfe.dk> 2.0.0
- Upgrade to 2.1.2
- Has unsolved issues with rpath in version 2.12

* Wed Aug 14 2013 Jesper Kihlberg <jekih@gst.dk> 1.0.0
- Initial version

