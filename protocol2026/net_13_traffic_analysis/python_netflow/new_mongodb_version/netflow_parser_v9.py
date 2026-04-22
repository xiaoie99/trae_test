#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import ipaddress
from typing import Dict, Any, List

# Expanded field mapping; unknowns are stored as FIELD_<type>
FIELD_TYPES = {
	0: 'UNKNOWN_FIELD_TYPE',
	1: 'IN_BYTES',
	2: 'IN_PKTS',
	3: 'FLOWS',
	4: 'PROTOCOL',
	5: 'SRC_TOS',
	6: 'TCP_FLAGS',
	7: 'L4_SRC_PORT',
	8: 'IPV4_SRC_ADDR',
	9: 'SRC_MASK',
	10: 'INPUT_INTERFACE_ID',
	11: 'L4_DST_PORT',
	12: 'IPV4_DST_ADDR',
	13: 'DST_MASK',
	14: 'OUTPUT_INTERFACE_ID',
	15: 'IPV4_NEXT_HOP',
	16: 'SRC_AS',
	17: 'DST_AS',
	18: 'BGP_IPV4_NEXT_HOP',
	19: 'MUL_DST_PKTS',
	20: 'MUL_DST_BYTES',
	21: 'LAST_SWITCHED',
	22: 'FIRST_SWITCHED',
	23: 'OUT_BYTES',
	24: 'OUT_PKTS',
	25: 'MIN_PKT_LNGTH',
	26: 'MAX_PKT_LNGTH',
	27: 'IPV6_SRC_ADDR',
	28: 'IPV6_DST_ADDR',
	29: 'IPV6_SRC_MASK',
	30: 'IPV6_DST_MASK',
	31: 'IPV6_FLOW_LABEL',
	32: 'ICMP_TYPE',
	33: 'MUL_IGMP_TYPE',
	34: 'SAMPLING_INTERVAL',
	35: 'SAMPLING_ALGORITHM',
	36: 'FLOW_ACTIVE_TIMEOUT',
	37: 'FLOW_INACTIVE_TIMEOUT',
	38: 'ENGINE_TYPE',
	39: 'ENGINE_ID',
	40: 'TOTAL_BYTES_EXP',
	41: 'TOTAL_PKTS_EXP',
	42: 'TOTAL_FLOWS_EXP',
	44: 'IPV4_SRC_PREFIX',
	45: 'IPV4_DST_PREFIX',
	46: 'MPLS_TOP_LABEL_TYPE',
	47: 'MPLS_TOP_LABEL_IP_ADDR',
	48: 'FLOW_SAMPLER_ID',
	49: 'FLOW_SAMPLER_MODE',
	50: 'NTERVAL',
	52: 'MIN_TTL',
	53: 'MAX_TTL',
	54: 'IPV4_IDENT',
	55: 'DST_TOS',
	56: 'IN_SRC_MAC',
	57: 'OUT_DST_MAC',
	58: 'SRC_VLAN',
	59: 'DST_VLAN',
	60: 'IP_PROTOCOL_VERSION',
	61: 'DIRECTION',
	62: 'IPV6_NEXT_HOP',
	63: 'BPG_IPV6_NEXT_HOP',
	64: 'IPV6_OPTION_HEADERS',
	70: 'MPLS_LABEL_1',
	71: 'MPLS_LABEL_2',
	72: 'MPLS_LABEL_3',
	73: 'MPLS_LABEL_4',
	74: 'MPLS_LABEL_5',
	75: 'MPLS_LABEL_6',
	76: 'MPLS_LABEL_7',
	77: 'MPLS_LABEL_8',
	78: 'MPLS_LABEL_9',
	79: 'MPLS_LABEL_10',
	80: 'IN_DST_MAC',
	81: 'OUT_SRC_MAC',
	82: 'IF_NAME',
	83: 'IF_DESC',
	84: 'SAMPLER_NAME',
	85: 'IN_PERMANENT_BYTES',
	86: 'IN_PERMANENT_PKTS',
	88: 'FRAGMENT_OFFSET',
	89: 'FORWARDING_STATUS',
	90: 'MPLS_PAL_RD',
	91: 'MPLS_PREFIX_LEN',
	92: 'SRC_TRAFFIC_INDEX',
	93: 'DST_TRAFFIC_INDEX',
	94: 'APPLICATION_DESCRIPTION',
	95: 'APPLICATION_TAG',
	96: 'APPLICATION_NAME',
	98: 'postipDiffServCodePoint',
	99: 'replication_factor',
	100: 'DEPRECATED',
	102: 'layer2packetSectionOffset',
	103: 'layer2packetSectionSize',
	104: 'layer2packetSectionData',
	148: 'NF_F_CONN_ID',
	152: 'NF_F_FLOW_CREATE_TIME_MSEC',
	176: 'NF_F_ICMP_TYPE',
	177: 'NF_F_ICMP_CODE',
	178: 'NF_F_ICMP_TYPE_IPV6',
	179: 'NF_F_ICMP_CODE_IPV6',
	225: 'NF_F_XLATE_SRC_ADDR_IPV4',
	226: 'NF_F_XLATE_DST_ADDR_IPV4',
	227: 'NF_F_XLATE_SRC_PORT',
	228: 'NF_F_XLATE_DST_PORT',
	231: 'NF_F_FWD_FLOW_DELTA_BYTES',
	232: 'NF_F_REV_FLOW_DELTA_BYTES',
	233: 'NF_F_FW_EVENT',
	281: 'NF_F_XLATE_SRC_ADDR_IPV6',
	282: 'NF_F_XLATE_DST_ADDR_IPV6',
	323: 'NF_F_EVENT_TIME_MSEC',
	33000: 'NF_F_INGRESS_ACL_ID',
	33001: 'NF_F_EGRESS_ACL_ID',
	33002: 'NF_F_FW_EXT_EVENT',
	346: 'PANOS_privateEnterpriseNumber',
	40000: 'NF_F_USERNAME',
	45010: 'CONNECTION_ID',
	56701: 'PANOS_APPID',
	56702: 'PANOS_USERID',
}

# Types for formatting
_IPV4_FIELD_TYPES = {8, 12, 15, 18, 225, 226, 47}
_IPV6_FIELD_TYPES = {27, 28, 62, 63, 281, 282}
_MAC_FIELD_TYPES = {56, 57, 80, 81}


def ipv4_from_int(value: int) -> str:
	return '.'.join([
		str((value >> 24) & 0xFF),
		str((value >> 16) & 0xFF),
		str((value >> 8) & 0xFF),
		str(value & 0xFF),
	])


def mac_from_bytes(raw: bytes) -> str:
	return ':'.join(f"{b:02x}" for b in raw)


class TemplateField:
	def __init__(self, field_type: int, field_length: int) -> None:
		self.field_type = field_type
		self.field_length = field_length


class TemplateRecord:
	def __init__(self, template_id: int, fields: List[TemplateField]) -> None:
		self.template_id = template_id
		self.fields = fields


class TemplateFlowSet:
	def __init__(self, data: bytes) -> None:
		pack = struct.unpack('!HH', data[:4])
		self.flowset_id = pack[0]
		self.length = pack[1]
		self.templates: Dict[int, TemplateRecord] = {}

		offset = 4
		while offset < self.length:
			# Template header
			template_id, field_count = struct.unpack('!HH', data[offset:offset+4])
			offset += 4
			fields: List[TemplateField] = []
			for _ in range(field_count):
				field_type, field_length = struct.unpack('!HH', data[offset:offset+4])
				offset += 4
				fields.append(TemplateField(field_type, field_length))
			self.templates[template_id] = TemplateRecord(template_id, fields)


class DataFlowSet:
	def __init__(self, data: bytes, templates: Dict[int, TemplateRecord]) -> None:
		self.template_id, self.length = struct.unpack('!HH', data[:4])
		self.flows: List[Dict[str, Any]] = []
		template = templates.get(self.template_id)
		if not template:
			return

		offset = 4
		record_len = sum(f.field_length for f in template.fields)
		end = self.length
		while offset + record_len <= end:
			record_bytes = data[offset:offset + record_len]
			offset += record_len
			flow: Dict[str, Any] = {}
			cursor = 0
			for f in template.fields:
				raw = record_bytes[cursor:cursor + f.field_length]
				cursor += f.field_length
				# Integer value (big-endian) fallback
				value = 0
				for idx, b in enumerate(reversed(bytearray(raw))):
					value += b << (idx * 8)
				name = FIELD_TYPES.get(f.field_type, f"FIELD_{f.field_type}")
				# Best-effort formatting based on type and length
				if f.field_type in _IPV4_FIELD_TYPES and f.field_length == 4:
					flow[name] = ipv4_from_int(value)
				elif f.field_type in _IPV6_FIELD_TYPES and f.field_length == 16:
					try:
						flow[name] = str(ipaddress.IPv6Address(raw))
					except Exception:
						flow[name] = value
				elif f.field_type in _MAC_FIELD_TYPES and f.field_length == 6:
					flow[name] = mac_from_bytes(raw)
				else:
					flow[name] = value
			self.flows.append(flow)


class ExportPacket:
	def __init__(self, data: bytes, templates: Dict[int, TemplateRecord]) -> None:
		(self.version, self.count, self.uptime, self.timestamp,
		 self.sequence, self.source_id) = struct.unpack('!HHIIII', data[:20])
		self.templates = templates
		self.flows: List[Dict[str, Any]] = []

		offset = 20
		while offset < len(data):
			flowset_id = struct.unpack('!H', data[offset:offset+2])[0]
			if flowset_id == 0:
				tfs = TemplateFlowSet(data[offset:])
				self.templates.update(tfs.templates)
				offset += tfs.length
			else:
				dfs = DataFlowSet(data[offset:], self.templates)
				self.flows.extend(dfs.flows)
				offset += dfs.length
