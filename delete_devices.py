from extras.scripts import Script, StringVar
from dcim.models import Device


class BulkDeleteDevicesByPrefix(Script):

    class Meta:
        name = "Bulk Delete Devices By Prefix"
        description = "Deletes all devices matching a name prefix"

    device_prefix = StringVar(
        description="Device name prefix to delete (e.g. SYD-DEMO-VM-)"
    )

    def run(self, data, commit):

        devices = Device.objects.filter(name__startswith=data["device_prefix"])

        if not devices.exists():
            self.log_info("No devices found with the given prefix")
            return

        deleted_count = 0

        for device in devices:
            name = device.name
            device.delete()
            deleted_count += 1
            self.log_success(f"Deleted device {name}")

        self.log_info(f"Total devices deleted: {deleted_count}")
