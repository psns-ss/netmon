import {api} from '@/api';
import {getStoreAccessors} from 'typesafe-vuex';
import {ActionContext} from 'vuex';
import {State} from '../state';
import {commitSetMachine, commitSetMachines} from './mutations';
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
    async actionUpdateMachine(context: MainContext, payload: { id: number, machine: IMachineUpdate }) {
        try {
            const loadingNotification = {content: 'saving', showProgress: true};
            commitAddNotification(context, loadingNotification);
            const response = (await Promise.all([
                api.updateMachine(context.rootState.main.token, payload.id, payload.machine),
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
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
                await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
            ]))[0];
            commitSetMachine(context, response.data);
            commitRemoveNotification(context, loadingNotification);
            commitAddNotification(context, {content: 'Machine successfully created', color: 'success'});
        } catch (error) {
            await dispatchCheckApiError(context, error);
        }
    },
};

const {dispatch} = getStoreAccessors<MachinesState | any, State>('');

export const dispatchGetMachines = dispatch(actions.actionGetMachines);
export const dispatchUpdateMachine = dispatch(actions.actionUpdateMachine);
export const dispatchCreateMachine = dispatch(actions.actionCreateMachine);
