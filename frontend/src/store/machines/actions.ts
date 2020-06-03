import {api} from '@/api';
import {getStoreAccessors} from 'typesafe-vuex';
import {ActionContext} from 'vuex';
import {State} from '../state';
import {
  commitDeleteMachine,
  commitSetMachine, commitSetMachineActiveProcess,
  commitSetMachineActiveProcesses,
  commitSetMachineInterfaces,
  commitSetMachines,
} from './mutations';
import {MachinesState} from './state';
import {IMachineCreate, IMachineUpdate} from '@/interfaces';
import {commitAddNotification, commitRemoveNotification} from '@/store/main/mutations';
import {dispatchCheckApiError} from '@/store/main/actions';

type MainContext = ActionContext<MachinesState, State>;

export const actions = {
  async actionGetMachines(context: MainContext) {
    try {
      const response = await api.getMachines(context.rootState.main.token);
      if (response.data) {
        commitSetMachines(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetMachine(context: MainContext, payload: { id: number }) {
    try {
      const response = await api.getMachine(context.rootState.main.token, payload.id);
      if (response.data) {
        commitSetMachine(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionUpdateMachine(context: MainContext, payload: { id: number, machine: IMachineUpdate }) {
    try {
      const loadingNotification = {content: 'saving', showProgress: true};
      commitAddNotification(context, loadingNotification);
      const response = (await Promise.all([
        api.updateMachine(context.rootState.main.token, payload.id, payload.machine),
        await new Promise((resolve, _) => setTimeout(() => resolve(), 500)),
      ]))[0];
      commitSetMachine(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {content: 'Machine successfully updated', color: 'success'});
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionCreateMachine(context: MainContext, payload: IMachineCreate) {
    try {
      const loadingNotification = {content: 'saving', showProgress: true};
      commitAddNotification(context, loadingNotification);
      const response = (await Promise.all([
        api.createMachine(context.rootState.main.token, payload),
        await new Promise((resolve, _) => setTimeout(() => resolve(), 500)),
      ]))[0];
      commitSetMachine(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {content: 'Machine successfully created', color: 'success'});
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionDeleteMachine(context: MainContext, payload: { id: number }) {
    try {
      const loadingNotification = {content: 'deleting', showProgress: true};
      commitAddNotification(context, loadingNotification);
      const response = (await Promise.all([
        api.deleteMachine(context.rootState.main.token, payload.id),
        await new Promise((resolve, _) => setTimeout(() => resolve(), 500)),
      ]))[0];
      commitDeleteMachine(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {content: 'Machine successfully deleted', color: 'red'});
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetMachineActiveProcesses(context: MainContext, payload: { id: number }) {
    try {
      const response = await api.getMachinesActiveProcesses(context.rootState.main.token, payload.id);
      if (response.data) {
        commitSetMachineActiveProcesses(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionGetMachineInterfaces(context: MainContext, payload: { id: number }) {
    try {
      const response = await api.getMachinesInterfaces(context.rootState.main.token, payload.id);
      if (response.data) {
        commitSetMachineInterfaces(context, response.data);
      }
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
  async actionDismissMachineProcessHashChange(
    context: MainContext, payload: { machineId: number, machineProcessId: number },
  ) {
    try {
      const loadingNotification = {content: 'dismissing hash change', showProgress: true};
      commitAddNotification(context, loadingNotification);
      const response = (await Promise.all([
        api.updateMachinesActiveProcess(
          context.rootState.main.token,
          payload.machineId,
          payload.machineProcessId,
          {is_hash_same: true},
        ),
        await new Promise((resolve, _) => setTimeout(() => resolve(), 500)),
      ]))[0];
      commitSetMachineActiveProcess(context, response.data);
      commitRemoveNotification(context, loadingNotification);
      commitAddNotification(context, {content: 'Hash change dismissed', color: 'success'});
    } catch (error) {
      await dispatchCheckApiError(context, error);
    }
  },
};

const {dispatch} = getStoreAccessors<MachinesState | any, State>('');

export const dispatchGetMachines = dispatch(actions.actionGetMachines);
export const dispatchGetMachine = dispatch(actions.actionGetMachine);
export const dispatchUpdateMachine = dispatch(actions.actionUpdateMachine);
export const dispatchCreateMachine = dispatch(actions.actionCreateMachine);
export const dispatchDeleteMachine = dispatch(actions.actionDeleteMachine);
export const dispatchGetMachineActiveProcesses = dispatch(actions.actionGetMachineActiveProcesses);
export const dispatchGetMachineInterfaces = dispatch(actions.actionGetMachineInterfaces);
export const dispatchDismissMachineProcessHashChange = dispatch(actions.actionDismissMachineProcessHashChange);
