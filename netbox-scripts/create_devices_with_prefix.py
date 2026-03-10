from extras.scripts import Script, ObjectVar, IntegerVar, StringVar
from dcim.models import Device, DeviceRole, DeviceType, Site


class BulkCreateDevicesWithPrefix(Script):

    class Meta:
        name = "Bulk Create Devices With Prefix"
        description = "Creates multiple devices using a name prefix"

    device_prefix = StringVar(
        description="Device name prefix (e.g. AU-SYD-DEMO-VM-)"
    )

    count = IntegerVar(
        description="Number of devices to create",
        min_value=1
    )

    site = ObjectVar(
        model=Site,
        description="Target site"
    )

    role = ObjectVar(
        model=DeviceRole,
        description="Device role"
    )

    device_type = ObjectVar(
        model=DeviceType,
        description="Device type"
    )

    def run(self, data, commit):

        created = 0

        for i in range(1, data["count"] + 1):

            device_name = f"{data['device_prefix']}{i:02}"

            if Device.objects.filter(name=device_name).exists():
                self.log_warning(f"Device {device_name} already exists, skipping")
                continue

            device = Device(
                name=device_name,
                site=data["site"],
                role=data["role"],
                device_type=data["device_type"],
                status="active",
            )

            device.full_clean()
            device.save()

            created += 1
            self.log_success(f"Created device {device_name}")

        self.log_info(f"Total devices created: {created}")
