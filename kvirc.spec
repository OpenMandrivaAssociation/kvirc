%define svnrev 6296
%define branch_ver 4.3
%define _disable_ld_no_undefined 1

%define major		4
%define libname		%mklibname kvilib %{major}
%define develname	%mklibname kvilib -d

Name:		kvirc
Summary:	Qt IRC client
Group:		Networking/IRC
Version:	4.3.1
Release:	1
License:	GPLv2+ with exceptions
URL:		http://www.kvirc.net
%if 0%svnrev
Source0:	kvirc-%svnrev.tar.xz
%else
Source0:	ftp://ftp.kvirc.net/pub/kvirc/%{version}/source/%{name}-%{version}.tar.bz2
%endif
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
%{_datadir}/%{name}/%{branch_ver}/doc
%{_datadir}/%{name}/%{branch_ver}/help
%{_datadir}/%{name}/%{branch_ver}/license
%dir %{_datadir}/%{name}/%{branch_ver}/locale
%{_datadir}/%{name}/%{branch_ver}/modules
%{_datadir}/%{name}/%{branch_ver}/msgcolors
%{_datadir}/%{name}/%{branch_ver}/pics
%{_datadir}/%{name}/%{branch_ver}/themes
%{_datadir}/apps/kvirc/kvirc.notifyrc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/kde4/services/*
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
Group:		System/Libraries
Obsoletes:	%{mklibname kvirc 4 4} < 4.2.0

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
Obsoletes:	%{mklibname kvirc 4 -d} < 4.2.0

%description -n %{develname}
Development headers for KVirc 4.

%files  -n %{develname}
%{_bindir}/%{name}-config
%{_libdir}/libkvilib.so

#--------------------------------------------------------------------
%prep
%setup -q

%build
%cmake_kde4 \
%if 0%svnrev
    -DMANUAL_REVISION=%{svnrev} \
%endif
    -DWANT_DCC_VIDEO=ON \
    -DWANT_OGG_THEORA=ON

# FIXME this is evil...
sed -i -e 's|-Wl,--fatal-warnings|-Wl,--no-fatal-warnings|' src/modules/perlcore/CMakeFiles/kviperlcore.dir/link.txt

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
desktop-file-validate %{buildroot}%{_kde_datadir}/applications/%{name}.desktop

%changelog
* Mon Jan 30 2012 Bernhard Rosenkraenzer <bero@bero.eu> 4.1.3-0.svn6063.1mdv2012.0
+ Revision: 769867
- Mark locale related files as such
- Update to rev. 6063, fixing the cursor-off-by-some-pixels bug
- Add Provides: kde4-irc-client (metapackage required by task-kde)

* Sat Dec 17 2011 Zé <ze@mandriva.org> 4.1.3-0.svn5993.1
+ Revision: 743188
- use revision 5993
- we need to manually add svn revision since that only provided by svn files
- move to svn (version 4.1.3)
- clean defattr, BR and clean section
- add check section
- 2009 is no longer maintained
- add dcc video and theora support
- use pkg in buildrequires
- clean duplicated files

* Thu Apr 21 2011 Zé <ze@mandriva.org> 4.0.4-1
+ Revision: 656538
- update source file
- version 4.0.4
- add missing buildrequires for: cmake, shared-mime-info, gsm-devel
- remove buildrequire qt4-devel since its already required by kdelibs4-devel
- use macro cmake_kde4 since kde support is enabled by default

* Mon Nov 29 2010 Michael Scherer <misc@mandriva.org> 4.0.2-2mdv2011.0
+ Revision: 603106
- rebuild for new perl

* Sun Aug 08 2010 Rémy Clouard <shikamaru@mandriva.org> 4.0.2-1mdv2011.0
+ Revision: 567692
- update to stable release 4.0.2 \o/
- clean spec

* Sun Apr 25 2010 Rémy Clouard <shikamaru@mandriva.org> 4.0.0-0.4255.1mdv2010.1
+ Revision: 538572
- update to rc3
- fix iconlist to avoid CMakeLists to be copied
- fix filelist
- use xz instead of lzma for compression

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 4.0.0-0.3065.2mdv2010.0
+ Revision: 438172
- rebuild

* Wed Feb 04 2009 Adam Williamson <awilliamson@mandriva.org> 4.0.0-0.3065.1mdv2009.1
+ Revision: 337495
- go back to my naming scheme (or upgrading breaks)
- from shika: new snapshot 3065, drop desktop.patch (merged)

* Sun Nov 09 2008 Adam Williamson <awilliamson@mandriva.org> 4.0.0-0.2842.2mdv2009.1
+ Revision: 301629
- fix menu entry (again), thanks Adam Pigg

* Sun Nov 09 2008 Adam Williamson <awilliamson@mandriva.org> 4.0.0-0.2842.1mdv2009.1
+ Revision: 301192
- switch to kvirc4 in the main package, drop kvirc4 package

* Sun Sep 07 2008 Adam Williamson <awilliamson@mandriva.org> 3.4.1-0.2417.1mdv2009.0
+ Revision: 282376
- correct libdir in configure
- mention SVN location for 3.4 branch
- move to /opt
- enable SSL support (license problem resolved)
- update license
- bump to current SVN of 3.4 branch for updated license and misc fixes
- disable underlinking protection (breaks build, can't fix easily and I
  need to get a new build through)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Apr 17 2008 Adam Williamson <awilliamson@mandriva.org> 3.4.0-1mdv2009.0
+ Revision: 195298
- use qt3 macros
- version the obsolete
- new release 3.4.0

* Fri Mar 21 2008 Adam Williamson <awilliamson@mandriva.org> 3.2.6-2mdv2008.1
+ Revision: 189333
- drop irc.protocol (causes conflict with kopete) (#38453)

* Wed Feb 06 2008 Adam Williamson <awilliamson@mandriva.org> 3.2.6-1mdv2008.1
+ Revision: 162955
- disable parallel build again (doesn't seem to work)
- rebuild for new era (and fixes 20120)
- adjust file list
- add --with-kde-lib-dir parameter to fix KDE-supporting build on x86-64
- include working XDG menu entry
- new library policy
- new license policy
- extensive spec clean and rearrange to fit MDV norms
- new release 3.2.6 final

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Nicolas Lécureuil <nlecureuil@mandriva.com>
    - Fix File list
    - Add BuildRequires
    - Import kvirc

