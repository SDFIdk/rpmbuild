#
# Needs to be built with:  QA_RPATHS=$[ 0x0001|0x002 ] rpmbuild -bb rpmbuild/SPECS/libecwj2.spec
# otherwise it complains about some rpaths - which we cannot see any problem with.. 
#
Name:	libecwj2	
Version:	3.3
Release:	2%{?dist}
Summary:	Library for handling Enhanced Compression Wavelet

Group:		libs
License:	ECWPL
URL:		http://wiki.openstreetmap.org/wiki/ECW
Source0:	http://mirror.ovh.net/gentoo-distfiles/distfiles/libecwj2-3.3-2006-09-06.zip
Patch0:		libecwj2-3.3-msvc90-fixes.patch
Patch1:		libecwj2-3.3-NCSPhysicalMemorySize-Linux.patch
Patch2:		libecwj2-3.3-wcharfix.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description

%prep
%setup -q
cd ..
%patch0 -p0
cd libecwj2-3.3/
%patch1 -p0
%patch2 -p1


%build
#%configure
./configure --prefix=/opt/libecw
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
mkdir %{buildroot}/opt/libecw/include -p
mkdir %{buildroot}/opt/libecw/lib 
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/opt/libecw


%changelog
* Thu Jan 24 2019 - Jonas Lund Nielsen - jolni@sdfe.dk
- Initial build on RHEL7

* Fri Aug 09 2013 - Jesper Kihlberg - jekih@gst.dk
- Initial package creation
