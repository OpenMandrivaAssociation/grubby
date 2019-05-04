Name: grubby
Version: 8.40
Release: 30%{?dist}
Summary: Command line tool for updating bootloader configs
License: GPLv2+
URL: https://github.com/rhinstaller/grubby
# we only pull git snaps at the moment
# git clone git@github.com:rhinstaller/grubby.git
# git archive --format=tar --prefix=grubby-%%{version}/ HEAD |bzip2 > grubby-%%{version}.tar.bz2
# Source0: %%{name}-%%{version}.tar.bz2
Source0: https://github.com/rhboot/grubby/archive/%{version}-1.tar.gz
Source1: grubby-bls
Source2: grubby.in
Source3: installkernel.in
Source4: installkernel-bls
Patch0001: 0001-remove-the-old-crufty-u-boot-support.patch
Patch0002: 0002-Change-return-type-in-getRootSpecifier.patch
Patch0003: 0003-Add-btrfs-subvolume-support-for-grub2.patch
Patch0004: 0004-Add-tests-for-btrfs-support.patch
Patch0005: 0005-Use-system-LDFLAGS.patch
Patch0006: 0006-Honor-sbindir.patch
Patch0007: 0007-Make-installkernel-to-use-kernel-install-scripts-on-.patch
Patch0008: 0008-Add-usr-libexec-rpm-sort.patch
Patch0009: 0009-Improve-man-page-for-info-option.patch
Patch0010: 0010-Fix-GCC-warnings-about-possible-string-truncations-a.patch

BuildRequires: popt-devel 
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(blkid) git-core
# for make test / getopt:
BuildRequires: util-linux
BuildRequires: rpm-devel
%ifarch aarch64 i686 znver1 x86_64 %{power64}
BuildRequires: grub2-tools
Requires: grub2-tools
%endif
%ifarch s390 s390x
Requires: s390utils-base
%endif
Requires: findutils

Obsoletes:	%{name}-bls

%description
This package provides a grubby compatibility script that manages
BootLoaderSpec files and is meant to only be used for legacy compatibility
users with existing grubby users.

%prep
%setup -q -n grubby-%{version}-1

git init
git config user.email "noone@example.com"
git config user.name "no one"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
%set_build_flags
make %{?_smp_mflags} LDFLAGS="${LDFLAGS}"

%ifnarch aarch64 %{arm}
%check
make test
%endif

%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir} sbindir=%{_sbindir} libexecdir=%{_libexecdir}

mkdir -p %{buildroot}%{_libexecdir}/{grubby,installkernel}/ %{buildroot}%{_sbindir}/
mv -v %{buildroot}%{_sbindir}/grubby %{buildroot}%{_libexecdir}/grubby/grubby
mv -v %{buildroot}%{_sbindir}/installkernel %{buildroot}%{_libexecdir}/installkernel/installkernel
cp -v %{SOURCE1} %{buildroot}%{_libexecdir}/grubby/
cp -v %{SOURCE4} %{buildroot}%{_libexecdir}/installkernel/
sed -e "s,@@LIBEXECDIR@@,%{_libexecdir}/grubby,g" %{SOURCE2} \
	> %{buildroot}%{_sbindir}/grubby
sed -e "s,@@LIBEXECDIR@@,%{_libexecdir}/installkernel,g" %{SOURCE3} \
	> %{buildroot}%{_sbindir}/installkernel

%post
if [ "$1" = 2 ]; then
    arch=$(uname -m)
    [[ $arch == "s390x" ]] && \
    zipl-switch-to-blscfg --backup-suffix=.rpmsave &>/dev/null || :
fi

%package deprecated
Summary:	Legacy command line tool for updating bootloader configs
Conflicts:	%{name} <= 8.40-18

%description deprecated
This package provides deprecated, legacy grubby.  This is for temporary
compatibility only.

grubby is a command line tool for updating and displaying information about
the configuration files for the grub, lilo, elilo (ia64), yaboot (powerpc)
and zipl (s390) boot loaders. It is primarily designed to be used from
scripts which install new kernels and need to find information about the
current boot environment.

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_libexecdir}/grubby
%dir %{_libexecdir}/installkernel
%attr(0755,root,root) %{_libexecdir}/grubby/grubby-bls
%attr(0755,root,root) %{_libexecdir}/grubby/rpm-sort
%attr(0755,root,root) %{_sbindir}/grubby
%attr(0755,root,root) %{_libexecdir}/installkernel/installkernel-bls
%attr(0755,root,root) %{_sbindir}/installkernel
%{_mandir}/man8/[gi]*.8*

%files deprecated
%{!?_licensedir:%global license %%doc}
%license COPYING
%dir %{_libexecdir}/grubby
%dir %{_libexecdir}/installkernel
%attr(0755,root,root) %{_libexecdir}/grubby/grubby
%attr(0755,root,root) %{_libexecdir}/installkernel/installkernel
%attr(0755,root,root) %{_sbindir}/grubby
%attr(0755,root,root) %{_sbindir}/installkernel
%attr(0755,root,root) %{_sbindir}/new-kernel-pkg
 %{_mandir}/man8/*.8*
