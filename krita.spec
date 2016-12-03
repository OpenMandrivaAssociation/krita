%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
# See rpmlintrc for reason
%define __noautoreq 'devel.*'
%define _disable_lto 1

Name: krita
# Needs to match/outnumber calligra
Epoch: 16
Version: 3.0.1.1
Release: 1
Source0: http://files.kde.org/krita/%(echo %{version} |cut -d. -f1)/source/%{name}-%{version}.tar.gz
Source1000: %{name}.rpmlintrc
# Based on https://phabricator.kde.org/file/data/vdjjpfxia6f6ubclybqo/PHID-FILE-k7rnmfu4xctfe6jzrsas/D1327.diff
#Patch0: krita-2.99.90-vc-1.2.0.patch
Summary: Sketching and painting program
URL: http://krita.org/
License: GPL
Group: Graphics
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5PrintSupport)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF5Archive)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5WidgetsAddons)
BuildRequires: cmake(KF5Completion)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5GuiAddons)
BuildRequires: cmake(KF5I18n)
BuildRequires: cmake(KF5ItemModels)
BuildRequires: cmake(KF5ItemViews)
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(KF5KIO)
BuildRequires: cmake(KF5Crash)
BuildRequires: cmake(Gettext)
BuildRequires: cmake(PythonInterp)
# x86 package
%ifarch %{ix86} x86_64
BuildRequires: cmake(Vc)
%endif
BuildRequires: boost-devel
BuildRequires: pkgconfig(eigen3)
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(fftw3)
BuildRequires: pkgconfig(gsl)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(xi)
BuildRequires: jpeg-devel
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libraw)
BuildRequires: pkgconfig(libraw_r)
BuildRequires: pkgconfig(shared-mime-info)
BuildRequires: pkgconfig(OpenColorIO)
BuildRequires: pkgconfig(poppler-qt5)
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(zlib)
BuildRequires: gcc gcc-c++
BuildRequires: gomp-devel
# Optional -- for EXR file format support
BuildRequires: pkgconfig(IlmBase)
BuildRequires: pkgconfig(OpenEXR)

# Those used to be separate libpackages in 2.x, but it didn't make much
# sense, nothing outside of krita uses those libraries (and nothing can,
# they don't come with headers...)
Obsoletes: calligra-krita < %{EVRD}
Obsoletes: %{_lib}kritacolord < %{EVRD}
Obsoletes: %{_lib}kritacolor14 < %{EVRD}
Obsoletes: %{_lib}kritalibpaintop14 < %{EVRD}
Obsoletes: %{_lib}kritaui14 < %{EVRD}

%description
Krita offers an end–to–end solution for creating digital painting files
from scratch by masters. It supports concept art, creation of comics
and textures for rendering.

%prep
%setup -q
%apply_patches
# gcc currently gives us better performance with Krita
# because Krita uses OpenMP gcc-isms
export CC=gcc
export CXX=g++

%cmake_kde5 \
	-G Ninja

%build
%ninja -C build

%install
%ninja_install -C build
# We get those from breeze...
rm -f %{buildroot}%{_datadir}/color-schemes/Breeze*.colors

%find_lang krita || touch krita.lang

%files -f krita.lang
%config %{_sysconfdir}/xdg/kritarc
%{_bindir}/krita
%{_bindir}/gmicparser
%{_datadir}/metainfo/org.kde.krita.appdata.xml
%{_datadir}/applications/*
%{_libdir}/libkrita*.so*
%dir %{_libdir}/kritaplugins
%{_libdir}/kritaplugins/*.so
%{_datadir}/icons/*/*/*/calligrakrita.*
%{_datadir}/%{name}
%{_datadir}/kritaplugins
%{_datadir}/color/icc/krita
%{_datadir}/color-schemes/Krita*.colors
