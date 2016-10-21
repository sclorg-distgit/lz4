%{?scl:%scl_package lz4}
%{!?scl:%global pkg_name %{name}}

%global _hardened_build 1
%global commit d86dc916771c126afb797637dda9f6421c0cb998

%bcond_with static

Name:           %{?scl_prefix}lz4
Version:        r131
Release:        5%{?dist}
Summary:        Extremely fast compression algorithm

Group:          Applications/System
License:        GPLv2+ and BSD
URL:            https://code.google.com/p/lz4/
Source0:        https://github.com/Cyan4973/%{pkg_name}/archive/%{commit}/%{pkg_name}-%{commit}.tar.gz

%if 0%{?rhel}
BuildRoot:      %{_tmppath}/%{pkg_name}-%{version}-%{release}-buildroot
%endif

%{?scl:BuildRequires:%scl_runtime}
%{?scl:Requires:%scl_runtime}

%description
LZ4 is an extremely fast loss-less compression algorithm, providing compression
speed at 400 MB/s per core, scalable with multi-core CPU. It also features
an extremely fast decoder, with speed in multiple GB/s per core, typically
reaching RAM speed limits on multi-core systems.

%package        devel
Summary:        Development library for lz4
Group:          Development/Libraries
License:        BSD
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?scl:Requires:%scl_runtime}

%description    devel
This package contains the header(.h) and library(.so) files required to build
applications using liblz4 library.


%if %{with static}
%package        static
Summary:        Static library for lz4
Group:          Development/Libraries
License:        BSD
%{?scl:Requires:%scl_runtime}

%description    static
LZ4 is an extremely fast loss-less compression algorithm. This package
contains static libraries for static linking of applications.
%endif

%prep
%setup -q -n %{pkg_name}-%{commit}
echo '#!/bin/sh' > ./configure
chmod +x ./configure

sed -i -e 's/^LIBVER_MAJOR=/LIBVER_MAJOR=%{?scl_prefix}/' lib/Makefile

%build
%{?scl:scl enable %{scl} - << \EOF}
%configure
make %{?_smp_mflags}
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << \EOF}
%configure
%make_install LIBDIR=%{_libdir} PREFIX=%{_prefix} INSTALL="install -p"
chmod -x %{buildroot}%{_includedir}/*.h
%if %{without static}
rm -f %{buildroot}%{_libdir}/liblz4.a
%endif
%{?scl:EOF}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%doc programs/COPYING NEWS
%{_bindir}/lz4
%{_bindir}/lz4c
%{_bindir}/lz4cat
%{_bindir}/unlz4
%{_mandir}/man1/lz4*
%{_mandir}/man1/unlz4*
%{_libdir}/liblz4.so.*


%files devel
%doc lib/LICENSE
%{_includedir}/*.h
%{_libdir}/liblz4.so
%{_libdir}/pkgconfig/liblz4.pc


%if %{with static}
%files static
%doc lib/LICENSE
%{_libdir}/liblz4.a
%endif


%changelog
* Sun Jul 17 2016 Honza Horak <hhorak@redhat.com> - r131-5
- Prefix major version of the library with the scl name

* Fri Jul 15 2016 Honza Horak <hhorak@redhat.com> - r131-4
- Require runtime package from the scl

* Fri Jul 15 2016 Honza Horak <hhorak@redhat.com> - r131-3
- Convert to SCL package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - r131-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 06 2015 pjp <pjp@fedoraproject.org> - r131-1
- New: Dos/DJGPP target #114.
- Added: Example using lz4frame library #118.
- Changed: liblz4.a no longer compiled with -fPIC by default.

* Thu Jun 18 2015 pjp <pjp@fedoraproject.org> - r130-1
- Fixed: incompatibility sparse mode vs console.
- Fixed: LZ4IO exits too early when frame crc not present.
- Fixed: incompatibility sparse mode vs append mode.
- Performance fix: big compression speed boost for clang(+30%).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - r129-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 pjp <pjp@fedoraproject.org> - r129-1
- New LZ4_compress_fast() API.
- New LZ4 CLI improved performance with multiple files.
- Other bug fix and documentation updates.

* Mon Apr 06 2015 pjp <pjp@fedoraproject.org> - r128-2
- Update files section to install unlz4 & its manual

* Wed Apr 01 2015 pjp <pjp@fedoraproject.org> - r128-1
- lz4cli sparse file support
- Restored lz4hc compression ratio
- lz4 cli supports long commands
- Introduced lz4-static sub package BZ#1208203

* Thu Jan 08 2015 pjp <pjp@fedoraproject.org> - r127-2
- Bump dist to override an earlier build.

* Wed Jan 07 2015 pjp <pjp@fedoraproject.org> - r127-1
- Fixed a bug in LZ4 HC streaming mode
- New lz4frame API integrated into liblz4
- Fixed a GCC 4.9 bug on highest performance settings

* Thu Nov 13 2014 pjp <pjp@fedoraproject.org> - r124-1
- New LZ4 HC Streaming mode

* Tue Sep 30 2014 pjp <pjp@fedoraproject.org> - r123-1
- Added experimental lz4frame API.
- Fix s390x support.

* Sat Aug 30 2014 pjp <pjp@fedoraproject.org> - r122-1
- new release
- Fixed AIX & AIX64 support (SamG)
- Fixed mips 64-bits support (lew van)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - r121-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - r121-2
- fix destdir

* Fri Aug 08 2014 pjp <pjp@fedoraproject.org> - r121-1
- new release
- Added a pkg-config file.
- Fixed a LZ4 streaming crash bug.

* Thu Jul 03 2014 pjp <pjp@fedoraproject.org> - r119-1
- new release
- Fixed a high Address allocation issue in 32-bits mode.

* Sat Jun 28 2014 pjp <pjp@fedoraproject.org> - r118-1
- new release
- install libraries under appropriate _libdir directories.

* Sat Jun 14 2014 pjp <pjp@fedoraproject.org> - r117-3
- Move shared library object to -devel package.

* Sat Jun 07 2014 pjp <pjp@fedoraproject.org> - r117-2
- Skip static library from installation.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - r117-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jun 06 2014 pjp <pjp@fedoraproject.org> - r117-1
- new release
- added lz4c & lz4cat manual pages.

* Sun Apr 13 2014 pjp <pjp@fedoraproject.org> - r116-1
- new release 116
- added lz4cat utility for posix systems

* Sat Mar 15 2014 pjp <pjp@fedoraproject.org> - r114-1
- new release r114
- added RPM_OPT_FLAGS to CFLAGS
- introduced a devel package to build liblz4

* Thu Jan 02 2014 pjp <pjp@fedoraproject.org> - r110-1
- new release r110

* Sun Nov 10 2013 pjp <pjp@fedoraproject.org> - r108-1
- new release r108

* Wed Oct 23 2013 pjp <pjp@fedoraproject.org> - r107-1
- new release r107

* Mon Oct 07 2013 pjp <pjp@fedoraproject.org> - r106-3
- fixed install section to replace /usr/ with a macro.
  -> https://bugzilla.redhat.com/show_bug.cgi?id=1015263#c5

* Sat Oct 05 2013 pjp <pjp@fedoraproject.org> - r106-2
- fixed install section above as suggested in the review.
  -> https://bugzilla.redhat.com/show_bug.cgi?id=1015263#c1

* Sun Sep 22 2013 pjp <pjp@fedoraproject.org> - r106-1
- Initial RPM release of lz4-r106
