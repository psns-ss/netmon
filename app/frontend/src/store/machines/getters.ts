import { MachinesState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const getters = {
    machines: (state: MachinesState) => state.machines,
    machine: (state: MachinesState) => (machineId: number) => {
        const filteredMachines = state.machines.filter((machine) => machine.id === machineId);
        if (filteredMachines.length > 0) {
            return { ...filteredMachines[0] };
        }
    },
    activeProcesses: (state: MachinesState) => state.activeProcesses,
    interfaces: (state: MachinesState) => state.interfaces,
};

const {read} = getStoreAccessors<MachinesState, State>('');

export const readMachines = read(getters.machines);
export const readOneMachine = read(getters.machine);
export const readMachineActiveProcesses = read(getters.activeProcesses);
export const readMachineInterfaces = read(getters.interfaces);
