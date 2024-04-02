import { Component } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { FormControl } from '@angular/forms';
import { ApiServiceService } from '../../services/api-service.service';
import { Plc } from '../../interfaces/plc.interface';

@Component({
  selector: 'app-plc-config-card',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './plc-config-card.component.html',
  styleUrl: './plc-config-card.component.scss'
})
export class PlcConfigCardComponent {
  ip = new FormControl('');
  rack = new FormControl('');
  slot = new FormControl('');
  db = new FormControl('');
  bit = new FormControl('');

  constructor(private apiService: ApiServiceService) {
    this.apiService.plcEvent.subscribe((plc) => {
      this.setPlc(plc);
    });
  }

  private setPlc(data: Plc) {
    this.ip.setValue(data.plc.ip);
    this.rack.setValue(data.plc.rack);
    this.slot.setValue(data.plc.slot);
    this.db.setValue(data.plc.var_cam.split(',')[0]);
    this.bit.setValue(data.plc.var_cam.split(',')[1]);
  }
}
