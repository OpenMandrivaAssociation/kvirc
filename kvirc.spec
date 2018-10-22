%define gitdate 20181022
%define branch_ver 5.0
%define _disable_ld_no_undefined 1
%define debug_package	  %{nil}
%define beta %{nil}

%define major 5
%define oldlib %mklibname kvilib 4
%define libname %mklibname kvilib %{major}
%define develname %mklibname kvilib -d

Name:	kvirc
Summary:	Qt IRC client
Group:	Networking/IRC
Version:	5.0.0
License:	GPLv2+ with exceptions
URL:	http://www.kvirc.net
%if 0%gitdate
Source0:	https://github.com/kvirc/KVIrc/archive/master.tar.gz
Release:	0.git%gitdate.1
%else
%if "%{beta}" != "%{nil}"
Source0:	https://github.com/kvirc/KVIrc/archive/%{beta}.tar.gz
Release:	0.%{beta}.1
%else
Source0:	ftp://ftp.kvirc.net/pub/kvirc/%{version}/source/%{name}-%{version}.tar.bz2
Release:	1
%endif
%endif
Patch0:		kvirc-find-perl-headers.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gettext
BuildRequires:	gsm-devel
BuildRequires:	perl-devel
BuildRequires:	shared-mime-info > 0.23
BuildRequires:	pkgconfig(libv4l1)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	cmake(Phonon4Qt5)
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:	cmake(Qt5MultimediaWidgets)
BuildRequires:	cmake(Qt5WebKitWidgets)
BuildRequires:	cmake(Qt5Svg)
BuildRequires:	cmake(Qt5Xml)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	qmake5
BuildRequires:	qt5-qtmultimedia
Provides:	kde4-irc-client
%rename kvirc4

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%files -f %{name}.lang
%{_bindir}/%{name}
%{_libdir}/%{name}/%{branch_ver}/modules/
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/%{branch_ver}
%{_datadir}/%{name}/%{branch_ver}/audio
%{_datadir}/%{name}/%{branch_ver}/config
%{_datadir}/%{name}/%{branch_ver}/defscript
%{_datadir}/%{name}/%{branch_ver}/help
%{_datadir}/%{name}/%{branch_ver}/license
%dir %{_datadir}/%{name}/%{branch_ver}/locale
%{_datadir}/%{name}/%{branch_ver}/modules
%{_datadir}/%{name}/%{branch_ver}/msgcolors
%{_datadir}/%{name}/%{branch_ver}/pics
%{_datadir}/%{name}/%{branch_ver}/themes
%{_datadir}/applications/%{name}.desktop
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
%if 0%gitdate
%autosetup -p1 -n KVIrc-master
%else
%if "%{beta}" != ""
%autosetup -p1 -n %{name}-%{version}%{beta}
%else
%autosetup -p1
%endif
%endif

%build
# WANT_DCC_CANVAS tries to #include <QCanvas>, which fails on modern
# versions of Qt (replaced with GraphicsView)
# Should be enabled once this is fixed.
%cmake \
%if 0%{?gitdate}
	-DMANUAL_REVISION=%gitdate \
	-DMANUAL_SOURCES_DATE=%gitdate \
%endif
	-DWANT_QT4=OFF \
	-DWANT_PERL=ON \
	-DWANT_DCC_VIDEO=ON \
	-DWANT_DCC_CANVAS=OFF \
	-DWANT_OGG_THEORA=ON

# FIXME this is evil...
#sed -i -e 's|-Wl,--fatal-warnings|-Wl,--no-fatal-warnings|' src/modules/perlcore/CMakeFiles/kviperlcore.dir/link.txt
sed -i -e 's|-Wl,--no-undefined||g' src/modules/perlcore/CMakeFiles/kviperlcore.dir/link.txt

%make

%install
%makeinstall_std -C build

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

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
