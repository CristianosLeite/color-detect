import { Component, Input, ViewChild, ElementRef, Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer} from '@angular/platform-browser';
import { ApiServiceService } from '../../services/api-service.service';

@Pipe({ name: 'safe' })
export class SafePipe implements PipeTransform {
  constructor(private domSanitizer: DomSanitizer) {}
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
  @ViewChild('canvas') canvas: ElementRef | undefined;
  private startX: number = 0;
  private startY: number = 0;
  private currentX: number = 0;
  private currentY: number = 0;
  private drawing: boolean = false;

  private _url: string = '';

  @Input()
  set url(url: string) {
    this._url = url;
  }

  get url() {
    return this.safePipe.transform(this._url) as string;
  }

  constructor(private safePipe: SafePipe, private apiService: ApiServiceService) {
    this.apiService.urlEvent.subscribe((url: string) => {
      this.url = url;
    });
  }
}
