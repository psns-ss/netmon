import {IMachine, IMachineActiveProcess, IMachineInterface} from '@/interfaces';
import {MachinesState} from './state';
import {getStoreAccessors} from 'typesafe-vuex';
import {State} from '../state';


export const mutations = {
  setMachines(state: MachinesState, payload: IMachine[]) {
    state.machines = payload;
  },
  setMachineActiveProcesses(state: MachinesState, payload: IMachineActiveProcess[]) {
    state.activeProcesses = payload;
  },
  setMachineActiveProcess(state: MachinesState, payload: IMachineActiveProcess) {
    const activeProcesses = state.activeProcesses.filter(
      (process: IMachineActiveProcess) => (process.id !== payload.id),
    );
    activeProcesses.push(payload);
    state.activeProcesses = activeProcesses;
  },
  setMachineInterfaces(state: MachinesState, payload: IMachineInterface[]) {
    state.interfaces = payload;
  },
  setMachine(state: MachinesState, payload: IMachine) {
    const machines = state.machines.filter((machine: IMachine) => machine.id !== payload.id);
    machines.push(payload);
    state.machines = machines;
  },
  deleteMachine(state: MachinesState, payload: { id: number }) {
    state.machines = state.machines.filter((machine: IMachine) => machine.id !== payload.id);
  },
};

const {commit} = getStoreAccessors<MachinesState | any, State>('');

export const commitSetMachine = commit(mutations.setMachine);
export const commitSetMachines = commit(mutations.setMachines);
export const commitDeleteMachine = commit(mutations.deleteMachine);
export const commitSetMachineActiveProcesses = commit(mutations.setMachineActiveProcesses);
export const commitSetMachineActiveProcess = commit(mutations.setMachineActiveProcess);
export const commitSetMachineInterfaces = commit(mutations.setMachineInterfaces);
