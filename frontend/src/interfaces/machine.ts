import { Employee } from "./employees.interface";

export interface MachineTypeKeys {
  plastic_inyector: string;
  plastic_extruder: string;
}

export interface MachineType {
  machine_type: string;
  trained_employees: Employee[];
}

export interface Machine {
  machine_number: string;
  machine_title: string;
  machine_type: number;
}
