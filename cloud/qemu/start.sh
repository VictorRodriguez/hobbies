qemu-system-x86_64 \
    -enable-kvm \
    -smp sockets=1,cpus=4,cores=2 -cpu host \
    -m 1024 \
    -vga none -nographic \
    -hda CentOS-7-x86_64-GenericCloud.qcow2 \
    -netdev user,id=mynet0,hostfwd=tcp::${VMN}0022-:22,hostfwd=tcp::${VMN}2375-:2375 \
    -device virtio-net-pci,netdev=mynet0 \
    -device virtio-rng-pci \
    -debugcon file:debug.log -global isa-debugcon.iobase=0x402 $@
