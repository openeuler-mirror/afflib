Name:           afflib
Version:        3.7.18
Release:        6
Summary:        Library to support the Advanced Forensic Format
License:        LGPL-2.0 and LGPL-2.1 and GPL-2.0+ and Public Domain
URL:            https://github.com/sshock/AFFLIBv3
Source0:        %{url}/archive/v%{version}.tar.gz
BuildRequires:  gcc-c++ libtool curl-devel expat-devel ncurses-devel
BuildRequires:  libtermcap-devel openssl-devel zlib-devel
BuildRequires:  python3 python3-devel python3-setuptools python3-Cython
Provides:       bundled(lzma) = 443

%description
Afflib is a library for support of the Advanced Forensic Format.

%package -n     afftools
Summary:        The Utility for %{name}
Requires:       %{name} = %{version}-%{release}

%description -n afftools
The %{name}-utils package contains utilities to use %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel pkgconfig

%description    devel
The %{name}-devel package contains libraries for developing 
applications that use %{name}.

%package -n python3-pyaff
Summary:        The python3 binding for the AFFLIB
Provides:       python-pyaff(aarch-64) = 3.7.18-3
Provides:       python-pyaff = 3.7.18-3
Obsoletes:      python-pyaff < 3.7.18-3

%description -n python3-pyaff
Python3 bindings currently support a read-only file-like interface to AFFLIB and
basic metadata accessor functions. These bindings are not currently complete.

%prep
%autosetup -p1 -n AFFLIBv3-%{version}
find lzma443 -type f -exec chmod 0644 {} ';'
chmod 0644 lib/base64.{h,cpp}
./bootstrap.sh

%build
%configure --enable-shared --disable-static --enable-python=no --enable-s3=yes
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build
cd pyaff
%global py_setup_args build_ext --include-dirs %{_builddir}/AFFLIBv3-%{version}/include --library-dirs %{_builddir}/AFFLIBv3-%{version}/lib/.libs
%py3_build

%install
%make_install
%delete_la
cd pyaff
%py3_install

%post
/sbin/ldconfig
%postun
/sbin/ldconfig

%files
%doc AUTHORS BUGLIST.txt ChangeLog NEWS README COPYING
%doc doc/announce_2.2.txt
%{_libdir}/*.so.*

%files -n afftools
%{_bindir}/aff*
%{_mandir}/man1/aff*.1.*

%files devel
%doc doc/crypto_design.txt doc/crypto_doc.txt
%{_includedir}/afflib/
%{_libdir}/*.so
%{_libdir}/pkgconfig/afflib.pc

%files -n python3-pyaff
%doc pyaff/README COPYING
%{python3_sitearch}/PyAFF*
%{python3_sitearch}/pyaff*

%changelog
* Tue Jan 11 2022 houyingchao <houyingchao@huawei.com> - 3.7.18-6
- Resolve compilation failure of afflib

* Thu Dec 03 2020 Ge Wang <wangge20@huawei.com> - 3.7.18-5
- modify license

* Wed Oct 21 2020 wutao <wutao61@huawei.com> - 3.7.18-4
- delete python2 modules

* Mon Jun 1 2020 wangyue <wangyue92@huawei.com> - 3.7.18-3
- Upgrade package

* Wed Mar 04 2019 yangjian<yangjian79@huawei.com> - 3.7.16-9
- Change  buildrequires

* Wed Feb 22 2019 yangjian<yangjian79@huawei.com> - 3.7.16-8
- Package init
