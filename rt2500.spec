#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
Summary:	Linux driver for WLAN cards based on RT2500
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie RT2500
Name:		rt2500
Version:	1.1.0
%define		_subver	b2
%define		_rel	0.%{_subver}.2
Release:	%{_rel}
Group:		Base/Kernel
License:	GPL v2
# Source0:	http://www.minitar.com/downloads/rt2500_linux-%{version}-b1.tgz
Source0:	http://rt2x00.serialmonkey.com/%{name}-%{version}-%{_subver}.tar.gz
# Source0-md5:	8846a055cd05bf71af96645637e5a2d1
URL:		http://rt2x00.serialmonkey.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
%if %{with userspace}
BuildRequires:	XFree86-devel
BuildRequires:	pkgconfig
BuildRequires:	qt-devel >= 3.1.1
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A configuartion tool for WLAN cards based on RT2500.

%description -l pl
Program do konfiguracji kart bezprzewodowych opartych na uk³adzie
RT2500.

%package -n kernel-net-rt2500
Summary:	Linux driver for WLAN cards based on RT2500
Summary(pl):	Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie RT2500
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel}

%description -n kernel-net-rt2500
This is a Linux driver for WLAN cards based on RT2500.

This package contains Linux module.

%description -n kernel-net-rt2500 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie
RT2500.

Ten pakiet zawiera modu³ j±dra Linuksa.

%package -n kernel-smp-net-rt2500
Summary:	Linux SMP driver for WLAN cards based on RT2500
Summary(pl):	Sterownik dla Linuksa SMP do kart bezprzewodowych opartych na uk³adzie RT2500
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
%{?with_dist_kernel:Requires(postun):	kernel-smp}

%description -n kernel-smp-net-rt2500
This is a Linux driver for WLAN cards based on RT2500.

This package contains Linux SMP module.

%description -n kernel-smp-net-rt2500 -l pl
Sterownik dla Linuksa do kart bezprzewodowych opartych na uk³adzie
RT2500.

Ten pakiet zawiera modu³ j±dra Linuksa SMP.

%prep
%setup -q

%{__perl} -pi -e 's@/lib@/%{_lib}@g' Utilitys/Makefile

%build
%if %{with userspace}
%{__make} -C Utilitys \
	CXXFLAGS="%{rpmcflags} %(pkg-config qt-mt --cflags)" \
	LDFLAGS="%{rpmldflags}" \
	QTDIR="%{_prefix}"
%endif

%if %{with kernel}
# kernel module(s)
cd Module
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	install -d include/{linux,config}
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
		M=$PWD O=$PWD \
		%{?with_verbose:V=1}
	mv rt2500{,-$cfg}.ko
done
cd -
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -D Utilitys/RaConfig $RPM_BUILD_ROOT%{_bindir}/RaConfig
%endif

%if %{with kernel}
cd Module
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/drivers/net/wireless
install rt2500-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/drivers/net/wireless/rt2500.ko
%if %{with smp} && %{with dist_kernel}
install rt2500-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/drivers/net/wireless/rt2500.ko
%endif
cd -
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-net-rt2500
%depmod %{_kernel_ver}

%postun -n kernel-net-rt2500
%depmod %{_kernel_ver}

%post -n kernel-smp-net-rt2500
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-rt2500
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc CHANGELOG FAQ 
%attr(755,root,root) %{_bindir}/RaConfig
%endif

%if %{with kernel}
%files -n kernel-net-rt2500
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/drivers/net/wireless/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-rt2500
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/drivers/net/wireless/*.ko*
%endif
%endif
