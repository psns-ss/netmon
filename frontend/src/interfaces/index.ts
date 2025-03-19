export interface IUserProfile {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IMachine {
  name: string;
  host: string;
  id: number;
  was_recently_online?: boolean;
}

export interface IMachineCreate {
  name: string;
  host: string;
}

export interface IMachineUpdate {
  name?: string;
  host?: string;
}

export interface IMachineActiveProcess {
  name: string;
  id: number;
  path: string;
  hash: string;
  is_hash_same: boolean;
}

export interface IMachineActiveProcessUpdate {
  is_hash_same?: boolean;
}

export interface IMachineInterface {
  interface_description: string;
  ipv4_address: string;
  ipv4_default_gateway: string;
  dns_server: string;
}
