import { Component, Input } from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
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

  @Input() url: string = '';

  context: CanvasRenderingContext2D | null = null;

  constructor(private safePipe: SafePipe, private apiService: ApiServiceService) {
    this.apiService.urlEvent.subscribe((url: string) => {
      this.url = url;
      this.url = this.safePipe.transform(this.url) as string;
    });
  }

}
