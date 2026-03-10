from extras.scripts import Script, MultiObjectVar
from dcim.models import Device, Site
from extras.models import Tag


class TagDevicesByCompliance(Script):

    class Meta:
        name = "Tag Devices by Compliance (With Colors)"
        description = "Automatically tags devices as compliant or non-compliant with colors"

    sites = MultiObjectVar(
        model=Site,
        description="Select site(s) to evaluate"
    )

    def run(self, data, commit):

        compliant_tag, _ = Tag.objects.get_or_create(
            name="compliant",
            slug="compliant",
            defaults={"color": "4caf50"}  # Green
        )

        non_compliant_tag, _ = Tag.objects.get_or_create(
            name="non-compliant",
            slug="non-compliant",
            defaults={"color": "f44336"}  # Red
        )

        devices = Device.objects.filter(site__in=data["sites"])

        if not devices.exists():
            self.log_info("No devices found in selected site(s)")
            return

        for device in devices:

            issues = []

            if not device.primary_ip:
                issues.append("primary IP")

            if not device.platform:
                issues.append("platform")

            if not device.tenant:
                issues.append("tenant")

            # Remove previous compliance tags to avoid stale state
            device.tags.remove(compliant_tag, non_compliant_tag)

            if issues:
                device.tags.add(non_compliant_tag)
                self.log_warning(
                    f"NON-COMPLIANT | {device.name} | missing {', '.join(issues)}"
                )
            else:
                device.tags.add(compliant_tag)
                self.log_success(
                    f"COMPLIANT | {device.name}"
                )

            device.save()

        self.log_info("Device compliance tagging completed")
