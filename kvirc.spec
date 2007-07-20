%define lib_name_orig %mklibname %name
%define lib_major 3
%define lib_name %lib_name_orig%lib_major

%define revision 661

Name:           kvirc
Version:        3.2.6
Release:        %mkrel 1
Summary:        Unix based IRC client
Group:          Networking/IRC
License:        GPL
URL:            http://www.kvirc.net
Source:	        %{name}-%{version}.rev%{revision}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  qt3-devel
BuildRequires:  kdelibs-devel

%description

Unix based IRC client.

%files
%defattr(-,root,root,-)
%{_bindir}/kvi_run_netscape
%{_bindir}/kvi_search_help
%{_bindir}/kvirc
%{_bindir}/kvirc-config
%{_datadir}/kvirc/3.2/locale/*
%{_datadir}/kvirc/3.2/modules/*
%{_datadir}/kvirc/3.2/config/modules/*
%{_mandir}/man1/kvirc.1.*
%{_datadir}/services/irc.protocol
%{_datadir}/services/irc6.protocol
%{_datadir}/kvirc/3.2/pics/*.png
%{_datadir}/kvirc/3.2/icons/*/*
%{_datadir}/kvirc/3.2/pics/coresmall/*.png
%{_datadir}/kvirc/3.2/themes/silverirc/*.png
%{_datadir}/kvirc/3.2/help/en/*.html
%{_datadir}/kvirc/3.2/applnk/kvirc.desktop
%{_datadir}/kvirc/3.2/config/*
%{_datadir}/kvirc/3.2/defscript/*
%{_datadir}/kvirc/3.2/help/en/*
%{_datadir}/kvirc/3.2/license/COPYING
%{_datadir}/kvirc/3.2/mimelnk/*
%{_datadir}/kvirc/3.2/msgcolors/*
%{_datadir}/kvirc/3.2/themes/silverirc/*

#--------------------------------------------------------------------

%package -n %lib_name
Summary:        Headers files for %{name}
Group:          Development/Other
Provides:       lib%name

%description -n %lib_name
Libraries for %name

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %lib_name
%defattr(-,root,root)
%{_libdir}/libkvilib.so.%{lib_major}*

#--------------------------------------------------------------------

%package  -n    %lib_name-devel
Requires:       %{lib_name} = %{version}
Summary:        %{name} development files
Group:          Development/Other
Provides:       %name-devel

%description -n %lib_name-devel
%{name} development files.

%files  -n %lib_name-devel
%defattr(-,root,root)
%dir %{_includedir}/kvirc/%version
%{_includedir}/kvirc/%version/*.h
%{_libdir}/libkvilib.la
%{_libdir}/libkvilib.so

#--------------------------------------------------------------------

%prep 
%setup -q -n %name


%build
sh autogen.sh

%configure --with-qt-library-dir=%_prefix/lib/qt3/%_lib/


make

%install
%makeinstall_std
 
%clean
rm -rf $RPM_BUILD_ROOT
