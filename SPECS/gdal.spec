Name:		gdal
Version:	1.10.0
Release:	11%{?dist}
Summary:	GDAL

Group:		Libraries
License:	BSD
URL:		http://www.gdal.org/
Source0:	http://download.osgeo.org/gdal/1.10.0/%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	libecwj2
BuildRequires:	giflib-devel
BuildRequires:	geos-devel
BuildRequires:  libjpeg-devel
BuildRequires:	libtiff-devel
BuildRequires:  libpng-devel
BuildRequires:  python-devel
BuildRequires:  FileGDB_API
BuildRequires:  libgeotiff-devel

#Requires:	
Requires:	libecwj2
#Requires:	oracle-instantclient11.2-basic
#Requires:	oracle-instantclient11.2-devel
%description
GDAL Main files

%package devel
Summary:	GDAL library header files
Group:		Development/libraries

BuildRequires: gdal

%description devel
GDAL header files

%prep
%setup -q

#Fix Python installation path
sed -i 's|setup.py install|setup.py install --root=%{buildroot}|' swig/python/GNUmakefile


%build
%configure \
        --with-ecw=/opt/libecw \
        --with-fgdb=/usr/local \
        --with-gif=internal \
        --with-geos \
        --with-geotiff \
        --with-jpeg \
        --with-libtiff=internal \
        --with-png \
        --with-python 
#        --with-static-proj4
#        --with-fgdb=/usr/local \
 
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(644,root,root,755)
%doc NEWS PROVENANCE.TXT
#%attr(755,root,root) %{_bindir}/epsg_tr.py
#%attr(755,root,root) %{_bindir}/esri2wkt.py
#%attr(755,root,root) %{_bindir}/gcps2vec.py
#%attr(755,root,root) %{_bindir}/gcps2wld.py
#%attr(755,root,root) %{_bindir}/gdal2tiles.py
#%attr(755,root,root) %{_bindir}/gdal2xyz.py
%attr(755,root,root) /usr/bin/gdalserver
%attr(755,root,root) %{_bindir}/gdalserver
%attr(755,root,root) %{_bindir}/gdal_contour
#%attr(755,root,root) %{_bindir}/gdal_calc.py
#%attr(755,root,root) %{_bindir}/gdal_fillnodata.py
%attr(755,root,root) %{_bindir}/gdal_grid
#%attr(755,root,root) %{_bindir}/gdal_merge.py
#%attr(755,root,root) %{_bindir}/gdal_polygonize.py
#%attr(755,root,root) %{_bindir}/gdal_proximity.py
%attr(755,root,root) %{_bindir}/gdal_rasterize
#%attr(755,root,root) %{_bindir}/gdal_retile.py
#%attr(755,root,root) %{_bindir}/gdal_sieve.py
%attr(755,root,root) %{_bindir}/gdal_translate
%attr(755,root,root) %{_bindir}/gdaladdo
%attr(755,root,root) %{_bindir}/gdalbuildvrt
#%attr(755,root,root) %{_bindir}/gdalchksum.py
%attr(755,root,root) %{_bindir}/gdaldem
%attr(755,root,root) %{_bindir}/gdalenhance
#%attr(755,root,root) %{_bindir}/gdalident.py
#%attr(755,root,root) %{_bindir}/gdalimport.py
%attr(755,root,root) %{_bindir}/gdalinfo
%attr(755,root,root) %{_bindir}/gdallocationinfo
%attr(755,root,root) %{_bindir}/gdalmanage
%attr(755,root,root) %{_bindir}/gdalsrsinfo
%attr(755,root,root) %{_bindir}/gdaltindex
%attr(755,root,root) %{_bindir}/gdaltransform
%attr(755,root,root) %{_bindir}/gdalwarp
#%attr(755,root,root) %{_bindir}/mkgraticule.py
%attr(755,root,root) %{_bindir}/nearblack
%attr(755,root,root) %{_bindir}/ogr2ogr
%attr(755,root,root) %{_bindir}/ogrinfo
%attr(755,root,root) %{_bindir}/ogrtindex
#%attr(755,root,root) %{_bindir}/pct2rgb.py
#%attr(755,root,root) %{_bindir}/rgb2pct.py
%attr(755,root,root) %{_bindir}/testepsg
%attr(755,root,root) %{_libdir}/libgdal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgdal.so.1
%attr(755,root,root) %ghost %{_libdir}/libgdal.a
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
%attr(755,root,root) /usr/share/gdal_datum.csv
%attr(755,root,root) /usr/share/gdalicon.png
%attr(755,root,root) /usr/share/geoccs.csv
%attr(755,root,root) /usr/share/gt_datum.csv
%attr(755,root,root) /usr/share/gt_ellips.csv
%attr(755,root,root) /usr/share/header.dxf
%attr(755,root,root) /usr/share/nitf_spec.xml
%attr(755,root,root) /usr/share/nitf_spec.xsd
%attr(755,root,root) /usr/share/osmconf.ini
%attr(755,root,root) /usr/share/ozi_datum.csv
%attr(755,root,root) /usr/share/ozi_ellips.csv
%attr(755,root,root) /usr/share/pci_datum.txt
%attr(755,root,root) /usr/share/pci_ellips.txt
%attr(755,root,root) /usr/share/pcs.csv
%attr(755,root,root) /usr/share/pcs.override.csv
%attr(755,root,root) /usr/share/prime_meridian.csv
%attr(755,root,root) /usr/share/projop_wparm.csv
%attr(755,root,root) /usr/share/s57agencies.csv
%attr(755,root,root) /usr/share/s57attributes.csv
%attr(755,root,root) /usr/share/s57attributes_aml.csv
%attr(755,root,root) /usr/share/s57attributes_iw.csv
%attr(755,root,root) /usr/share/s57expectedinput.csv
%attr(755,root,root) /usr/share/s57objectclasses.csv
%attr(755,root,root) /usr/share/s57objectclasses_aml.csv
%attr(755,root,root) /usr/share/s57objectclasses_iw.csv
%attr(755,root,root) /usr/share/seed_2d.dgn
%attr(755,root,root) /usr/share/seed_3d.dgn
%attr(755,root,root) /usr/share/stateplane.csv
%attr(755,root,root) /usr/share/trailer.dxf
%attr(755,root,root) /usr/share/unit_of_measure.csv
%attr(755,root,root) /usr/share/vertcs.csv
%attr(755,root,root) /usr/share/vertcs.override.csv
%attr(755,root,root) /usr/bin/epsg_tr.py
%attr(755,root,root) /usr/bin/esri2wkt.py
%attr(755,root,root) /usr/bin/gcps2vec.py
%attr(755,root,root) /usr/bin/gcps2wld.py
%attr(755,root,root) /usr/bin/gdal2tiles.py
%attr(755,root,root) /usr/bin/gdal2xyz.py
%attr(755,root,root) /usr/bin/gdal_auth.py
%attr(755,root,root) /usr/bin/gdal_calc.py
%attr(755,root,root) /usr/bin/gdal_edit.dox
%attr(755,root,root) /usr/bin/gdal_edit.py
%attr(755,root,root) /usr/bin/gdal_fillnodata.dox
%attr(755,root,root) /usr/bin/gdal_fillnodata.py
%attr(755,root,root) /usr/bin/gdal_merge.py
%attr(755,root,root) /usr/bin/gdal_polygonize.dox
%attr(755,root,root) /usr/bin/gdal_polygonize.py
%attr(755,root,root) /usr/bin/gdal_proximity.dox
%attr(755,root,root) /usr/bin/gdal_proximity.py
%attr(755,root,root) /usr/bin/gdal_retile.py
%attr(755,root,root) /usr/bin/gdal_sieve.dox
%attr(755,root,root) /usr/bin/gdal_sieve.py
%attr(755,root,root) /usr/bin/gdalchksum.py
%attr(755,root,root) /usr/bin/gdalident.py
%attr(755,root,root) /usr/bin/gdalimport.py
%attr(755,root,root) /usr/bin/gdalmove.dox
%attr(755,root,root) /usr/bin/gdalmove.py
%attr(755,root,root) /usr/bin/mkgraticule.py
%attr(755,root,root) /usr/bin/pct2rgb.py
%attr(755,root,root) /usr/bin/rgb2pct.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/GDAL-1.10.0-py2.6.egg-info/PKG-INFO
%attr(755,root,root) /usr/lib64/python2.6/site-packages/GDAL-1.10.0-py2.6.egg-info/SOURCES.txt
%attr(755,root,root) /usr/lib64/python2.6/site-packages/GDAL-1.10.0-py2.6.egg-info/dependency_links.txt
%attr(755,root,root) /usr/lib64/python2.6/site-packages/GDAL-1.10.0-py2.6.egg-info/not-zip-safe
%attr(755,root,root) /usr/lib64/python2.6/site-packages/GDAL-1.10.0-py2.6.egg-info/top_level.txt
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdal.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdal.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdal.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdalconst.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdalconst.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdalconst.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdalnumeric.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdalnumeric.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/gdalnumeric.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/ogr.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/ogr.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/ogr.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/__init__.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/__init__.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/__init__.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/_gdal.so
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/_gdal_array.so
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/_gdalconst.so
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/_ogr.so
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/_osr.so
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdal.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdal.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdal.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdal_array.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdal_array.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdal_array.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdalconst.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdalconst.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdalconst.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdalnumeric.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdalnumeric.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/gdalnumeric.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/ogr.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/ogr.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/ogr.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/osr.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/osr.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osgeo/osr.pyo
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osr.py
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osr.pyc
%attr(755,root,root) /usr/lib64/python2.6/site-packages/osr.pyo
#%{_datadir}/gdal
#%{_mandir}/man1/gdal2tiles.1*
#%{_mandir}/man1/gdal_contour.1*
#%{_mandir}/man1/gdal_fillnodata.1*
#%{_mandir}/man1/gdal_grid.1*
#%{_mandir}/man1/gdal_merge.1*
#%{_mandir}/man1/gdal_rasterize.1*
#%{_mandir}/man1/gdal_retile.1*
#%{_mandir}/man1/gdal_sieve.1*
#%{_mandir}/man1/gdal_translate.1*
#%{_mandir}/man1/gdal_utilities.1*
#%{_mandir}/man1/gdaladdo.1*
#%{_mandir}/man1/gdalbuildvrt.1*
#%{_mandir}/man1/gdaldem.1*
#%{_mandir}/man1/gdalinfo.1*
#%{_mandir}/man1/gdallocationinfo.1*
#%{_mandir}/man1/gdalsrsinfo.1*
#%{_mandir}/man1/gdaltindex.1*
#%{_mandir}/man1/gdaltransform.1*
#%{_mandir}/man1/gdalwarp.1*
#%{_mandir}/man1/nearblack.1*
#%{_mandir}/man1/ogr2ogr.1*
#%{_mandir}/man1/ogr_utilities.1*
#%{_mandir}/man1/ogrinfo.1*
#%{_mandir}/man1/ogrtindex.1*
#%{_mandir}/man1/pct2rgb.1*
#%{_mandir}/man1/rgb2pct.1*

%files devel
%defattr(644,root,root,755)
#%doc _html/*
%attr(755,root,root) %{_bindir}/gdal-config
%attr(755,root,root) %{_libdir}/libgdal.so
%{_libdir}/libgdal.la
%{_includedir}/cpl_*.h
%{_includedir}/cplkeywordparser.h
%{_includedir}/gdal*.h
%{_includedir}/gvgcpfit.h
%{_includedir}/memdataset.h
%{_includedir}/ogr_*.h
%{_includedir}/ogrsf_frmts.h
%{_includedir}/rawdataset.h
%{_includedir}/thinplatespline.h
%{_includedir}/vrtdataset.h
#%{_mandir}/man1/gdal-config.1*

%changelog

* Wed Aug 14 2013 Jesper Kihlberg <jekih@gst.dk> 1.0.0
- Initial version

