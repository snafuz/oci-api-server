# coding: utf-8

from oci.config import from_file
from oci.identity import IdentityClient
from oci.core import ComputeClient, VirtualNetworkClient
from oci.core import models
from oci.exceptions import ServiceError
import oci.waiter
import json
import logging


class OciWrapper:
    
    def __init__(self, json_config=None):

        if json_config:
            self.config = from_file(profile_name=json_config.get("profile"))
        else:
            self.config = from_file()

        self._identity_client = IdentityClient(self.config)
        self._compute_client = ComputeClient(self.config)
        self._network_client = VirtualNetworkClient(self.config)


    def get_compartment_list(self):
        """
            :return list of all compartments in a tenancy
        """
        return self._identity_client.list_compartments(self.config.get('tenancy')).data

    def list_compartments(self):
        """
            Provide a list of compartments
            :return JSON with compartment list
        """
        d = self._identity_client.list_compartments(self.config.get('tenancy')).data
        return json.loads(str(d))

    def get_compartment_id_from_name(self, compartment_name):
        return next((item for item in self.get_compartment_list() if
                     item.name == compartment_name)).id

    def get_instance_id_from_name(self, compartment_id, instance_name):
        instance_ids = []
        for item in self._compute_client.list_instances(compartment_id).data:
            if item.display_name == instance_name and item.lifecycle_state == "RUNNING" or item.lifecycle_state == "STOPPED":
                instance_ids.append(item.id)
        return instance_ids

    def get_instance_details(self, compartment_id, instance_id):
          # get running instance details
        # this assumes that only one istance with the given display name is running
          return next((item for item in self._compute_client.list_instances(compartment_id).data if
                                     item.id == instance_id ))

    def get_bv_id(self, compartment_id, instance_id ):

        i_details = self.get_instance_details(compartment_id,instance_id)

        # get boot volume details
        _tmp = next((item for item in self._compute_client.list_boot_volume_attachments(i_details.availability_domain, compartment_id).data if
                     item.instance_id == instance_id))
        boot_vol_attachment_id = _tmp.id
        logging.debug("Boot volume attachment OCID: %s", boot_vol_attachment_id)
        boot_vol_id = _tmp.boot_volume_id
        logging.debug("Boot volume OCID: %s", boot_vol_id)
        return boot_vol_id, boot_vol_attachment_id

    def detach_bv(self, bv_id):
        """
            detach block volume
        """

        logging.info("Detaching boot volume...")
        response = self._compute_client.detach_boot_volume(bv_id)
        get_instance_response = oci.wait_until(self._compute_client,
                                               self._compute_client.get_boot_volume_attachment(bv_id),
                                               'lifecycle_state', 'DETACHED')
        logging.info("Boot volume detached")


    def launch_instance(self, instance_details):
        """
            launch instance
            :return istance OCID
        """

        try:
            logging.info("Starting new instance...")
            response = self._compute_client.launch_instance(instance_details)
            oci.wait_until(self._compute_client, self._compute_client.get_instance(response.data.id), 'lifecycle_state',
                           'RUNNING')
            logging.info("Instance started [%s]", response.data.id)
            return response.data.id
        except ServiceError as err:
            logging.error('unable to launch a new instance code %s - message %s'%(err.code, err.message))



    def stop_instance(self,instance_id, detach_bv = False):
        """
            stop instance
        """

        logging.info("Stopping instance...")
        response = self._compute_client.instance_action(instance_id, "stop")
        get_instance_response = oci.wait_until(self._compute_client, self._compute_client.get_instance(instance_id),
                                               'lifecycle_state', 'STOPPED')
        logging.info("Instance stopped")


    def terminate_instance(self, compartment_id, instance_id, preserve_bv=False):
        """
        terminate the smaller instance
        :param compartment_id: compartment OCID
        :param instance_id: instance OCID
        :param preserve_bv: if True preserve the boot volume
        :return:
        """
        logging.info("Terminating instance...")
        self._compute_client.terminate_instance(instance_id, preserve_boot_volume=preserve_bv)
        oci.wait_until(self._compute_client, self._compute_client.get_instance(instance_id),
                                               'lifecycle_state', 'TERMINATED')
        logging.info("Instance terminated")


    def scale(self, new_shape, compartment_name=None, compartment_ocid=None, instance_name=None, instance_ocid = None ):
        """
        Scale-up function
        """

        if not compartment_ocid:
            compartment_ocid = self.get_compartment_id_from_name(compartment_name)
            if not compartment_ocid:
                raise ValueError('unable to locate any compartment named: %s' % instance_name)

        if not instance_ocid:
            temp_instance_ids = self.get_instance_id_from_name(compartment_ocid, instance_name)
            if not temp_instance_ids or len(temp_instance_ids) < 1:
                raise ValueError('unable to locate any instance named: %s' % instance_name)
            elif len(temp_instance_ids)>1:
                raise ValueError('name (%s) is used by multiple instances'%instance_name)
            else:
                instance_ocid = temp_instance_ids[0]

        logging.info("Scaling up instance: %s [%s]", instance_name, instance_ocid)
        old_instance_details = self.get_instance_details(compartment_ocid,instance_ocid)

        #get vnic details
        # TODO: Manage multiple vnics. This assumes that instance has a single vnic.
        vnic_id =  next((item for item in self._compute_client.list_vnic_attachments(compartment_ocid).data if item.instance_id == instance_ocid)).vnic_id
        vnic_attachment_details = self._network_client.get_vnic(vnic_id).data
        logging.debug("vnic attachment details: %s", vnic_attachment_details)

        # TODO: manage Public floating IP
        # TODO: manage block volumes

        #stopping instance
        self.stop_instance(instance_ocid)

        #detach boot volume
        bv_ocid, bv_attachment_ocid=self.get_bv_id(compartment_ocid, instance_ocid)
        self.detach_bv(bv_attachment_ocid)

        #terminating the old instance
        self.terminate_instance(compartment_ocid,instance_ocid, True)

        instance_details=models.LaunchInstanceDetails(
            availability_domain= old_instance_details.availability_domain,
            compartment_id= old_instance_details.compartment_id,
            create_vnic_details= models.CreateVnicDetails(
                            assign_public_ip=bool(vnic_attachment_details.public_ip),
                            display_name=vnic_attachment_details.display_name,
                            hostname_label=vnic_attachment_details.hostname_label,
                            private_ip=vnic_attachment_details.private_ip,
                            skip_source_dest_check=vnic_attachment_details.skip_source_dest_check,
                            subnet_id=vnic_attachment_details.subnet_id,
                        ),
            display_name= old_instance_details.display_name,
            extended_metadata= old_instance_details.extended_metadata,
            ipxe_script= old_instance_details.ipxe_script,
            metadata= old_instance_details.metadata,
            shape= new_shape,
            source_details= models.InstanceSourceViaBootVolumeDetails(
                            source_type="bootVolume",
                            boot_volume_id=bv_ocid
                        )
        )
    
        new_instance_ocid = self.launch_instance(instance_details)
        return new_instance_ocid

    def _test(self):
        pass



if __name__ == "__main__":
    #test purpose
    config_path = './config.json'
    with open(config_path) as config_file:
        cfg = json.load(config_file)
    OciWrapper(cfg.get("oci"))._test( )