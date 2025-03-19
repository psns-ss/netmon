import {IMachine, IMachineActiveProcess, IMachineInterface} from '@/interfaces';


export interface MachinesState {
    machines: IMachine[];
    activeProcesses: IMachineActiveProcess[];
    interfaces: IMachineInterface[];
}
