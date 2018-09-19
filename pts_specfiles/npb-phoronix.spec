Name:           npb-phoronix
License:        BSD-3-Clause BSL-1.0
Version:        1.0.0
Release:        1
Summary:        NPB benchmark
Source0:        http://www.phoronix-test-suite.com/benchmark-files/NPB3.3.tar.gz
Source1:        https://raw.githubusercontent.com/phoronix-test-suite/test-profiles/master/pts/npb-1.2.4/install.sh
Source2:        https://raw.githubusercontent.com/phoronix-test-suite/test-profiles/master/pts/npb-1.2.4/results-definition.xml
Source3:        https://raw.githubusercontent.com/phoronix-test-suite/test-profiles/master/pts/npb-1.2.4/test-definition.xml

BuildRequires:  gcc
BuildRequires:  gcc-dev
BuildRequires:  gcc-dev32
BuildRequires:  gcc-libgcc32
BuildRequires:  gcc-libstdc++32
BuildRequires:  openmpi-dev
BuildRequires:  openmpi


Requires: openmpi

%description
NPB, NAS Parallel Benchmarks, is a benchmark developed by NASA for high-end
computer systems. This test profile currently uses the MPI version of NPB.

%prep

%build
export LANG=C
mkdir -p %{buildroot}/var/lib/phoronix-test-suite/test-profiles/pts/npb-1.2.4/
cp %{SOURCE1} %{buildroot}/var/lib/phoronix-test-suite/test-profiles/pts/npb-1.2.4/
cp %{SOURCE2} %{buildroot}/var/lib/phoronix-test-suite/test-profiles/pts/npb-1.2.4/
cp %{SOURCE3} %{buildroot}/var/lib/phoronix-test-suite/test-profiles/pts/npb-1.2.4/

mkdir -p %{buildroot}/var/lib/phoronix-test-suite/installed-tests/pts/npb-1.2.4/
cp %{SOURCE0} %{buildroot}/var/lib/phoronix-test-suite/installed-tests/pts/npb-1.2.4/
cp %{SOURCE1} %{buildroot}/var/lib/phoronix-test-suite/installed-tests/pts/npb-1.2.4/
pushd %{buildroot}/var/lib/phoronix-test-suite/installed-tests/pts/npb-1.2.4/
sed -i 's+~+.+g' install.sh
bash install.sh

popd

%install
#pushd %{buildroot}/usr/include/python3.7m
#cat %{SOURCE1} | patch -p0

%files
