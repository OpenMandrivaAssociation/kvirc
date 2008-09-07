%define _disable_ld_no_undefined 1
%define _disable_ld_as_needed 1

%define major		3
%define libname		%mklibname %name %major
%define develname	%mklibname %name -d

%define svn	2417
%define rel	1
%if %svn
%define release		%mkrel 0.%{svn}.%{rel}
%define distname	%{name}-%{svn}.tar.lzma
%define dirname		%{name}
%else
%define release		%mkrel %{rel}
%define distname	%{name}-%{version}.tar.bz2
%define dirname		%{name}-%{version}
%endif

Name:		kvirc
Version:	3.4.1
Release:	%{release}
Summary:	Qt IRC client
Group:		Networking/IRC
License:	GPLv2+ with exceptions
URL:		http://www.kvirc.net
Source:		ftp://ftp.kvirc.net/pub/kvirc/%{version}/source/%{distname}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	qt3-devel
BuildRequires:	kdelibs-devel
BuildRequires:	arts-devel
BuildRequires:	autoconf
BuildRequires:	perl-devel
BuildRequires:	esound-devel
BuildRequires:	openssl-devel

%description
Qt-based IRC client with support for themes, transparency, encryption,
many extended IRC features, and scripting.

%package -n %{libname}
Summary:        Shared library of %{name}
Group:          System/Libraries

%description -n %{libname}
Shared library provided by %{name}.

%package  -n    %{develname}
Requires:       %{libname} = %{version}-%{release}
Summary:        Development headers for %{name}
Group:          Development/C++
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname kvirc 3 -d} < %{version}-%{release}

%description -n %{develname}
Development headers for %{name}.

%prep 
%setup -q -n %{dirname}

%build
sh autogen.sh
%configure_kde3 --with-qt-library-dir=%{qt3lib} --with-kde-library-dir=/opt/kde3/lib/ --mandir=%{_kde3_mandir}
make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_kde3_datadir}/applications
cat > %{buildroot}%{_kde3_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=KVIrc (KDE 3)
Comment=IRC chat client
Exec=%{_kde3_bindir}/%{name} -m %u
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
MimeType=application/x-kva;application/x-kvt;
Categories=Qt;Network;IRCClient;
EOF

rm -rf %{buildroot}%{_kde3_datadir}/applnk
# conflicts with Kopete, Kopete should probably be default - AdamW
# 2008/03
rm -f %{buildroot}%{_kde3_datadir}/services/irc.protocol

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
%{_kde3_bindir}/*
%{_kde3_datadir}/%{name}
%{_kde3_mandir}/man1/*
%{_kde3_datadir}/services/*
%{_kde3_datadir}/applications/mandriva-%{name}.desktop
%{_kde3_datadir}/mimelnk/*
%{_kde3_iconsdir}/hicolor/[0-9]*/*/*.png
%{_kde3_iconsdir}/hicolor/scalable/*/*.svgz

%files -n %{libname}
%defattr(-,root,root)
%{_kde3_libdir}/libkvilib.so.%{major}*

%files  -n %{develname}
%defattr(-,root,root)
%{_kde3_includedir}/%{name}
%{_kde3_libdir}/libkvilib.la
%{_kde3_libdir}/libkvilib.so

