import { Component, ViewChild, ElementRef, Input } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer} from '@angular/platform-browser';

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
  @ViewChild('container', { static: true })
  container!: ElementRef;
  @Input() url: string = '';

  constructor(private safePipe: SafePipe) {
    this.url = this.safePipe.transform(this.url) as string;
  }
}
