#!/usr/bin/env python3
import boto3
from datetime import datetime


class R53:

    def __init__(self):
        self.client = boto3.client('route53')

    @staticmethod
    def __get_domain_from_fqdn(fqdn):
        fqdn_as_list = fqdn.split('.')
        del fqdn_as_list[0]
        domain = '.'.join(fqdn_as_list)
        return domain

    @staticmethod
    def __fqdn_with_root_level(fqdn):
        """ Remove . at the end of the FQDN """
        if not fqdn[:1] == '.':
            fqdn += '.'

        return fqdn

    def get_current_zones(self):
        """
        Returns list of current hosted zones for
        configured amazon account
        """
        return self.client.list_hosted_zones()

    def get_private_zones(self) -> dict:
        return {'HostedZones': [zone for zone in self.get_current_zones()['HostedZones'] if zone['Config']['PrivateZone']]}

    def get_public_zones(self) -> dict:
        return {'HostedZones': [zone for zone in self.get_current_zones()['HostedZones'] if not zone['Config']['PrivateZone']]}

    def list_zones_by_name(self, name: str) -> dict:
        name = self.__fqdn_with_root_level(name)
        response = None
        for zone in self.client.list_hosted_zones_by_name(DNSName=name)['HostedZones']:
            if zone['Name'] == name:
                response = zone
        return response

    def list_public_zones_by_name(self, name):
        name = self.__fqdn_with_root_level(name)
        print(name)
        response = None
        for zone in self.get_public_zones()['HostedZones']:
            if zone['Name'] == name:
                response = zone

        return response

    def get_public_zone_id_by_name(self, name):
        return self.list_public_zones_by_name(name)['Id'].split('/')[2]

    def list_private_zones_by_name(self, name):
        name = self.__fqdn_with_root_level(name)
        response = None
        for zone in self.get_private_zones()['HostedZones']:
            if zone['Name'] == name:
                response = zone

        return response

    def get_private_zone_id_by_name(self, name):
        return self.list_private_zones_by_name(name)['Id'].split('/')[2]

    def update_a_record(self, record_name: str, ip: str, zone_id: str=None, ttl=600,
                        comment: str='Updated by R53_RECORD_UPDATE'):
        """
        Modifies a given resource record set for
        HostedZoneId
        """
        if not zone_id:
            zone_id = self.get_public_zone_id_by_name(name=self.__get_domain_from_fqdn(record_name))

        response = self.client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Comment': comment,
                'Changes': [
                    {
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'TTL': ttl,
                            'Name': record_name,
                            'Type': 'A',
                            'ResourceRecords': [
                                {
                                    'Value': ip
                                },
                            ]
                        }
                    },
                ]
            }
        )
        return response

if __name__ == '__main__':
    """ CLI version unbundled from kraken """

    import json
    from sys import argv

    r53 = R53()
    args = argv
    record_name, ip = args[1], args[2]

    response = r53.update_a_record(record_name=record_name, ip=ip)
    print(json.dumps(response, indent=4))
