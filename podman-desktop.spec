%global pkg_name Podman-Desktop
%global _optpkgdir /opt/%{pkg_name}
%global _icondir %{_datadir}/icons/hicolor/512x512/apps
%global debug_package %{nil}

Name: podman-desktop
Version: 1.3.1
Release: 0%{?dist}
Summary: Podman Desktop
License: ASL 2.0
URL: https://github.com/containers/%{name}
Source0: %{url}/archive/v%{version}.tar.gz
Source1: %{name}.desktop
BuildRequires: python3-devel
BuildRequires: gcc-c++
BuildRequires: git-core
BuildRequires: make
BuildRequires: npm
BuildRequires: yarnpkg
BuildRequires: libglvnd-devel
Requires: vulkan-loader
Requires: python3
ExclusiveArch: x86_64

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}

%build
sed -i "/target: \['flatpak'/d" .electron-builder.config.cjs

yarn install
yarn compile:current

rm -f dist/linux-unpacked/resources/app.asar.unpacked/node_modules/ssh2/lib/protocol/crypto/build/node_gyp_bins/python3
rm -f dist/linux-unpacked/resources/app.asar.unpacked/node_modules/cpu-features/build/node_gyp_bins/python3

%install
# install everything to /opt/%%{pkg_name}
install -dp %{buildroot}%{_optpkgdir}
cp -Rp dist/linux-unpacked/* %{buildroot}%{_optpkgdir}

# install icon
install -dp %{buildroot}%{_icondir}
install -Dp -m0755 buildResources/icon-512x512.png %{buildroot}%{_icondir}/%{name}.png

# install desktop file
install -dp %{buildroot}%{_datadir}/applications
install -Dp -m0755 %{SOURCE1} %{buildroot}%{_datadir}/applications

# symlink main binary to /usr/bin
install -dp %{buildroot}%{_bindir}
ln -s %{_optpkgdir}/%{name} %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc CODE-OF-CONDUCT.md CONTRIBUTING.md README.md SECURITY.md
%{_bindir}/%{name}
%dir %{_optpkgdir}
%{_optpkgdir}/*
%dir %{_icondir}
%{_icondir}/%{name}.png
%dir %{_datadir}/applications
%{_datadir}/applications/%{name}.desktop

%changelog
