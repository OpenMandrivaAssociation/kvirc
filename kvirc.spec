%define svn 1
%define svnrev 6063
%define branch_ver 4.1

%define major		4
%define libname		%mklibname kvilib %major
%define develname	%mklibname kvilib -d

Name:		kvirc
Summary:	Qt IRC client
Group:		Networking/IRC
Version:	4.1.3
Release:	%mkrel -c svn%{svnrev} 1
License:	GPLv2+ with exceptions
URL:		http://www.kvirc.net
Source0:	ftp://ftp.kvirc.net/pub/kvirc/%{version}/source/%{name}%{?!svn:-%{version}}%{?svn:-%{svnrev}}.tar.xz
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	gsm-devel
BuildRequires:	kdelibs4-devel
BuildRequires:	perl-devel
BuildRequires:	shared-mime-info > 0.23
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(phonon)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(theora)
Obsoletes:	kvirc4 < %version-%release
Provides:	kvirc4 = %version-%release
Provides:	kde4-irc-client

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%files
%{_bindir}/%{name}
%{_libdir}/%{name}/%{branch_ver}/modules/
%{_datadir}/%{name}/
%{_datadir}/apps/kvirc/kvirc.notifyrc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/kde4/services/*
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/scalable/*/*.svgz
%{_mandir}/man1/*.1*
%lang(de) %_mandir/de/man1/*.1*
%lang(it) %_mandir/it/man1/*.1*
%lang(fr) %_mandir/fr/man1/*.1*
%lang(pt) %{_mandir}/pt/man1/*

#--------------------------------------------------------------------
%package -n %{libname}
Summary:	Shared library for KVirc 4
Group:		System/Libraries
Obsoletes:	%{mklibname kvirc 4 4} 

%description -n %{libname}
Shared library provided by KVirc 4.

%files -n %{libname}
%{_libdir}/libkvilib.so.%{major}*

#--------------------------------------------------------------------
%package -n %{develname}
Requires:	%{libname} = %{version}-%{release}
Summary:	Development headers for KVirc 4
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname kvirc 3 -d} < %{version}-%{release}
Obsoletes:	%{mklibname kvirc 4 -d} 

%description -n %{develname}
Development headers for KVirc 4.

%files  -n %{develname}
%{_bindir}/%name-config
%{_libdir}/libkvilib.so

#--------------------------------------------------------------------
%prep
%setup -q%{?svn:n %{name}}

%build
%cmake_kde4 \
    -DWANT_DCC_VIDEO=ON \
    -DWANT_OGG_THEORA=ON \
%{?svn:\
    -DMANUAL_REVISION=%{svnrev}}

%make

%install
rm -rf %{buildroot}
%makeinstall_std -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,scalable}/apps
for i in 16x16 32x32 48x48 64x64 128x128; do \
	cp data/icons/$i/*.png %{buildroot}%{_iconsdir}/hicolor/$i/apps; \
done
cp data/icons/scalable/*.svg* %{buildroot}%{_iconsdir}/hicolor/scalable/apps

%check
desktop-file-validate %{buildroot}%{_kde_datadir}/applications/%{name}.desktop
