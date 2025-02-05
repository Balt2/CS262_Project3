# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import server_messages_pb2 as server__messages__pb2


class ServerExchangeStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SyncDB = channel.unary_unary(
                '/ServerExchange/SyncDB',
                request_serializer=server__messages__pb2.SyncDBRequest.SerializeToString,
                response_deserializer=server__messages__pb2.SyncDBResponse.FromString,
                )
        self.GetLogicalClock = channel.unary_unary(
                '/ServerExchange/GetLogicalClock',
                request_serializer=server__messages__pb2.GetLogicalClockRequest.SerializeToString,
                response_deserializer=server__messages__pb2.GetLogicalClockResponse.FromString,
                )


class ServerExchangeServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SyncDB(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLogicalClock(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerExchangeServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SyncDB': grpc.unary_unary_rpc_method_handler(
                    servicer.SyncDB,
                    request_deserializer=server__messages__pb2.SyncDBRequest.FromString,
                    response_serializer=server__messages__pb2.SyncDBResponse.SerializeToString,
            ),
            'GetLogicalClock': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLogicalClock,
                    request_deserializer=server__messages__pb2.GetLogicalClockRequest.FromString,
                    response_serializer=server__messages__pb2.GetLogicalClockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ServerExchange', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServerExchange(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SyncDB(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ServerExchange/SyncDB',
            server__messages__pb2.SyncDBRequest.SerializeToString,
            server__messages__pb2.SyncDBResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetLogicalClock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ServerExchange/GetLogicalClock',
            server__messages__pb2.GetLogicalClockRequest.SerializeToString,
            server__messages__pb2.GetLogicalClockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
