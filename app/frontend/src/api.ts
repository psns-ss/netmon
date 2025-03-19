import axios from 'axios';
import {apiUrl} from '@/env';
import {
  IMachineActiveProcess, IMachineInterface,
  IMachine,
  IMachineCreate,
  IMachineUpdate,
  IUserProfile,
  IUserProfileCreate,
  IUserProfileUpdate, IMachineActiveProcessUpdate,
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getMachines(token: string) {
    return axios.get<IMachine[]>(`${apiUrl}/api/v1/machines/`, authHeaders(token));
  },
  async getMachine(token: string, machineId: number) {
    return axios.get<IMachine>(`${apiUrl}/api/v1/machines/${machineId}/`, authHeaders(token));
  },
  async deleteMachine(token: string, machineId: number) {
    return axios.delete<IMachine>(`${apiUrl}/api/v1/machines/${machineId}/`, authHeaders(token));
  },
  async updateMachine(token: string, machineId: number, data: IMachineUpdate) {
    return axios.put(`${apiUrl}/api/v1/machines/${machineId}`, data, authHeaders(token));
  },
  async createMachine(token: string, data: IMachineCreate) {
    return axios.post(`${apiUrl}/api/v1/machines/`, data, authHeaders(token));
  },
  async getMachinesActiveProcesses(token: string, machineId: number) {
    return axios.get<IMachineActiveProcess[]>(`${apiUrl}/api/v1/machines/${machineId}/active-processes/`,
      authHeaders(token));
  },
  async updateMachinesActiveProcess(token: string, machineId: number, processId: number,
                                    data: IMachineActiveProcessUpdate) {
    return axios.put<IMachineActiveProcess>(
      `${apiUrl}/api/v1/machines/${machineId}/active-processes/${processId}`,
      data,
      authHeaders(token),
    );
  },
  async getMachinesInterfaces(token: string, machineId: number) {
    return axios.get<IMachineInterface[]>(`${apiUrl}/api/v1/machines/${machineId}/interfaces/`, authHeaders(token));
  },
  async pingMachine(token: string, machineId: number) {
    return axios.get(`${apiUrl}/api/v1/machines/${machineId}/ping/`, authHeaders(token));
  },
};
