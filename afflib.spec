Name:           afflib
Version:        3.7.16
Release:        8
Summary:        Libraries supporting advanced forensic formats

License:        BSD with advertising
URL:            https://github.com/sshock/AFFLIBv3
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         Sanity-check-size-passed-to-malloc.patch

BuildRequires:  gcc-c++ libtool curl-devel expat-devel lzma-devel zlib-devel
BuildRequires:  ncurses-devel libtermcap-devel openssl-devel python2-devel

Provides:      afftools = %{version}-%{release}
Obsoletes:     afftools < %{version}-%{release}

%description
AFF® is an open and extensible file format designed to store
disk images and associated metadata.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       openssl-devel pkgconfig

%description    devel
The %{name}-devel package contains libraries for
developing applications that use %{name}.

%package        help
Summary:        Help for %{name}

%description  help
The %{name}-help package contains help for %{name}.

%prep
%autosetup -p1 -n AFFLIBv3-%{version}

find lzma443 -type f -exec chmod 0644 {} ';'
chmod 0644 lib/base64.{h,cpp}

./bootstrap.sh

%build
%configure --enable-shared --disable-static --enable-python=yes --enable-s3=yes

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build


%install
%make_install
%delete_la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/*.so.*
%{_bindir}/aff*
%{python2_sitearch}/*

%files devel
%doc doc/crypto_design.txt doc/crypto_doc.txt
%{_includedir}/afflib/
%{_libdir}/*.so
%{_libdir}/pkgconfig/afflib.pc

%files help
%doc AUTHORS BUGLIST.txt ChangeLog NEWS README
%doc doc/announce_2.2.txt
%{_mandir}/man1/aff*.1.*

%changelog
* Wed Feb 22 2019 yangjian<yangjian79@huawei.com> - 3.7.16-8
- Package init
