import { Component, Output } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { FormControl } from '@angular/forms';
import { ApiServiceService } from '../../services/api-service.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-controller-config-card',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './controller-config-card.component.html',
  styleUrl: './controller-config-card.component.scss'
})
export class ControllerConfigCardComponent {
  @Output() ip = new FormControl('');

  constructor(private apiService: ApiServiceService) { }

  public connectController() {
    if (this.ip.value === '') {
      Swal.fire({
        icon: 'error',
        title: 'Não foi possível conectar ao controlador!',
        text: 'Informe um IP válido!',
      });
      return;
    }

    if (this.ip.value !== undefined && this.ip.value !== '' && this.ip.value !== null)
      this.apiService.connectController(this.ip.value);
  }
}
