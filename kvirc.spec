%define svn	2842
%define rel	1

%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %rel
%define distname	%{name}-%{version}.tar.bz2
%define dirname		%{name}-%{version}
%endif

%define major		4
%define libname		%mklibname kvilib4_ %major
%define develname	%mklibname kvilib4 -d

Name:		kvirc
Version:	4.0.0
Release:	%{release}
Summary:	Qt IRC client
Group:		Networking/IRC
License:	GPLv2+ with exceptions
URL:		http://www.kvirc.net
Source0:	%{distname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	qt4-devel
BuildRequires:	kdelibs4-devel
BuildRequires:	perl-devel
BuildRequires:	gettext
BuildRequires:	phonon-devel
BuildRequires:	openssl-devel
Obsoletes:	kvirc4
Provides:	kvirc4

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%package -n %{libname}
Summary:	Shared library for KVirc 4
Group:		System/Libraries

%description -n %{libname}
Shared library provided by KVirc 4.

%package -n %{develname}
Requires:	%{libname} = %{version}-%{release}
Summary:	Development headers for KVirc 4
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname kvirc 3 -d} < %{version}-%{release}

%description -n %{develname}
Development headers for KVirc 4.

%prep 
%setup -q -n %{dirname}

%build
%cmake -DWITH_KDE4=true -DLIB_INSTALL_PREFIX=%{_libdir}
%make

%install
rm -rf %{buildroot}
pushd build
%makeinstall_std
popd

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48,64x64,128x128,scalable}/apps
for i in 16x16 32x32 48x48 64x64 128x128 scalable; do \
	cp data/icons/$i/*.* %{buildroot}%{_iconsdir}/hicolor/$i/apps; \
done
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
%{_iconsdir}/hicolor/*/apps/*
%{_iconsdir}/hicolor/*/*.png
%{_iconsdir}/hicolor/scalable/*.svgz
%{_mandir}/man1/*.1*
%{_datadir}/applications/%{name}4.desktop
%{_datadir}/mimelnk/*/*.desktop

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libkvilib4.so.%{major}*

%files  -n %{develname}
%defattr(-,root,root)
%{_libdir}/libkvilib4.so

