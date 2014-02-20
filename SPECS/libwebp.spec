Name:		libwebp
Version:	0.3.1
Release:	1%{?dist}
Summary:	WebP library

Group:		System/Libraries
License:	BSD
URL:		http://code.google.com/speed/webp/
Source0:	http://webp.googlecode.com/files/libwebp-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#BuildRequires:	
#Requires:	

%description
WebP is a method of lossy compression that can be used on photographic images.
The degree of compression is adjustable so a user can choose the trade-off between file size and image quality.

%package devel
Group:         Development/Libraries
Summary:       Static libraries and headers for %{name}
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description devel
WebP is a method of lossy compression that can be used on photographic images.
The degree of compression is adjustable so a user can choose the trade-off between file size and image quality.

This package contains static libraries and header files need for development.

%package tools
Group:         Applications/Graphics
Summary:       The WebP command line tools
Requires:      %{name} = %{?epoch:%epoch:}%{version}-%{release}

%description tools
WebP is a method of lossy compression that can be used on photographic images.
The degree of compression is adjustable so a user can choose the trade-off between file size and image quality.

This package contains utility applications for %{name}.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}


%clean
rm -rf %{buildroot}


#%files
#%defattr(-,root,root,-)
#%doc

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%doc AUTHORS COPYING
/usr/lib64/libwebp.a
#ChangeLog NEWS README

%files devel
%defattr(-,root,root)
%{_includedir}/webp
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Aug 14 2013 Jesper Kihlberg <jekih@gst.dk> 0.3.1-1
- Initial version

