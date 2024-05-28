import { Component, Input, Pipe, PipeTransform, HostListener } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ApiServiceService } from '../../services/api-service.service';
import { Mask } from '../../interfaces/mask.interface';

@Pipe({ name: 'safe' })
export class SafePipe implements PipeTransform {
  constructor(private domSanitizer: DomSanitizer) { }
  transform(url: string) {
    return this.domSanitizer.bypassSecurityTrustResourceUrl(url);
  }
}

@Component({
  selector: 'app-canvas',
  standalone: true,
  providers: [SafePipe],
  imports: [],
  templateUrl: './canvas.component.html',
  styleUrl: './canvas.component.scss'
})
export class CanvasComponent {
  private drawing = false;
  private rect = { x: 0, y: 0, width: 0, height: 0 };

  @Input() mask = {} as Mask;
  @Input()
  set url(url: string) {
    this._url = url;

  }
  private _url: string = '';

  get url() {
    return this.safePipe.transform(this._url) as string;
  }

  constructor(private safePipe: SafePipe, private apiService: ApiServiceService) {
    const defaultUrl = '../../../assets/default.png';
    this._url = defaultUrl;
    this.apiService.urlEvent.subscribe((url: string) => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = document.getElementById('video') as HTMLImageElement;

      img.crossOrigin = 'anonymous';
      canvas.width = img.width;
      canvas.height = img.height;

      if (url === '') { // If the stream is stopped
        ctx?.drawImage(img, 0, 0, img.width, img.height);
        const data = canvas.toDataURL('image/png');
        this._url = data;

        img.src = this._url;
      } else {
        this._url = url;
      }
    });
  }

  @HostListener('mousedown', ['$event'])
  onMouseDown(event: MouseEvent) {
    this.drawing = true;
    this.rect.x = event.clientX - 25;
    this.rect.y = event.clientY - 100;
  }

  @HostListener('mousemove', ['$event'])
  onMouseMove(event: MouseEvent) {
    if (!this.drawing) return;
    this.rect.width = event.clientX - this.rect.x;
    this.rect.height = event.clientY - this.rect.y;
    this.draw();
  }

  @HostListener('mouseup', ['$event'])
  onMouseUp() {
    if (!this.drawing) return;
    this.drawing = false;
    this.draw();
    this.updateMask();
  }

  draw() {
    const rectangleElement = document.querySelector('.rectangle') as HTMLElement;
    rectangleElement.style.left = `${this.rect.x}px`;
    rectangleElement.style.top = `${this.rect.y}px`;
    rectangleElement.style.width = `${this.rect.width}px`;
    rectangleElement.style.height = `${this.rect.height}px`;
  }

  updateMask() {
    const mask: Mask = {
      mask: {
        mask: [
          //começa em x
          String(this.rect.x + 15),
          //começa em y
          String(this.rect.y),
          //caminha em x para a direita
          String(this.rect.width + this.rect.x - 15),
          //y permanece o mesmo
          String(this.rect.y),
          //x permanece o mesmo
          String(this.rect.width + this.rect.x - 15),
          //caminha em y para baixo
          String(this.rect.height + this.rect.y - 18),
          //x retorna ao início
          String(this.rect.x + 15),
          //y permanece o mesmo
          String(this.rect.height + this.rect.y - 18)
        ]
      }
    };
    this.apiService.maskEvent.emit(mask);
  }
}
