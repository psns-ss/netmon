from pydantic import BaseModel, Field


class MachineInterface(BaseModel):
    interface_description: str
    ipv4_address: str
    ipv4_default_gateway: str
    dns_server: str


class MachineInterfaceFromClient(MachineInterface):
    interface_description: str = Field(alias="InterfaceDescription")
    ipv4_address: str = Field(alias="IPv4Address")
    ipv4_default_gateway: str = Field(alias="IPv4DefaultGateway")
    dns_server: str = Field(alias="DNSServer")
