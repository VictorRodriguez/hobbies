source openrc
wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
qemu-img convert -f qcow2 -O raw cirros-0.3.4-x86_64-disk.img cirros-0.3.4-x86_64-disk.raw
openstack image create --public --disk-format raw --file ./cirros-0.3.4-x86_64-disk.raw cirros-cloud
