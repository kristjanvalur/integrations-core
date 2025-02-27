# (C) Datadog, Inc. 2019-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
from typing import List, Optional, Type  # noqa: F401

from pyVmomi import vim
from six import iteritems

from datadog_checks.base import to_string
from datadog_checks.vsphere.config import VSphereConfig  # noqa: F401
from datadog_checks.vsphere.constants import MOR_TYPE_AS_STRING, REFERENCE_METRIC, SHORT_ROLLUP
from datadog_checks.vsphere.resource_filters import ResourceFilter, match_any_regex  # noqa: F401
from datadog_checks.vsphere.types import InfrastructureData, MetricFilters, MetricName  # noqa: F401

METRIC_TO_INSTANCE_TAG_MAPPING = {
    # Structure:
    # prefix: tag key used for instance value
    'cpu.': 'cpu_core',
    # Examples: 0, 15
    'datastore.': 'vmfs_uuid',
    # Examples: fd3f776b-2ca26041, 5deed40f-cef2b3f6-0bcd-000c2927ce06
    'disk.': 'device_path',
    # Examples: mpx.vmhba0:C0:T1:L0, mpx.vmhba0:C0:T1:L0
    'net.': 'nic',
    # Examples: vmnic1, 4000
    'storageAdapter.': 'storage_adapter',
    # Examples: vmhba1, vmhba64
    'storagePath.': 'storage_path',
    # Examples: ide.vmhba64-ide.0:0-mpx.vmhba64:C0:T0:L0, pscsi.vmhba0-pscsi.0:1-mpx.vmhba0:C0:T1:L0
    'sys.resource': 'resource_path',
    # Examples: host/system/vmotion, host/system
    'virtualDisk.': 'disk',
    # Examples: scsi0:0, scsi0:0
}


def format_metric_name(counter):
    # type: (vim.PerformanceManager.PerfCounterInfo) -> MetricName
    return "{}.{}.{}".format(
        to_string(counter.groupInfo.key), to_string(counter.nameInfo.key), SHORT_ROLLUP[str(counter.rollupType)]
    )


def is_resource_collected_by_filters(mor, infrastructure_data, resource_filters, resource_tags=None):
    # type: (vim.ManagedEntity, InfrastructureData, List[ResourceFilter], List[str]) -> bool
    resource_type = MOR_TYPE_AS_STRING[type(mor)]
    resource_tags = resource_tags or []

    # Limit filters to those for the resource_type of the mor
    resource_filters = [f for f in resource_filters if f.resource_type == resource_type]

    whitelist_filters = [f for f in resource_filters if f.is_whitelist]
    blacklist_filters = [f for f in resource_filters if not f.is_whitelist]

    # First check if the resource match any blacklist filter, if so do not collect it.
    for resource_filter in blacklist_filters:
        if resource_filter.match(mor, infrastructure_data, resource_tags):
            return False

    # Extra logic to consider that no whitelist filters means "collect everything"
    if not whitelist_filters:
        return True

    # Finally check if the resource match any whitelist filter, if so collect it
    for resource_filter in whitelist_filters:
        if resource_filter.match(mor, infrastructure_data, resource_tags):
            return True

    # Otherwise, do not collect it
    return False


def is_metric_excluded_by_filters(metric_name, mor_type, metric_filters):
    # type: (str, Type[vim.ManagedEntity], MetricFilters) -> bool
    if metric_name.startswith(REFERENCE_METRIC):
        # Always collect at least one metric for reference
        return False
    filters = metric_filters.get(MOR_TYPE_AS_STRING[mor_type])
    if not filters:
        # No filters means collect everything
        return False
    if match_any_regex(metric_name, filters):
        return False

    return True


def get_tags_recursively(mor, infrastructure_data, config, include_only=None):
    # type: (vim.ManagedEntity, InfrastructureData, VSphereConfig, Optional[List[str]]) -> List[str]
    """Go up the resources hierarchy from the given mor. Note that a host running a VM is not considered to be a
    parent of that VM.

    rootFolder(vim.Folder):
      - vm(vim.Folder):
          VM1-1
          VM1-2
      - host(vim.Folder):
          HOST1
          HOST2

    """
    tags = []
    properties = infrastructure_data.get(mor, {})
    entity_name = to_string(properties.get('name', 'unknown'))
    if isinstance(mor, vim.HostSystem):
        tags.append('vsphere_host:{}'.format(entity_name))
    elif isinstance(mor, vim.Folder):
        if isinstance(mor, vim.StoragePod):
            tags.append('vsphere_datastore_cluster:{}'.format(entity_name))
            # Legacy mode: keep it as "folder"
            if config.include_datastore_cluster_folder_tag:
                tags.append('vsphere_folder:{}'.format(entity_name))
        else:
            tags.append('vsphere_folder:{}'.format(entity_name))
    elif isinstance(mor, vim.ComputeResource):
        if isinstance(mor, vim.ClusterComputeResource):
            tags.append('vsphere_cluster:{}'.format(entity_name))
        tags.append('vsphere_compute:{}'.format(entity_name))
    elif isinstance(mor, vim.Datacenter):
        tags.append('vsphere_datacenter:{}'.format(entity_name))
    elif isinstance(mor, vim.Datastore):
        tags.append('vsphere_datastore:{}'.format(entity_name))

    parent = infrastructure_data.get(mor, {}).get('parent')
    if parent is not None:
        tags.extend(get_tags_recursively(parent, infrastructure_data, config))
    if not include_only:
        return tags
    filtered_tags = []
    for tag in tags:
        for prefix in include_only:
            if not tag.startswith(prefix + ":"):
                continue
            filtered_tags.append(tag)
    return filtered_tags


def should_collect_per_instance_values(config, metric_name, resource_type):
    # type: (VSphereConfig, str, Type[vim.ManagedEntity]) -> bool
    filters = config.collect_per_instance_filters.get(MOR_TYPE_AS_STRING[resource_type], [])
    metric_matched = match_any_regex(metric_name, filters)
    return metric_matched


def get_mapped_instance_tag(metric_name):
    # type: (str) -> str
    """
    When collecting per-instance metric, the `instance` tag can mean a lot of different things. The meaning of the
    tag cannot be guessed by looking at the api results and has to be inferred using documentation or experience.
    This method acts as a utility to map a metric_name to the meaning of its instance tag.
    """
    for prefix, tag_key in iteritems(METRIC_TO_INSTANCE_TAG_MAPPING):
        if metric_name.startswith(prefix):
            return tag_key
    return 'instance'
