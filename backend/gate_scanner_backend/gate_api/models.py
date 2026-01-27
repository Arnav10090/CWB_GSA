from __future__ import annotations

from django.db import models


class ZoneType(models.Model):
    type_name = models.CharField(max_length=255, primary_key=True, db_column='typeName')
    standard_time = models.IntegerField(null=True, blank=True, db_column='standardTime')

    class Meta:
        managed = False
        db_table = 'ZoneType'


class Users(models.Model):
    id = models.IntegerField(primary_key=True)
    emp_id = models.CharField(max_length=255, null=True, blank=True, db_column='empId')
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    zone_type_name = models.ForeignKey(
        ZoneType,
        on_delete=models.DO_NOTHING,
        db_column='zoneTypeName',
        to_field='type_name',
        null=True,
        blank=True,
    )
    user_type = models.CharField(max_length=255, null=True, blank=True, db_column='userType')
    first_name = models.CharField(max_length=255, null=True, blank=True, db_column='firstName')
    last_name = models.CharField(max_length=255, null=True, blank=True, db_column='lastName')
    telephone = models.CharField(max_length=255, unique=True, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_authenticated(self) -> bool:
        return True

    class Meta:
        managed = False
        db_table = 'Users'


class Zone(models.Model):
    id = models.IntegerField(primary_key=True)
    zone_name = models.CharField(max_length=255, null=True, blank=True, db_column='zoneName')
    type_name = models.ForeignKey(
        ZoneType,
        on_delete=models.DO_NOTHING,
        db_column='typeName',
        to_field='type_name',
        null=True,
        blank=True,
    )
    is_working = models.BooleanField(null=True, blank=True, db_column='isWorking')
    created_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Zone'


class VehicleDetails(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    vehicle_registration_no = models.CharField(max_length=255, db_column='vehicleRegistrationNo')
    remark = models.CharField(max_length=255, null=True, blank=True)
    ratings = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'VehicleDetails'


class DriverHelper(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, null=True, blank=True)
    phone_no = models.CharField(max_length=255, db_column='phoneNo')
    uid = models.CharField(max_length=255, unique=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    is_blacklisted = models.BooleanField(null=True, blank=True, db_column='isBlacklisted')
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'DriverHelper'


class DriverVehicleTagging(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    driver = models.ForeignKey(DriverHelper, on_delete=models.DO_NOTHING, db_column='driverId', related_name='+', null=True, blank=True)
    helper = models.ForeignKey(DriverHelper, on_delete=models.DO_NOTHING, db_column='helperId', related_name='+', null=True, blank=True)
    vehicle = models.ForeignKey(VehicleDetails, on_delete=models.DO_NOTHING, db_column='vehicleId', null=True, blank=True)
    is_verified = models.BooleanField(null=True, blank=True, db_column='isVerified')

    class Meta:
        managed = False
        db_table = 'DriverVehicleTagging'


class DocumentControl(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    reference_id = models.IntegerField(null=True, blank=True, db_column='referenceId')
    file_path = models.CharField(max_length=1024, null=True, blank=True, db_column='filePath')

    class Meta:
        managed = False
        db_table = 'DocumentControl'


class RFTags(models.Model):
    id = models.IntegerField(primary_key=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(null=True, blank=True, db_column='isActive')
    is_deployed = models.BooleanField(null=True, blank=True, db_column='isDeployed')

    class Meta:
        managed = False
        db_table = 'RFTags'


class PODetails(models.Model):
    id = models.IntegerField(primary_key=True)
    dap_name = models.IntegerField(db_column='dapName')
    customer_user_id = models.IntegerField(null=True, blank=True, db_column='customerUserId')
    exp_reporting_time = models.DateTimeField(null=True, blank=True, db_column='expReportingTime')

    class Meta:
        managed = False
        db_table = 'PODetails'


class ParkingSpot(models.Model):
    id = models.IntegerField(primary_key=True)
    zone_id = models.IntegerField(db_column='zoneId')

    class Meta:
        managed = False
        db_table = 'ParkingSpot'


class PODriverVehicleTagging(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    po = models.ForeignKey(PODetails, on_delete=models.DO_NOTHING, db_column='poId', null=True, blank=True)
    driver_vehicle_tagging = models.ForeignKey(
        DriverVehicleTagging,
        on_delete=models.DO_NOTHING,
        db_column='driverVehicleTaggingId',
        null=True,
        blank=True,
    )
    rftag = models.ForeignKey(RFTags, on_delete=models.DO_NOTHING, db_column='rftagId', null=True, blank=True)
    act_reporting_time = models.DateTimeField(null=True, blank=True, db_column='actReportingTime')
    exit_time = models.DateTimeField(null=True, blank=True, db_column='exitTime')

    class Meta:
        managed = False
        db_table = 'PODriverVehicleTagging'


class VehicleTracking(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    po_driver_vehicle_tagging = models.ForeignKey(
        PODriverVehicleTagging,
        on_delete=models.DO_NOTHING,
        db_column='poDriverVehicleTaggingId',
        null=True,
        blank=True,
    )
    current_zone_id = models.IntegerField(null=True, blank=True, db_column='currentZoneId')
    next_zone_id = models.IntegerField(null=True, blank=True, db_column='nextZoneId')
    parking_zone_id = models.IntegerField(null=True, blank=True, db_column='parkingZoneId')
    parking_spot_id = models.IntegerField(null=True, blank=True, db_column='parkingSpotId')
    parking_reporting_time = models.DateTimeField(null=True, blank=True, db_column='parkingReportingTime')
    parking_leaving_time = models.DateTimeField(null=True, blank=True, db_column='parkingLeavingTime')
    currrent_zone_reporting_time = models.DateTimeField(null=True, blank=True, db_column='currrentZoneReportingTime')
    current_zone_leaving_time = models.DateTimeField(null=True, blank=True, db_column='currentZoneLeavingTime')

    class Meta:
        managed = False
        db_table = 'VehicleTracking'


class Alarms(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(null=True, blank=True)
    severity = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    zone_id = models.IntegerField(null=True, blank=True, db_column='zoneId')
    vehicle_id = models.IntegerField(null=True, blank=True, db_column='vehicleId')
    is_acknowledged = models.BooleanField(null=True, blank=True, db_column='isAcknowledged')
    acknowledged_user_id = models.IntegerField(null=True, blank=True, db_column='acknowledgedUserId')
    acknowledged_time = models.DateTimeField(null=True, blank=True, db_column='acknowledgedTime')

    class Meta:
        managed = False
        db_table = 'Alarms'
