%define branch_ver 5.0
%define _disable_ld_no_undefined 1


%define major 5
%define oldlib %mklibname kvilib 4
%define libname %mklibname kvilib %{major}
%define develname %mklibname kvilib -d

%global optflags %{optflags} -Wno-error=register -fno-semantic-interposition -Wl,-Bsymbolic,-Bsymbolic-functions

%bcond_without kde

Name:		kvirc
Summary:	Qt IRC client
Group:		Networking/IRC
Version:	5.2.0
License:	GPLv2+ with exceptions
URL:		http://www.kvirc.net
Source0:	https://github.com/kvirc/KVIrc/archive/refs/tags/%{version}/KVIrc-%{version}.tar.gz
# Looks like no longer updated
#Source0:	ftp://ftp.kvirc.net/pub/kvirc/%{version}/source/%{name}-%{version}.tar.bz2
Release:	1

Patch0:		kvirc-find-perl-headers.patch
#Patch1:		kvirc-c++2a.patch
#Patch2:		kvirc-QTBUG-82415.patch
Patch3:		kvirc-20220810-compile.patch
Patch4:		kvirc-20230824-compile.patch
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	gsm-devel
BuildRequires:	perl-devel
BuildRequires:	shared-mime-info > 0.23
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	cmake(Phonon4Qt6)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	cmake(Qt6Multimedia)
BuildRequires:	cmake(Qt6MultimediaWidgets)
#BuildRequires:	cmake(Qt5WebKitWidgets)
BuildRequires:	cmake(Qt6Svg)
#BuildRequires:	cmake(Qt6X11Extras)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	qmake5
#BuildRequires:	qt5-qtmultimedia
BuildRequires:	perl(ExtUtils::Embed)
BuildRequires:	pkgconfig(enchant-2)
Provides:	kde4-irc-client

%if %{with kde}
# For KDE support (optional)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	cmake(KF6WindowSystem)
BuildRequires:	cmake(KF6Notifications)
BuildRequires:	cmake(KF6Service)
%endif

%rename kvirc4

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%files 
#-f %{name}.lang
%{_bindir}/%{name}
#{_libdir}/%{name}/%{branch_ver}/modules/
%dir %{_datadir}/%{name}/
#dir %{_datadir}/%{name}/%{branch_ver}
#{_datadir}/%{name}/%{branch_ver}/audio
#{_datadir}/%{name}/%{branch_ver}/config
#{_datadir}/%{name}/%{branch_ver}/defscript
#{_datadir}/%{name}/%{branch_ver}/help
#{_datadir}/%{name}/%{branch_ver}/license
#dir %{_datadir}/%{name}/%{branch_ver}/locale
#{_datadir}/%{name}/%{branch_ver}/modules
#{_datadir}/%{name}/%{branch_ver}/msgcolors
#{_datadir}/%{name}/%{branch_ver}/pics
#{_datadir}/%{name}/%{branch_ver}/themes
%{_datadir}/applications/net.kvirc.KVIrc5.desktop
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/scalable/*/*.svgz
%{_mandir}/man1/*.1*
%lang(de) %{_mandir}/de/man1/*.1*
%lang(it) %{_mandir}/it/man1/*.1*
%lang(fr) %{_mandir}/fr/man1/*.1*
%lang(pt) %{_mandir}/pt/man1/*.1*
%lang(uk) %{_mandir}/uk/man1/*.1*

#--------------------------------------------------------------------
%package -n %{libname}
Summary:	Shared library for KVirc 4
Group:	System/Libraries
Obsoletes:	%{mklibname kvirc 4 4} < 4.2.0
Obsoletes:	%{oldlib} < %{EVRD}

%description -n %{libname}
Shared library provided by KVirc 4.

%files -n %{libname}
%{_libdir}/libkvilib.so.%{major}*

#--------------------------------------------------------------------
%package -n %{develname}
Requires:	%{libname} = %{version}-%{release}
Summary:	Development headers for KVirc 4
Group:	Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname kvirc 4 -d} < 4.2.0

%description -n %{develname}
Development headers for KVirc 4.

%files  -n %{develname}
%{_bindir}/%{name}-config
%{_libdir}/libkvilib.so

#--------------------------------------------------------------------
%prep
%autosetup -n KVIrc-%{version} -p1
%cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DWANT_PERL:BOOL=ON \
	-DWANT_PYTHON:BOOL=ON \
	-DWANT_ESD:BOOL=OFF \
	-DWANT_DCC_VIDEO:BOOL=ON \
	-DWANT_OGG_THEORA:BOOL=ON \
 	-DBUILD_WITH_QT6:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,scalable}/apps
for i in 16x16 32x32 48x48 64x64 128x128; do \
	cp data/icons/$i/*.png %{buildroot}%{_iconsdir}/hicolor/$i/apps; \
done
cp data/icons/scalable/*.svg* %{buildroot}%{_iconsdir}/hicolor/scalable/apps

rm -f %{name}.lang
find %{buildroot}%{_datadir}/%{name}/%{branch_ver}/locale -name "*.mo" |while read r; do
	LNG=`echo $r |sed -e 's,.*_,,g;s,\.mo,,'`
	echo "%lang($LNG) $r" |sed -e 's,%{buildroot},,' >>%{name}.lang
done
