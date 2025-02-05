# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\";\n\x07\x41\x63\x63ount\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\x08loggedIn\x18\x02 \x01(\x08H\x00\x88\x01\x01\x42\x0b\n\t_loggedIn\"U\n\x07Message\x12\x11\n\tsender_id\x18\x01 \x01(\t\x12\x13\n\x0breceiver_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\x12\x11\n\ttimestamp\x18\x04 \x01(\t\"\x1e\n\x0e\x41\x63\x63ountRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"?\n\x0f\x41\x63\x63ountResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x15\n\rresponse_text\x18\x02 \x01(\t\"*\n\x15GetNewMessagesRequest\x12\x11\n\tsender_id\x18\x01 \x01(\t\"-\n\x13ListAccountsRequest\x12\x16\n\x0esearch_pattern\x18\x01 \x01(\t\"I\n\x14ListAccountsResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x1a\n\x08\x61\x63\x63ounts\x18\x02 \x03(\x0b\x32\x08.Account\"M\n\x12SendMessageRequest\x12\x11\n\tsender_id\x18\x01 \x01(\t\x12\x13\n\x0breceiver_id\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"?\n\x13SendMessageResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x11\n\tdelivered\x18\x02 \x01(\t\"@\n\x16RequestMessagesRequest\x12\x11\n\tsender_id\x18\x01 \x01(\t\x12\x13\n\x0breceiver_id\x18\x02 \x01(\t\"j\n\x17RequestMessagesResponse\x12\x15\n\rresponse_code\x18\x01 \x01(\x05\x12\x1a\n\x08messages\x18\x02 \x03(\x0b\x32\x08.Message\x12\x12\n\x05\x65rror\x18\x03 \x01(\tH\x00\x88\x01\x01\x42\x08\n\x06_error2\xe3\x03\n\x0fMessageExchange\x12\x34\n\rCreateAccount\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12,\n\x05LogIn\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12=\n\x0cListAccounts\x12\x14.ListAccountsRequest\x1a\x15.ListAccountsResponse\"\x00\x12-\n\x06LogOut\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12\x34\n\rDeleteAccount\x12\x0f.AccountRequest\x1a\x10.AccountResponse\"\x00\x12:\n\x0bSendMessage\x12\x13.SendMessageRequest\x1a\x14.SendMessageResponse\"\x00\x12\x46\n\x0fRequestMessages\x12\x17.RequestMessagesRequest\x1a\x18.RequestMessagesResponse\"\x00\x12\x44\n\x0eGetNewMessages\x12\x16.GetNewMessagesRequest\x1a\x18.RequestMessagesResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACCOUNT._serialized_start=18
  _ACCOUNT._serialized_end=77
  _MESSAGE._serialized_start=79
  _MESSAGE._serialized_end=164
  _ACCOUNTREQUEST._serialized_start=166
  _ACCOUNTREQUEST._serialized_end=196
  _ACCOUNTRESPONSE._serialized_start=198
  _ACCOUNTRESPONSE._serialized_end=261
  _GETNEWMESSAGESREQUEST._serialized_start=263
  _GETNEWMESSAGESREQUEST._serialized_end=305
  _LISTACCOUNTSREQUEST._serialized_start=307
  _LISTACCOUNTSREQUEST._serialized_end=352
  _LISTACCOUNTSRESPONSE._serialized_start=354
  _LISTACCOUNTSRESPONSE._serialized_end=427
  _SENDMESSAGEREQUEST._serialized_start=429
  _SENDMESSAGEREQUEST._serialized_end=506
  _SENDMESSAGERESPONSE._serialized_start=508
  _SENDMESSAGERESPONSE._serialized_end=571
  _REQUESTMESSAGESREQUEST._serialized_start=573
  _REQUESTMESSAGESREQUEST._serialized_end=637
  _REQUESTMESSAGESRESPONSE._serialized_start=639
  _REQUESTMESSAGESRESPONSE._serialized_end=745
  _MESSAGEEXCHANGE._serialized_start=748
  _MESSAGEEXCHANGE._serialized_end=1231
# @@protoc_insertion_point(module_scope)
