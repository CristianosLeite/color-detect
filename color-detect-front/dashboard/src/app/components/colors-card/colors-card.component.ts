import { Component } from '@angular/core';
import { ApiServiceService } from '../../services/api-service.service';
import { Color } from '../../interfaces/color.interface';
import { ReactiveFormsModule } from '@angular/forms';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-colors-card',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './colors-card.component.html',
  styleUrl: './colors-card.component.scss',
})
export class ColorsCardComponent {
  colorMax = new FormControl('#FFFFFF');
  colorMin = new FormControl('#FFFFFF');
  minColorH = new FormControl('255');
  maxColorH = new FormControl('255');
  minColorS = new FormControl('255');
  maxColorS = new FormControl('255');
  minColorV = new FormControl('255');
  maxColorV = new FormControl('255');

  colors: Color = {} as Color;

  constructor(private apiService: ApiServiceService) {
    this.apiService.colorEvent.subscribe((colors: Color) => {
      this.colors = JSON.parse(JSON.stringify(colors));
      this.setColors(this.colors);
    });
  }

  private setColors(data: Color) {
    this.minColorH.setValue(data.color.colormin.split(',')[0]);
    this.minColorS.setValue(data.color.colormin.split(',')[1]);
    this.minColorV.setValue(data.color.colormin.split(',')[2]);
    this.maxColorH.setValue(data.color.colormax.split(',')[0]);
    this.maxColorS.setValue(data.color.colormax.split(',')[1]);
    this.maxColorV.setValue(data.color.colormax.split(',')[2]);
    this.colorMin.setValue(
      this.convertRGBToColor(data.color.colormin.split(',').join(','))
    );
    this.colorMax.setValue(
      this.convertRGBToColor(data.color.colormax.split(',').join(','))
    );
  }

  changeColorMax(e: any) {
    if (e.toString().startsWith('#')) {
      this.maxColorH.setValue(this.convertColorToRGB(e).split(',')[0]);
      this.maxColorS.setValue(this.convertColorToRGB(e).split(',')[1]);
      this.maxColorV.setValue(this.convertColorToRGB(e).split(',')[2]);
    } else {
      this.colorMax.setValue(
        this.convertRGBToColor(
          this.maxColorH.value +
            ',' +
            this.maxColorS.value +
            ',' +
            this.maxColorV.value
        )
      );
    }
  }

  changeColorMin(e: any) {
    if (e.toString().startsWith('#')) {
      this.minColorH.setValue(this.convertColorToRGB(e).split(',')[0]);
      this.minColorS.setValue(this.convertColorToRGB(e).split(',')[1]);
      this.minColorV.setValue(this.convertColorToRGB(e).split(',')[2]);
    } else {
      this.colorMin.setValue(
        this.convertRGBToColor(
          this.minColorH.value +
            ',' +
            this.minColorS.value +
            ',' +
            this.minColorV.value
        )
      );
    }
  }

  convertColorToRGB(color: string) {
    let r = parseInt(color.substring(1, 3), 16);
    let g = parseInt(color.substring(3, 5), 16);
    let b = parseInt(color.substring(5, 7), 16);
    return r + ',' + g + ',' + b;
  }

  private componentToHex(c: number) {
    let hex = c.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  }

  convertRGBToColor(rgb: string) {
    console.log(rgb);
    let r = parseInt(rgb.split(',')[0]);
    let g = parseInt(rgb.split(',')[1]);
    let b = parseInt(rgb.split(',')[2]);
    return (
      '#' +
      this.componentToHex(r) +
      this.componentToHex(g) +
      this.componentToHex(b)
    );
  }

  saveColors() {
    this.apiService.saveColors({
      color: {
        colormin:
          this.minColorH.value +
          ',' +
          this.minColorS.value +
          ',' +
          this.minColorV.value,
        colormax:
          this.maxColorH.value +
          ',' +
          this.maxColorS.value +
          ',' +
          this.maxColorV.value,
      },
    });
  }
}
