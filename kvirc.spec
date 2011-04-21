%define major		4
%define libname		%mklibname kvilib %major
%define develname	%mklibname kvilib -d

Name:		kvirc
Version:	4.0.4
Release:	%mkrel 1
Summary:	Qt IRC client
Group:		Networking/IRC
License:	GPLv2+ with exceptions
URL:		http://www.kvirc.net
Source0:	%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	cmake
BuildRequires:	kdelibs4-devel
BuildRequires:	perl-devel
BuildRequires:	gettext
BuildRequires:	phonon-devel
BuildRequires:	openssl-devel
BuildRequires:	doxygen
BuildRequires:	shared-mime-info > 0.23
BuildRequires:	gsm-devel
Obsoletes:	kvirc4 < %version-%release
Provides:	kvirc4 = %version-%release

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%package -n %{libname}
Summary:	Shared library for KVirc 4
Group:		System/Libraries
Obsoletes:	%{mklibname kvirc 4 4} 

%description -n %{libname}
Shared library provided by KVirc 4.

%package -n %{develname}
Requires:	%{libname} = %{version}-%{release}
Summary:	Development headers for KVirc 4
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname kvirc 3 -d} < %{version}-%{release}
Obsoletes:	%{mklibname kvirc 4 -d} 

%description -n %{develname}
Development headers for KVirc 4.

%prep 
%setup -q

%build
%cmake_kde4
%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,scalable}/apps
for i in 16x16 32x32 48x48 64x64 128x128; do \
	cp data/icons/$i/*.png %{buildroot}%{_iconsdir}/hicolor/$i/apps; \
done
cp data/icons/scalable/*.svg* %{buildroot}%{_iconsdir}/hicolor/scalable/apps
rm -f %{buildroot}%{_iconsdir}/hicolor/scalable/apps/createpng.sh

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_libdir}/%{name}/4.0
%{_datadir}/%{name}/4.0
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/scalable/*/*.svgz
%{_mandir}/man1/*.1*
%lang(de) %_mandir/de/man1/*.1*
%lang(it) %_mandir/it/man1/*.1*
%lang(fr) %_mandir/it/man1/*.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libkvilib.so.%{major}*

%files  -n %{develname}
%defattr(-,root,root)
%{_bindir}/%name-config
%{_libdir}/libkvilib.so
