import { Injectable, EventEmitter } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Color } from '../interfaces/color.interface';
import { Mask } from '../interfaces/mask.interface';
import Swal, { SweetAlertIcon } from 'sweetalert2';
import { Plc } from '../interfaces/plc.interface';

export interface Controller {
  ip_address: string;
}

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  baseUrl = location.origin.split(":8080")[0] + ':4000/';
  endpoint = 'cam01/'
  controller = 'get_ip_address'
  color = 'color';
  mask = 'mask';
  plc = 'plc';
  url = this.baseUrl + this.endpoint;
  statusController: boolean = false;
  ip: string = '';
  title = 'Erro!';
  text = 'Ocorreu um erro inesperado!';
  icon: SweetAlertIcon = 'error';

  statusControllerEvent = new EventEmitter<boolean>();
  colorEvent = new EventEmitter<Color>();
  maskEvent = new EventEmitter<Mask>();
  plcEvent = new EventEmitter<Plc>();
  urlEvent = new EventEmitter<string>();

  constructor(private http: HttpClient) { }

  public connectController(ip: string) {
    this.http.get<Controller>(this.url + this.controller).subscribe((data) => {
      if (data.ip_address === ip) {
        Swal.fire({
          title: 'Conectado!',
          text: 'Conexão com o controlador estabelecida com sucesso!',
          icon: 'success',
          confirmButtonText: 'OK'
        });
        this.getColors().subscribe((data) => {
          this.colorEvent.emit(data);
        });
        this.getMaskConfig().subscribe((data) => {
          this.maskEvent.emit(data);
        });
        this.getPlcConfig().subscribe((data) => {
          this.plcEvent.emit(data);
        });
        this.ip = ip;
        this.statusController = true;
        this.statusControllerEvent.emit(true);
        return;
      }

      Swal.fire({
        title: 'Erro!',
        text: 'Endereço de IP inválido!',
        icon: 'error',
        confirmButtonText: 'OK'
      });

      this.statusController = false;
      return;
    });
  }

  startStream() {
    if (!this.statusController) {
      Swal.fire({
        title: 'Erro!',
        text: 'Conecte-se ao controlador antes de iniciar a transmissão!',
        icon: 'error',
        confirmButtonText: 'OK'
      });
      return;
    }

    this.http.get<string>(this.url + this.controller).subscribe(() => {
      this.urlEvent.emit(`http://${this.ip}:4000/cam01`);
    });
  }

  stopStream() {
    if (!this.statusController) {
      Swal.fire({
        title: 'Erro!',
        text: 'Nenum vídeo conectado!',
        icon: 'error',
        confirmButtonText: 'OK'
      });
      return;
    }
    this.urlEvent.emit('');
  }

  public getColors(): Observable<Color> {
    return this.http.get<Color>(this.url + this.color);
  }

  public saveColors(data: Color) {
    this.stopStream();
    this.http.post<Response>(this.url + this.color, data.color).subscribe((data) => {
      this.text = data.statusText;

      if (data.status === 200) {
        this.title = 'Sucesso!';
        this.icon = 'success';
      } else {
        this.title = 'Erro!';
        this.icon = 'error';
      }

      Swal.fire({
        title: this.title,
        text: this.text,
        icon: this.icon,
        confirmButtonText: 'OK'
      });
    });

    this.connectController(this.ip);
    this.startStream();
  }

  public getMaskConfig() {
    return this.http.get<Mask>(this.url + this.mask);
  }

  public saveMask(data: Mask) {
    this.stopStream();
    this.http.post<Response>(this.url + this.mask, data['mask']).subscribe((data) => {
      this.text = data.statusText;

      if (data.status === 200) {
        this.title = 'Sucesso!';
        this.icon = 'success';
      } else {
        this.title = 'Erro!';
        this.icon = 'error';
      }

      Swal.fire({
        title: this.title,
        text: this.text,
        icon: this.icon,
        confirmButtonText: 'OK'
      });
    });

    this.connectController(this.ip);
    this.startStream();
  }

  public getPlcConfig() {
    return this.http.get<Plc>(this.url + this.plc);
  }

  public updatePlcConfig(plc: Plc['plc']) {
    this.stopStream();
    this.http.post<Response>(this.url + this.plc, plc).subscribe((data) => {
      this.text = data.statusText;

      if (data.status === 200) {
        this.title = 'Sucesso!';
        this.icon = 'success';
      } else {
        this.title = 'Erro!';
        this.icon = 'error';
      }

      Swal.fire({
        title: this.title,
        text: this.text,
        icon: this.icon,
        confirmButtonText: 'OK'
      });
    });

    this.connectController(this.ip);
    this.startStream();
  }
}
