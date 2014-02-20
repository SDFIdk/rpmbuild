%define bdbdir	/usr/local/berkeleydb
%define real_name db

Name:		berkeleydb
Version:	6.0.20
Release:	1%{?dist}
Summary:	Berkeley DB

Group:		Applications/System
License:	GPL
URL:		http://www.oracle.com/technology/products/berkeley-db/db/index.html
Source0:	%{real_name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{real_name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc, make
	

%description
Berkeley DB, the most widely-used developer database in the world, is open 
source and runs on all major operating systems, including embedded Linux, 
Linux, MacOS X, QNX, UNIX, VxWorks and Windows.

%prep
%setup -n %{real_name}-%{version}


%build
cd build_unix
export CC=gcc 
../dist/configure --prefix=%{bdbdir}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
cd build_unix
make install DESTDIR=%{buildroot}

# PATH modification
mkdir -p %{buildroot}/etc/profile.d
#install -m 755 %{SOURCE1} %{buildroot}/etc/profile.d/
#sed -i 's:^BDB_BIN.*:BDB_BIN='%{bdbdir}/bin':' %{buildroot}/etc/profile.d/berkeleydb.sh

%post
# Don't do this if older version is installed
if [ $1 -eq 1 ]
then
	# Add BerkeleyDB libraries to the system
	echo "%{bdbdir}/lib" >> /etc/ld.so.conf
	/sbin/ldconfig
fi

%preun
# Don't do this if newer version is installed
if [ $1 -eq 0 ]
then
	# Remove BerkeleyDB libraries from the system
	sed -i '\:'%{bdbdir}/lib':d' /etc/ld.so.conf
	/sbin/ldconfig
fi

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, 0755)
%doc %{bdbdir}/docs
%dir %{bdbdir}
%{bdbdir}/bin
%{bdbdir}/include
%{bdbdir}/lib
#/etc/profile.d/berkeleydb.sh



%changelog

