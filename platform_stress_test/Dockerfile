FROM centos:latest as builder

RUN yum install git -y
RUN yum install clang -y
RUN dnf install dnf-plugins-core -y
RUN dnf copr enable vbatts/bazel -y
RUN dnf install bazel4 -y
RUN dnf --enablerepo=powertools install glibc-static -y
RUN dnf --enablerepo=powertools install libstdc++-static -y

RUN git clone https://github.com/google/platform_benchmarks.git
RUN cd platform_benchmarks/ && CC=/usr/bin/clang bazel build \
	--linkopt=-static -c dbg //third_party/platform_benchmarks/cputest:cputest

CMD platform_benchmarks/bazel-bin/third_party/platform_benchmarks/cputest/cputest --branch_history 100

