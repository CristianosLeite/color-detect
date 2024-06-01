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
  minColorR = new FormControl('255');
  maxColorR = new FormControl('255');
  minColorG = new FormControl('255');
  maxColorG = new FormControl('255');
  minColorB = new FormControl('255');
  maxColorB = new FormControl('255');

  colors: Color = {} as Color;

  constructor(private apiService: ApiServiceService) {
    this.apiService.colorEvent.subscribe((colors: Color) => {
      this.colors = JSON.parse(JSON.stringify(colors));
      this.setColors(this.colors);
    });
  }

  private setColors(data: Color) {
    this.minColorR.setValue(data.color.colormin.split(',')[0]);
    this.minColorG.setValue(data.color.colormin.split(',')[1]);
    this.minColorB.setValue(data.color.colormin.split(',')[2]);
    this.maxColorR.setValue(data.color.colormax.split(',')[0]);
    this.maxColorG.setValue(data.color.colormax.split(',')[1]);
    this.maxColorB.setValue(data.color.colormax.split(',')[2]);
    this.colorMin.setValue(
      this.convertRGBToColor(data.color.colormin.split(',').join(','))
    );
    this.colorMax.setValue(
      this.convertRGBToColor(data.color.colormax.split(',').join(','))
    );
  }

  changeColorMax(e: any) {
    if (e.toString().startsWith('#')) {
      this.maxColorR.setValue(this.convertColorToRGB(e).split(',')[0]);
      this.maxColorG.setValue(this.convertColorToRGB(e).split(',')[1]);
      this.maxColorB.setValue(this.convertColorToRGB(e).split(',')[2]);
    } else {
      this.colorMax.setValue(
        this.convertRGBToColor(
          this.maxColorR.value +
            ',' +
            this.maxColorG.value +
            ',' +
            this.maxColorB.value
        )
      );
    }
  }

  changeColorMin(e: any) {
    if (e.toString().startsWith('#')) {
      this.minColorR.setValue(this.convertColorToRGB(e).split(',')[0]);
      this.minColorG.setValue(this.convertColorToRGB(e).split(',')[1]);
      this.minColorB.setValue(this.convertColorToRGB(e).split(',')[2]);
    } else {
      this.colorMin.setValue(
        this.convertRGBToColor(
          this.minColorR.value +
            ',' +
            this.minColorG.value +
            ',' +
            this.minColorB.value
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
          this.minColorR.value +
          ',' +
          this.minColorG.value +
          ',' +
          this.minColorB.value,
        colormax:
          this.maxColorR.value +
          ',' +
          this.maxColorG.value +
          ',' +
          this.maxColorB.value,
      },
    });
  }
}
