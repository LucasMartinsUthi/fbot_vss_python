# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: command.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='command.proto',
  package='vss_command',
  syntax='proto2',
  serialized_pb=_b('\n\rcommand.proto\x12\x0bvss_command\"4\n\rRobot_Command\x12\x10\n\x08left_vel\x18\x01 \x02(\x02\x12\x11\n\tright_vel\x18\x02 \x02(\x02\"E\n\x0fGlobal_Commands\x12\x32\n\x0erobot_commands\x18\x01 \x03(\x0b\x32\x1a.vss_command.Robot_Command')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_ROBOT_COMMAND = _descriptor.Descriptor(
  name='Robot_Command',
  full_name='vss_command.Robot_Command',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='left_vel', full_name='vss_command.Robot_Command.left_vel', index=0,
      number=1, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='right_vel', full_name='vss_command.Robot_Command.right_vel', index=1,
      number=2, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=82,
)


_GLOBAL_COMMANDS = _descriptor.Descriptor(
  name='Global_Commands',
  full_name='vss_command.Global_Commands',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='robot_commands', full_name='vss_command.Global_Commands.robot_commands', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=84,
  serialized_end=153,
)

_GLOBAL_COMMANDS.fields_by_name['robot_commands'].message_type = _ROBOT_COMMAND
DESCRIPTOR.message_types_by_name['Robot_Command'] = _ROBOT_COMMAND
DESCRIPTOR.message_types_by_name['Global_Commands'] = _GLOBAL_COMMANDS

Robot_Command = _reflection.GeneratedProtocolMessageType('Robot_Command', (_message.Message,), dict(
  DESCRIPTOR = _ROBOT_COMMAND,
  __module__ = 'command_pb2'
  # @@protoc_insertion_point(class_scope:vss_command.Robot_Command)
  ))
_sym_db.RegisterMessage(Robot_Command)

Global_Commands = _reflection.GeneratedProtocolMessageType('Global_Commands', (_message.Message,), dict(
  DESCRIPTOR = _GLOBAL_COMMANDS,
  __module__ = 'command_pb2'
  # @@protoc_insertion_point(class_scope:vss_command.Global_Commands)
  ))
_sym_db.RegisterMessage(Global_Commands)


# @@protoc_insertion_point(module_scope)
