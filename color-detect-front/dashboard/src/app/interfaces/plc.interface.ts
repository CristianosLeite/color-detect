export interface Plc {
  conectado?: boolean;
  plc: {
    ip: string;
    rack: string;
    slot: string;
    var_cam: string;
  }
}
