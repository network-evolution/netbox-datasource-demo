from extras.scripts import Script, ObjectVar, ChoiceVar
from dcim.models import Device, DeviceType


class ApplyDeviceStatusByType(Script):

    class Meta:
        name = "Apply Device Status by Device Type"
        description = "Uses NetBox default device status choices"

    device_type = ObjectVar(
        model=DeviceType,
        description="Select device type"
    )

    status = ChoiceVar(
        description="Select target device status",
        choices=Device._meta.get_field("status").choices
    )

    def run(self, data, commit):

        devices = Device.objects.filter(device_type=data["device_type"])

        if not devices.exists():
            self.log_info("No devices found for the selected device type")
            return

        for device in devices:
            old_status = device.status
            device.status = data["status"]
            device.save()
            self.log_success(f"{device.name}: {old_status} → {device.status}")