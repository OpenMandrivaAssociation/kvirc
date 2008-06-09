%define major		3
%define libname		%mklibname %name %major
%define develname	%mklibname %name -d

Name:		kvirc
Version:	3.4.0
Release:	%mkrel 1
Summary:	Qt IRC client
Group:		Networking/IRC
License:	GPLv2+
URL:		http://www.kvirc.net
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:	qt3-devel
BuildRequires:	kdelibs-devel
BuildRequires:	arts-devel
BuildRequires:	autoconf
BuildRequires:	perl-devel
BuildRequires:	esound-devel

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
%setup -q

%build
sh autogen.sh
%configure2_5x --with-qt-library-dir=%{qt3lib} --with-kde-library-dir=%{_libdir}/kde3/
make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=KVIrc
Comment=IRC chat client
Exec=%{_bindir}/%{name} -m %u
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
MimeType=application/x-kva;application/x-kvt;
Categories=Qt;Network;IRCClient;
EOF

rm -rf %{buildroot}%{_datadir}/applnk
# conflicts with Kopete, Kopete should probably be default - AdamW
# 2008/03
rm -f %{buildroot}%{_datadir}/services/irc.protocol

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
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/services/*
%{_iconsdir}/hicolor/*/*/*.*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/mimelnk/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libkvilib.so.%{major}*

%files  -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/libkvilib.la
%{_libdir}/libkvilib.so

