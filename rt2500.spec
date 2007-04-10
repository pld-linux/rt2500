#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	up		# don't build UP module
%bcond_without	userspace	# don't build userspace tool
%bcond_with	verbose		# verbose build (V=1)
#
%ifarch sparc
%undefine	with_smp
%endif
#
%define		_subver	b4
%define		_rel	0.%{_subver}.1
Summary:	Linux driver for WLAN cards based on RT2500
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie RT2500
Name:		rt2500
Version:	1.1.0
Release:	%{_rel}
License:	GPL v2
Group:		Base/Kernel
# Source0:	http://www.minitar.com/downloads/rt2500_linux-%{version}-b1.tgz
Source0:	http://dl.sourceforge.net/rt2400/%{name}-%{version}-%{_subver}.tar.gz
# Source0-md5:	83b8b9a091705c08d99268479f3b3b6a
Patch0:		%{name}-qt.patch
URL:		http://rt2x00.serialmonkey.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
%if %{with userspace}
BuildRequires:	pkgconfig
BuildRequires:	qmake
BuildRequires:	qt-devel >= 6:3.1.1
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A configuartion tool for WLAN cards based on RT2500.

%description -l pl.UTF-8
Program do konfiguracji kart bezprzewodowych opartych na układzie
RT2500.

%package -n kernel%{_alt_kernel}-net-rt2500
Summary:	Linux driver for WLAN cards based on RT2500
Summary(pl.UTF-8):	Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie RT2500
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-net-rt2500
This is a Linux driver for WLAN cards based on RT2500.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-net-rt2500 -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
RT2500.

Ten pakiet zawiera moduł jądra Linuksa.

%package -n kernel%{_alt_kernel}-smp-net-rt2500
Summary:	Linux SMP driver for WLAN cards based on RT2500
Summary(pl.UTF-8):	Sterownik dla Linuksa SMP do kart bezprzewodowych opartych na układzie RT2500
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif

%description -n kernel%{_alt_kernel}-smp-net-rt2500
This is a Linux driver for WLAN cards based on RT2500.

This package contains Linux SMP module.

%description -n kernel%{_alt_kernel}-smp-net-rt2500 -l pl.UTF-8
Sterownik dla Linuksa do kart bezprzewodowych opartych na układzie
RT2500.

Ten pakiet zawiera moduł jądra Linuksa SMP.

%prep
%setup -q -n %{name}-%{version}-%{_subver}
%patch0 -p1

%build
%if %{with userspace}
qmake -unix Utilitys/raconfig2500.pro -o Utilitys/Makefile

%{__make} -C Utilitys \
	CXXFLAGS="%{rpmcflags} %(pkg-config qt-mt --cflags)" \
	LDFLAGS="%{rpmldflags}" \
	CXX="%{__cxx}" \
	QTDIR="%{_prefix}"
%endif

%if %{with kernel}
%build_kernel_modules -C Module -m rt2500
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -D Utilitys/RaConfig2500 $RPM_BUILD_ROOT%{_bindir}/RaConfig2500
%endif

%if %{with kernel}
%install_kernel_modules -m Module/rt2500 -d kernel/drivers/net/wireless
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-net-rt2500
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-net-rt2500
%depmod %{_kernel_ver}

%post -n kernel%{_alt_kernel}-smp-net-rt2500
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-net-rt2500
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc CHANGELOG FAQ
%attr(755,root,root) %{_bindir}/RaConfig2500
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-net-rt2500
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-net-rt2500
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*.ko*
%endif
%endif
