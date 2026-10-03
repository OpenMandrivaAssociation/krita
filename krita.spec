%define _python_bytecompile_errors_terminate_build 0
#define git 20260109

%define stable %([ -n "%{?beta:%{beta}}" ] && echo -n un; echo -n stable)
# See rpmlintrc for reason
%define __requires_exclude 'devel.*'
#define _disable_lto 1

# Vision ML tools (segment/background-removal/inpaint) via system vision.cpp
%bcond_without visiontools

Name: krita
Version: 6.0.4%{?git:~%{git}}
Release: 2
%if 0%{?git:1}
Source0: https://invent.kde.org/graphics/krita/-/archive/%{?git:master/krita-master}%{!?git:v%{version}/krita-v%{version}}.tar.bz2%{?git:#/%{name}-%{git}.tar.gz}
%else
# Official tarball is not on download.kde.org yet; use the tagged git archive.
Source0: https://invent.kde.org/graphics/krita/-/archive/v%{version}/krita-v%{version}.tar.bz2
%endif
%if %{with visiontools}
# Successor of krita-ai-tools; native plugin loaded via a small Python wrapper
Source2: https://github.com/Acly/krita-vision-tools/archive/refs/tags/v3.0.0.tar.gz#/krita-vision-tools-3.0.0.tar.gz
Source9: krita-vision-tools.kritarc
%endif
Source1000: %{name}.rpmlintrc
#ifarch %{arm} %{armx}
#Patch0:	krita-4.4.2-OpenMandriva-fix-build-with-OpenGLES-aarch64-and-armvhnl.patch
#endif
#Patch1: krita-5.2.3-xsimd-compile.patch
# Fix build with SSE
#Patch2: krita-4.4.8-sse-compile.patch
Patch3: krita-5.0.0-fix-libatomic-linkage.patch
# And make it compile
#Patch4: krita-dont-hardcode-ancient-sip-abi.patch
# This is needed because discover (as of 5.27.6) barfs on tags inside <caption>
# It should be removed if and when discover can deal with links inside caption.
#Patch6: metadata-no-links.patch
%if %{with visiontools}
# Use system libvisioncpp; install as a distro Python plugin
Patch7: krita-vision-tools-offline-system-build.patch
# Find the plugin in system pykrita and models in /usr/share/visioncpp
Patch8: krita-vision-tools-find-system-plugin.patch
%endif
Patch9: krita-5.2.9-open-avif-through-qimageio.patch

Patch12:	krita-6.0-fix-underlinking.patch
# Qt 6.12 removed QTEST_DISABLE_KEYPAD_NAVIGATION with keypad navigation.
Patch13:	krita-6.0.4-qt612-no-keypad-navigation.patch
# Qt 6.12 uic rejects a widget class name with a leading space.
Patch14:	krita-6.0.4-qt612-uic-class-name.patch

Summary: Sketching and painting program
URL: https://krita.org/
License: GPL
Group: Graphics
BuildRequires: cmake(Qt6Multimedia)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6PrintSupport)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6SvgWidgets)
BuildRequires: cmake(Qt6Sql)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6LinguistTools)
BuildRequires: cmake(Qt6QuickControls2)
BuildRequires: cmake(ECM)
BuildRequires: cmake(KF6Archive)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KF6Completion)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6GuiAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6ItemModels)
BuildRequires: cmake(KF6ItemViews)
BuildRequires: cmake(KF6WindowSystem)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6Crash)
BuildRequires: cmake(KDcrawQt6)
BuildRequires: cmake(Mlt7)
BuildRequires: cmake(SDL2)
BuildRequires: pkgconfig(mlt-framework-7)
BuildRequires: pkgconfig(mlt++-7)
BuildRequires: pkgconfig(libwebp)
#BuildRequires: cmake(KSeExpr)
# FIXME figure out why -- doesn't look like anything is
# actually insane enough to link libjpeg statically
BuildRequires: jpeg-static-devel
BuildRequires: cmake(QuaZip-Qt6)
# x86 package
%ifarch %{ix86} %{x86_64}
BuildRequires: cmake(Vc)
%endif
BuildRequires: cmake(Immer)
BuildRequires: %mklibname -d zug
BuildRequires: %mklibname -d lager
BuildRequires: cmake(xsimd)
BuildRequires: boost-devel
BuildRequires: boost-system-devel
BuildRequires: pkgconfig(libunibreak)
BuildRequires: %{_lib}atomic-devel
BuildRequires: pkgconfig(python)
BuildRequires: pkgconfig(eigen3)
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(fftw3)
BuildRequires: pkgconfig(gsl)
BuildRequires: pkgconfig(lcms2)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libjxl)
BuildRequires: pkgconfig(libopenjp2)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(libraw)
BuildRequires: pkgconfig(libraw_r)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(fribidi)
BuildRequires: pkgconfig(shared-mime-info)
BuildRequires: pkgconfig(OpenColorIO) >= 2
BuildRequires: pkgconfig(poppler-qt6)
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libmypaint)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: atomic-devel
# Optional -- for EXR file format support
BuildRequires: pkgconfig(OpenEXR) >= 3.0.0
BuildRequires: pkgconfig(gsl)
BuildRequires: giflib-devel
BuildRequires: python-qt6-devel
BuildRequires: python-qt6-core
BuildRequires: python-qt6-gui
BuildRequires: python-qt6-widgets
BuildRequires: python-qt6-xml
BuildRequires: python-sip
%if %{with visiontools}
BuildRequires: cmake(visioncpp)
# Plugin is a subpackage so a plain krita install need not pull ~160 MB of ML bits
Recommends: %{name}-vision-tools
%endif
Requires: qt6-qtbase-sql-sqlite
Requires: python-qt6-core
Requires: python-qt6-gui
Requires: python-qt6-widgets
Requires: python-qt6-xml

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

%if %{with visiontools}
%package vision-tools
Summary:	ML selection, background-removal and inpaint tools for Krita
Group:		Graphics
Requires:	%{name} = %{EVRD}
Requires:	%mklibname visioncpp
Recommends:	vision.cpp-models

%description vision-tools
Krita Vision Tools (krita-vision-tools) — click-to-select, box select,
background removal and smart patch. Built inside the Krita tree (it uses
private Krita headers and cmake macros, so it is not a standalone package).

Needs libvisioncpp. Default GGUF weights come from vision.cpp-models
(~120 MB); you can omit that package and drop your own .gguf files into
%{_datadir}/visioncpp/ or ~/.local/share/krita/pykrita/vision_tools/models/.
%endif

%prep
%setup -q -n %{name}-%{?git:master}%{!?git:v%{version}%{?beta:%{beta}}}
%if %{with visiontools}
cd plugins
tar xf %{S:2}
mv krita-vision-tools-* krita-vision-tools
echo 'add_subdirectory(krita-vision-tools)' >>CMakeLists.txt
cd ../
%endif
%autopatch -p1

%cmake \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DALLOW_UNSTABLE=QT6 \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DUSE_QT_XCB:BOOL=TRUE \
	-DENABLE_BSYMBOLICFUNCTIONS:BOOL=TRUE \
	-DPC_xsimd_CONFIG_DIR=%{_libdir}/cmake/xsimd \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# We get those from breeze...
rm -f %{buildroot}%{_datadir}/color-schemes/Breeze*.colors
# Currently nothing uses Krita headers, so we don't need them
rm -rf %{buildroot}%{_includedir}
# This isn't an AppImage, so we don't need the update dummy
rm -f %{buildroot}%{_bindir}/AppImageUpdateDummy
%if %{with visiontools}
# Enable the vision-tools Python loader by default (user kritarc still wins)
install -D -m 644 %{S:9} %{buildroot}%{_sysconfdir}/xdg/kritarc
%endif

%find_lang krita || touch krita.lang

%files -f krita.lang
%{_bindir}/krita
%{_bindir}/kritarunner
%{_bindir}/krita_version
%{_datadir}/metainfo/org.kde.krita.appdata.xml
%{_datadir}/applications/*
%{_libdir}/libkrita*.so*
%{_libdir}/krita-python-libs/
%dir %{_libdir}/kritaplugins
%{_libdir}/kritaplugins/*.so
%{_iconsdir}/hicolor/*x*/apps/krita.png
%{_iconsdir}/hicolor/scalable/apps/krita.svgz
%{_datadir}/icons/*/*/*/application-x-krita.*
%{_datadir}/%{name}
%{_datadir}/kritaplugins
%{_datadir}/color/icc/krita
%{_datadir}/color-schemes/Krita*.colors
%{_qtdir}/qml/org/krita/components
%if %{with visiontools}
%exclude %{_datadir}/krita/pykrita/vision_tools
%exclude %{_datadir}/krita/pykrita/vision_tools.desktop

%files vision-tools
%{_datadir}/krita/pykrita/vision_tools.desktop
%{_datadir}/krita/pykrita/vision_tools/
%config(noreplace) %{_sysconfdir}/xdg/kritarc
%endif
