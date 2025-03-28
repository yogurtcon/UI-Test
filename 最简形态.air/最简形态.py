from airtest.core.api import sleep, touch, connect_device
dev=connect_device("android:///")

sleep(0.5)
touch([1,1])