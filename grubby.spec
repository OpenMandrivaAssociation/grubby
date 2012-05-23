Name: grubby
Version: 8.11
Release: 1
Summary: Command line tool for updating bootloader configs
Group: System/Base
License: GPLv2+
URL: http://git.fedorahosted.org/git/grubby.git
# we only pull git snaps at the moment
# git clone git://git.fedorahosted.org/git/grubby.git
# git archive --format=tar --prefix=grubby-%{version}/ HEAD |bzip2 > grubby-%{version}.tar.bz2
Source0: %{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig glib2-devel popt-devel 
BuildRequires: libblkid-devel
# for make test / getopt:
BuildRequires: util-linux-ng
%ifarch %{arm}
Requires: uboot-tools
%endif

%description
grubby  is  a command line tool for updating and displaying information about 
the configuration files for the grub, lilo, elilo (ia64),  yaboot (powerpc)  
and zipl (s390) boot loaders. It is primarily designed to be used from scripts
which install new kernels and need to find information about the current boot 
environment.

%prep
%setup -q

%build
make %{?_smp_mflags}

%check
make test

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} mandir=%{_mandir}
%ifarch %{arm}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
install -p uboot %{buildroot}%{_sysconfdir}/sysconfig/uboot
%endif

%files
%doc COPYING
/sbin/installkernel
/sbin/new-kernel-pkg
/sbin/grubby
%{_mandir}/man8/*.8*
%ifarch %{arm}
%config(noreplace) %{_sysconfdir}/sysconfig/uboot
%endif
