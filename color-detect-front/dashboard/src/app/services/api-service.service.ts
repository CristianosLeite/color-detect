import { Injectable, EventEmitter, Output } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Color } from '../interfaces/color.interface';
import Swal from 'sweetalert2';

@Injectable({
  providedIn: 'root'
})
export class ApiServiceService {
  baseUrl = 'http://127.0.0.1:4000/';
  endpoint = 'cam01/'
  controller = 'get_ip_address'
  color = 'color';
  url = this.baseUrl + this.endpoint;

  colorEvent = new EventEmitter<Color>();

  constructor(private http: HttpClient) { }

  public connectController(ip: string) {
    this.http.get<any>(this.url + this.controller).subscribe((data) => {
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
        return;
      }

      Swal.fire({
        title: 'Erro!',
        text: 'Endereço de IP inválido!',
        icon: 'error',
        confirmButtonText: 'OK'
      });
      return;
    });
  }

  public getColors(): Observable<Color> {
    return this.http.get<Color>(this.url + this.color);
  }

  public updateColor(color: Color) {
    this.http.post<any>(this.url + this.color, color).subscribe((data) => {
      this.colorEvent.emit(data);
    });
  }
}
