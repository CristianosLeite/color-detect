import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { FormControl } from '@angular/forms';
import { ApiServiceService } from '../../services/api-service.service';
import { Mask } from '../../interfaces/mask.interface';

@Component({
  selector: 'app-mask-config-card',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './mask-config-card.component.html',
  styleUrl: './mask-config-card.component.scss'
})
export class MaskConfigCardComponent implements OnChanges {
  @Input() maskChange = {} as Mask;

  x1 = new FormControl('');
  y1 = new FormControl('');
  x2 = new FormControl('');
  y2 = new FormControl('');
  x3 = new FormControl('');
  y3 = new FormControl('');
  x4 = new FormControl('');
  y4 = new FormControl('');

  constructor(private apiService: ApiServiceService) {
    this.apiService.maskEvent.subscribe((mask) => {
      this.setMask(mask);
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes['maskChange'].currentValue) {
      this.setMask(changes['maskChange'].currentValue);
    }
  }

  private setMask(data: Mask) {
    this.x1.setValue(data.mask['mask'][0]);
    this.y1.setValue(data.mask['mask'][1]);
    this.x2.setValue(data.mask['mask'][2]);
    this.y2.setValue(data.mask['mask'][3]);
    this.x3.setValue(data.mask['mask'][4]);
    this.y3.setValue(data.mask['mask'][5]);
    this.x4.setValue(data.mask['mask'][6]);
    this.y4.setValue(data.mask['mask'][7]);
  }

  saveMask() {
    this.apiService.saveMask({
      mask : {
        mask: [
          String(this.x1.value) ?? '0',
          String(this.y1.value) ?? '0',
          String(this.x2.value) ?? '0',
          String(this.y2.value) ?? '0',
          String(this.x3.value) ?? '0',
          String(this.y3.value) ?? '0',
          String(this.x4.value) ?? '0',
          String(this.y4.value) ?? '0'
        ]
      }
    });
  }
}
