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
}

export interface IMachineCreate {
    name: string;
    host: string;
}

export interface IMachineUpdate {
    name?: string;
    host?: string;
}
