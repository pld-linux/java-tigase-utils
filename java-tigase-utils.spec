#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
%bcond_without	source		# don't build source jar
%bcond_with	tests		# build and run tests

%include	/usr/lib/rpm/macros.java

%define		srcname		tigase-utils
%define		build_id	623
Summary:	Tigase utility classes
Name:		java-tigase-utils
Version:	3.2.0
Release:	1
License:	GPL v3
Group:		Libraries/Java
Source0:	https://projects.tigase.org/attachments/download/18/%{srcname}-%{version}-b%{build_id}.src.tar.gz
# Source0-md5:	157a60680810282a5829b51626371bdb
URL:		https://projects.tigase.org/projects/tigase-utils/
%{?with_tests:BuildRequires:	ant-junit}
BuildRequires:	java-tigase-xmltools
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.555
BuildRequires:	sed >= 4.0
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
All utility code used in other Tigase projects.

%package javadoc
Summary:	Online manual for %{srcname}
Summary(pl.UTF-8):	Dokumentacja online do %{srcname}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Documentation for %{srcname}.

%description javadoc -l pl.UTF-8
Dokumentacja do %{srcname}.

%description javadoc -l fr.UTF-8
Javadoc pour %{srcname}.

%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}-b%{build_id}.src

%build
export JAVA_HOME="%{java_home}"

required_jars="%{?with_tests:junit} tigase-xmltools"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%ant prepare-dist jar-dist

%if %{with tests}
%ant run-unittests
%endif

%if %{with javadoc}
%ant docs
%endif

%if %{with source}
cd src
%jar cf ../%{srcname}.src.jar $(find -name '*.java')
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a jars/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a docs-%{srcname}/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# source
%if %{with source}
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{srcname}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%if %{with source}
%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
%endif
