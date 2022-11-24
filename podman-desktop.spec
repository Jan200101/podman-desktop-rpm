%global debug_package %{nil}

%global pkg_name Podman-Desktop

#%%global nodejs_includedir %%{_includedir}/electron

#%%global electron_req_version 17.3.1
#%%global electron_includedir %%{_includedir}/electron

%global _optpkgdir /opt/%{pkg_name}

Name: podman-desktop
Version: 0.9.1
Release: 0
Summary: Podman Desktop
License: ASL 2.0
URL: https://github.com/containers/%{name}
Source0: %{url}/archive/v%{version}.tar.gz
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
%autosetup -Sgit -n %{name}-%{version}

%build
yarn install
sed -i "/target: \['flatpak'/d" .electron-builder.config.js

sed -i "s/cross-env\ /node_modules\/.bin\/cross-env\ /g" package.json
sed -i "s/vite build/..\/..\/node_modules\/.bin\/vite build/" package.json
sed -i "s/vite \-c/node_modules\/.bin\/vite \-c/" package.json

sed -i "s/rollup\ /..\/..\/node_modules\/.bin\/rollup\ /g" extensions/crc/package.json

sed -i "s/rollup\ /..\/..\/node_modules\/.bin\/rollup\ /g" extensions/podman/package.json
sed -i "s/ts-node\ /..\/..\/node_modules\/.bin\/ts-node\ /g" extensions/podman/package.json

sed -i "s/rollup\ /..\/..\/node_modules\/.bin\/rollup\ /g" extensions/kube-context/package.json

sed -i "s/electron-builder\ /node_modules\/.bin\/electron-builder\ /g" package.json
yarn compile:current

rm -f dist/linux-unpacked/resources/app.asar.unpacked/node_modules/ssh2/lib/protocol/crypto/build/node_gyp_bins/python3
rm -f dist/linux-unpacked/resources/app.asar.unpacked/node_modules/cpu-features/build/node_gyp_bins/python3

%install
install -dp %{buildroot}%{_optpkgdir}
cp -Rp dist/linux-unpacked/* %{buildroot}%{_optpkgdir}

install -dp %{buildroot}%{_bindir}
ln -s %{_optpkgdir}/%{name} %{buildroot}%{_bindir}/%{name}

%files
%dir %{_optpkgdir}
%{_optpkgdir}/*
%{_bindir}/%{name}

%changelog
