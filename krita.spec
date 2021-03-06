%define _python_bytecompile_errors_terminate_build 0

%define stable %([ -n "%{?beta:%{beta}}" ] && echo -n un; echo -n stable)
# See rpmlintrc for reason
%define __requires_exclude 'devel.*'
%define _disable_lto 1

Name: krita
# Needs to match/outnumber calligra
Epoch: 16
Version: 4.4.5
Release: 1
Source0: http://download.kde.org/stable/krita/%(echo %{version} |cut -d. -f1-3)/%{name}-%{version}%{?beta:%{beta}}.tar.xz
Source1000: %{name}.rpmlintrc
#ifarch %{arm} %{armx}
#Patch0:	krita-4.4.2-OpenMandriva-fix-build-with-OpenGLES-aarch64-and-armvhnl.patch
#endif
Patch0:	krita-4.4.3-find-quazip-1.1.patch
Patch1: krita-4.4.3-libstdc++-11.patch
Summary: Sketching and painting program
URL: http://krita.org/
License: GPL
Group: Graphics
BuildRequires: cmake(Qt5Multimedia)
BuildRequires: cmake(Qt5Concurrent)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Network)
BuildRequires: cmake(Qt5PrintSupport)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5QuickWidgets)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5X11Extras)
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
BuildRequires: cmake(QuaZip-Qt5)
# x86 package
%ifarch %{ix86} %{x86_64}
BuildRequires: cmake(Vc)
%endif
BuildRequires: boost-devel
BuildRequires: pkgconfig(python3)
BuildRequires: pkgconfig(eigen3)
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(fftw3)
BuildRequires: pkgconfig(gsl)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libraw)
BuildRequires: pkgconfig(libraw_r)
BuildRequires: pkgconfig(shared-mime-info)
%ifnarch %{armx}
BuildRequires: pkgconfig(OpenColorIO)
%endif
BuildRequires: pkgconfig(poppler-qt5)
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(zlib)
BuildRequires: gmic-devel
BuildRequires: atomic-devel
# Optional -- for EXR file format support
BuildRequires: pkgconfig(IlmBase)
BuildRequires: pkgconfig(OpenEXR)
BuildRequires: pkgconfig(gsl)
BuildRequires: giflib-devel
BuildRequires: python-qt5-devel
BuildRequires: python-qt5-core
BuildRequires: python-qt5-gui
BuildRequires: python-qt5-widgets
BuildRequires: python-qt5-xml
BuildRequires: python-sip
Requires: python-qt5-xml

# Those used to be separate libpackages in 2.x, but it didn't make much
# sense, nothing outside of krita uses those libraries (and nothing can,
# they don't come with headers...)
Obsoletes: calligra-krita < %{EVRD}
Obsoletes: %{_lib}kritacolord < %{EVRD}
Obsoletes: %{_lib}kritacolor14 < %{EVRD}
Obsoletes: %{_lib}kritalibpaintop14 < %{EVRD}
Obsoletes: %{_lib}kritaui14 < %{EVRD}

%define langlist af ar ast be bg br bs ca cs cy da de el en_GB eo es et eu fa fi fr fy ga gl he hi hne hr hu ia is it ja kk km ko lt lv mai mk mr ms nb nds ne nl nn oc pa pl pt pt_BR ro ru se sk sl sq sv ta tg th tr ug uk uz vi wa xh zh_CN zh_TW

%{expand:%(for lang in %langlist; do echo "Obsoletes:	krita-l10n-$lang"; done)}

%description
Krita offers an end–to–end solution for creating digital painting files
from scratch by masters. It supports concept art, creation of comics
and textures for rendering.

%prep
%autosetup -p1 -n %{name}-%{version}%{?beta:%{beta}}

# We need to use the system version
rm cmake/modules/FindQuaZip.cmake

# As of Krita 4.3.0 and boost 1.73, krita failed to build due error: 
# /usr/include/boost/geometry/index/detail/rtree/node/variant_visitor.hpp:51:5: error: no matching function for call to 'apply_visitor'
# boost::apply_visitor(v, n);
# Looks like krita want to build with c++11 and this cause issue, to fix we need force c++14 here (angry)
# Fix stolen from https://bugs.gentoo.org/728744
sed -e "/CMAKE_CXX_STANDARD/s/11/14/" -i CMakeLists.txt || die

%cmake_kde5 \
	-DUSE_QT_XCB:BOOL=TRUE \
	-G Ninja

%build
%ifarch %{arm} %{armx}
export CXXFLAGS="%{optflags} -DHAS_ONLY_OPENGL_ES"
%endif
%ninja -C build -w dupbuild=warn

%install
%ninja_install -C build -w dupbuild=warn
# We get those from breeze...
rm -f %{buildroot}%{_datadir}/color-schemes/Breeze*.colors

%find_lang krita || touch krita.lang

%files -f krita.lang
%config %{_sysconfdir}/xdg/kritarc
%{_bindir}/krita
%{_bindir}/krita_version
%{_datadir}/metainfo/org.kde.krita.appdata.xml
%{_datadir}/applications/*
%{_libdir}/libkrita*.so*
%dir %{_libdir}/kritaplugins
%{_libdir}/kritaplugins/*.so
%{_libdir}/qt5/qml/org/krita
%{_iconsdir}/hicolor/*x*/apps/krita.png
%{_iconsdir}/hicolor/scalable/apps/krita.svgz
%{_datadir}/icons/*/*/*/application-x-krita.*
%{_datadir}/%{name}
%{_datadir}/kritaplugins
%{_datadir}/color/icc/krita
%{_datadir}/color-schemes/Krita*.colors
