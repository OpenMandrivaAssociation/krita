%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
# See rpmlintrc for reason
%define __noautoreq 'devel.*'

Name: krita
Version: 2.99.89
Release: 1
Source0: http://download.kde.org/%{stable}/%{name}/%{version}/%{name}-%{version}.tar.xz
Source1000: %{name}.rpmlintrc
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
# x86_64 package
%ifarch x86_64
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
Obsoletes: %{_lib}kritacolord < %{EVRD}
Obsoletes: %{_lib}kritacolor14 < %{EVRD}

%description
Krita offers an end–to–end solution for creating digital painting files
from scratch by masters. It supports concept art, creation of comics
and textures for rendering.

%prep
%setup -q
# gcc currently gives us better performance with Krita
# because Krita uses OpenMP gcc-isms
export CC=gcc
export CXX=g++

%cmake_kde5 -G Ninja

%build
%ninja -C build

%install
%ninja_install -C build

%files
%config %{_sysconfdir}/xdg/kritarc
%config %{_sysconfdir}/xdg/kritasketchrc
%config %{_sysconfdir}/xdg/kritasketchpanelsrc
%{_bindir}/krita
%{_bindir}/gmicparser
%{_bindir}/kritasketch
%{_datadir}/appdata/krita.appdata.xml
%{_datadir}/applications/*
%{_libdir}/libkrita*.so*
%dir %{_libdir}/kritaplugins
%{_libdir}/kritaplugins/*.so
%{_libdir}/qt5/qml/org/krita
%{_datadir}/icons/*/*/*/calligrakrita.*
%{_datadir}/icons/*/*/*/kritasketch.*
%{_datadir}/%{name}
%{_datadir}/kritagemini
%{_datadir}/kritaplugins
%{_datadir}/kritaanimation
%{_datadir}/kritasketch
%{_datadir}/color/icc/krita
%{_datadir}/color-schemes/Krita*.colors
%{_datadir}/mime/packages/*.xml
