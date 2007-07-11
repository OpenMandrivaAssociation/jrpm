%define section         free
%define gcj_support     1

Name:           jrpm
Version:        0.9
Release:        %mkrel 1.1.1
Epoch:          0
Summary:        Java library to manipulate and create RPM archives
License:        Apache License
Group:          Development/Java
URL:            http://jrpm.sourceforge.net/
Source0:        http://umn.dl.sourceforge.net/sourceforge/jrpm/jrpm-%{version}-src.tar.gz
Source1:        %{name}.script
Source2:        %{name}.desktop
Source3:        %{name}.applications
Source4:        %{name}-16x16.png
Source5:        %{name}-32x32.png
Source6:        %{name}-64x64.png
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:       java
Requires:       jpackage-utils >= 0:1.6
BuildRequires:  ant
BuildRequires:  desktop-file-utils
BuildRequires:  jpackage-utils >= 0:1.6
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
jRPM is a Java version of RPM. It includes a packager as well as a
deployment environment that will not only allow deployment like the
normal rpm (unix + sleepycat db), but it is also designed to support
deployment on all Java-enabled platforms.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}-src
%{__perl} -pi -e 's|<javac|<javac nowarn="true"|g' build.xml
%{_bindir}/find . -type d -name .svn | %{_bindir}/xargs %{__rm} -r
%{_bindir}/find . -type f -name '*.jar' | %{_bindir}/xargs %{__rm}
%{_bindir}/find . -type f -name '*.rpm' -o -name '*.hdr' | %{_bindir}/xargs %{__rm}

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} jar javadocs

%install
%{__rm} -rf %{buildroot}

%{__mkdir_p} %{buildroot}%{_javadir}
%{__cp} -a _build/%{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

%{__mkdir_p} %{buildroot}%{_bindir}
%{__perl} -pe 's|/usr/lib|%{_libdir}|g;s|/usr/share|%{_datadir}|g' %{SOURCE1} > %{buildroot}%{_bindir}/%{name}

%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a _build/javadocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%{__mkdir_p} %{buildroot}%{_datadir}/pixmaps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_datadir}/pixmaps/%{name}.png
%{__install} -m 644 %{SOURCE4} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__install} -m 644 %{SOURCE5} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__install} -m 644 %{SOURCE6} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%{__mkdir_p} %{buildroot}%{_datadir}/applications
%{_bindir}/desktop-file-install --vendor mandriva                     \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications               \
        --remove-category Application                                 \
        --add-category X-MandrivaLinux-System-Configuration-Packaging \
        %{SOURCE2}

%{__mkdir_p} %{buildroot}%{_datadir}/application-registry
%{__install} -m 644 %{SOURCE3} %{buildroot}%{_datadir}/application-registry

%{__perl} -pi -e 's/\r$//g' changelog.txt

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
%{update_desktop_database}
%{update_mime_database}
%update_icon_cache hicolor

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_desktop_database}
%{clean_mime_database}
%clean_icon_cache hicolor

%files
%defattr(0644,root,root,0755)
%doc changelog.txt LICENSE.txt readme.txt
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif
%{_datadir}/applications/*-%{name}.desktop
%{_datadir}/application-registry/%{name}.applications
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
